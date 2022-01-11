
# Thresholds of blink and yawn counters used in the drowsiness classification
# All the values are based on experiments


# constants
FRAMES_PER_SECOND = 3  # number of frame per a second the drowsiness classification is based on
YAWN_DURATION = 7  # humans yawn for an average length of 7 seconds


def blink_count_threshold(current_time, travel_duration):
    """
    This function returns the threshold of the blink count, based on time (datetime) and travel duration (timedelta)
    It defines a basic threshold, and then decreases one frame if it is nighttime or the travel is too long
    """
    threshold = FRAMES_PER_SECOND * (10 / 3)  # basic threshold (seconds per frame * seconds of blink)
    if current_time.hour >= 22 or current_time.hour <= 5:  # the threshold is lower if the time is 22:00 - 05:00
        threshold -= 1
    if travel_duration.seconds >= 60 * 60 * 2.5:  # the threshold is lower if the travel duration is more than 2.5 hours
        threshold -= 1
    return threshold


def yawn_count_threshold(current_time, travel_duration):
    """
    This function returns the threshold of the blink count, based on time (datetime) and travel duration (timedelta)
    It defines a basic threshold, and then decreases a single yawn if it is nighttime or the travel is too long
    """
    threshold = FRAMES_PER_SECOND * YAWN_DURATION * 3  # basic threshold (seconds per frame * seconds of single yawn * number of yawns)
    if current_time.hour >= 22 or current_time.hour <= 5:  # the threshold is lower if the time is 22:00 - 05:00
        threshold -= FRAMES_PER_SECOND * YAWN_DURATION
    if travel_duration.seconds >= 60 * 60 * 2.5:  # the threshold is lower if the travel duration is more than 2.5 hours
        threshold -= FRAMES_PER_SECOND * YAWN_DURATION
    return threshold
