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
 
    '''
    0 = idle, listen to hey jane
    1 = taking photo
    2 = telling a joke
    3 = grab a drink
    '''
    state = 0

    def start(self):
        rospy.Subscriber("/joker_status", String, self.on_joker_finished)
        rospy.Subscriber("/photo_status", String, self.on_take_photo_finished)
        while not rospy.is_shutdown():
            # obtain audio from the microphone
            r = sr.Recognizer()

            with sr.Microphone() as source:
                print("[JANE-SR]> speechreg # Say something!")
                audio = r.record(source, duration=4)

            try:
                result = r.recognize_google(audio).lower()
                print("[SR]> speechreg # result: " + result)
                if self.state == 0:
                    self.state_0(result)
                elif self.state == 1:
                    self.state_1(result)
                elif self.state == 2:
                    self.state_2(result)
                elif self.state == 3:
                    self.state_3(result)
            except sr.UnknownValueError:
                print("[SR]> speechreg # could not understand audio")
            except sr.RequestError as e:
                print("[SR]> speechreg # Could not request results from Google Speech Recognition service; {0}".format(e))
        
    def on_joker_finished(self, data):
        print('on_joker_finished')
        self.state = 0

    def on_take_photo_finished(self, data):
        print('on_take_photo_finished')
        self.state = 0

    # idle
    def state_0(self, sentense):
        rospy.loginfo('state 0 # sentense %s', sentense)
        if (
            sentense.startswith('hey jane') or
            sentense.startswith('hey jan') or
            sentense.startswith('hey jen') or
            sentense.startswith('computer') or 
            sentense.startswith('okay')
            ):
            if 'photo' in sentense:
                print('state 0 # command take photo')
                self.tts_pub.publish('got it let\'s take a photo')
                self.take_photo_pub.publish('')
                self.state = 1
            elif 'joke' in sentense or 'funny' in sentense:
                print('state 0 # command get joke')
                self.get_joke_pub.publish('')
                self.state = 2
            elif 'grab' in sentense or 'drink' in sentense:
                print('state 0 # command grab a drink')
                # get drink
                self.state = 3
            else:
                print('state 0 # unknown command')
                self.tts_pub.publish('sorry i do not understand')
                self.state = 0

    # taking a phto
    def state_1(self, sentense):
        print('state 1')

    # telling a joke
    def state_2(self, sentense):
        print('state 2')
    
    # grab a drink
    def state_3(self, sentense):
        print('state 3')


if __name__ == '__main__':
    rospy.init_node('x_jane_sr', anonymous=False)
    JaneSR().start()