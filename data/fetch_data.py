# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 16:00
# @Author  : yhdu@tongwoo.cn
# @简介    : 获取数据
# @File    : fetch_data.py


from geo import bl2xy
from time import clock
from datetime import datetime


def cmp1(data1, data2):
    if data1.stime > data2.stime:
        return 1
    elif data1.stime < data2.stime:
        return -1
    else:
        return 0


class TaxiData:
    def __init__(self, veh, px, py, stime, speed, direction):
        self.veh, self.direction = veh, direction
        self.px, self.py, self.stime, self.speed = px, py, stime, speed


def read_data(filename, minx, miny):
    """
    从txt里面读取gps数据
    :param filename: 
    :param minx:
    :param miny:
    :return: 
    """
    bt = clock()
    maxx, maxy = minx + 2000, miny + 2000
    trace_dict = {}
    cnt = 0
    try:
        with open(filename) as fp:
            for line in fp:
                items = line.split(',')
                veh, px, py, stime, state, speed, car_state, ort = items[:]
                px, py, speed, ort = float(px), float(py), float(speed), float(ort)
                if minx < px < maxx and miny < py < maxy:
                    stime = datetime.strptime(stime, "%Y-%m-%d %H:%M:%S")
                    taxi_data = TaxiData(veh, px, py, stime, speed, ort)
                    cnt += 1
                    try:
                        trace_dict[veh].append(taxi_data)
                    except KeyError:
                        trace_dict[veh] = [taxi_data]
                    # if cnt == 100:
                    #     break
    except IOError:
        pass

    for veh, trace in trace_dict.iteritems():
        trace.sort(cmp1)
        new_trace = []
        last_data = None
        for taxi_data in trace:
            if last_data is not None:
                if last_data.direction == taxi_data.direction and last_data.px == taxi_data.px:
                    pass
                else:
                    new_trace.append(taxi_data)
            last_data = taxi_data
        trace_dict[veh] = new_trace

    et = clock()
    print "read data", et - bt
    return trace_dict


def save_trace(trace_dict, filename):
    fp = open(filename, 'w')
    for veh, trace in trace_dict.iteritems():
        for taxi_data in trace:
            str_data = "{0},{1},{2},{3},{4},{5}".format(taxi_data.veh, taxi_data.px, taxi_data.py,
                                                        taxi_data.stime, taxi_data.speed, taxi_data.direction) + '\n'
            fp.write(str_data)
    fp.close()


def filter_gps():
    minx, miny = 77366, 83293
    trace = read_data("2018-05-01.txt", minx, miny)
    save_trace(trace, "area.txt")


filter_gps()
