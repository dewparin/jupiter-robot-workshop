#!/usr/bin/env python
from mimetypes import init
import rospy
from std_msgs.msg import String
from gtts import gTTS
import os

class JaneTTS:

    def start(self):
        rospy.Subscriber("/jane_tts", String, self.callback)
        rospy.spin()

    def callback(self, data):
        rospy.loginfo("[TTS]> Input: %s", data.data)
        text = data.data
        tts = gTTS(text)
        tts.save("speech.mp3")
        os.system("mpg321 speech.mp3")
        os.remove("speech.mp3")

if __name__ == '__main__':
    rospy.init_node('x_jane_tts', anonymous=True)
    JaneTTS().start()