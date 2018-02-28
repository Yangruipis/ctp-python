一个基于[pyctp](https://github.com/lovelylain/pyctp)的CTP接口Python再封装
=====

![](https://img.shields.io/npm/l/express.svg)

# 使用方法
## 1. 添加期货账户

在 **utils.py** 中添加账户名称，如

```python
def get_account(account):
    if account == 0:
        # 南华期货
        brokerID = '****'
        userID = '******'
        password = '*****'
        mdapi_front = 'tcp://115.238.106.253:41213'
        trade_front = 'tcp://115.238.106.253:41205'
    else:
        raise Exception('No such account')
```

然后在 **main.py** 中调用，可以直接输入数字（此时账户为0），也可以进行枚举

## 2. 添加商品品种

在 **utils.py** 中修改 *_Instruments* 变量，添加想要的品种，并在 **main.py** 中进行修改调用

## 3. 策略撰写

**strategy.py** 中展示了一个股指期货策略框架，下单逻辑需要用户自行填写。

- 当前框架只支持tick级的策略，如果要做分钟线或者小时线的策略，可以自行编写蜡烛线类，将每次tick跳价存入该类，并进行记录。用户可参考 **candle.py**
- 下单逻辑通过四个函数实现：卖出开仓sell_open、买入开仓buy_open、卖出平仓sell_close、买入平仓buy_close，用户可根据需求自行修改
- 下单时操作不清楚，可直接进入 **tdapi.py** 中查看回调函数的参数解释，如提交报单函数：

```python

 def ReqOrderInsert2(self, InstrumentID, LimitPrice, Volumes, Direction = ApiStruct.D_Buy,
                       TimeCondition = ApiStruct.TC_IOC, CombOffsetFlag = ApiStruct.OF_Open, OrderPriceType = '2'):
        """
        OrderPriceType: #报单价格条件, char
            OPT_AnyPrice = '1' #任意价
            OPT_LimitPrice = '2' #限价
            OPT_BestPrice = '3' #最优价
            OPT_LastPrice = '4' #最新价
        Direction:
            D_Buy = '0' #买
            D_Sell = '1' #卖
        TimeCondition: #有效期类型, char
            TC_IOC = '1' #立即完成，否则撤销
            TC_GFS = '2' #本节有效
            TC_GFD = '3' #当日有效
            TC_GTD = '4' #指定日期前有效
            TC_GTC = '5' #撤销前有效
            TC_GFA = '6' #集合竞价有效
        CombOffsetFlag：
            OF_Open = '0' #开仓
            OF_Close = '1' #平仓
            OF_ForceClose = '2' #强平
            OF_CloseToday = '3' #平今
            OF_CloseYesterday = '4' #平昨
            OF_ForceOff = '5' #强减
            OF_LocalForceClose = '6' #本地强平
        。。。
        """
```

