
# Thresholds of blink / yawn counters used in the drowsiness classification
# All the values are based on experiments


def blink_count_threshold(current_time, travel_duration):
    """
    This function returns the threshold of the blink count, based on time (datetime) and travel duration (timedelta)
    It defines a basic threshold, and then decreases it if it is nighttime or if the travel is long
    """
    threshold = 10  # basic threshold
    if current_time.hour >= 22 or current_time.hour <= 5:  # the threshold is lower if the time is 22:00 - 05:00
        threshold -= 1
    if travel_duration.seconds >= 60 * 60 * 2.5:  # the threshold is lower if the travel duration is more than 2.5 hours
        threshold -= 1
    return threshold


def yawn_count_threshold(current_time, travel_duration):
    """
    This function returns the threshold of the blink count, based on time (datetime) and travel duration (timedelta)
    It ???
    """
    threshold = 123456789  # basic threshold

    return threshold
