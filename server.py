import tkinter as tk
import tkinter.font as tkfont
import cv2
import PIL.Image
import PIL.ImageTk
import time
import socket, threading

class Client:  # 선생님 클래스.
    def __init__(self):
        self.clients = []
        self.allChat=None

    def addClient(self, c):  # c: 텔레마케터 . 클라이언트 1명씩 전담하는 쓰레드
        self.clients.append(c)

    def delClient(self, c):
        self.clients.remove(c)

    def sendMsgAll(self, msg):  # 채팅방에 있는 모든 사람한테 메시지 전송
        print(self.clients)
        for i in self.clients:
            print(i)
            i.sendMsg(msg)


class AttendClient:  # 텔레마케터
    def __init__(self, r, soc):
        self.room = r  # 채팅방. Room 객체
        self.soc = soc  # 사용자와 1:1 통신할 소켓

    def readAtnd(self):
        while True:
            try:
                readmsg = self.soc.recv(1024).decode()  # 사용자의 출석 여부 읽음
                # print(readmsg)
                if readmsg=='stop':
                    print('stop')
                    self.room.delClient(self)
                elif readmsg=='end.':
                    print('end.')
                    cs.client.sendMsgAll('end.')
                elif readmsg!='':
                    name=readmsg.split('/')[0]
                    atnd=readmsg.split('/')[1]
                    sendmsg=name+'/'+atnd
                    if atnd=='True' or 'False':
                        cs.client.sendMsgAll(sendmsg)
                    print(name,atnd)
            except ConnectionResetError:
                # print(ConnectionResetError)
                pass
            except ConnectionAbortedError:
                pass

    def sendMsg(self, msg):
        print(type(msg))
        self.soc.sendall(msg.encode(encoding='utf-8'))

class AttendServer:
    ip = '10.171.38.80'  # or 본인 ip or 127.0.0.1
    port = 9999

    def __init__(self):
        self.server_soc = None  # 서버 소켓(대문)
        self.client = Client()

    def open(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((AttendServer.ip, AttendServer.port))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('서버 시작!!')

        while True:
            client_soc, addr = self.server_soc.accept()
            print(client_soc, addr, '접속')
            c = AttendClient(self.client, client_soc)
            self.client.addClient(c)
            print('클라:', self.client.clients)
            th = threading.Thread(target=c.readAtnd)
            th.start()

        self.server_soc.close()


cs = AttendServer()
cs.run()
