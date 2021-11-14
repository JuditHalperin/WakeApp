from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound

ALARM = "../Data/bigwarning.wav"  # path alarm .WAV file

a = AudioSegment.from_file(file=ALARM, format="wav")
play(a)
#playsound(ALARM)
