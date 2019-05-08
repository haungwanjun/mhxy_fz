#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import threading
from pydoc import text

import win32con
import win32api, win32gui
import random
import time
import tkinter as tk
from memory_pic import *
from PIL import ImageGrab, Image
import base64

# 从.py文件获取图片
def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(base64.b64decode(pic_code))
    image.close()
# 导入图片
get_pic(bangpai_jpg, 'bangpai_jpg')
get_pic(bangpai_renwu_jpg, 'bangpai_renwu_jpg')
get_pic(bangpai_renwu2_jpg, 'bangpai_renwu2_jpg')
get_pic(goumai_cw_jpg, 'goumai_cw_jpg')
get_pic(goumai_sc_jpg, 'goumai_sc_jpg')
get_pic(goumai_yp_jpg, 'goumai_yp_jpg')
get_pic(shangjiao_cw_jpg, 'shangjiao_cw_jpg')
get_pic(shangjiao_yp_jpg, 'shangjiao_yp_jpg')
get_pic(shimen_jpg, 'shimen_jpg')
get_pic(shimen_songxin_jpg, 'shimen_songxin_jpg')
get_pic(shiyong_jpg, 'shiyong_jpg')
get_pic(qiecuo_jpg, 'qiecuo_jpg')
get_pic(qiecuo_yulin_jpg, 'qiecuo_yulin_jpg')

def move_click(x, y, t=0):  # 移动鼠标并点击左键
    win32api.SetCursorPos((x, y))  # 设置鼠标位置(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # 点击鼠标左键
    if t == 0:
        time.sleep(random.random()*2+1)  # sleep一下
    else:
        time.sleep(t)
    return 0

# 测试
# move_click(300, 300)

def resolution():  # 获取屏幕分辨率
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

# screen_resolution = resolution()

# 获取梦幻西游窗口信息吗，返回一个矩形窗口四个坐标
def get_window_info():
    wdname = u'《梦幻西游》手游'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle == 0:
        # text.insert('end', '提示：请打开梦幻西游\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)

# window_size = get_window_info()
 # 返回x相对坐标
def get_posx(x, window_size):
    return int((window_size[2] - window_size[0]) * x / 804)


 # 返回y相对坐标
def get_posy(y, window_size):
    return int((window_size[3] - window_size[1]) * y / 630)

# topx, topy = window_size[0], window_size[1]

# # 抓取游戏指定坐标的图像
# img_ready = ImageGrab.grab((topx + get_posx(500, window_size), topy + get_posy(480, window_size),
#                             topx + get_posx(540, window_size), topy + get_posy(500, window_size)))
# # 查看图片
# img_ready.show()

# 获得图像的hash值
def get_hash(img):
    img = img.resize((16, 16), Image.ANTIALIAS).convert('L')  # 抗锯齿 灰度
    avg = sum(list(img.getdata())) / 256  # 计算像素平均值
    s = ''.join(map(lambda i: '0' if i < avg else '1', img.getdata()))  # 每个像素进行比对,大于avg为1,反之为0
    return ''.join(map(lambda j: '%x' % int(s[j:j+4], 2), range(0, 256, 4)))

# 计算两个图像的汉明距离
def hamming(hash1, hash2, n=20):
    b = False
    assert len(hash1) == len(hash2)
    if sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)) < n:
        b = True
    return b

# 抓鬼
def zhua_gui(window_size):
    global is_start
    is_start = True
    topx, topy = window_size[0], window_size[1]

    # 是否继续
    isContinue = Image.open("shimen_songxin.jpg")
    isContinue_hash = get_hash(isContinue)

    # 是否使用
    shiyong = Image.open("shiyong.jpg")
    shiyong_hash = get_hash(shiyong)
    # 开始
    while is_start:
        time.sleep(1)
        # 是否继续抓鬼/是否自动加入匹配
        img_isContinue = ImageGrab.grab((topx + get_posx(750, window_size), topy + get_posy(465, window_size),
                                    topx + get_posx(840, window_size), topy + get_posy(500, window_size)))

        if hamming(get_hash(img_isContinue), isContinue_hash, 10):
            move_click(topx + get_posx(740, window_size), topy + get_posy(380, window_size))
            time.sleep(3)
            continue

        # 使用按钮
        img_shiyong = ImageGrab.grab((topx + get_posx(635, window_size), topy + get_posy(510, window_size),
                                      topx + get_posx(710, window_size), topy + get_posy(540, window_size)))
        if hamming(get_hash(img_shiyong), shiyong_hash, 20):
            move_click(topx + get_posx(670, window_size), topy + get_posy(525, window_size))
            print("点击使用")
            time.sleep(3)
            continue


#师门任务
def shimen(window_size):
    global is_start
    is_start = True
    topx, topy = window_size[0], window_size[1]
    # 使用按钮（比如是x1,y1,x2,y2）
    shiyong = Image.open("shiyong_jpg")
    shiyong_hash = get_hash(shiyong)
    # shiyong.show()
    # print(shiyong_hash)
    # 购买宠物（比如是x1,y1,x2,y2）
    goumai_cw = Image.open("goumai_cw_jpg")
    goumai_cw_hash = get_hash(goumai_cw)
    # 上交药品按钮（比如是x1,y1,x2,y2）
    shangjiao_yp = Image.open("shangjiao_yp_jpg")
    shangjiao_yp_hash = get_hash(shangjiao_yp)
    # 上交宠物按钮
    shangjiao_cw = Image.open("shangjiao_cw_jpg")
    shangjiao_cw_hash = get_hash(shangjiao_cw)
    #师门任务栏
    shimen = Image.open("shimen_jpg")
    shimen_hash = get_hash(shimen)

    # 师门任务栏
    shimen_songxin = Image.open("shimen_songxin_jpg")
    shimen_songxin_hash = get_hash(shimen_songxin)

    # 药店购买
    goumai_yp = Image.open("goumai_yp_jpg")
    goumai_yp_hash = get_hash(goumai_yp)
    # 商城购买
    goumai_sc = Image.open("goumai_sc_jpg")
    goumai_sc_hash = get_hash(goumai_sc)
    i=0
    count = 0
    while is_start:
        time.sleep(2)
        i=i+1
        print("第%i次循环" %i)
        # 使用按钮（635 ，510 ，710 ，540）
        img_shiyong = ImageGrab.grab((topx + get_posx(635, window_size), topy + get_posy(510, window_size),
                                    topx + get_posx(710, window_size), topy + get_posy(540, window_size)))
        # img_shiyong.show()
        # img_shiyong.save("shiyong.jpg")
        # print("显示图片")
        # print(get_hash(img_shiyong))
        # print(hamming(get_hash(img_shiyong), shiyong_hash, 20))
        if hamming(get_hash(img_shiyong), shiyong_hash, 30):
            move_click(topx + get_posx(670, window_size), topy + get_posy(525, window_size))
            print("点击使用")
            time.sleep(3)
            continue

        # 购买宠物610，505，740，540
        img_goumai_cw = ImageGrab.grab((topx + get_posx(610, window_size), topy + get_posy(505, window_size),
                                    topx + get_posx(740, window_size), topy + get_posy(540, window_size)))
        # img_goumai_cw.save("goumai_cw.jpg")
        if hamming(get_hash(img_goumai_cw), goumai_cw_hash, 20):
            move_click(topx +get_posx(680, window_size), topy + get_posy(520, window_size))
            print("点击购买宠物")
            time.sleep(3)
            continue

        # 药店购买 570，470，700，505
        img_goumai_yp = ImageGrab.grab((topx + get_posx(560, window_size), topy + get_posy(460, window_size),
                                        topx + get_posx(690, window_size), topy + get_posy(500, window_size)))
        # img_goumai_yp.save("goumai_yp.jpg")
        if hamming(get_hash(img_goumai_yp), goumai_yp_hash, 20):
            move_click(topx + get_posx(620, window_size), topy + get_posy(480, window_size))
            print("点击购买药")
            time.sleep(3)
            continue

        # 商城购买 520，520，715，550
        img_goumai_sc = ImageGrab.grab((topx + get_posx(580, window_size), topy + get_posy(515, window_size),
                                        topx + get_posx(715, window_size), topy + get_posy(550, window_size)))
        # img_goumai_sc.save("goumai_sc.jpg")
        if hamming(get_hash(img_goumai_sc), goumai_sc_hash, 20):
            move_click(topx + get_posx(650, window_size), topy + get_posy(530, window_size))
            print("点击商城购买")
            time.sleep(3)
            continue

        # 上交药品按钮 600，470，700，500
        img_shangjiao_yp = ImageGrab.grab((topx + get_posx(590, window_size), topy + get_posy(465, window_size),
                                        topx + get_posx(695, window_size), topy + get_posy(490, window_size)))
        # img_shangjiao_yp .save("shangjiao_yp.jpg")
        if hamming(get_hash(img_shangjiao_yp), shangjiao_yp_hash, 20):
            move_click(topx + get_posx(640, window_size), topy + get_posy(478, window_size))
            print("点击药品上交")
            time.sleep(3)
            continue

        # 上交宠物按钮
        img_shangjiao_cw = ImageGrab.grab((topx + get_posx(500, window_size), topy + get_posy(460, window_size),
                                           topx + get_posx(600, window_size), topy + get_posy(500, window_size)))
        # img_shangjiao_cw.save("shangjiao_cw.jpg")
        if hamming(get_hash(img_shangjiao_cw), shangjiao_cw_hash, 20):
            move_click(topx + get_posx(550, window_size), topy + get_posy(480, window_size))
            print("点击宠物上交")
            time.sleep(3)
            continue

        # 师门送信按钮
        img_shimen_songxin1 = ImageGrab.grab((topx + get_posx(620, window_size), topy + get_posy(290, window_size),
                                             topx + get_posx(700, window_size), topy + get_posy(325, window_size)))
        # img_shimen_songxin1 .save("shimen_songxin1.jpg")
        # img_shimen_songxin1.show()
        if hamming(get_hash(img_shimen_songxin1), shimen_songxin_hash, 30):
            move_click(topx + get_posx(660, window_size), topy + get_posy(310, window_size))
            print("点击师门任务1")
            time.sleep(3)
            continue

        # 师门任务按钮
        img_shimen_songxin = ImageGrab.grab((topx + get_posx(620, window_size), topy + get_posy(345, window_size),
                                           topx + get_posx(700, window_size), topy + get_posy(370, window_size)))
        # img_shimen_songxin .save("shimen_songxin1.jpg")

        if hamming(get_hash(img_shimen_songxin), shimen_songxin_hash, 30):
            move_click(topx + get_posx(660, window_size), topy + get_posy(360, window_size))
            print("点击师门任务")
            time.sleep(3)
            continue

        # # 师门任务栏 630，150，665，175
        img_shimen = ImageGrab.grab((topx + get_posx(630, window_size), topy + get_posy(160, window_size),
                                        topx + get_posx(670, window_size), topy + get_posy(180, window_size)))
        # img_shimen.save("shimen.jpg")
        if hamming(get_hash(img_shimen), shimen_hash, 50):
            move_click(topx + get_posx(650, window_size), topy + get_posy(170, window_size))
            print("点击师门任务栏")
            time.sleep(3)
            continue

        #结束师门任务
        # img_finish = ImageGrab.grab((topx + get_posx(630, window_size), topy + get_posy(160, window_size),
        #                              topx + get_posx(670, window_size), topy + get_posy(180, window_size)))
        # # img_finish.save("finish.jpg")
        # if hamming(get_hash(img_finish), finish_hash, 20):
        #     move_click(topx + get_posx(650, window_size), topy + get_posy(170, window_size))
        #     print("师门任务完成")
        #     break

#帮派任务
def bang_pai(window_size):
    global is_start
    is_start = True
    topx, topy = window_size[0], window_size[1]
    # 使用按钮（比如是x1,y1,x2,y2）
    shiyong = Image.open("shiyong_jpg")
    shiyong_hash = get_hash(shiyong)
    # shiyong.show()
    # print(shiyong_hash)
    # 购买宠物（比如是x1,y1,x2,y2）
    goumai_cw = Image.open("goumai_cw_jpg")
    goumai_cw_hash = get_hash(goumai_cw)
    # 上交药品按钮（比如是x1,y1,x2,y2）
    shangjiao_yp = Image.open("shangjiao_yp_jpg")
    shangjiao_yp_hash = get_hash(shangjiao_yp)
    # 上交宠物按钮
    shangjiao_cw = Image.open("shangjiao_cw_jpg")
    shangjiao_cw_hash = get_hash(shangjiao_cw)
    #帮派任务栏
    bangpai = Image.open("bangpai_jpg")
    bangpai_hash = get_hash(bangpai)

    # 门派切磋
    qiecuo = Image.open("qiecuo_jpg")
    qiecuo_hash = get_hash(qiecuo)
    # 御林军切磋
    qiecuo_yulin = Image.open("qiecuo_yulin_jpg")
    qiecuo_yulin_hash = get_hash(qiecuo_yulin)

    # 帮派任务按钮
    bangpai_renwu = Image.open("bangpai_renwu_jpg")
    bangpai_renwu_hash = get_hash(bangpai_renwu)

    # 帮派任务按钮2
    bangpai_renwu2 = Image.open("bangpai_renwu2_jpg")
    bangpai_renwu2_hash = get_hash(bangpai_renwu2)

    # 药店购买
    goumai_yp = Image.open("goumai_yp_jpg")
    goumai_yp_hash = get_hash(goumai_yp)
    # 商城购买
    goumai_sc = Image.open("goumai_sc_jpg")
    goumai_sc_hash = get_hash(goumai_sc)
    i=0
    count = 0
    while is_start:
        time.sleep(2)
        i=i+1
        print("第%i次循环" %i)
        # 使用按钮（635 ，510 ，710 ，540）
        img_shiyong = ImageGrab.grab((topx + get_posx(635, window_size), topy + get_posy(510, window_size),
                                    topx + get_posx(710, window_size), topy + get_posy(540, window_size)))
        # img_shiyong.show()
        #  img_shiyong.save("shiyong.jpg")

        if hamming(get_hash(img_shiyong), shiyong_hash, 20):
            move_click(topx + get_posx(670, window_size), topy + get_posy(525, window_size))
            print("点击使用")
            time.sleep(3)
            continue

        img_qiecuo_yulin = ImageGrab.grab((topx + get_posx(620, window_size), topy + get_posy(200, window_size),
                                     topx + get_posx(710, window_size), topy + get_posy(230, window_size)))
        # img_shiyong.show()
        # img_qiecuo_yulin.save("qiecuo_yulin.jpg")
        # break
        if hamming(get_hash(img_qiecuo_yulin), qiecuo_yulin_hash, 20):
            move_click(topx + get_posx(670, window_size), topy + get_posy(215, window_size))
            print("点击切磋")
            time.sleep(3)
            continue



        # 购买宠物610，505，740，540
        img_goumai_cw = ImageGrab.grab((topx + get_posx(610, window_size), topy + get_posy(505, window_size),
                                    topx + get_posx(740, window_size), topy + get_posy(540, window_size)))
        # img_goumai_cw.save("goumai_cw.jpg")
        if hamming(get_hash(img_goumai_cw), goumai_cw_hash, 20):
            move_click(topx +get_posx(680, window_size), topy + get_posy(520, window_size))
            print("点击购买宠物")
            time.sleep(3)
            continue

        # 药店购买 570，470，700，505
        img_goumai_yp = ImageGrab.grab((topx + get_posx(560, window_size), topy + get_posy(460, window_size),
                                        topx + get_posx(690, window_size), topy + get_posy(500, window_size)))
        # img_goumai_yp.save("goumai_yp.jpg")
        if hamming(get_hash(img_goumai_yp), goumai_yp_hash, 20):
            move_click(topx + get_posx(620, window_size), topy + get_posy(480, window_size))
            print("点击购买药")
            time.sleep(3)
            continue

        # 商城购买 520，520，715，550
        img_goumai_sc = ImageGrab.grab((topx + get_posx(580, window_size), topy + get_posy(515, window_size),
                                        topx + get_posx(715, window_size), topy + get_posy(550, window_size)))
        # img_goumai_sc.save("goumai_sc.jpg")
        if hamming(get_hash(img_goumai_sc), goumai_sc_hash, 20):
            move_click(topx + get_posx(650, window_size), topy + get_posy(530, window_size))
            print("点击商城购买")
            time.sleep(3)
            continue

        # 上交药品按钮 600，470，700，500
        img_shangjiao_yp = ImageGrab.grab((topx + get_posx(590, window_size), topy + get_posy(465, window_size),
                                        topx + get_posx(695, window_size), topy + get_posy(490, window_size)))
        # img_shangjiao_yp .save("shangjiao_yp.jpg")
        if hamming(get_hash(img_shangjiao_yp), shangjiao_yp_hash, 20):
            move_click(topx + get_posx(640, window_size), topy + get_posy(478, window_size))
            print("点击药品上交")
            time.sleep(3)
            continue

        # 上交宠物按钮
        # img_shangjiao_cw = ImageGrab.grab((topx + get_posx(500, window_size), topy + get_posy(460, window_size),
        #                                    topx + get_posx(600, window_size), topy + get_posy(500, window_size)))
        # # img_shangjiao_cw.save("shangjiao_cw.jpg")
        # if hamming(get_hash(img_shangjiao_cw), shangjiao_cw_hash, 20):
        #     move_click(topx + get_posx(550, window_size), topy + get_posy(480, window_size))
        #     print("点击宠物上交")
        #     time.sleep(5)
        #     continue

        # 帮派任务按钮
        img_bangpai_renwu = ImageGrab.grab((topx + get_posx(620, window_size), topy + get_posy(300, window_size),
                                           topx + get_posx(700, window_size), topy + get_posy(330, window_size)))
        # img_bangpai_renwu .save("bangpai_renwu.jpg")
        if hamming(get_hash(img_bangpai_renwu), bangpai_renwu_hash, 20):
            move_click(topx + get_posx(660, window_size), topy + get_posy(315, window_size))
            print("点击帮派任务提交按钮")
            time.sleep(3)
            continue

        # 帮派任务按钮2
        img_bangpai_renwu2 = ImageGrab.grab((topx + get_posx(620, window_size), topy + get_posy(250, window_size),
                                           topx + get_posx(700, window_size), topy + get_posy(280, window_size)))
        # img_bangpai_renwu2 .save("bangpai_renwu2.jpg")
        if hamming(get_hash(img_bangpai_renwu2), bangpai_renwu2_hash, 20):
            move_click(topx + get_posx(660, window_size), topy + get_posy(265, window_size))
            print("点击帮派任务提交按钮2")
            time.sleep(3)
            continue

        # #切磋
        img_qiecuo = ImageGrab.grab((topx + get_posx(625, window_size), topy + get_posy(431, window_size),
                                     topx + get_posx(710, window_size), topy + get_posy(468, window_size)))
        # img_shiyong.show()
        # img_qiecuo.save("qiecuo.jpg")
        if hamming(get_hash(img_qiecuo), qiecuo_hash, 20):
            move_click(topx + get_posx(670, window_size), topy + get_posy(450, window_size))
            print("点击切磋")
            time.sleep(3)
            continue

        # # # 帮派任务栏
        img_bangpai = ImageGrab.grab((topx + get_posx(630, window_size), topy + get_posy(160, window_size),
                                        topx + get_posx(670, window_size), topy + get_posy(180, window_size)))
        # img_bangpai.save("bangpai.jpg")
        if hamming(get_hash(img_bangpai), bangpai_hash, 40):
            move_click(topx + get_posx(650, window_size), topy + get_posy(170, window_size))
            print("点击帮派任务栏")
            time.sleep(3)
            continue
        # break
    # print("帮派任务停止...")

# 挖宝图
def baotu(window_size):
    global is_start
    is_start = True
    topx, topy = window_size[0], window_size[1]
    # 使用按钮（比如是x1,y1,x2,y2）
    shiyong = Image.open("shiyong_jpg")
    shiyong_hash = get_hash(shiyong)

    i = 0
    count =0
    while is_start:
        time.sleep(2)
        i = i + 1
        print("第%i次循环" % i)
        # 使用按钮（635 ，510 ，710 ，540）
        img_shiyong = ImageGrab.grab((topx + get_posx(635, window_size), topy + get_posy(510, window_size),
                                      topx + get_posx(710, window_size), topy + get_posy(540, window_size)))
        # img_shiyong.show()
        #  img_shiyong.save("shiyong.jpg")

        if hamming(get_hash(img_shiyong), shiyong_hash, 20):
            move_click(topx + get_posx(670, window_size), topy + get_posy(525, window_size))
            print("点击使用")
            count = count+1
            if(count == 15):
                break
            time.sleep(3)
            continue


def stop():
    global  is_start
    is_start = False
    print("停止")


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


# 启动
if __name__ == "__main__":
    screen_resolution = resolution()
    # print(screen_resolution)
    window_size = get_window_info()
    print(window_size)
    global is_start
    # shimen(window_size)
    # zhua_gui(window_size)
    # bang_pai(window_size)
    # baotu(window_size)

    # 创建主窗口
    root = tk.Tk()
    root.title("梦幻西游手游辅助")
    root.minsize(300, 250)
    root.maxsize(300, 250)
    # 创建按钮
    button_shimen = tk.Button(root, text=u"师门", command=lambda: MyThread(shimen, window_size), width = 15,height = 2)
    button_shimen.place(relx=0.2, rely=0.15, width=200)
    button_shimen.pack()

    button_bangpai = tk.Button(root, text="帮派", command=lambda: MyThread(bang_pai, window_size), width = 15,height = 2)
    button_bangpai.place(relx=0.2, rely=0.35, width=200)
    button_bangpai.pack()

    button_baotu = tk.Button(root, text="宝图", command=lambda: MyThread(baotu,window_size), width = 15,height = 2)
    button_baotu.place(relx=0.4, rely=0.55, width=200)
    button_baotu.pack()

    button_zhuagui = tk.Button(root, text="带队抓鬼", command=lambda: MyThread(zhua_gui, window_size), width = 15,height = 2)
    button_zhuagui.place(relx=0.4, rely=0.65, width=100)
    button_zhuagui.pack()

    button_tingzhi = tk.Button(root,text=u"停止", command=lambda: MyThread(stop), width = 15,height = 2)
    button_tingzhi.place(relx=0.4, rely=0.85, width=200)
    button_tingzhi.pack()

    root.mainloop()