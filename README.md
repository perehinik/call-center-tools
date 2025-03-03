# call-center-tools

Package contains essential tools for call center staffing calculations.

Package installation:
```shell
pip install call_center_tools
```

Let's try to calculate number of agents for call center with average of 1000 calls per hour.
Average duration of call is 120 sec. Agents should be occupied max 85% of time. 
80% of calls should be answered in 20 sec.

```python
from call_center_tools import calc_staffing

result = calc_staffing(
    calls_per_hour=1000,
    aht=120,
    max_occupancy=0.85,
    target_answer_time=20,
    target_service_level=0.8,
    shrinkage=0.3
)
```
Result:
```text
Inputs:
  Calls per hour:           1000
  Average handling time:    120 sec
  Shrinkage:                30.0 %
  Max occupancy             85.0 %
  Target answer time        20 sec
  Target service level      80.0 %

Outputs:
  Traffic intensity:        33.333 Erlangs
  Waiting probability:      19.07 %
  Immediate answer:         80.93 %
  Service level:            93.72 %
  Average speed of answer:  3.43 sec
  Occupancy:                83.33 %
  Agents:                   40
  Agents + shrinkage:       58
```
So recommended number of agents for such call center is `40`, not counting shrinkage.

Let's imagine we have only `35` agents, not recommended `40`:

```python
from call_center_tools import calc_staffing

result = calc_staffing(
    calls_per_hour=1000,
    aht=120,
    agents=35,
    max_occupancy=0.85,
    target_answer_time=20,
    target_service_level=0.8,
    shrinkage=0.3
)
```
Result:
```text
Inputs:
  Calls per hour:           1000
  Average handling time:    120 sec
  Available agents:         35
  Shrinkage:                30.0 %
  Max occupancy             85.0 %
  Target answer time        20 sec
  Target service level      80.0 %

Outputs:
  Traffic intensity:        33.333 Erlang
  Waiting probability:      69.65 %
  Immediate answer:         30.35 %
  Service level:            47.24 %
  Average speed of answer:  50.15 sec
  Occupancy:                95.24 %
  Agents + shrinkage:       50
```

Try to use `example.py` to test your own parameters.

You can also find method for Erlang C and Erlang B calculations:
```python
from call_center_tools import erlang_c, erlang_b
```
