# -*- coding:utf-8 -*-
import time
import datetime
import utils
import pandas as pd
from ctp.futures import ApiStruct
from collections import Counter
from abc import ABCMeta,abstractmethod


class Strategy:

    __doc__ = "策略接口"
    __metaclass__ = ABCMeta

    @abstractmethod
    def begin(self):pass

    @abstractmethod
    def buy_open(self):pass

    @abstractmethod
    def buy_close(self):pass

    @abstractmethod
    def sell_open(self):pass

    @abstractmethod
    def sell_close(self):pass
    
class MyStrategy(Strategy):

    def __init__(self, mdapi1, trade, logger, *param):
        self.mdapi1 = mdapi1
        self.tradeapi = trade
        self.logger = logger

    def buy_open(self, ask_price):
        self.last_trade_price = ask_price
        self.position = 1
        instrument = self.tradeapi.instruimentIDs[0]
        self.tradeapi.ReqOrderInsert2(instrument, ask_price, 1,Direction=ApiStruct.D_Buy)
        if self.tradeapi.order_status_dict[(instrument, ask_price)] == '0':
            time.sleep(0.02)
            deal_price = self.tradeapi.real_deal_price
            print ('%s,买入开仓，报单价格：%s，成交价格：%s，滑点：%s' % (self.current_time, ask_price, deal_price, deal_price - ask_price))

    def sell_open(self, bid_price):
        self.last_trade_price = bid_price
        self.position = -1
        instrument = self.tradeapi.instruimentIDs[0]
        self.tradeapi.ReqOrderInsert2(instrument, bid_price, 1,Direction=ApiStruct.D_Sell)
        if self.tradeapi.order_status_dict[(instrument, bid_price)] == '0':
            time.sleep(0.02)
            deal_price = self.tradeapi.real_deal_price
            print ('%s,卖出开仓，报单价格：%s，成交价格：%s，滑点：%s' % (self.current_time, bid_price, deal_price, -deal_price + bid_price))

    def buy_close(self, ask_price):
        self.position = 0
        self.last_trade_price = ask_price
        self.max_profit = 0
        instrument = self.tradeapi.instruimentIDs[0]
        self.tradeapi.ReqOrderInsert2(instrument, ask_price, 1, Direction=ApiStruct.D_Buy, CombOffsetFlag=ApiStruct.OF_Close)
        if self.tradeapi.order_status_dict[(instrument, ask_price)] == '0':
            time.sleep(0.02)
            deal_price = self.tradeapi.real_deal_price
            print ('%s,买入平仓，报单价格：%s，成交价格：%s，滑点：%s' % (self.current_time, ask_price, deal_price, deal_price - ask_price))

    def sell_close(self, bid_price):
        instrument = self.tradeapi.instruimentIDs[0]
        self.tradeapi.ReqOrderInsert2(instrument, bid_price, 1, Direction=ApiStruct.D_Sell, CombOffsetFlag=ApiStruct.OF_Close)
        if self.tradeapi.order_status_dict[(instrument, bid_price)] == '0':
            time.sleep(0.02)
            deal_price = self.tradeapi.real_deal_price
            print ('%s,卖出平仓，报单价格：%s，成交价格：%s，滑点：%s' % (self.current_time, bid_price, deal_price, -deal_price + bid_price))


    def begin(self):
    	if self.ma_list == None:
        	self.ma_list = MaList(self.lenth_short, self.lenth_long)
        while 1:
            if self.mdapi1.tick_change:
                self.mdapi1.tick_change = False
                self.tradeapi.price_update()

                ask_price = self.mdapi1.depth_info.AskPrice1
                bid_price = self.mdapi1.depth_info.BidPrice1
                last_price = self.mdapi1.depth_info.LastPrice
                self.current_time = pd.to_datetime(self.mdapi1.depth_info.UpdateTime + '.'
                                              + str(self.mdapi1.depth_info.UpdateMillisec)).time()
                
                """
                此处下单
                """

if __name__ == '__main__':
    pass
