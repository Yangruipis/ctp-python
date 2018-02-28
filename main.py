# -*- coding:utf-8 -*-

import utils
from tdapi import *
from mdapi import *
from strategy import *
import pickle
import datetime
import sys

def main(account, instrument_type, param):
    brokerID, userID, password, mdapi_front, trade_front = utils.get_account(account=account)

    logger = utils.get_logger("spread_arbitrage", "logs/%s.log" % instrument_type)

    mdapi1 = MyMdApi(brokerID, userID, password, [utils._Instruments[instrument_type][0]], logger)
    mdapi1.RegisterFront(mdapi_front)
    mdapi1.Init()
    time.sleep(1)

    trade = my_tdapi(broker_id=brokerID, investor_id=userID, passwd=password,
                     instrumentIDs=utils._Instruments[instrument_type], logger=logger)
    trade.Create(pszFlowPath='TdFile/')
    trade.SubscribePrivateTopic(ApiStruct.TERT_RESTART)
    trade.SubscribePublicTopic(ApiStruct.TERT_RESTART)
    trade.RegisterFront(trade_front)
    trade.Init()
    time.sleep(5)
    strategy = MyArbitrage(mdapi1, trade, logger, *param)
    try:
        strategy.begin()
    except KeyboardInterrupt:
        # 最好加上close方法 为了线程安全
        pass

if __name__ == '__main__':
    account = utils._YangRui
    instrument_type = 'IC'
    #param = [80, 40, 25, 25, 37]
    param = None # 你的参数，有就输入，没有就不输入
    main(account, instrument_type, param)