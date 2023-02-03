#!/usr/bin/env python
import os
import rospy
import paramiko
import std_msgs.msg
from link_quality.msg import WirelessLink
ssh = paramiko.SSHClient()
msg = WirelessLink()


def wireless_quality(pep):
	hostname = rospy.get_param('~host_name')
	username = rospy.get_param('username', 'ubnt')
	password = rospy.get_param('password', 'underwaterpass')
	update_rate = rospy.get_param('~update_rate', 1)	
	pub_wireles_info = rospy.Publisher('network_analysis/wireless_quality', WirelessLink, queue_size=10)
	rate = rospy.Rate(update_rate)

	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username=username, password=password)
	print("Connected...")

	while not rospy.is_shutdown():
		msg.header.stamp = rospy.Time.now()
		values = get_info_from_device()
		# print("-----------------------------------------")
		# print(values)
		# print(type(values))

		for value in values:

			if "SSID" in value :
				SSID = value.split (":")
				msg.SSID = SSID[1]

			if "Mode" in value :
				mode = value.split (":")
				msg.mode = mode[1]

			if "Access Point" in value :
				access_point = value.split (":")
				msg.access_point = access_point[1]
				# msg.access_point = access_point

			if "Frequency" in value :
				frequency = value.split (":")
				frequency = frequency[1]
				frequency = frequency.split (" ")
				msg.frequency = float(frequency[0])

			if "Bit Rate" in value :
				bitrate = value.split ("=")
				bitrate = bitrate[1]
				bitrate = bitrate.split (" ")
				msg.bitrate = float(bitrate[0])

			if "Tx-Power" in value :
				tx_power = value.split ("=")
				tx_power = tx_power[1]
				tx_power = tx_power.split (" ")
				msg.tx_power = float(tx_power[0])

			if "Sensitivity" in value :
				sensitivity = value.split (":")
				msg.sensitivity = sensitivity[1]

			if "Link Quality" in value :
				link_quality = value.split ("=")
				msg.link_quality = link_quality[1]

			if "Signal level" in value :
				signal_level = value.split ("=")
				signal_level = signal_level[1]
				signal_level = signal_level.split (" ")
				msg.signal_level = int(signal_level[0])

			if "Noise level" in value :
				noise_level = value.split ("=")
				noise_level = noise_level[1]
				noise_level = noise_level.split (" ")
				msg.noise_level = int(noise_level[0])

			if "Rx invalid nwid" in value :
				rx_invalid_nwid = value.split (":")
				msg.rx_invalid_nwid = int(rx_invalid_nwid[1])

			if "Rx invalid crypt" in value :
				rx_invalid_crypt = value.split (":")
				msg.rx_invalid_crypt = int(rx_invalid_crypt[1])

			if "Rx invalid frag" in value :
				rx_invalid_frag = value.split (":")
				msg.rx_invalid_frag = int(rx_invalid_frag[1])

			if "Tx excessive retries" in value :
				tx_excessive_retries = value.split (":")
				msg.tx_excessive_retries = int(tx_excessive_retries[1])

			if "Invalid misc" in value :
				invalid_misc = value.split (":")
				msg.invalid_misc = int(invalid_misc[1])

			if "Missed beacons" in value :
				missed_beacons = value.split (":")
				msg.missed_beacons = int(missed_beacons[1])

	  	pub_wireles_info.publish(msg)
    		rate.sleep()

def get_info_from_device():

	try:

		cmd ="iwconfig ath0" 
		stdin, stdout, stderr = ssh.exec_command(cmd)
		out = stdout.read().strip()
		return  out.split("  ")

	except:
    		rospy.loginfo("The specified interface does not exist or is disconnected. Please check it")
		pass

if __name__ == '__main__':

	try:
		rospy.init_node('wireless_quality')
		wireless_quality = wireless_quality(rospy.get_name())
		rospy.spin()
	except rospy.ROSInterruptException:
		pass




