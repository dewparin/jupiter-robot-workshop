#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import time

class JaneSR:
    tts_pub = rospy.Publisher('/jane_tts', String, queue_size=10)
    take_photo_pub = rospy.Publisher('/jane_take_photo', String, queue_size=10)
    get_joke_pub = rospy.Publisher('/joker', String, queue_size=10)
    nav_pub = rospy.Publisher('/jane_nav', String, queue_size=10)
 
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
                # if result.startswith('hey jane') or result.startswith('hey jen'):
                if result.startswith('computer') or result.startswith('okay'):
                    self.command(result)
            except sr.UnknownValueError:
                print("[SR]> speechreg # could not understand audio")
            except sr.RequestError as e:
                print("[SR]> speechreg # Could not request results from Google Speech Recognition service; {0}".format(e))
        
    def command(self, sentense):
        if 'photo' in sentense:
            print('[SR]> command # take photo')
            self.tts_pub.publish('got it let\'s take a photo')
            self.take_photo_pub.publish('')
        elif 'joke' in sentense or 'funny' in sentense:
            print('[SR]> command # get joke')
            # self.tts_pub.publish('hah hah')
            self.get_joke_pub.publish('')
        elif 'kitchen' in sentense:
            print('[SR]> command # goto kitchen')
            self.nav_pub.publish('kitchen')
        else:
            print('[SR] command # unknown command')
            self.tts_pub.publish('sorry i do not understand')


if __name__ == '__main__':
    rospy.init_node('x_jane_sr', anonymous=False)
    JaneSR().start()