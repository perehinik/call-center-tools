"""
Exemple of calculating call center staffing
"""

from staffing import calc_staffing

CALLS_PER_HOUR = 1000
AVERAGE_HANDLING_TIME = 120  # sec
AVAILABLE_AGENTS = None
MAX_OCCUPANCY = 0.85
TARGET_ANSWER_TIME = 20  # sec
TARGET_SERVICE_LEVEL = 0.8
SHRINKAGE = 0.3

result = calc_staffing(
    calls_per_hour=CALLS_PER_HOUR,
    aht=AVERAGE_HANDLING_TIME,
    agents=AVAILABLE_AGENTS,
    max_occupancy=MAX_OCCUPANCY,
    target_answer_time=TARGET_ANSWER_TIME,
    target_service_level=TARGET_SERVICE_LEVEL,
    shrinkage=SHRINKAGE,
)

print("Inputs:")
print(f"  Calls per hour:           {CALLS_PER_HOUR}")
print(f"  Average handling time:    {AVERAGE_HANDLING_TIME} sec")
if AVAILABLE_AGENTS:
    print(f"  Available agents:         {AVAILABLE_AGENTS}")
if SHRINKAGE:
    print(f"  Shrinkage:                {SHRINKAGE * 100} %")
print(f"  Max occupancy             {MAX_OCCUPANCY * 100} %")
print(f"  Target answer time        {TARGET_ANSWER_TIME} sec")
print(f"  Target service level      {TARGET_SERVICE_LEVEL * 100} %")
print("")

print("Outputs:")
print(f"  Traffic intensity:        {round(result.traffic_intensity, 3)} Erlang")
print(f"  Waiting probability:      {round(result.wait_probability * 100, 2)} %")
print(f"  Immediate answer:         {round(result.immediate_answer * 100, 2)} %")
print(f"  Service level:            {round(result.service_level * 100, 2)} %")
print(f"  Average speed of answer:  {round(result.average_speed_of_answer, 2)} sec")
print(f"  Occupancy:                {round(result.occupancy * 100, 2)} %")
# if number of agents was not given show calculated number
if not AVAILABLE_AGENTS:
    print(f"  Agents:                   {result.agents}")
if SHRINKAGE:
    print(f"  Agents + shrinkage:       {result.agents_with_shrinkage}")
