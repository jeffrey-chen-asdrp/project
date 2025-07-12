To test, modify test_simulation.py and run. Sample log below
% pytest -s test_simulation.py                                                               
============================================================================ test session starts =============================================================================
platform darwin -- Python 3.12.1, pytest-8.4.1, pluggy-1.6.0
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 1 item                                                                                                                                                             

test_simulation.py 
=== AGENT INITIALIZATION ===
all_cooperate_1 (all_cooperate) initialized.
all_defect_1 (all_defect) initialized.
tit_for_tat_1 (tit_for_tat) initialized.

--- Round 1 ---
all_cooperate_1 (C) vs all_defect_1 (D) --> Scores: 0, 5
all_cooperate_1 (C) vs tit_for_tat_1 (C) --> Scores: 3, 3
all_defect_1 (D) vs tit_for_tat_1 (C) --> Scores: 5, 0

Current Total Scores:
  all_cooperate_1: 3
  all_defect_1: 10
  tit_for_tat_1: 3

--- Round 2 ---
all_cooperate_1 (C) vs all_defect_1 (D) --> Scores: 0, 5
all_cooperate_1 (C) vs tit_for_tat_1 (D) --> Scores: 0, 5
all_defect_1 (D) vs tit_for_tat_1 (C) --> Scores: 5, 0

Current Total Scores:
  all_cooperate_1: 3
  all_defect_1: 20
  tit_for_tat_1: 8

--- Round 3 ---
all_cooperate_1 (C) vs all_defect_1 (D) --> Scores: 0, 5
all_cooperate_1 (C) vs tit_for_tat_1 (D) --> Scores: 0, 5
all_defect_1 (D) vs tit_for_tat_1 (C) --> Scores: 5, 0

Current Total Scores:
  all_cooperate_1: 3
  all_defect_1: 30
  tit_for_tat_1: 13

=== FINAL RESULTS ===
all_cooperate_1: Final Score = 3
all_defect_1: Final Score = 30
tit_for_tat_1: Final Score = 13
.

============================================================================= 1 passed in 0.15s ==============================================================================
