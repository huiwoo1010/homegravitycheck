import tkinter as tk
import tkinter.font as tkfont
import matplotlib.pyplot as plt
import cv2
import PIL.Image
import PIL.ImageTk
import time
import socket
import threading
import model

aiclass = 0
start_time = 0
first_time = 0
name_idx = 0
name = ''
recog_results=[0 for i in range(0,10)]
class_attend=dict()


def open_frame(frame):
    try:
        if frame == main_frm:
            root.geometry('333x500')
        frame.tkraise()
    except IndexError:
        pass


class Web:
    ip = '10.171.38.80'
    port = 9999

    def __init__(self, win, video_source=0):
        self.win = win
        self.conn_soc = None
        self.conn()

        self.th2 = threading.Thread(target=self.recvMsg)
        self.th2.start()
        # self.win.mainloop()
        self.video_source = video_source
        self.ok = False

        self.resultcnt = 0

        if aiclass==1:
            self.webframe_image = tk.PhotoImage(file='files/webframe1.png')
        else:
            self.webframe_image = tk.PhotoImage(file='files/webframe2.png')
        tk.Label(win, image=self.webframe_image).place(x=0, y=0)
        self.btn_home = tk.Button(win, image=home_image, command=lambda: [save_result(), open_frame(main_frm), self.close_camera(),
                                                                          self.close_conn()])
        self.btn_home.place(x=85, y=260)

        self.vid = VideoCapture(self.video_source)

        self.webcamcanvas = tk.Canvas(win, width=188, height=105)
        self.webcamcanvas.place(x=6, y=40)

        self.time_label=tk.Label(win, text="00:00.00", bg='navy', fg='white', font=tkfont.Font(size=20, weight="bold"))
        self.time_label.place(x=45, y=150)

        # self.btn_snapshot = tk.Button(win, text='Snapshot', command=self.snapshot)
        # self.btn_snapshot.place(x=10, y=200)
        self.flag = False
        self.start_time = start_time
        self.delay = 10
        self.update()
        self.win.mainloop()

    def conn(self):
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((Web.ip, Web.port))

    def sendAtnd(self, name,atnd):  # 출석 정보 전송
        print('sendAtnd')
        if atnd==True:
            atnd='True'
        elif atnd==False:
            atnd='False'
        msg2send=name+'/'+atnd
        msg2send=msg2send.encode(encoding='utf-8')

        self.conn_soc.send(msg2send)
        print('전송')

    def recvMsg(self):  # 상대방이 보낸 메시지 읽어서 화면에 출력
        # print('리드')
        global class_attend, name
        while True:
            # print('리드')
            try:
                msg = self.conn_soc.recv(1024).decode()
                print(msg)
                if msg=='end.':
                    print('end.')
                    self.resultcnt=10
            except OSError:
                exit()
                print(OSError)
                pass

    # def run(self):
    #     self.conn()
    #
    #     th2 = threading.Thread(target=self.recvMsg)
    #     th2.start()
    #     self.win.mainloop()

    def close_conn(self):
        self.conn_soc.send('stop'.encode(encoding='utf-8'))
        self.conn_soc.close()
        print('종료되었습니다')

    def snapshot(self):
        global aiclass, name_idx
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("image/" + "%d_" % aiclass + name + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)) #+ time.strftime("%H-%M-%S")

    def close_camera(self):
        self.ok = False
        self.vid.vid.release()
        self.done = True

    def update(self):
        global recog_results
        if self.resultcnt>=10:
            return
        try:
            ret, frame = self.vid.get_frame()

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.webcamcanvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.win.after(self.delay, self.update)

            self.cur_time = time.time()
            if self.cur_time-first_time>0 and self.flag==False:
                self.flag=True
                self.snapshot()
                print('snapshot')
                atnd, recogname = model.recog(aiclass, name)
                print(atnd)
                print(recogname)
                if atnd==True:
                    recog_results[self.resultcnt]=1
                    label_O=tk.Label(self.win,image=O_image,bg='#000080')
                    label_O.image=O_image
                    if self.resultcnt>=7:
                        label_O.place(x=19 * (self.resultcnt) + 9, y=218)
                    else:
                        label_O.place(x=19*(self.resultcnt)+10,y=218)
                elif atnd==False:
                    recog_results[self.resultcnt]=0
                    label_X=tk.Label(self.win,image=X_image,bg='#000080')
                    label_X.image=X_image
                    if self.resultcnt>=7:
                        label_X.place(x=19 * (self.resultcnt) + 9, y=218)
                    else:
                        label_X.place(x=19*(self.resultcnt)+10,y=218)
                self.sendAtnd(name, atnd)
            if 5 <= (self.cur_time - self.start_time) :
                self.start_time = self.cur_time
                self.snapshot()
                print('snapshot')
                atnd,recogname=model.recog(aiclass, name)
                print(atnd)
                print(recogname)
                if atnd==True:
                    recog_results[self.resultcnt]=1
                    label_O=tk.Label(self.win,image=O_image,bg='#000080')
                    label_O.image=O_image
                    if self.resultcnt>=7:
                        label_O.place(x=19 * (self.resultcnt+1) + 9, y=218)
                    else:
                        label_O.place(x=19*(self.resultcnt+1)+10,y=218)
                    self.resultcnt = self.resultcnt + 1
                elif atnd==False:
                    recog_results[self.resultcnt]=0
                    label_X=tk.Label(self.win,image=X_image,bg='#000080')
                    label_X.image=X_image
                    if self.resultcnt>=7:
                        label_X.place(x=19 * (self.resultcnt+1) + 9, y=218)
                    else:
                        label_X.place(x=19*(self.resultcnt+1)+10,y=218)
                    self.resultcnt = self.resultcnt + 1
                self.sendAtnd(name,atnd)
            time_flow=self.cur_time-first_time
            self.time_label.config(text="%02d"%((time_flow/60)%60)+":%02d"%((time_flow%60)))
        except TypeError:
            pass


class VideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        res = (1280, 720)
        self.vid.set(3, res[0])
        self.vid.set(4, res[1])
        self.width, self.height = res

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                resize_frame = cv2.resize(frame, (188, 105), interpolation=cv2.INTER_CUBIC)
                return ret, cv2.cvtColor(resize_frame, cv2.COLOR_RGB2BGR)
            else:
                return ret, None
        else:
            return None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()

def save_result():
    global recog_results
    X_num=0
    O_num=0
    for i in range(0,10):
        if recog_results[i]==0:
            X_num=X_num+1
        elif recog_results[i]==1:
            O_num=O_num+1
    print(O_num,X_num)
    ratio = [O_num*10, X_num*10]
    labels = ['O', 'X']
    explode = [0.05, 0.05]
    colors = ['blue','silver']

    plt.pie(ratio, labels=labels, autopct='%.1f%%',explode=explode, colors=colors, shadow=True)
    plt.savefig('result_graph.jpg')

def class1_go(input):
    global name_idx, start_time, name, first_time
    print(name)
    class1_names = ['juwon', 'seonho', 'yuchan', 'taeyoungK', 'taeyoungY', 'damhyun', 'hanjin', 'wonyoung', 'youngbin',
                    'chanmo', 'yerim', 'donghwa', 'sungbin']
    for i in range(0, 13):
        if class1_names[i] == input:
            name_idx = i
            name = class1_names[i]
            first_time = time.time()
            start_time = time.time()
            class1_frm = tk.Frame(root, width=200, height=300)
            class1_frm.grid(row=0, column=0, sticky="nsew")
            try:
                root.after(10, Web(class1_frm))
            except AttributeError:
                pass
            break


def class2_go(input):
    global name_idx, start_time, name, first_time
    class2_names = ['wooseok', 'seongho', 'beomjun', 'sanghoon', 'jinsoo', 'minjun', 'minsu', 'donggun', 'seokjun',
                    'sieun', 'huiwoo', 'jinuk']
    for i in range(0, 12):
        if class2_names[i] == input:
            name_idx = i
            name = class2_names[i]
            first_time = time.time()
            start_time = time.time()
            class2_frm = tk.Frame(root, width=200, height=300)
            class2_frm.grid(row=0, column=0, sticky="nsew")
            try:
                root.after(10, Web(class2_frm))
            except AttributeError:
                pass
            break


def class1():
    global aiclass, start_time
    root.geometry('200x300')
    aiclass = 1
    name1_frm = tk.Frame(root, width=200, height=300)
    name1_frm.grid(row=0, column=0, sticky="nsew")
    tk.Label(name1_frm, image=background_image).place(x=0, y=0)
    btn_home = tk.Button(name1_frm, image=home_image, command=lambda: (open_frame(main_frm)))
    btn_home.place(x=85, y=260)
    class1_entry = tk.Entry(name1_frm, width=12)
    class1_entry.place(x=30, y=23)
    entry1_btn = tk.Button(name1_frm, text="Enter",bg='navy',fg='white', command=lambda: class1_go(class1_entry.get()))
    entry1_btn.place(x=135, y=20)
    root.bind("<Return>", class1_go(class1_entry.get()))


def class2():
    global aiclass, start_time, name
    root.geometry('200x300')
    aiclass = 2
    name2_frm = tk.Frame(root, width=200, height=300)
    name2_frm.grid(row=0, column=0, sticky="nsew")
    tk.Label(name2_frm, image=background_image).place(x=0, y=0)
    btn_home = tk.Button(name2_frm, image=home_image, command=lambda: (open_frame(main_frm)))
    btn_home.place(x=85, y=260)
    class2_entry = tk.Entry(name2_frm, width=12)
    class2_entry.place(x=30, y=23)
    entry2_btn = tk.Button(name2_frm, text="Enter",bg='navy',fg='white', command=lambda: class2_go(class2_entry.get()))
    entry2_btn.place(x=135, y=20)
    root.bind("<Return>", class2_go(class2_entry.get()))


def teacher():
    root.geometry('200x300')
    teacher_frm = tk.Frame(root, width=200, height=300)
    teacher_frm.grid(row=0, column=0, sticky="nsew")
    tk.Label(teacher_frm, image=background_image).place(x=0, y=0)
    btn_home = tk.Button(teacher_frm, image=home_image, command=lambda: open_frame(main_frm))
    btn_home.place(x=85, y=260)


root = tk.Tk()
root.title('인공프 출석 확인 시스템(학생용)')
root.geometry('333x500+0+0')
root.resizable(False, False)

main_frm = tk.Frame(root, width=333, height=500)
start_image = tk.PhotoImage(file='files/start.png')
start_label = tk.Label(main_frm, image=start_image)
start_label.place(x=0, y=0)

main_frm.grid(row=0, column=0, sticky="nsew")
class1_image = tk.PhotoImage(file='files/aiclass1.png')
class2_image = tk.PhotoImage(file='files/aiclass2.png')
class1_btn = tk.Button(main_frm, image=class1_image, command=class1)
class2_btn = tk.Button(main_frm, image=class2_image, command=class2)
quit_btn = tk.Button(main_frm, text="끝내기", bg='navy', fg='white', command=lambda:[root.destroy(), exit()])
home_image=tk.PhotoImage(file='files/home2.png')
background_image=tk.PhotoImage(file='files/background.png')
O_image=tk.PhotoImage(file='files/o.png')
X_image=tk.PhotoImage(file='files/x.png')

class1_btn.place(x=30, y=320)
class2_btn.place(x=30, y=355)
quit_btn.place(x=272, y=11)

root.mainloop()
