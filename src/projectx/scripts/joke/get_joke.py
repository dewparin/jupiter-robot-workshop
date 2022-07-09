#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import requests

class Joker:
    def start(self):
        rospy.Subscriber("/joker", String, self.callback)

    def callback(self, data):
        rospy.loginfo("[JOKER]> Getting Joke")
        url = 'https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt&type=single'
        response = requests.get(url)
        print("[JOKER]> response")
        rospy.loginfo("[JOKER]> Response: %s", response.text)
        pub = rospy.Publisher('/jane_tts', String, queue_size=10)
        pub.publish(response.text)

if __name__ == '__main__':
    rospy.init_node('x_joker', anonymous=False)
    Joker().start()
    rospy.spin()