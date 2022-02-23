#!/usr/bin/env python
import os
import rospy
import std_msgs.msg
from link_quality.msg import  AcousticLink
from evologics_ros_sync.msg import EvologicsChannelDiagnostics,EvologicsUsbllong

class AcousticQuality():

    def __init__(self,name):
        #Subscribers
        rospy.Subscriber("/turbot/evologics_channel",
                        EvologicsChannelDiagnostics,    
                        self.update_evologics_channel,
                        queue_size=1)

        rospy.Subscriber("/xiroi/usbllong",
                        EvologicsUsbllong,    
                        self.update_evologics_usbllong,
                        queue_size=1)

        #Publishers
        self.acoustic_message_pub = rospy.Publisher("network_analysis/acoustic_quality",
                                                AcousticLink,
                                                queue_size=1)

        # Init periodic timer
        rospy.Timer(rospy.Duration(1.0), self.message_publisher)
        self.msg = AcousticLink()
                        

    def update_evologics_channel(self,chanel_msg):
        self.msg.rssi_modem = chanel_msg.rssi
        self.msg.integrity_modem = chanel_msg.integrity


    def update_evologics_usbllong(self,usbllong_msg):
        self.msg.rssi_usbl = usbllong_msg.rssi
        self.msg.integrity_usbl = usbllong_msg.integrity
        self.msg.accuracy_usbl = usbllong_msg.accuracy

    def message_publisher(self,event):

        self.msg.header.stamp = rospy.Time.now()
        self.acoustic_message_pub.publish(self.msg)


if __name__ == '__main__':

	try:
		rospy.init_node('acoustic_quality')
		AcousticQuality = AcousticQuality(rospy.get_name())
		rospy.spin()
	except rospy.ROSInterruptException:
		pass


