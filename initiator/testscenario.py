import quickfix as fix
import time
from datetime import datetime, timedelta
import pytz

def genExecID():
    return str(int(time.time() * 1000))

def cancelOrder(OrigClOrdID, Symbol, Side):
    trade = fix.Message()
    header = trade.getHeader()

    header.setField(fix.BeginString("FIX.4.2"))
    header.setField(fix.MsgType("F"))

    trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
    trade.setField(fix.ClOrdID(genExecID()))  #11 = Unique order
    trade.setField(fix.OrigClOrdID(OrigClOrdID))    # 41 = 

    dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    tTag = fix.TransactTime()
    tTag.setString(dnow)
    trade.setField(tTag)  # 60 = 
    trade.setField(fix.Symbol(Symbol))  # 55 = 
    trade.setField(fix.Side(Side))    # 54

    return trade

def cancelReplaceOrder(OrigClOrdID, Symbol, Side, OrderQty):
    trade = fix.Message()
    header = trade.getHeader()

    header.setField(fix.BeginString("FIX.4.2"))
    header.setField(fix.MsgType("G"))
    trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
    trade.setField(fix.ClOrdID(genExecID()))  #11 = Unique order
    trade.setField(fix.ExecInst(fix.ExecInst_ALL_OR_NONE))  #18 = G
    trade.setField(fix.OrderQty(float(OrderQty)))    # 38
    trade.setField(fix.OrdType(fix.OrdType_MARKET))  # 40 = 2 (limit order)

    trade.setField(fix.HandlInst(fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION))  # 21 = 1
    trade.setField(fix.OrigClOrdID(OrigClOrdID))    # 41 = 
    trade.setField(fix.Side(Side))    # 54     
    dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    tTag = fix.TransactTime()
    tTag.setString(dnow)
    trade.setField(tTag)  # 60 =  
    trade.setField(fix.Symbol(Symbol))  # 55 =         

    return trade    

def generateDollarAmountOrder(iSymbol, iBuySell, iCash, iQty, iType, iPrice):
    trade = fix.Message()
    trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))
    trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  #35 = D

    trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
    trade.setField(fix.ClOrdID(genExecID()))  #11 = Unique order
    # trade.setField(fix.ExecInst(fix.ExecInst_ALL_OR_NONE))  #18 = G
    trade.setField(fix.HandlInst(fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION))  # 21 = 1
    trade.setField(fix.OrderQty(iQty))  #38 = 

    trade.setField(fix.CashOrderQty(iCash))    # 152

    if iType == 'market':
        trade.setField(fix.OrdType(fix.OrdType_MARKET))  # 40 = 2 (limit order)
    elif iType == 'limit':
        trade.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40 = 2 (limit order)
        trade.setField(fix.Price(iPrice))   #44 = 

    if iBuySell.lower() == 'buy':
        trade.setField(fix.Side(fix.Side_BUY))  #54 = 1
    if iBuySell.lower() == 'sell':
        trade.setField(fix.Side(fix.Side_SELL))

    trade.setField(fix.Symbol(iSymbol))  # 55 = 
    trade.setField(fix.TimeInForce(fix.TimeInForce_DAY))  #59 = 0
    
    dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    tTag = fix.TransactTime()
    tTag.setString(dnow)
    trade.setField(tTag)

    return trade

def generateOrder(iSymbol, iBuySell, iQty):
    trade = fix.Message()
    trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))
    trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  #35 = D

    trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
    trade.setField(fix.ClOrdID(genExecID()))  #11 = Unique order
    # trade.setField(fix.ExecInst(fix.ExecInst_ALL_OR_NONE))  #18 = G
    trade.setField(fix.HandlInst(fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION))  # 21 = 1
    trade.setField(fix.OrderQty(iQty))  #38 = 
    trade.setField(fix.OrdType(fix.OrdType_MARKET))  # 40 = 2 (limit order)
    # trade.setField(fix.Price(100))   #44 = 

    if iBuySell.lower() == 'buy':
        trade.setField(fix.Side(fix.Side_BUY))  #54 = 1
    if iBuySell.lower() == 'sell':
        trade.setField(fix.Side(fix.Side_SELL))

    trade.setField(fix.Symbol(iSymbol))  # 55 = MSFT
    trade.setField(fix.TimeInForce(fix.TimeInForce_DAY))  #59 = 0
    # trade.setField(fix.TimeInForce('4'))  #59 = 4

    dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    tTag = fix.TransactTime()
    tTag.setString(dnow)
    trade.setField(tTag)

    return trade

def generatePrePostOrder(iSymbol, iBuySell, iQty, iPrice):
    trade = fix.Message()
    trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))
    trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  #35 = D

    trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
    trade.setField(fix.ClOrdID(genExecID()))  #11 = Unique order
    # trade.setField(fix.ExecInst(fix.ExecInst_ALL_OR_NONE))  #18 = G
    trade.setField(fix.HandlInst(fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION))  # 21 = 1
    trade.setField(fix.OrderQty(iQty))  #38 = 
    trade.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40 = 2 (limit order)
    trade.setField(fix.Price(iPrice))   #44 = 

    if iBuySell.lower() == 'buy':
        trade.setField(fix.Side(fix.Side_BUY))  #54 = 1
    if iBuySell.lower() == 'sell':
        trade.setField(fix.Side(fix.Side_SELL))

    trade.setField(fix.Symbol(iSymbol))  # 55 = MSFT
    trade.setField(fix.TimeInForce(fix.TimeInForce_DAY))  #59 = 0

    trade.setField(fix.TransactTime('20210720-21:55:00.000'))

    trade.setField(fix.NoTradingSessions(1))  # 386 = 
    trade.setField(fix.TradingSessionID('POST'))   # 336 =
    # trade.setField(fix.StringField(386, '1'))
    # trade.setField(fix.StringField(336, 'PRE'))

    dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    tTag = fix.TransactTime()
    tTag.setString(dnow)
    trade.setField(tTag)

    return trade

def resetSequence():
    trade = fix.Message()
    header = trade.getHeader()

    header.setField(fix.BeginString(fix.BeginString_FIX42))
    header.setField(fix.MsgType("4"))
    trade.setField(fix.MsgSeqNum(1))
    trade.setField(fix.NewSeqNo(10))

    return trade

def algoOrder():
    trade = fix.Message()
    trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))
    trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  #35 = D

    trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
    trade.setField(fix.ClOrdID(genExecID()))  #11 = Unique order
    trade.setField(fix.HandlInst(fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION))  # 21 = 1

    trade.setField(fix.StringField(6000, "TWAP"))

    start = datetime.now(pytz.timezone('America/New_York') ).replace(hour=11, minute=30).strftime('%Y%m%d-%H:%M:%S')
    end = datetime.now(pytz.timezone('America/New_York') ).replace(hour=11, minute=55).strftime('%Y%m%d-%H:%M:%S')

    trade.setField(fix.StringField(6001, start))
    trade.setField(fix.StringField(6002, end))

    trade.setField(fix.TimeInForce(fix.TimeInForce_DAY))  #59 = 0
    trade.setField(fix.OrdType(fix.OrdType_MARKET))

    trade.setField(fix.Side(fix.Side_BUY))    # 54
    trade.setField(fix.Symbol('NOK'))  # 55
    trade.setField(fix.OrderQty(5000))  #38 = 

    dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    tTag = fix.TransactTime()
    tTag.setString(dnow)
    trade.setField(tTag)  # 60 = 

    return trade