import tkinter as tk
import tkinter.font as tkfont
import cv2
import PIL.Image
import PIL.ImageTk
import time
import socket
import threading

aiclass = 0
start_time = 0
first_time = 0
name_idx = 0
name = ''
class1_attend=['0000000000' for i in range(0, 13)]
class1_names = ['juwon', 'seonho', 'yuchan', 'taeyoungK', 'taeyoungY', 'damhyun', 'hanjin', 'wonyoung', 'youngbin',
                'chanmo', 'yerim', 'donghwa', 'sungbin']
class2_attend=['0000000000' for i in range(0, 12)]
class2_names = ['wooseok', 'seongho', 'beomjun', 'sanghoon', 'jinsoo', 'minjun', 'minsu', 'donggun', 'seokjun',
                'sieun', 'huiwoo', 'jinuk']

class_names=['juwon', 'seonho', 'yuchan', 'taeyoungK', 'taeyoungY', 'damhyun', 'hanjin', 'wonyoung', 'youngbin',
            'chanmo', 'yerim', 'donghwa', 'sungbin', 'wooseok', 'seongho', 'beomjun', 'sanghoon', 'jinsoo',
             'minjun', 'minsu', 'donggun', 'seokjun', 'sieun', 'huiwoo', 'jinuk']

def open_frame(frame):
    try:
        frame.tkraise()
        print('d')
        root.after(10, Web(frame))
        # try:
        #     root.after(10, Web(frame))
        # except AttributeError:
        #     pass

    except IndexError:
        pass


class Web:
    ip = '10.171.38.80'
    port = 9999

    def __init__(self, win):
        global aiclass, start_time
        self.win = win
        self.conn_soc = None
        self.conn()

        self.th2 = threading.Thread(target=self.recvMsg)
        self.th2.start()
        # self.win.mainloop()
        self.ok = False
        self.resultcnt = 0
        self.yes_cnt=0

        self.time_label=tk.Label(self.win, text="00:00.00", bg='navy', fg='white', font=tkfont.Font(size=30, weight="bold"))
        self.time_label.place(x=90, y=325)

        # self.btn_home = tk.Button(win, image=home_image, command=lambda: [main_frm.tkraise(), self.close_conn()])
        # self.btn_home.place(x=152, y=457)
        self.quit_btn = tk.Button(self.win, text="끝내기", bg='navy', fg='white', command=lambda: [root.destroy(), self.close_conn(), exit()])
        self.quit_btn.place(x=272, y=11)

        self.start_time=start_time

        # for i in range(0, 12):
        #     class1_attend[i]='0000000000'
        #     class2_attend[i]='0000000000'
        # class1_attend[12]='0000000000'

        self.oxlabels=[]
        for i in range(0, 10):
            self.oxlabels.append(tk.Label(self.win, image=blank_image, bg='#000080'))
            self.oxlabels[i].image=blank_image
            self.oxlabels[i].place(x=19+i*31, y=269)

        self.num1_label=tk.Label(self.win, image=number_img[0], bg='#000080')
        self.num1_label.image=blank_image
        self.num1_label.place(x=120, y=393)
        self.num2_label=tk.Label(self.win, image=number_img[0], bg='#000080')
        self.num2_label.image=blank_image
        self.num2_label.place(x=170, y=393)

        self.class1_name_btn = []
        self.class2_name_btn = []
        if aiclass==1:
            if self.class1_name_btn==[]:
                for i in range(0, 13):
                    self.class1_name_btn.append(tk.Button(self.win))

                self.class1_name_btn[0]=tk.Button(self.win, image=class1_name_n_img[0], command=lambda: [self.idx_set(0), self.class1_btn_config(0)])
                self.class1_name_btn[1]=tk.Button(self.win, image=class1_name_n_img[1], command=lambda: [self.idx_set(1), self.class1_btn_config(1)])
                self.class1_name_btn[2]=tk.Button(self.win, image=class1_name_n_img[2], command=lambda: [self.idx_set(2), self.class1_btn_config(2)])
                self.class1_name_btn[3]=tk.Button(self.win, image=class1_name_n_img[3], command=lambda: [self.idx_set(3), self.class1_btn_config(3)])
                self.class1_name_btn[4]=tk.Button(self.win, image=class1_name_n_img[4], command=lambda: [self.idx_set(4), self.class1_btn_config(4)])
                self.class1_name_btn[5]=tk.Button(self.win, image=class1_name_n_img[5], command=lambda: [self.idx_set(5), self.class1_btn_config(5)])
                self.class1_name_btn[6]=tk.Button(self.win, image=class1_name_n_img[6], command=lambda: [self.idx_set(6), self.class1_btn_config(6)])
                self.class1_name_btn[7]=tk.Button(self.win, image=class1_name_n_img[7], command=lambda: [self.idx_set(7), self.class1_btn_config(7)])
                self.class1_name_btn[8]=tk.Button(self.win, image=class1_name_n_img[8], command=lambda: [self.idx_set(8), self.class1_btn_config(8)])
                self.class1_name_btn[9]=tk.Button(self.win, image=class1_name_n_img[9], command=lambda: [self.idx_set(9), self.class1_btn_config(9)])
                self.class1_name_btn[10]=tk.Button(self.win, image=class1_name_n_img[10], command=lambda: [self.idx_set(10), self.class1_btn_config(10)])
                self.class1_name_btn[11]=tk.Button(self.win, image=class1_name_n_img[11], command=lambda: [self.idx_set(11), self.class1_btn_config(11)])
                self.class1_name_btn[12]=tk.Button(self.win, image=class1_name_n_img[12], command=lambda: [self.idx_set(12), self.class1_btn_config(12)])

            for i in range(0, 10):
                self.class1_name_btn[i].place(x=20+(i%5)*60, y=int(i/5)*33+90)
            self.class1_name_btn[10].place(x=80, y=2 * 33 + 90)
            self.class1_name_btn[11].place(x=140, y=2 * 33 + 90)
            self.class1_name_btn[12].place(x=200, y=2*33+90)

        elif aiclass==2:
            if self.class2_name_btn==[]:
                for i in range(0, 12):
                    self.class2_name_btn.append(tk.Button(self.win))

                self.class2_name_btn[0]=tk.Button(self.win, image=class2_name_n_img[0], command=lambda: [self.idx_set(13), self.class2_btn_config(0)])
                self.class2_name_btn[1]=tk.Button(self.win, image=class2_name_n_img[1], command=lambda: [self.idx_set(14), self.class2_btn_config(1)])
                self.class2_name_btn[2]=tk.Button(self.win, image=class2_name_n_img[2], command=lambda: [self.idx_set(15), self.class2_btn_config(2)])
                self.class2_name_btn[3]=tk.Button(self.win, image=class2_name_n_img[3], command=lambda: [self.idx_set(16), self.class2_btn_config(3)])
                self.class2_name_btn[4]=tk.Button(self.win, image=class2_name_n_img[4], command=lambda: [self.idx_set(17), self.class2_btn_config(4)])
                self.class2_name_btn[5]=tk.Button(self.win, image=class2_name_n_img[5], command=lambda: [self.idx_set(18), self.class2_btn_config(5)])
                self.class2_name_btn[6]=tk.Button(self.win, image=class2_name_n_img[6], command=lambda: [self.idx_set(19), self.class2_btn_config(6)])
                self.class2_name_btn[7]=tk.Button(self.win, image=class2_name_n_img[7], command=lambda: [self.idx_set(20), self.class2_btn_config(7)])
                self.class2_name_btn[8]=tk.Button(self.win, image=class2_name_n_img[8], command=lambda: [self.idx_set(21), self.class2_btn_config(8)])
                self.class2_name_btn[9]=tk.Button(self.win, image=class2_name_n_img[9], command=lambda: [self.idx_set(22), self.class2_btn_config(9)])
                self.class2_name_btn[10]=tk.Button(self.win, image=class2_name_n_img[10], command=lambda: [self.idx_set(23), self.class2_btn_config(10)])
                self.class2_name_btn[11]=tk.Button(self.win, image=class2_name_n_img[11], command=lambda: [self.idx_set(24), self.class2_btn_config(11)])

            for i in range(0, 10):
                self.class2_name_btn[i].place(x=20 + (i % 5) * 60, y=int(i / 5) * 33 + 90)
            self.class2_name_btn[10].place(x=110, y=2 * 33 + 90)
            self.class2_name_btn[11].place(x=170, y=2 * 33 + 90)

        # self.delay = 10
        self.update()
        self.win.mainloop()

    def idx_set(self, i):
        global name_idx
        print('set')
        name_idx = i
        if name_idx <= 12:
            atnd_list = list(class1_attend[name_idx])
            self.yes_cnt=0
            for i in range(0, 10):
                if atnd_list[i] == 'o':
                    self.yes_cnt+=1
                    self.oxlabels[i].config(image=O_image)
                elif atnd_list[i] == 'x':
                    self.oxlabels[i].config(image=X_image)
                elif atnd_list[i] == '0':
                    self.oxlabels[i].config(image=blank_image)
                else:
                    print('something went wrong...')

        elif name_idx > 12:
            atnd_list = list(class2_attend[name_idx - 13])
            self.yes_cnt=0
            for i in range(0, 10):
                if atnd_list[i] == 'o':
                    self.yes_cnt += 1
                    self.oxlabels[i].config(image=O_image)
                elif atnd_list[i] == 'x':
                    self.oxlabels[i].config(image=X_image)
                elif atnd_list[i] == '0':
                    self.oxlabels[i].config(image=blank_image)
                else:
                    print('something went wrong...')
        self.num1_label.config(image=number_img[self.yes_cnt])
        self.num2_label.config(image=number_img[self.resultcnt+1 if self.resultcnt<=9 else 10])


    def conn(self):
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((Web.ip, Web.port))

    # def sendAtnd(self, atnd):  # 출석 정보 전송
    #     print('sendAtnd')
    #     if atnd==True:
    #         atnd='True'
    #     elif atnd==False:
    #         atnd='False'
    #     atnd=atnd.encode(encoding='utf-8')
    #     self.conn_soc.send(atnd)
    #     print('전송')

    def recvMsg(self):  # 상대방이 보낸 메시지 읽어서 화면에 출력
        # print('리드')
        global class1_attend, class2_attend, name, name_idx
        while True:
            # print('리드')
            try:
                rcv_msg = self.conn_soc.recv(1024).decode()
                if rcv_msg=='end.':
                    return
                name= rcv_msg.split('/')[0]
                atnd = rcv_msg.split('/')[1]
                print(name, atnd)
                tmp_idx=class_names.index(name)
                if tmp_idx<=12:
                    tmp=list(class1_attend[tmp_idx])
                    tmp[self.resultcnt]='o' if atnd=='True' else 'x'
                    class1_attend[tmp_idx]=''.join(map(str, tmp))
                elif tmp_idx<25:
                    tmp = list(class2_attend[tmp_idx-13])
                    tmp[self.resultcnt] = 'o' if atnd == 'True' else 'x'
                    class2_attend[tmp_idx-13] = ''.join(map(str, tmp))
                print(class1_attend)
                print(class2_attend)
            except ConnectionAbortedError:
                pass

    def close_conn(self):
        global class1_attend, class2_attend
        self.conn_soc.send('end.'.encode(encoding='utf-8'))
        self.conn_soc.send('stop'.encode(encoding='utf-8'))
        self.conn_soc.close()
        print('종료되었습니다')

    def class1_btn_config(self, idx):
        for i in range(0, 13):
            self.class1_name_btn[i].config(image=class1_name_n_img[i])
        self.class1_name_btn[idx].config(image=class1_name_img[idx])

    def class2_btn_config(self, idx):
        for i in range(0, 12):
            self.class2_name_btn[i].config(image=class2_name_n_img[i])
        self.class2_name_btn[idx].config(image=class2_name_img[idx])

    def update(self):
        global class1_attend, class2_attend, name_idx
        if self.resultcnt>=10:
            self.conn_soc.send('end.'.encode(encoding='utf-8'))
            return
        try:
            self.win.after(10, self.update)

            self.cur_time = time.time()
            if 5 <= (self.cur_time - self.start_time) :
                self.start_time = self.cur_time
                self.idx_set(name_idx)
                self.resultcnt = self.resultcnt + 1

                #self.sendAtnd(atnd)
            time_flow=self.cur_time-first_time
            self.time_label.config(text="%02d"%((time_flow/60)%60)+":%02d"%((time_flow%60)))
        except TypeError:
            pass


def class1_go():
    global name_idx, start_time, name, first_time, aiclass
    aiclass=1
    class1_frm = tk.Frame(root, width=334, height=500)
    class1_frm.grid(row=0, column=0, sticky="nsew")
    tk.Label(class1_frm, image=class1_frm_img).place(x=0, y=0)
    first_time = time.time()
    start_time = time.time()
    Web(class1_frm)


def class2_go():
    global name_idx, start_time, name, first_time, aiclass
    aiclass=2
    class2_frm = tk.Frame(root, width=334, height=500)
    class2_frm.grid(row=0, column=0, sticky="nsew")
    tk.Label(class2_frm, image=class2_frm_img).place(x=0, y=0)
    first_time = time.time()
    start_time = time.time()
    Web(class2_frm)


root = tk.Tk()
root.title('인공프 출석 확인 시스템')
root.geometry('334x500+0+0')
root.resizable(False, False)

main_frm = tk.Frame(root, width=333, height=500)
start_image = tk.PhotoImage(file='files/t_start.png')
start_label = tk.Label(main_frm, image=start_image)
start_label.place(x=0, y=0)

main_frm.grid(row=0, column=0, sticky="nsew")
class1_image = tk.PhotoImage(file='files/aiclass1.png')
class2_image = tk.PhotoImage(file='files/aiclass2.png')
class1_btn = tk.Button(main_frm, image=class1_image, command=class1_go)
class2_btn = tk.Button(main_frm, image=class2_image, command=class2_go)
quit_btn = tk.Button(main_frm, text="끝내기", bg='navy', fg='white', command=lambda: [root.destroy(), exit()])
home_image=tk.PhotoImage(file='files/home2.png')
background_image=tk.PhotoImage(file='files/background.png')
O_image=tk.PhotoImage(file='files/t_o.png')
X_image=tk.PhotoImage(file='files/t_x.png')
blank_image=tk.PhotoImage(file='files/blank.png')
class1_frm_img = tk.PhotoImage(file='files/t_frame1.png')
class2_frm_img = tk.PhotoImage(file='files/t_frame2.png')
class1_name_img=[]
class2_name_img=[]
class1_name_n_img=[]
class2_name_n_img=[]
number_img=[]

for i in range(0, 11):
    number_img.append(tk.PhotoImage(file='files/t_'+str(i)+'.png'))

for i in range(0, 13):
    class1_name_img.append(tk.PhotoImage(file='files/t_1_'+class1_names[i]+'.png'))
    class1_name_n_img.append(tk.PhotoImage(file='files/t_1_' + class1_names[i] + '_n.png'))
for i in range(0, 12):
    class2_name_img.append(tk.PhotoImage(file='files/t_2_'+class2_names[i]+'.png'))
    class2_name_n_img.append(tk.PhotoImage(file='files/t_2_' + class2_names[i] + '_n.png'))

class1_btn.place(x=30, y=320)
class2_btn.place(x=30, y=355)
quit_btn.place(x=272, y=11)

root.mainloop()