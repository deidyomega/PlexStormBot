import socketio
import requests
import json
from yaml import load, Loader


class User:
    def __init__(self, username, password, channel):
        self.username = username
        self.password = password
        self.channel = channel
        self.token = None

    def login(self):
        data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
            "client_id": "1",
            "client_secret": "tJ1Ng4AoDwnecJ1zknyX0cDd3BaxWAKR10s7YKnw",
        }
        result = requests.post(
            "https://api.plexstorm.com/oauth/token", data=data
        ).json()
        self.token = result["access_token"]

    def send_message(self, msg):
        if msg and isinstance(msg, str):
            self.__send_message(msg)
        else:
            for line in msg:
                USER.__send_message(line)

    def __send_message(self, msg):
        r = requests.post(
            "https://api.plexstorm.com/api/channels/{}/messages".format(self.channel),
            json={"message": msg},
            headers={
                "authorization": "Bearer " + self.token,
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json;charset=UTF-8",
            },
        )


class Message:
    def __init__(self, msg):
        self.raw = msg

    def content(self):
        return self.raw["data"]["message"]["content"]

    def is_tip(self):
        return self.raw["data"]["message"]["type"] == "tip"

    def user(self):
        return self.raw["data"]["message"]["user"]["name"]


class Settings:
    def __init__(self):
        with open("settings.yml", "r") as f:
            data = load(f, Loader=Loader)
            print(data)

        self.username = data["username"]
        self.password = data["password"]
        self.channel = data["channel"]
        self.commands = data["commands"]
        self.tip_commands = data["tip_commands"]


## SETUP APPLICATION

SETTINGS = Settings()
sio = socketio.Client()
USER = User(SETTINGS.username, SETTINGS.password, SETTINGS.channel)
USER.login()


@sio.event
def connect():
    print("Connected to WSS")

    sio.emit(
        "subscribe",
        {
            "channel": "channel." + SETTINGS.channel,
            "auth": {"headers": {"Authorization": "Bearer " + USER.token}},
        },
    )


def get_cmd(content, tip=False):
    if not tip:
        content = content[1:]
        for item in SETTINGS.commands:
            if content in item.keys():
                return item[content[1:]]
    # TIP MENU
    for item in SETTINGS.tip_commands:
        if content in item.keys():
            return item[content[1:]]


@sio.on("App\Events\MessageCreated")
def my_message(channel, data):
    m = Message(data)
    if m.content().startswith("!") or m.is_tip():
        cmd = get_cmd(m.content(), m.is_tip())
        if cmd:
            USER.send_message(cmd)


@sio.event
def disconnect():
    print("disconnected from server")


sio.connect("https://websocket.plexstorm.com/socket.io/")
sio.wait()
