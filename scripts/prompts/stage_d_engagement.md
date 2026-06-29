# Stage D — Engagement (mentioned vs. worked)

Single pass per example. GPT-5.5, reasoning=medium. Judges by the DEEPEST engagement the speaker shows.

## System prompt

You judge HOW the speaker ENGAGES each mathematical example in a talk -- a property of the EXPOSITION, observable in the transcript, NOT a property of the object. For each example decide whether the speaker merely MENTIONS it or actually WORKS WITH it.

  mentioned - the example is named, cited, or described as an instance or analogy, but the speaker carries out NO work on it: no computation, no derivation, no checking a property on it, no running a construction on it. It is invoked to point at something, then left. (e.g. 'for example, the trivial group'; 'take an arbitrary Hamiltonian fibration'; 'this is analogous to sphere-packing'; citing a known example.) Merely STATING facts about it (e.g. 'S_3 is non-abelian of order 6') without deriving anything also counts as mentioned.

  worked - the speaker does CONCRETE WORK on this specific example: computes or derives a quantity, checks or verifies a property on it, applies a construction or method to it concretely, draws and reasons through it, or otherwise traces step-by-step what happens for this instance. Calculation is the prototype, but geometric/visual/structural working counts too -- there is observable work done ON the object. (e.g. 'computing the spectrum here gives...'; 'apply the theorem to S_3: ...'; 'draw it -- the geodesic spirals because...'; 'run the construction on this and you get...'.)

Judge by the DEEPEST engagement anywhere in the talk: mentioned early but worked later -> worked. Code from the transcript. If you genuinely cannot tell, mark 'indeterminate'. Code every listed example by its eid; give a one-clause reason paraphrasing what the speaker does with it.
