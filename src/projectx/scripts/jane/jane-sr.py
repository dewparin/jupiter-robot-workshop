#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import time

def speechreg():
    rospy.init_node('x_jane_sr', anonymous=True)
    while not rospy.is_shutdown():
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("[SR]> speechreg # Say something!")
            audio = r.record(source, duration=4)
            
        # recognize speech using Google Speech Recognition
        try:
            result = r.recognize_google(audio).lower()
            print("[SR]> speechreg # result: " + result)
            pub = rospy.Publisher('/jane_tts', String, queue_size=10)
            sentense = 'you said ' + result
            pub.publish(sentense)
        except sr.UnknownValueError:
            print("[SR]> speechreg # could not understand audio")
        except sr.RequestError as e:
            print("[SR]> speechreg # Could not request results from Google Speech Recognition service; {0}".format(e))
        

if __name__ == '__main__':
    try:
        speechreg()
    except rospy.ROSInterruptException:
        pass