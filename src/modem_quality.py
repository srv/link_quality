#!/usr/bin/env python
import os
import rospy
import std_msgs.msg
import message_filters
from link_quality.msg import  AcousticLink
from evologics_ros_sync.msg import EvologicsChannelDiagnostics,EvologicsUsbllong
from cola2_msgs.msg import NavSts
from math import *

class AcousticQuality():

    def __init__(self,name):
        self.msg = AcousticLink()
        #Publishers
        self.acoustic_message_pub = rospy.Publisher("network_analysis/acoustic_quality",
                                                AcousticLink,
                                                queue_size=1)
        # Subscribers
        rospy.Subscriber("/turbot/evologics_channel",
                        EvologicsChannelDiagnostics,    
                        self.update_turbot_evologics_channel,
                        queue_size=1)

        rospy.Subscriber("/xiroi/usbllong",
                        EvologicsUsbllong,    
                        self.position_callback,
                        queue_size=1)
                  
    def update_turbot_evologics_channel(self,chanel_msg):
        self.msg.rssi_modem = chanel_msg.rssi
        self.msg.integrity_modem = chanel_msg.integrity
        self.msg.header.stamp = rospy.Time.now()
        self.acoustic_message_pub.publish(self.msg)
  
    def position_callback(self,position_msg):
        self.x_distance = position_msg.X
        self.y_distance = position_msg.Y
        self.z_distance = position_msg.Z
        self.distance = sqrt((self.x_distance)**2 + (self.y_distance)**2 +(self.z_distance)**2)
        self.msg.distance = self.distance

 
if __name__ == '__main__':

	try:
		rospy.init_node('acoustic_quality')
		AcousticQuality = AcousticQuality(rospy.get_name())
		rospy.spin()
	except rospy.ROSInterruptException:
		pass


