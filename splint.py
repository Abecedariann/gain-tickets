# -*- coding: UTF-8 -*-
import time
from splinter import Browser

class ticket(object):
	def __init__(self,data,fromw,tow,trainnum,autorefresh=False):
		self.b = Browser('chrome')
		self.url = "https://kyfw.12306.cn/otn/login/init"
		self.autorefresh=autorefresh
		self.data=data
		self.fromw=fromw
		self.tow=tow
		self.trainnum=trainnum
		
	def login(self):
		self.b.visit(self.url)
		self.b.fill('loginUserDTO.user_name','')	###用户名
		self.b.fill('userDTO.password','')			###密码
		while True:
			if self.b.url!='https://kyfw.12306.cn/otn/index/initMy12306':
				time.sleep(1)						###等待跳转 
			else:
				break
		self.capture_ticket()
	def capture_ticket(self):
		self.b.find_by_id('selectYuding').click()
		self.b.cookies.add({"_jc_save_fromDate":self.data})				
		self.b.cookies.add({"_jc_save_fromStation":self.fromw})	###  添加cookie
		self.b.cookies.add({"_jc_save_toStation":self.tow})		###	 
		self.b.reload()
		self.b.find_by_id('query_ticket').click()
		while True:
			try:
				path="//a[contains(@onclick,'"+self.trainnum+"')]"
				self.b.find_by_xpath(path)[1].click()	###0表示前面车次 1表示预定  
				self.b.find_by_xpath("//*[@id='normalPassenger_0']").click()
				self.b.find_by_id('submitOrder_id').click()
				time.sleep(2)							###点击确认按钮等待时间
				self.b.find_by_xpath('//*[@id="qr_submit_id"]').click()
				print('购票成功，请及时付款')
			except Exception as e:
				print(e)
				if str(e).startswith('no elements could be found with xpath'):
					print(('暂时没有票'+time.strftime("%H:%M:%S", time.localtime())))
					if self.autorefresh==True:
						time.sleep(10)				###网页刷新时间
						self.b.find_by_id('query_ticket').click()		###自动点击查询
						continue
					else:
						break
			else:
				break
			finally:
				pass

	def start(self):
		self.login()

if __name__ == '__main__':
	a=ticket('''''')
	a.start()

