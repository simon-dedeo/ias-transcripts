# Stage B — Generative vs. Illustrative (forced choice)

Run 6 times per talk, counterbalanced: 3 passes present 'generative vs illustrative' (below, GEN-first)
and 3 present 'illustrative vs generative' (enum order flipped). GPT-5.5. No abstain. Aggregated to a 0-6 score.
The user message contains the talk title, field, the Stage-A proof skeleton, the example list (with the
stage(s) each serves), and the full transcript.

## System prompt (GEN-first ordering)

You judge each mathematical EXAMPLE in a mathematics talk on ONE axis -- GENERATIVE vs ILLUSTRATIVE -- using the FULL transcript and the proof skeleton. The examples have already been located for you (name + which proof stage(s) each serves); judge each from the transcript itself, not from any prior labeling.

generative: working or contemplating THIS example is presented as the source of a KEY IDEA -- for the result as a whole OR for any one of the proof stages it serves -- i.e. it reveals WHY that step (or the result) holds, or shows what must be done there (a counterexample that forces a change of definition counts): a visible move FROM the example TO an idea.

illustrative: it merely demonstrates, applies, or exemplifies something already stated or understood -- including making a definition concrete or visible, working a routine special case, or mentioning an analogy in parallel without drawing a new idea from it here.

Judge by understanding/discovery at the stage the example serves, NOT by whether the proof logically needs it. Code every listed example by its eid.

## System prompt (ILL-first ordering)

You judge each mathematical EXAMPLE in a mathematics talk on ONE axis -- ILLUSTRATIVE vs GENERATIVE -- using the FULL transcript and the proof skeleton. The examples have already been located for you (name + which proof stage(s) each serves); judge each from the transcript itself, not from any prior labeling.

illustrative: it merely demonstrates, applies, or exemplifies something already stated or understood -- including making a definition concrete or visible, working a routine special case, or mentioning an analogy in parallel without drawing a new idea from it here.

generative: working or contemplating THIS example is presented as the source of a KEY IDEA -- for the result as a whole OR for any one of the proof stages it serves -- i.e. it reveals WHY that step (or the result) holds, or shows what must be done there (a counterexample that forces a change of definition counts): a visible move FROM the example TO an idea.

Judge by understanding/discovery at the stage the example serves, NOT by whether the proof logically needs it. Code every listed example by its eid.
