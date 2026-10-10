# LTL benchmark dataset v0.2 (Draft LTL Bench Mark Cases)

Files
- `dataset.jsonl`  74 entries, including negative test cases at the bottom
- `props.yaml`     proposition vocabulary the formulas are written against
- `validate.py`    checks semantics with spot

Run: `python validate.py` (needs PyYAML; install Spot for the full checks)

## Fields
| field | meaning |
|---|---|
| id | `t` single-agent, `p` paraphrase, `m` multi-agent (3v3), `n` negative |
| english | input sentence |
| ltl | gold formula in Spot syntax, or null for negatives that expect a refusal |
| category | basic_goal, safety, ordering, until, combined, nested, paraphrase, multi_agent, contradictory, out_of_vocab, not_a_command |
| difficulty | easy / medium / hard |
| split | `fewshot` (put in the prompt) or `test` (never show to the model) |
| mode | `1v1` uses a1/o1 only; `3v3` uses a1-a3 / o1-o3 |
| group | entries sharing a group have equivalent formulas on purpose |
| expected_error | null, UNSAT, UNSAT_DOMAIN, OUT_OF_VOCAB, NOT_A_COMMAND |
| notes | why the entry is tricky, or the reading chosen for an ambiguous sentence |

## Scoring
- Positive entries (`expected_error` null): correct if `spot.are_equivalent(pred, gold)`.
- `UNSAT`: correct if the pipeline's verifier flags the prediction as unsatisfiable.
- `UNSAT_DOMAIN`: the command is satisfiable as pure logic but impossible under the game rules
  (e.g. grabbing the flag while tagged). The verifier must conjoin the `domain_constraints` from
  `props.yaml` before checking satisfiability; plain Spot will call these satisfiable.
- `OUT_OF_VOCAB` / `NOT_A_COMMAND`: correct if the translator refuses instead of inventing a formula.
- Report accuracy by category and difficulty, and consistency over repeated runs.

## Known limits
- Formulas are unverified. Every entry needs a second person's independent check, especially `until` and `nested`.
- Equivalence is checked with standard LTL. If you adopt LTLf, convert before comparing.
- Several readings are judgment calls (see `notes`), e.g. "capture" meaning `flag_captured`.