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
        # Subscribers
        rospy.Subscriber("/turbot/evologics_channel",
                        EvologicsChannelDiagnostics,    
                        self.update_turbot_evologics_channel,
                        queue_size=1)
        
        rospy.Subscriber("/xiroi/evologics_channel",
                        EvologicsChannelDiagnostics,    
                        self.update_xiroi_evologics_channel,
                        queue_size=1)

        turbot_position = message_filters.Subscriber("/turbot/navigator/navigation",NavSts)
        turbot_position_acoustic = message_filters.Subscriber("/turbot/navigator/navigation_throttle_acoustic",NavSts)
        xiroi_position = message_filters.Subscriber("/xiroi/navigator/navigation",NavSts)

        # Topic synchronization
        ts =  message_filters.ApproximateTimeSynchronizer([turbot_position, xiroi_position], 10, 10)
        ts1 =  message_filters.ApproximateTimeSynchronizer([turbot_position_acoustic, xiroi_position], 10, 10)
        
        ts.registerCallback(self.position_callback)
        ts1.registerCallback(self.position_callback)

        #Publishers
        self.acoustic_message_pub = rospy.Publisher("network_analysis/acoustic_quality",
                                                AcousticLink,
                                                queue_size=1)

        # Init periodic timer
        # rospy.Timer(rospy.Duration(1.0), self.message_publisher)
        self.msg = AcousticLink()
    
    def acoustic_link_info_callback(self,usbl_msg, modem_msg):
        self.msg.rssi_modem = modem_msg.rssi
        self.msg.integrity_modem = modem_msg.integrity
        self.msg.rssi_usbl = usbl_msg.rssi
        self.msg.integrity_usbl = usbl_msg.integrity
        self.acoustic_channel_info = True 
                  
    def update_turbot_evologics_channel(self,chanel_msg):
        self.msg.rssi_modem = chanel_msg.rssi
        self.msg.integrity_modem = chanel_msg.integrity
    
    def update_xiroi_evologics_channel(self,chanel_msg):
        self.msg.rssi_usbl = chanel_msg.rssi
        self.msg.integrity_usbl = chanel_msg.integrity
  
    def position_callback(self,xiroi_p,turbot_p):
        print("IM IIIIIIN")
        self.x_distance = turbot_p.position.north-xiroi_p.position.north
        self.y_distance = turbot_p.position.east-xiroi_p.position.east
        self.distance = sqrt((self.x_distance)**2 + (self.y_distance)**2)
        self.msg.distance = self.distance
        self.position_info = True
        self.msg.header.stamp = rospy.Time.now()
        self.acoustic_message_pub.publish(self.msg)
 
if __name__ == '__main__':

	try:
		rospy.init_node('acoustic_quality')
		AcousticQuality = AcousticQuality(rospy.get_name())
		rospy.spin()
	except rospy.ROSInterruptException:
		pass


