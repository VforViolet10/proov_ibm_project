# What I checked, and what the agent got wrong

## What the agent got wrong

There were five bugs fixed in this session. The trickiest one the agent had to be
careful about was bug #2 in `km_wachter.needs_service`: the original fallback was
`car.get("last_service_km", 0)`, which made a car with no reading appear to have
zero km since service — 0 km since "last service" at odometer 0, so 92,000 km worth
of wear — and get flagged immediately. The fix was to fall back to the car's own
odometer reading, which means 0 km has elapsed since the imagined service, and no
false alarm fires.

The quiet bug that tests never caught was in `fleet_utils.py`: `MILES_PER_KM = 1.609`.
That constant is actually km-per-mile (how many km make up one mile), not miles-per-km.
Multiplying by it gave 160.9 miles for a 100 km trip instead of 62.1. The nightly UK
partner report has been sending out numbers 2.6× too large for years.

## What I checked before accepting the work

- Ran `python verify.py` before and after — the score went from 2/11 to 11/11.
- Confirmed `SERVICE_INTERVAL_KM == 15000` and `WARN_AT_PERCENT == 80` were untouched
  in both `km_wachter.py` and `settings.cfg`.
- Confirmed `km_to_miles(100)` now returns 62.1, not 160.9.
- Ran `python analyze.py` and read the output to verify the numbers were sensible.

## What the data actually said

The obvious guess — that high-mileage, old cars break down — turns out to be almost
completely wrong. Pearson correlation between `odometer_km` and `broke_down` is +0.002,
and between `age_years` and `broke_down` is −0.001. Both are effectively zero.

The two factors that actually separate the breakdown cars from the healthy ones are:

1. **`km_since_service`** (r = +0.404): cars that broke down had driven on average
   11,678 km since their last service, versus 7,261 km for healthy cars — a 61%
   difference. This makes sense: the service interval is 15,000 km, so cars
   approaching that limit without being serviced are accumulating real wear.

2. **`load_factor`** (r = +0.215): breakdown cars average a load factor of 0.60 vs
   0.51 for healthy cars — about 18% heavier usage.

The `avg_daily_km` sits in between (r = +0.252). High daily use puts more kilometres
on the car between services, so it amplifies the km_since_service risk.

The practical conclusion: age and total mileage are not useful signals on their own.
A 10-year-old car with a light load and a recent service is fine. A 2-year-old car
heavily loaded and well past its service interval is the one to watch.
