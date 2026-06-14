#!/usr/bin/env python3
"""
老 SpringBoot 项目 AI 资产化 —— 流水线编排器 / 状态机

用法:
  python assetize.py init --project 订单中心 --repo /path/to/repo --stack "Spring Boot 2.7 / Java 8 / MyBatis"
  python assetize.py status        # 看进度表
  python assetize.py next          # 取下一个该做的任务(返回完整提示词,或 HUMAN_GATE / ALL_DONE)
  python assetize.py done T1       # 标记某任务完成
  python assetize.py gate-clear after_T12C   # 人工确认通过某 gate

设计目标:让 agent 能"做完一个立刻 next 下一个",中途不停;
state 落盘 -> 会话被压缩/中断后,跑一次 next 即可无缝续上。
"""
import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASKS_DEF = HERE / "tasks.json"

# state.json 放在被分析项目的 docs/ai 下,跟产物在一起,方便续跑
def state_path(repo: str) -> Path:
    return Path(repo) / "docs" / "ai" / ".assetize" / "state.json"


def load_state(repo: str) -> dict:
    p = state_path(repo)
    if not p.exists():
        sys.exit(f"未找到状态文件:{p}\n请先运行:python assetize.py init --project <名> --repo {repo} --stack <技术栈>")
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(repo: str, state: dict) -> None:
    p = state_path(repo)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


DOC_DIRS = ["docs/ai", "docs/ai/diagrams", "docs/ai/.assetize"]
REVIEW_QUEUE_HEADER = (
    "# REVIEW-QUEUE · 需人工确认队列\n\n"
    "> 所有 token 关不掉的高危项汇总。按风险排序。这是给\"人\"的核心交付物。\n\n"
    "| 问题(一句话能回答) | 涉及文件 | 为什么 token 解决不了 | 风险等级 |\n"
    "|---|---|---|---|\n"
)


def cmd_init(args):
    repo = os.path.abspath(args.repo)
    defs = json.loads(TASKS_DEF.read_text(encoding="utf-8"))
    subs = {"{{PROJECT}}": args.project, "{{REPO}}": repo, "{{STACK}}": args.stack}

    tasks = {}
    for t in defs["tasks"]:
        prompt = t["prompt"]
        for k, v in subs.items():
            prompt = prompt.replace(k, v)
        tasks[t["id"]] = {
            "id": t["id"],
            "title": t["title"],
            "layer": t["layer"],
            "deps": t["deps"],
            "human": t["human"],
            "prompt": prompt,
            "done": False,
        }

    state = {
        "project": args.project,
        "repo": repo,
        "stack": args.stack,
        "tasks": tasks,
        "order": [t["id"] for t in defs["tasks"]],
        "gates": defs.get("gates", {}),
        "gates_cleared": [],
    }

    # 建目录 + REVIEW-QUEUE 骨架
    for d in DOC_DIRS:
        (Path(repo) / d).mkdir(parents=True, exist_ok=True)
    rq = Path(repo) / "docs" / "ai" / "REVIEW-QUEUE.md"
    if not rq.exists():
        rq.write_text(REVIEW_QUEUE_HEADER, encoding="utf-8")

    save_state(repo, state)
    print(f"已初始化:{args.project}")
    print(f"产物目录:{Path(repo) / 'docs' / 'ai'}")
    print(f"任务数:{len(tasks)}  状态文件:{state_path(repo)}")
    print("\n下一步:python assetize.py next --repo", repo)


def _deps_done(state, t) -> bool:
    return all(state["tasks"][d]["done"] for d in t["deps"])


def cmd_status(args):
    state = load_state(args.repo)
    done = sum(1 for t in state["tasks"].values() if t["done"])
    total = len(state["tasks"])
    print(f"项目:{state['project']}   进度:{done}/{total}")
    print("-" * 64)
    for tid in state["order"]:
        t = state["tasks"][tid]
        if t["done"]:
            mark = "✅"
        elif _deps_done(state, t):
            mark = "🟡 可执行" if not t["human"] else "✋ 需人工"
        else:
            mark = "⏸ 等依赖"
        deps = ("←" + ",".join(t["deps"])) if t["deps"] else ""
        print(f"  {mark:8} L{t['layer']} {t['id']:5} {t['title']} {deps}")


def _emit_next(state):
    """打印下一个该做的任务 / HUMAN_GATE / ALL_DONE。被 next 与 run 共用。"""
    repo = state["repo"]

    # gate 检查:若某 gate 的触发任务已完成但 gate 未清除,则挡住
    for gate, msg in state["gates"].items():
        trigger = gate.replace("after_", "")
        if trigger in state["tasks"] and state["tasks"][trigger]["done"] \
                and gate not in state["gates_cleared"]:
            # 仅当后续还有任务时才作为 gate 拦截
            remaining = [tid for tid in state["order"] if not state["tasks"][tid]["done"]]
            if remaining:
                print("HUMAN_GATE")
                print(f"gate: {gate}")
                print(msg)
                print(f"\n确认通过后运行:python assetize.py gate-clear {gate} --repo {repo}")
                print(f"再运行:python assetize.py run --repo {repo} 继续流水线。")
                return

    # 找第一个可自动执行的任务(依赖已完成 & 非 human)
    for tid in state["order"]:
        t = state["tasks"][tid]
        if not t["done"] and not t["human"] and _deps_done(state, t):
            print(f"TASK {t['id']} · {t['title']} (Layer {t['layer']})")
            print("=" * 64)
            print(t["prompt"])
            print("=" * 64)
            print("\n做完这个任务后,一步到位标记完成并取下一个:")
            print(f"  python assetize.py run --completed {t['id']} --repo {repo}")
            print("循环执行,中途不要停、不要问,直到 HUMAN_GATE 或 ALL_DONE。")
            return

    # 没有可自动执行的;看是否卡在 human 任务
    for tid in state["order"]:
        t = state["tasks"][tid]
        if not t["done"] and t["human"] and _deps_done(state, t):
            print("HUMAN_GATE")
            print(f"task: {t['id']} · {t['title']}")
            print("-" * 64)
            print(t["prompt"])
            print("-" * 64)
            print("这一步需要你本人参与,自动流水线到此为止。")
            print(f"完成后:python assetize.py run --completed {tid} --repo {repo}")
            return

    if all(t["done"] for t in state["tasks"].values()):
        print("ALL_DONE")
        print("所有任务完成。请对照 docs/ai/ 收尾检查清单逐项核对。")
    else:
        print("BLOCKED:存在未完成任务但依赖未满足,运行 status 排查。")


def cmd_next(args):
    state = load_state(args.repo)
    _emit_next(state)


def cmd_run(args):
    """流水线驱动入口:可选地标记上一个任务完成,然后吐出下一个任务。
    典型循环:run(取 T1)→ 执行 → run --completed T1(取 T2)→ ...
    """
    state = load_state(args.repo)
    if args.completed:
        tid = args.completed
        if tid not in state["tasks"]:
            sys.exit(f"未知任务:{tid}")
        if not state["tasks"][tid]["done"]:
            state["tasks"][tid]["done"] = True
            save_state(args.repo, state)
            print(f"✓ 已完成 {tid} · {state['tasks'][tid]['title']}\n")
    _emit_next(state)


def cmd_done(args):
    state = load_state(args.repo)
    tid = args.task_id
    if tid not in state["tasks"]:
        sys.exit(f"未知任务:{tid}")
    state["tasks"][tid]["done"] = True
    save_state(args.repo, state)
    print(f"已标记完成:{tid}")


def cmd_gate_clear(args):
    state = load_state(args.repo)
    if args.gate not in state["gates"]:
        sys.exit(f"未知 gate:{args.gate}(可用:{list(state['gates'])})")
    if args.gate not in state["gates_cleared"]:
        state["gates_cleared"].append(args.gate)
    save_state(args.repo, state)
    print(f"已清除 gate:{args.gate},可继续 next。")


def main():
    p = argparse.ArgumentParser(description="老项目 AI 资产化流水线编排器")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init")
    pi.add_argument("--project", required=True)
    pi.add_argument("--repo", required=True)
    pi.add_argument("--stack", required=True)
    pi.set_defaults(func=cmd_init)

    for name, fn in [("status", cmd_status), ("next", cmd_next)]:
        sp = sub.add_parser(name)
        sp.add_argument("--repo", default=".")
        sp.set_defaults(func=fn)

    pr = sub.add_parser("run", help="驱动入口:标记上一个完成并取下一个,一步到位")
    pr.add_argument("--completed", default=None, help="上一个刚完成的任务 id,如 T1")
    pr.add_argument("--repo", default=".")
    pr.set_defaults(func=cmd_run)

    pd = sub.add_parser("done")
    pd.add_argument("task_id")
    pd.add_argument("--repo", default=".")
    pd.set_defaults(func=cmd_done)

    pg = sub.add_parser("gate-clear")
    pg.add_argument("gate")
    pg.add_argument("--repo", default=".")
    pg.set_defaults(func=cmd_gate_clear)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # 输出被 head/less 等提前关闭管道时,静默退出而非抛栈
        try:
            sys.stdout.close()
        except Exception:
            pass
