# -*- coding:utf-8 -*-
from ctp.futures import ApiStruct, MdApi
import utils
import time


class MyMdApi(MdApi):
    def __init__(self, brokerID, userID, password, instrumentIDs, logger):
        self.requestID = 0 # 请求编号
        self.brokerID = brokerID # 代理商id
        self.userID = userID # 用户id
        self.password = password # 密码
        self.instrumentIDs = instrumentIDs # 合约id，列表，注意大小写！['IC1707']
        self.depth_info = None # 存储 深度行情
        self.tick_change = False
        self.logger = logger
        self.Create() # 创建行情本地存储

    def Create(self, pszFlowPath='', bIsUsingUdp=False, bIsMulticast=False):
        # 创建本地行情
        MdApi.Create(self, pszFlowPath = 'MdFile/')
        self.logger.info('=========== 行情实例开始创建 ===========')

    def RegisterFront(self, front):
        """
        登陆前置机
        :param front: 前置机IP地址和端口号
        :return: None
        """
        if isinstance(front, bytes):
            return MdApi.RegisterFront(self, front)
        for front in front:
            MdApi.RegisterFront(self, front)

    def OnFrontConnected(self):
        """
        回调函数：前置机连接成功
        """
        self.logger.info('行情前置机连接成功!')
        self.logger.info('用户登录中... ...')
        req = ApiStruct.ReqUserLogin(
            BrokerID=self.brokerID, UserID=self.userID, Password=self.password) # 用户登陆
        self.requestID += 1
        self.ReqUserLogin(req, self.requestID)

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID == 0: # Success
            self.logger.info('用户登录成功!')
            self.logger.info('交易日期: %s', self.GetTradingDay())
            self.SubscribeMarketData(self.instrumentIDs)

    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID == 0:
            self.logger.info("行情订阅成功!合约号:%s", pSpecificInstrument.InstrumentID)
        else:
            self.logger.info("行情订阅失败...")
            self.logger.info("错误代码: %s, 错误信息 %s:", pRspInfo.ErrorID, utils.decode(pRspInfo.ErrorMsg))

    def OnRtnDepthMarketData(self, pDepthMarketData):
        self.depth_info = pDepthMarketData
        self.tick_change = True