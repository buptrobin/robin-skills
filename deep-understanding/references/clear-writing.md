# Clear Technical Writing

[ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) inspired Karpathy's suggestion to ask for a clear, constrained explanation, sometimes "80% of the way" to the standard. Use the principles below for ordinary English explanations. Do not claim formal ASD-STE100 compliance without checking the official rules and dictionary. For Chinese or another language, apply the clarity principles without labeling the result ASD-STE100.

- Name the actor when responsibility matters. Put the actor and action early in the sentence.
- Give one main action or causal link per sentence. Break a long chain into ordered steps.
- Use short, familiar words where they retain the correct meaning. Keep established technical terms when replacements would be ambiguous.
- Use one term for one concept. Define a term or abbreviation at first use if the reader needs it.
- Put conditions and exceptions beside the rule they qualify. State what a pronoun or "this" refers to when it could point to several things.
- Separate what happened, what you infer, and what remains unknown. Do not turn a plausible explanation into an observed fact.

Preserve distinctions that change behavior, such as desired versus observed state, retry versus replay, timeout versus failure, event time versus processing time, and correlation versus causation. A concise explanation that merges these can mislead the reader.

A useful example shows a small input, the relevant step, and the resulting output or state. It should let the reader predict another case. Avoid decorative analogies that replace the actual mechanism.
