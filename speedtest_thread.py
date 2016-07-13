#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import time
import sys
import os
import configloader
import importloader
from speedtest import speedtest_cli
import cymysql


def speedtest_thread():
	while True :
		hour = configloader.get_config().SPEEDTEST
		if hour == 0:
			break
		
		time.sleep(3600*hour)
		
		config = speedtest_cli.getConfig()
		
		CTid = 0
		servers = speedtest_cli.closestServers(config['client'], True)
		for server in servers:
			if server['country'].find('China') != -1 and server['sponsor'].find('Telecom') != -1:
				CTid = server['id']
		CTNode = speedtest_cli.getBestServer(filter(lambda x: x['id'] == CTid ,
                                        servers))
		CTPing = str(round(CTNode['latency'],2)) + ' ms'
		sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
		urls = []
		for size in sizes:
			for i in range(0, 4):
				urls.append('%s/random%sx%s.jpg' %
							(os.path.dirname(CTNode['url']), size, size))
		dlspeed = speedtest_cli.downloadSpeed(urls, True)
		CTDLSpeed = str(round((dlspeed / 1000 / 1000) * 8,2)) + " Mbps"
		
		sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
		sizes = []
		for size in sizesizes:
			for i in range(0, 25):
				sizes.append(size)
		ulspeed = speedtest_cli.uploadSpeed(CTNode['url'], sizes, True)
		CTUpSpeed = str(round((ulspeed / 1000 / 1000) * 8,2)) + " Mbps"
		
		
		
		
		CUid = 0
		servers = speedtest_cli.closestServers(config['client'], True)
		for server in servers:
			if server['country'].find('China') != -1 and server['sponsor'].find('Unicom') != -1:
				CUid = server['id']
		CUNode = speedtest_cli.getBestServer(filter(lambda x: x['id'] == CTid ,
                                        servers))
		CUPing = str(round(CUNode['latency'],2)) + " ms"
		sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
		urls = []
		for size in sizes:
			for i in range(0, 4):
				urls.append('%s/random%sx%s.jpg' %
							(os.path.dirname(CUNode['url']), size, size))
		dlspeed = speedtest_cli.downloadSpeed(urls, True)
		CUDLSpeed = str(round((dlspeed / 1000 / 1000) * 8,2)) + " Mbps"
		
		sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
		sizes = []
		for size in sizesizes:
			for i in range(0, 25):
				sizes.append(size)
		ulspeed = speedtest_cli.uploadSpeed(CUNode['url'], sizes, True)
		CUUpSpeed = str(round((ulspeed / 1000 / 1000) * 8,2)) + " Mbps"
		
		
		
		CMid = 0
		servers = speedtest_cli.closestServers(config['client'], True)
		for server in servers:
			if server['country'].find('China') != -1 and server['sponsor'].find('Mobile') != -1:
				CMid = server['id']
		CMNode = speedtest_cli.getBestServer(filter(lambda x: x['id'] == CTid ,
                                        servers))
		CMPing = str(round(CMNode['latency'],2)) + " ms"
		sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
		urls = []
		for size in sizes:
			for i in range(0, 4):
				urls.append('%s/random%sx%s.jpg' %
							(os.path.dirname(CMNode['url']), size, size))
		dlspeed = speedtest_cli.downloadSpeed(urls, True)
		CMDLSpeed = str(round((dlspeed / 1000 / 1000) * 8,2)) + " Mbps"
		
		sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
		sizes = []
		for size in sizesizes:
			for i in range(0, 25):
				sizes.append(size)
		ulspeed = speedtest_cli.uploadSpeed(CMNode['url'], sizes, True)
		CMUpSpeed = str(round((ulspeed / 1000 / 1000) * 8,2)) + " Mbps"
		
		
		
		conn = cymysql.connect(host=configloader.get_config().MYSQL_HOST, port=configloader.get_config().MYSQL_PORT, user=configloader.get_config().MYSQL_USER,
								passwd=configloader.get_config().MYSQL_PASS, db=configloader.get_config().MYSQL_DB, charset='utf8')
		cur = conn.cursor()
		cur.execute("INSERT INTO `speedtest` (`id`, `nodeid`, `datetime`, `telecomping`, `telecomeupload`, `telecomedownload`, `unicomping`, `unicomupload`, `unicomdownload`, `cmccping`, `cmccupload`, `cmccdownload`) VALUES (NULL, '" + str(configloader.get_config().NODE_ID) + "', unix_timestamp(), '" + CTPing + "', '" + CTUpSpeed + "', '" + CTDLSpeed + "', '" + CUPing + "', '" + CUUpSpeed + "', '" + CUDLSpeed + "', '" + CMPing + "', '" + CMUpSpeed + "', '" + CMDLSpeed + "')")
		cur.close()
		conn.commit()
		conn.close()
		
		logging.info("Speedtest finished")
		
		
