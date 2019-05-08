#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import base64


def pic2py(picture_names, py_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        open_pic = open("%s" % picture_name, 'rb')
        b64str = base64.b64encode(open_pic.read())
        open_pic.close()
        # 注意这边b64str一定要加上.decode()
        write_data.append('%s = "%s"\n' % (filename, b64str.decode()))

    f = open('%s.py' % py_name, 'w+')
    for data in write_data:
        f.write(data)
    f.close()


if __name__ == '__main__':
    pics = ["bangpai.jpg", "bangpai_renwu.jpg", "bangpai_renwu2.jpg", "goumai_cw.jpg","goumai_sc.jpg","goumai_yp.jpg","shangjiao_cw.jpg"
            ,"shangjiao_yp.jpg","shimen.jpg","shimen_songxin.jpg","shiyong.jpg","qiecuo.jpg", "qiecuo_yulin.jpg"]
    pic2py(pics, 'memory_pic')  # 将pics里面的图片写到 memory_pic.py 中
    print("ok")
