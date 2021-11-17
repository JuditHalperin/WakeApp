import time
from datetime import datetime as dt


def Score_time_minutes(score_time, end_time_hr):
    '''The function receives a dictionary of range of hours  and time in hours,the function returns the score taking into account the minutes'''
    for i in score_time.keys():
        start = i[0]
        end = i[1]
        if end_time_hr == start:
            return score_time[start, end]


def Score_time():
    '''The function returns a score  by time of travel time according to a calculation'''
    current_time_hr = dt.now().hour
    current_time_m = dt.now().minute

    score_time = {}  # a dictionary that contains a range of hours of the day
    score = 11  # temp calculation score

    score_time[6, 11] = score * 1.15
    score_time[11, 17] = score * 1.75
    score_time[17, 21] = score * 1.25
    score_time[21, 00] = score * 1.5
    score_time[00, 6] = score * 2

    for i in score_time.keys():
        start = i[0]
        end = i[1]
        if start <= current_time_hr < end:
            return score_time[i]
        elif end == current_time_hr:
            # In case that the min is more than the score changes,the hour is sent to the score calculation function taking into account the minutes
            if current_time_m != 0:
                return Score_time_minutes(score_time, current_time_hr)
            else:
                return score_time[i]


# print(Score_time())

def Score_travel_duration(travel_duration_hr, travel_duration_minutes):
    '''The function receives 2 parameters,duration of travel in hours and minutes, the function returns returns the score by travel time according to a calculation'''
    if travel_duration_minutes >= 30:
        travel_duration_hr += 1
    else:
        travel_duration_hr -= 1
    Travel_duration = {}  # A dictionary containing the hours range, each range has its own score
    # As the hours range increases so does the score
    score = 0  # score
    i = 0  # A parameter that rises every time in 2 that symbolizes the time range
    # Hours range to 24, after 24 hours the score will be very high
    while i < 24:
        # temp calculation score
        score += 1
        score = score * 3
        Travel_duration[i, i + 2] = str(score)
        i += 2
    Travel_duration[(24, "<")] = score * score  # temp calculation score
    #print(Travel_duration)
    if (travel_duration_hr, travel_duration_hr + 2) in Travel_duration.keys():
        return Travel_duration[travel_duration_hr, travel_duration_hr + 2]
    else:
        return Travel_duration[travel_duration_hr - 1, travel_duration_hr + 1]


#print(Score_travel_duration(8, 40))


def compute_time_score():
    """compute the time score"""
    # return score
