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
    3 = select a drink menu
    4 = getting a drink at the kitchen
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
                elif self.state == 4:
                    self.state_4(result)
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

    def on_get_drink_finished(self, data):
        print('on_get_drink_finished')
        self.state = 0

    # idle
    def state_0(self, sentense):
        rospy.loginfo('state 0 # sentense %s', sentense)
        if (
            sentense.startswith('jane') or
            sentense.startswith('jan') or
            sentense.startswith('jen') or
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
            elif 'grab' in sentense or 'drink' in sentense or 'thirsty' in sentense:
                print('state 0 # command grab a drink')
                # get drink
                self.tts_pub.publish('would you like some tea or coffee?')
                rospy.sleep(2)
                self.state = 3
            else:
                print('state 0 # unknown command')
                self.tts_pub.publish('sorry i do not understand')
                self.state = 0

    # taking a phto
    def state_1(self, sentense):
        print('state 1 # taking a photo')
        # do nothing

    # telling a joke
    def state_2(self, sentense):
        print('state 2 # telling a joke')
        # do nothing
    
    # select a drink menu
    def state_3(self, sentense):
        rospy.loginfo('state 3 # selecting drink menu: sentense %s', sentense)
        if 'tea' in sentense:
            self.tts_pub.publish('I will get you a cup of tea')
            rospy.sleep(4)
        elif 'coffee' in sentense:
            self.tts_pub.publish('I will buy it at Starbucks, please wait.')
            rospy.sleep(4)
        else:
            self.tts_pub.publish('Just a drinking water then')
            rospy.sleep(4)
        # todo nav to kitchen then back
        self.state = 4

    # getting a drink at the kitchen
    def state_4(self, sentense):
        print('state 4')
        self.tts_pub.publish('I am getting you a drink, please wait')
        rospy.sleep(4)
    
if __name__ == '__main__':
    rospy.init_node('x_jane_sr', anonymous=False)
    JaneSR().start()