parameters = {

    "community-link":
        "http://aminoapps.com/invite/F51YRR9TTD"}

import os
import time
import json
import hmac
import base64
import random
import datetime
from base64 import b64encode
from hmac import new
from binascii import hexlify
from hashlib import sha1

try:
    import pytz
    import requests
    from flask import Flask
    from json_minify import json_minify
except:
    os.system("pip3 install pytz requests flask json_minify")
finally:
    import requests
    from flask import Flask
    from json_minify import json_minify

from threading import Thread
from uuid import uuid4
from hashlib import sha1







os.system("clear")
print(f"{os.getcwd()}\n")
session = requests.Session()
#######################################################
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "~~8;> ~~8;>"
    

def run(): flask_app.run(host = '0.0.0.0', port = random.randint(2000, 9000))
###########################################################
class Client:
    def __init__(self):
        self.api = "https://service.narvii.com/api/v1"
        self.device_Id = self.generate_device_Id()
        self.headers = {"NDCDEVICEID": self.device_Id, "SMDEVICEID": "b89d9a00-f78e-46a3-bd54-6507d68b343c", "Accept-Language": "en-EN", "Content-Type": "application/json; charset=utf-8", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)", "Host": "service.narvii.com", "Accept-Encoding": "gzip", "Connection": "keep_alive"}
        self.sid, self.auid = None, None

    def generate_device_Id(self):
        identifier = os.urandom(20)
        return ("42" + identifier.hex() + hmac.new(bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F"), b"\x42" + identifier, sha1).hexdigest()).upper()

    def generate_signature_message(self, data):
        return base64.b64encode(bytes.fromhex("42") + hmac.new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), data.encode("utf-8"), sha1).digest()).decode("utf-8")

    def login(self, email: str, password: str):
        data = json.dumps({"email": email, "secret": f"0 {password}", "deviceID": self.device_Id, "clientType": 100, "action": "normal", "timestamp": (int(time.time() * 1000))})
        self.headers["ndc-msg-sig"] = self.generate_signature_message(data = data)
        request = session.post(f"{self.api}/g/s/auth/login", data = data, headers = self.headers)
        try: self.sid, self.auid = request.json()["sid"], request.json()["auid"]
        except: pass
        return request.json()

    def send_active_object(self, comId: int, start_time: int = None, end_time: int = None, timers: list = None, tz: int = -time.timezone // 1000):
        data = {"userActiveTimeChunkList": [{"start": start_time, "end": end_time}], "timestamp": int(time.time() * 1000), "optInAdsFlags": 2147483647, "timezone": tz}
        if timers: data["userActiveTimeChunkList"] = timers
        data = json_minify(json.dumps(data))
        self.headers["ndc-msg-sig"] = self.generate_signature_message(data = data)
        request = session.post(f"{self.api}/x{comId}/s/community/stats/user-active-time?sid={self.sid}", data = data, headers = self.headers)
        return request.json()

    def watch_ad(self): return session.post(f"{self.api}/g/s/wallet/ads/video/start?sid={self.sid}", headers = self.headers).json()

    def get_from_link(self, link: str): return session.get(f"{self.api}/g/s/link-resolution?q={link}", headers = self.headers).json()

    def lottery(self, comId, time_zone: str = -int(time.timezone) // 1000):
        data = json.dumps({"timezone": time_zone, "timestamp": int(time.time() * 1000)})
        self.headers["ndc-msg-sig"] = self.generate_signature_message(data = data)
        request = session.post(f"{self.api}/x{comId}/s/check-in/lottery?sid={self.sid}", data = data, headers = self.headers)
        return request.json()

    def join_community(self, comId: int, inviteId: str = None):
        data = {"timestamp": int(time.time() * 1000)}
        if inviteId: data["invitationId"] = inviteId
        data = json.dumps(data)
        self.headers["ndc-msg-sig"] = self.generate_signature_message(data=data)
        request = session.post(f"{self.api}/x{comId}/s/community/join?sid={self.sid}", data = data, headers = self.headers)
        return request.json()

class App:
    def __init__(self):
        self.client = Client()
        extensions = self.client.get_from_link(parameters["community-link"])["linkInfoV2"]["extensions"]
        self.comId = extensions["community"]["ndcId"]
        try: self.invitationId = extensions["invitationId"]
        except: self.invitationId = None 
    def tzc(self):
        UTC = {"+11":'+660',"+10":'+600',"+09":'+540',"+08":'+480',"+07":'+420',"+06":'+360',"+05":'+300',"+04":'+240',"+03":'+180',"+02":'+120',"+01":'+60',"GMT":'+0',"-01":'-60',"-02":'-120',"-03":'-180',"-04":'-240',"-05":'-300',"-06":'-360',"-07":'-420',"-08":'-480',"-09":'-540',"-10":'-600',"-11":'-660',"-12":'+720'}
        zones = ['Etc/GMT-11','Etc/GMT-10','Etc/GMT-9','Etc/GMT-8','Etc/GMT-7','Etc/GMT-6','Etc/GMT-5','Etc/GMT-4','Etc/GMT-3','Etc/GMT-2','Etc/GMT-1','Etc/GMT0','Etc/GMT+1','Etc/GMT+2','Etc/GMT+3','Etc/GMT+4','Etc/GMT+5','Etc/GMT+6','Etc/GMT+7','Etc/GMT+8','Etc/GMT+9','Etc/GMT+10','Etc/GMT+11','Etc/GMT+12']
        for _ in zones:
            H = datetime.datetime.now(pytz.timezone(_)).strftime("%H"); Z = datetime.datetime.now(pytz.timezone(_)).strftime("%Z")
            if H=="23": break
        return int(UTC[Z])
    def generation(self, email: str, password: str):
        try:
            print(f"\n[\033[1;31mXXX-GEN-XXX\033[0m][\033[1;34mInicio de sesion\033[0m][{email}]: {self.client.login(email = email, password = password)['api:message']}.")
            print(f"[\033[1;31mXXX-GEN-XXX\033[0m][\033[1;36mEntro en la Comunidad\033[0m]: {self.client.join_community(comId = self.comId, inviteId = self.invitationId)['api:message']}.")
            print(f"[\033[1;31mXXX-GEN-XXX\033[0m][\033[1;32mLoteria\033[0m]: {self.client.lottery(comId = self.comId, time_zone = self.tzc())['api:message']}")
            print(f"[\033[1;31m\033[0m][\033[1;33mAnuncios\033[0m]: {self.client.watch_ad()['api:message']}.")
            for i2 in range(24):
                time.sleep(12)
                print(f"[\033[1;31mXXX-GEN-XXX\033[0m][\033[1;35mProcesos\033[0m][{email}]: {self.client.send_active_object(comId = self.comId, timers = [{'start': int(time.time()), 'end': int(time.time()) + 300} for _ in range(50)], tz = self.tzc())['api:message']}.")
            print(f"[\033[1;31mXXX-GEN-XXX\033[0m][\033[1;25;32mFin\033[0m][{email}]: Finalizado.")
        except Exception as error: print(f"[\033[1;31mC01?-G3?3R4?0R\033[0m]][\033[1;31merror\033[0m]]: {error}")

    def run(self):
        print("COIN GENERATOR ")
        with open("accounts.json", "r") as emails:
            emails = json.load(emails)
            print(f"{len(emails)} Accounts loaded")
            for account in emails:
                self.client.device_Id = account["device"]
                self.client.headers["NDCDEVICEID"] = self.client.device_Id
                self.generation(email = account["email"], password = account["password"])

if __name__ == "__main__":
    while True:
      App().run()
