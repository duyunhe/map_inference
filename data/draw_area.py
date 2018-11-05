# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 17:36
# @Author  : yhdu@tongwoo.cn
# @简介    : 
# @File    : draw_area.py


import matplotlib.pyplot as plt


def load_trace(filename):
    xy_list = []
    fp = open(filename)
    for line in fp.readlines():
        items = line.strip('\n').split(',')
        _, px, py, _, _, ort = items[:]
        px, py = float(px), float(py)
        xy_list.append([px, py])
    return xy_list


xy_list = load_trace('./area.txt')
x_list, y_list = zip(*xy_list)
plt.plot(x_list, y_list, linestyle='', marker='+')
plt.show()
