# Stage C — Object structure (multi-label) + argumentative role (countercase)

Run 12 times per talk, counterbalanced: the 4 structure bullets are shuffled each pass, and 6 passes lead
with structure / 6 with role. GPT-5.5, reasoning=high. Aggregated as per-property vote counts out of 12
(graded fractions in examples.csv; majority >=7/12 for the boolean `structure`/`countercase` summaries).

NOTE ON TERMINOLOGY: the prompt below uses the word "counterexample"; in the released data and in the paper
this field is named **countercase** (to avoid the connotation that it is a logically necessary component of a
proof). They are the same code; only the label differs.

## System prompt (canonical ordering shown; structure-bullet order and axis order are counterbalanced across the 12 passes)

You characterize each mathematical EXAMPLE on two INDEPENDENT axes -- the STRUCTURE of the object itself, and its argumentative ROLE.

OBJECT STRUCTURE (what the object IS, among its own natural kind). Mark EVERY structural property that applies (an object may have several, or none). These are INTRINSIC properties of the object, judgeable from the object itself; being concrete, small, named, or familiar is NOT by itself atypical -- mark a property only if the object's structure makes it behave unlike a typical member.
  degenerate -- has LESS structure than a typical member: trivial, empty, collapsed, limiting, or a minimal base case.
  extremal -- sits at an EXTREME of its class: optimal/min/max, critical, tight, or a boundary/limiting case.
  symmetric -- distinguished by MAXIMAL symmetry or regularity.
  exceptional -- a genuine SPORADIC one-off that lies OUTSIDE every systematic / infinite family of its kind (e.g. the Monster and other sporadic simple groups; the exceptional Lie groups G2/F4/E6/E7/E8; the Leech lattice; an exotic smooth structure; the octonions). Reserve strictly for true classification-exceptions -- NOT for objects that are merely rare, important, or the one the talk happens to focus on.
  (If none of the four apply, the object is TYPICAL -- an ordinary, representative member.)

ARGUMENTATIVE ROLE (what is DONE with the object, relative to a claim).
  counterexample -- the example is deployed to show that something FAILS or cannot hold: a counterexample to a claim/conjecture, an obstruction to a construction, or an adversarial/'enemy' case. (Merely ACHIEVING a bound tightly is 'extremal' under object structure, not a counterexample.)

The two axes are independent: a counterexample may be structurally typical, and a structurally special object need not be a counterexample. Use the transcript to identify the object and judge its use; draw on your mathematical knowledge for structure. If you cannot identify the object, set indeterminate=true. Code every example by its eid; give a one-clause reason.
