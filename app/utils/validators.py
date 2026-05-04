from datetime import time

def normalize_time(v):
    if v is None:
        return None

    if isinstance(v, time):
        return v

    v = str(v)

    parts = v.split(":")

    if len(parts) == 1:
        return time(int(parts[0]), 0)

    if len(parts) == 2:
        return time(int(parts[0]), int(parts[1]))

    if len(parts) == 3:
        return time(int(parts[0]), int(parts[1]), int(parts[2]))

    raise ValueError("Invalid time format")