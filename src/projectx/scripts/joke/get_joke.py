#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import requests

class Joker:
    status_pub = rospy.Publisher('/joker_status', String, queue_size=10)

    def start(self):
        rospy.Subscriber("/joker", String, self.callback)

    def callback(self, data):
        rospy.loginfo("[JOKER]> Getting Joke")
        try:
            url = 'https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt&type=single'
            response = requests.get(url)
            rospy.loginfo("[JOKER]> Response: %s", response.text)
            short_joke = response.text[:300] if len(response.text) > 300 else response.text
            rospy.loginfo("[JOKER]> Short Joke: %s", short_joke)
            pub = rospy.Publisher('/jane_tts', String, queue_size=10)
            pub.publish(short_joke)
        finally:
            rospy.sleep(3)
            self.status_pub.publish('')

if __name__ == '__main__':
    rospy.init_node('x_joker', anonymous=False)
    Joker().start()
    rospy.spin()