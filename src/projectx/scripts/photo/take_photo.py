#!/usr/bin/env python

'''
Copyright (c) 2016, Nadya Ampilogova
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# Script for simulation
# Launch gazebo world prior to run this script

from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time

class TakePhoto:
    status_pub = rospy.Publisher('/photo_status', String, queue_size=10)

    def __init__(self):

        self.bridge = CvBridge()
        self.image_received = False

        # Connect image topic
        #img_topic = "/camera/rgb/image_raw"
        #img_topic = "/camera_top/rgb/image_raw"
        img_topic = "/usb_cam/image_raw"
        self.image_sub = rospy.Subscriber(img_topic, Image, self.callback)

        # Allow up to one second to connection
        rospy.sleep(1)

        rospy.Subscriber('/jane_take_photo', String, self.response_take_photo)

    def callback(self, data):
        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.image_received = True
        self.image = cv_image

    def take_picture(self, img_title):
        if self.image_received:
            # Save an image
            cv2.imwrite(img_title, self.image)
            return True
        else:
            return False

    def response_take_photo(self, data):
        print('[PHOTOGRAPHER] taking photo')
        try:
            # Take a photo
            timestr = time.strftime("%Y%m%d-%H%M%S-")
            img_title = timestr + "photo.jpg"
            pub = rospy.Publisher('/jane_tts', String, queue_size=10)
            if self.take_picture(img_title):
                rospy.loginfo("Saved image " + img_title)
                time.sleep(2)
                pub.publish('Looking Good.')
            else:
                rospy.loginfo("No images received")
        finally:
            self.status_pub.publish('')
 

if __name__ == '__main__':

    # Initialize
    rospy.init_node('x_jane_photographer', anonymous=False)
    TakePhoto()
 
    rospy.spin()
    # Sleep to give the last log messages time to be sent
    #rospy.sleep(1)
