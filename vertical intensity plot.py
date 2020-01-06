# -*- coding: utf-8 -*-
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import sys
import matplotlib.patches as patches
#import matplotlib.ticker as tick
import pyautogui

# 横方向の信号強度マップを表示するバージョン

mz_counter = 0 # 何番目の質量数を表示するかのカウンター
mz_num = [] # 選択された質量数が何番目かを示す（最大３つまで）
# colormap = ['Reds', 'Greens', 'Blues']

def show_mz(flag):
    global mz_counter
    mz_counter += flag

    if mz_counter < 0:
        mz_counter = 0
    elif mz_counter == 96:
        mz_counter = 95
    else:
        for i in range(5):
            num_str = tk.StringVar()
            num_str.set(str(df.iat[2,i+3+mz_counter]))

            label = tk.Label(textvariable = num_str, width=10)
            label.bind("<1>",get_mz_num)
            label.bind("<3>",remove_mz_num)
            label.place(x=125, y=5+20*i)


def get_mz_num(event):
    if len(mz_num)>1:
        pass
    else:
        for i in range(6):
            if df.iat[2,mz_counter+2+i] == float(event.widget["text"]):
                mz_num.append(mz_counter+i)
                break

# 選択した質量を表示
        num_str = tk.StringVar()
        num_str.set(str(event.widget["text"]))
        label = tk.Label(textvariable = num_str, width=10)
        label.place(x=160, y=150+25*((len(mz_num)-1)))


def remove_mz_num(event):
    if len(mz_num)>0:
        label = tk.Label(text = '', width=10)
        label.place(x=160, y=150+25*((len(mz_num)-1)))
        mz_num.pop(-1)


def draw_multimap():
    step = float(EditBox2.get())
    global max_int
    max_int = float(EditBox11.get())

    root2.destroy()

    x = df.iloc[3:,1]
    y = df.iloc[3:,2]

    x_start = df.iat[3,1]
    x_end = df.iat[-1,1]
    y_start = df.iat[3,2]
    y_end = df.iat[-1,2]

    x_point = int(round((x_end - x_start)/step) + 1)
    y_point = int(round((y_end - y_start)/step) + 1)

    xx = x.values.reshape(y_point, x_point)
    yy = y.values.reshape(y_point, x_point)

    mz_num_min = max(len(mz_num)-3,0)

    for i in range(mz_num_min,len(mz_num)):
        z = df.iloc[3:,mz_num[i]+2]
        title = df.iat[2,mz_num[i]+2]

    zz = z.values.reshape(y_point, x_point)

    mapping(x_point, y_point, x_start, x_end, y_start, y_end, title, xx, yy, zz, step, z, max_int)


def mapping(x_point, y_point, x_start, x_end, y_start, y_end, title, xx, yy, zz, step, z, max_int):

    while True:

        fig = plt.figure(figsize=(x_point/10*2, y_point/10))

        ax1 = fig.add_subplot(121)
        ax1.set_title(title)
        ax1.axis([x_start, x_end, y_end, y_start])

        ax1.contourf(xx, yy, zz, levels=10, cmap='CMRmap')

        a = plt.ginput(n=1, mouse_add=1, mouse_pop=None, mouse_stop=3, timeout=60)

        x_cood1 = int((a[0][0]+0.1)*5)/5-0.1
        y_cood1 = int((a[0][1]+0.1)*5)/5

        ax1.axvline(x_cood1, color='w', linestyle='--')

        if (x_cood1 < x_start+0.4 and y_cood1 < y_start+0.4):
            sys.exit()

        ax2 = fig.add_subplot(122)
        ax2.set_title('y-direction')
        ax2.axis([y_start, y_end, 0, max_int])

        point = int((x_cood1-x_start)/step+1)

        temp_y = []
        temp_z = []

        for y2 in range(int((y_end-y_start)/step)+1):
            temp_y.append(y_start+y2*step)
            temp_z.append(z[point+x_point*y2])

        ax2.plot(temp_y, temp_z)


        plt.pause(5)
        plt.close('all')


root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('等高線表示プログラム','csv(UTF-8)ファイルを選択してください')

file = tkinter.filedialog.askopenfilenames(filetypes = fTyp,initialdir = iDir)

root.destroy()

path = str(os.path.dirname(file[0]))
onlyfilename, ext = os.path.splitext(os.path.basename(file[0]))
str_onlyfilename = str(onlyfilename)

df = pd.read_csv(file[0], sep=',', header=None)

# 情報入力
root2 = tkinter.Tk()
root2.title(u"質量数選択")
root2.geometry("400x300")

# 縦、横画像数入力
Static1 = tk.Label(text=u'マッピングする質量数')
Static1.place(x=5,y=5)

Static2 = tk.Label(text=u'データ取り込み周期')
Static2.place(x=5,y=110)
EditBox2 = tkinter.Entry(width=5)
EditBox2.insert(tkinter.END,"0.2")
EditBox2.place(x=115, y=110)
Static3 = tk.Label(text=u'mm')
Static3.place(x=145,y=110)

Static11 = tk.Label(text=u'max intensity')
Static11.place(x=5,y=210)
EditBox11 = tkinter.Entry(width=10)
EditBox11.insert(tkinter.END,"1000000")
EditBox11.place(x=120, y=210)

show_mz(0)

b_up = tkinter.Button(text='▲', command=lambda:show_mz(-1))
b_up.place(x=250, y=5)

b_down = tkinter.Button(text='▼', command=lambda:show_mz(1))
b_down.place(x=250, y=30)

#b1 = tkinter.Button(text='質量選択', command=get_mz_num)
#b1.place(x=5,y=150)

b2 = tkinter.Button(text='処理開始', command=draw_multimap)
b2.place(x=5, y=250)

root2.mainloop()

