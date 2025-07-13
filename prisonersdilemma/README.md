# PRISONERS DILEMMMA

## PAYOFFS
- T = Temptation (defect while opponent cooperates) : Default 
- R = Reward (both cooperate)
- P = Punishment (both defect)
- S = Sucker (cooperate while opponent defects)
## STRATEGEY
- 'all_cooperate': Always Cooperates
- 'all_defect': Always Defects
- 'tit_for_tat': Cooperates on first move, then copies opponent's previous move
- 'tit_for_2_tat': Only defects if opponent defects twice in a row
- '2_tit_for_tat': Defects twice if opponent defects once
- 'random': Randomly cooperates or defects
- 'pavlov': Win-Stay, Lose-Shift strategy
- 'grudger': Cooperates until opponent defects, then always defects

## HOW TO TEST
- To test, modify test_simulation.py as needed and run
```
uv sync
source .venv/bin/activate
pytest -s test_simulation.py 
```
- Will generate verbose log, plot and Pass/Fail
