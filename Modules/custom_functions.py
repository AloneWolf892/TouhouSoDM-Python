import time
def check_time_passed():
    actual_time = time.time()
    global last_time
    time_has_passed = actual_time > last_time + 1
    if time_has_passed:
        last_time = time.time()
