# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return the percentage of the service interval consumed (0–100+)."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when the car has consumed >= WARN_AT_PERCENT of its service interval.

    If 'last_service_km' is absent the car is treated as freshly serviced
    (fallback = odometer), so a missing reading never triggers a false alarm.
    """
    last = car.get("last_service_km", car["odometer"])
    km_since = car["odometer"] - last
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Flag every car that needs service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
