# -*- coding:utf-8 -*-
import logging
import sys
import json


_MaZhaoYang = 0
_YangRui = 1
_NanHuaQiHuo = 2

_Instruments = {
"IC": ["IC1711", "IC1712"],
"IH": ["IH1708", "IH1709"],
"IF": ["IF1708", "IF1709"],
"rb": ["rb1801", "rb1801"], # 螺纹钢   [0, 500, 170, 180] 1, 0.5
"SR" : ["SR709", "SR801"]   # 白糖    [0, 500, 0, 30] 1, 0.5
}

def decode(text):
    return text.decode('gb2312').encode('utf-8')

def get_logger(logger_name, output_file):
    logger = logging.getLogger(logger_name)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s [%(levelname)-8s]: %(message)s')
    # 文件日志
    file_handler = logging.FileHandler(output_file)
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)
    return logger


def get_account(account):
    if account == 2:
        # 南华期货
        brokerID = '****'
        userID = '******'
        password = '*****'
        mdapi_front = 'tcp://115.238.106.253:41213'
        trade_front = 'tcp://115.238.106.253:41205'
    else:
        raise Exception('No such account')

    return brokerID, userID, password, mdapi_front, trade_front

if __name__ == '__main__':
    pass
