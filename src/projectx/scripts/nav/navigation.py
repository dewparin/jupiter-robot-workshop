#!/usr/bin/env python

import rospy

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from std_msgs.msg import String

class NavToPoint:

    target = 0
    
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

	    # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)

	    # Get the initial pose from the user
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
            rospy.sleep(1)
        rospy.sleep(1)
        rospy.Subscriber('/jane_nav', String, self.nav_callback)
        rospy.loginfo("Ready to go")

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
        self.move_base.cancel_goal()

    def nav_callback(self, data):
        target = data.data
        rospy.loginfo('[NAV] target = %s', target)
        if target == 'kitchen':
            print('[NAV] goto kitchen')
            self.target = 1
        else:
            print('[NAV] unknown target')
            self.target = 0

    def run_loop(self):
        A_theta = 1.5708
        quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
        kitchen_point = Pose(Point(1.0, 1.0, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
        self.goal = MoveBaseGoal()

        while not rospy.is_shutdown():
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()

            if self.target == 1:
                rospy.loginfo("Going to kitchen")
                rospy.sleep(2)
                self.goal.target_pose.pose = kitchen_point
                self.move_base.send_goal(self.goal)
                waiting = self.move_base.wait_for_result(rospy.Duration(300))
                if waiting == 1:
                    rospy.loginfo("Reached point A")
                    rospy.sleep(2)
                    rospy.loginfo("Ready to go back")
                    rospy.sleep(2)
                    self.target = 0
            
            rospy.Rate(5).sleep()


if __name__=="__main__":
    rospy.init_node('x_jane_nav', anonymous=False)
    NavToPoint()
    rospy.spin()