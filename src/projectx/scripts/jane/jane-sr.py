#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import time

class JaneTTS:
 
    def start(self):
        while not rospy.is_shutdown():
            # obtain audio from the microphone
            r = sr.Recognizer()

            with sr.Microphone() as source:
                print("[JANE-SR]> speechreg # Say something!")
                audio = r.record(source, duration=4)

            # recognize speech using Google Speech Recognition
            try:
                result = r.recognize_google(audio).lower()
                print("[SR]> speechreg # result: " + result)
                if result.startswith('hey jane') or result.startswith('hey jen'):
                    self.command(result)
            except sr.UnknownValueError:
                print("[SR]> speechreg # could not understand audio")
            except sr.RequestError as e:
                print("[SR]> speechreg # Could not request results from Google Speech Recognition service; {0}".format(e))
        
    def command(self, sentense):
        if 'take photo' in sentense:
            print('[SR]> command # take photo')
        else:
            print('[SR] command # unknown command')


if __name__ == '__main__':
    rospy.init_node('x_jane_sr', anonymous=False)
    JaneTTS().start()