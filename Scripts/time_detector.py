import time
from datetime import datetime as dt
def Score_time(current_time_m,current_time_hr):
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
    score_time[6,11]=score*1.15
    score_time[11,17]=score*1.75
    score_time[17,21]=score*1.25
    score_time[21,00]=score*1.5
    score_time[00, 6]=score*2
    print(score_time.keys())
    for i in score_time.keys():
            print(i,i[0],i[1])
            start=i[0]
            end=i[1]
            if start<=current_time_hr<end:
                if current_time_m!=0 and end==current_time_hr:
                          print("in !0")
                          return score_time[end,]
                else:
                    return score_time[i]
current_time_hr=dt.now().hour
current_time_m=dt.now().minute
#print(current_time_m,current_time_hr)
print(Score_time(10,11))

def Score_travel_duration(start_time,stop_time):
    '''The function returns a dictionary that contains a range of hours and their score according to a calculation'''
    travel_duration=stop_time-stop_time
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
    return Travel_duration[travel_duration]
def compute_time_score():
    """compute the time score"""
    # return score