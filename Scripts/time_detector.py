import time
def Score_time():
    '''
    00:00-6:00-28%
    11:00-17:00-26%
    21:00-00:00-20%
    17:00-21:00-17%
    6:00-11:00-9%
    '''
    '''The function returns a dictionary that contains a range of time of the day and their score according to a calculation'''
    score_time={}
    score=11  #temp calculation score
    score_time[6:00,11:00]=score*1.15
    score_time[11:00,17:00]=score*1.75
    score_time[17:00,21:00]=score*1.25
    score_time[21:00,00:00]=score*1.5
    score_time[00:00, 6:00]=score*2
    return  score_time

def Score_travel_duration():
    '''The function returns a dictionary that contains a range of hours and their score according to a calculation'''
    Travel_duration={}#A dictionary containing the hours range, each range has its own score
    # As the hours range increases so does the score
    score=0# score
    i=0#A parameter that rises every time in 2 that symbolizes the time range
    #Hours range to 24, after 24 hours the score will be very high
    while i<24:
      #temp calculation score
      score+=1
      score=score*3
      Travel_duration[i,i+2]=str(score)
      i+=2
    Travel_duration[(24,"<")]=score*score  #temp calculation score
    return Travel_duration
def compute_time_score():
    """compute the time score"""
    # return score