# Example-making in mathematics research talks — data release

Pre-release version for peer-review only; not to be circulated publicly.

This release contains the coded data for **1,025 research seminars** from the School of
Mathematics at the Institute for Advanced Study (IAS), together with the transcripts they
were coded from and the figures and prompts used to produce them. Each talk has been
decomposed into **proof stages** and **examples**, and every example has been coded for
its function (illustrative vs. generative), its degree of engagement (mentioned vs.
worked), its object structure (degenerate / extremal / symmetric / exceptional), and its
argumentative role (**countercase**). Coding was performed with GPT-5.5; see *Pipeline*
below.

Totals: **1,025 talks**, **6,359 coded examples**, **7,628 proof stages**. Talks span
2001–2026 across 48 MSC subject areas.

---

## Layout

```
talks.csv                 one row per talk: metadata + #examples / #stages
examples.csv              one row per example (6,359): analysis-ready predictors
data/<key>.json           per-talk structured coding (stages + DAG + examples + per-pass reasons)
transcripts/<key>.json    full Deepgram Nova-3 ASR transcript (word-level timings)
dag/<key>.dot  /.pdf       proof-stage dependency graph + example attachments
bands/<key>.txt /.pdf      temporal "band plot" of stages and examples
scripts/render_v4.py       renderer that produces the dag/ and bands/ figures
scripts/prompts/           the four GPT-5.5 prompts (Stages A–D), verbatim
```

`<key>` is a stable 32-character talk id used consistently across every folder.

---

## `data/<key>.json` schema

**Talk level.** `key`, `title`, `speaker`, `affiliation`, `date` (ISO 8601; empty for two
talks whose date could not be recovered), `field_msc` (primary MSC2020 2-digit class, taken
as the majority of the three Stage-A runs; empty for two talks where the runs gave no
2-of-3 majority), `duration_sec`, `abstract`, `youtube_url`, `page_url`, `tags`, plus
`proof_stages` and `examples`.

**`proof_stages[]`** — the logical skeleton of the talk's argument:
| field | meaning |
|---|---|
| `id` | stage id (`s1`, `s2`, …), the join key used by `depends_on` and `attaches_to` |
| `code` | display label (`S1`, …) matching the figures |
| `label`, `summary` | GPT-5.5's name and one-line description of the stage |
| `spans` | `[{start_sec, end_sec}]` — when the stage is presented |
| `depends_on` | list of stage ids this stage logically depends on (the DAG edges) |

**`examples[]`** — the examples found in each talk:
| field | meaning |
|---|---|
| `code` | example label (`E1`, …), ordered by first appearance, matching the figures |
| `name`, `note` | GPT-5.5's name and one-line description |
| `first_introduced_sec` | first time the example is raised (defines the `E#` ordering) |
| `spans`, `total_seconds` | time-spans where the example is discussed, and their summed duration |
| `attaches_to`, `primary_stage` | proof stage(s) the example serves; `primary_stage` = the principal one |
| `depth` | longest path from a root stage to `primary_stage` in the DAG |
| `natt_talk` | # proof stages whose spans **strictly** overlap the example in time |
| `from_question` | `true` if raised in an (inferred) Q&A / spontaneous exchange |
| `engagement`, `engagement_reason` | `mentioned` vs. `worked`, with rationale (Stage D) |
| `generative` | `generative` / `illustrative` (majority of 6 passes; Stage B) |
| `generative_score`, `generative_n`, `generative_votes` | the 6 Stage-B votes (`G0..G2` = generative-first, `I0..I2` = illustrative-first); score = # generative |
| `structure` | majority object-structure tags (≥7/12), a subset of {degenerate, extremal, symmetric, exceptional} |
| `countercase` | `true` if the example is a countercase by majority (≥7/12) |
| `votes`, `votes_n` | the 12-pass vote **counts** for each structure tag, `countercase`, and `indeterminate` |
| `passes[]` | the 12 individual Stage-C passes, each with `pass`, `axis_first`, `struct_order`, the `flags` it assigned, and its free-text `reason` |

> **Terminology — `countercase`.** This field is called `counterexample` inside the raw
> Stage-C prompt (`scripts/prompts/stage_c_structure_countercase.md`) and in the verbatim
> free-text `reason` of some `passes`. Everywhere in the released data — the `countercase`
> field, the `votes` keys, and the `passes` `flags` — it is renamed **`countercase`** (to
> avoid implying the example is a *logically necessary* component of a proof); only the
> model's quoted prose is left unedited. The code is identical; only the label differs.

---

## `examples.csv` columns

One row per example (6,359), joinable to the JSON on `(key, code)`:

`key, code, field_msc, gen, worked, q, fdeg, fext, fsym, fexc, fcc, logtime, depth, natt_talk`

- `gen` — 1 if generative (Stage-B score ≥4), 0 if illustrative (≤2), **blank** for the
  3-3 ties dropped from the regressions.
- `worked` — 1 if `engagement == "worked"`. `q` — 1 if `from_question`.
- `fdeg, fext, fsym, fexc, fcc` — graded vote-**fractions** (out of 12) for degenerate,
  extremal, symmetric, exceptional, and **countercase**.
- `logtime` — `ln(total_seconds / 60)` (i.e. log-minutes; blank if the example has no
  measured duration).
- `depth`, `natt_talk` — as defined above.

The regression sample reported in the paper (Tables 3–4, n = 6,169) is the subset of rows
with a non-blank `gen` and defined `logtime` and `depth`; filtering this file that way
yields 6,166 (a ±3 difference from listwise-NA handling in the original regression build).

---

## Transcripts

`transcripts/<key>.json` is the **verbatim Deepgram Nova-3** output. Every coded span is in
seconds and reconstructable from `results.channels[0].alternatives[0].words[]`, each of
which carries `word`, `punctuated_word`, `start`, and `end`. To extract the ASR for a span
`[s, e]`, join the `punctuated_word`s of all words with `s ≤ start ≤ e`. (Transcripts are
ASR and contain recognition errors.)

---

## Pipeline (how the codings were produced)

All coding used **GPT-5.5**. Prompts are in `scripts/prompts/`.

- **Stage A — extraction.** From the transcript, extract proof stages and examples, their
  time-spans, the inter-stage DAG, and each example's stage attachment(s) and
  `from_question` flag.
- **Stage B — illustrative vs. generative.** Forced binary choice, **6 counterbalanced
  passes** (3 generative-first, 3 illustrative-first); aggregated to a 0–6 score. Judgements
  are strongly bimodal (≈84% unanimous).
- **Stage C — structure + role.** Two independent axes: multi-label object **structure**
  (degenerate/extremal/symmetric/exceptional) and the binary **countercase** role,
  **12 counterbalanced passes** (structure-bullet order shuffled; 6 structure-first /
  6 role-first), reasoning-high. Stored as per-property vote counts out of 12. Inter-pass
  reliability (Cohen's κ): countercase 0.91, exceptional 0.94, symmetric 0.81,
  degenerate 0.79, extremal 0.76.
- **Stage D — engagement.** `mentioned` vs. `worked`, judged by the deepest engagement
  shown (κ ≈ 0.90).

Stage C is coded blind to Stage B. The figures (`dag/`, `bands/`) are produced by
`scripts/render_v4.py`; in them illustrative examples are purple, generative orange, and a
red border marks an (inferred) Q&A example.
