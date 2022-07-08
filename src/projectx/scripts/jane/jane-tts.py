#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gtts import gTTS
import os

def callback(data):
    rospy.loginfo("[TTS]> Input: %s", data.data)

    text = data.data
    tts = gTTS(text)
    
    tts.save("speech.mp3")
    os.system("mpg321 speech.mp3")
    os.remove("speech.mp3")
    
def googletts():
    rospy.init_node('x_jane_tts', anonymous=True)

    rospy.Subscriber("/jane_tts", String, callback)

    rospy.spin()

if __name__ == '__main__':
    googletts()