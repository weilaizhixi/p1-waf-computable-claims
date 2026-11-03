# Data dictionary and evidence limits

All CSVs use comma separators, one header row and integer count fields. They are unchanged copies of the approved archived aggregates. Application names and route labels are research labels, not personal identities. English definitions below accompany the original Chinese result anchor and output tables.

## p1_cell_partition.csv

Ten rows: five archived route labels, each under `neutral` and `explicit`. Each row contains `cells = 493`.

|Column|Definition|
|---|---|
|model|Archived route label: haiku, gpt6luna, glm, mimo or deepseek; not a verified provider/model-version assertion|
|condition|neutral or explicit prompt condition; order was not randomized|
|cells|Selected response cells in the 493-task main analysis for this label/condition|
|value_discrepancies|Numeric or other value disagreements, excluding type-name substitutions and absent fields|
|type_name_echoes|Response cells substituting a type name such as bool for a value; multiple substituted fields in one response count once|
|missing_field_cells|Response cells missing a required field; two cells from T222 across conditions|
|format_only_complete_answers|Complete answers whose values match under the declared coercion rules but whose types differ|
|complete_value_and_type_consistent|Complete answers matching both declared values and types|

The five outcome columns form a mutually exclusive partition, summing to 493 per row and 4930 overall. The last two per-route counts exist in the CSV for cross-checking; the anchor reports their overall totals, so the generated research tables do not add new per-route breakdowns. An incomplete-object diagnostic on the two missing-field cells is not another two failures.

## p1_execution_control.csv

Six rows, eight tasks per application evidence bundle. `tasks` is the paired-task denominator; `direct_correct` and `program_correct` are numbers of correct tasks; `direct_wrong_program_correct` counts discordant pairs favoring program execution; `reverse_pairs` counts the reverse direction. The 48 tasks have 96 condition-specific answers. The reported 2/48 difference (4.17 percentage points) describes this fixed set, with no representative-population inference.

## p1_shared_replay.csv

Twelve rows, one per application. `candidates` counts final loaded candidate-rule cells; `measurement_valid` counts valid measurements; `benign_response_contracts` counts cells satisfying the declared benign-response contract; `example_conformance` counts cells conforming to the tested examples. Totals are 213, 213, 211 and 141. This is one test stack and is shared evidence with the companion deployment study. These fields do not measure a general vulnerability-blocking rate, protection against unseen attack families or arbitrary legitimate workflows.

## results_anchor_A-J.md

|Section|Research content|
|---|---|
|A|15 task families: original 500 tasks and main 493 tasks; T403–T409 excluded for contradictory median/sum requirements|
|B|Overlapping questions/evidence/schema; provenance and reconstruction qualifications|
|C|Per-route/condition counts; 20 discrepancy cells across 19 tasks|
|D|Five-category partition of 4930 cells|
|E|Illustrative classification cases; no inference about model-internal causes|
|F|500-task and 484-task sensitivity summaries and leave-one-application-out descriptions|
|G|48-task direct/program comparison|
|H|Reported H007 and H019 discrepancies and historical execution/check qualifications|
|I|213-cell shared replay counts and limits|
|J|Seven instrument failure chains and bounded correction evidence|

Statements about raw input hashes, reference generation or program execution in the anchor describe the archived study. The minimal package cannot independently revalidate them. Task IDs in examples do not imply that the original task evidence or expert review records are released. The paired figure uses the pre-existing sequential-order assumption; tile locations beyond the two identified discordances are illustrative positions derived from aggregates.
