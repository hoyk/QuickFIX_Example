#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import os
# from datetime import datetime
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
from model import Field
from model.Message import __SOH__

# Logger
setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class Application(fix.Application):
    """FIX Application"""
    execID = 0
    testCaseID = ''
    exeONE = 1
    exeTWO = 2

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        # print('onCreate()')
        return
    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print(f'[Successful Logon to session {sessionID.toString()}]')
        return
    def onLogout(self, sessionID): 
        print(f'[Successful Logout to session {sessionID.toString()}]')
        return

    def toAdmin(self, message, sessionID):
        if message.getHeader().getField(35) == 'A' :
            message.getHeader().setField(fix.StringField(95, '32'))
            message.getHeader().setField(fix.StringField(96, os.environ.get('Orbis_FIX_Token')))

        msg = message.toString().replace(__SOH__, " ")
        logfix.info(f"S >> {msg}")
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, " ")
        logfix.info("R << %s" % msg)
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, " ")
        logfix.info("S >> %s" % msg)
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, " ")
        logfix.info("R << %s" % msg)
        self.onProcessMessage(message, sessionID)
        return
    
    def onProcessMessage(self, message, sessionID):
        OrdStatus = fix.OrdStatus()
        Symbol = fix.Symbol()
        Side = fix.Side()
        ClOrdID = fix.ClOrdID()
        OrderQty = fix.OrderQty()

        if self.testCaseID == '4' and message.getField(OrdStatus).getString() == '0' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)
        
        if self.testCaseID == '5' and message.getField(OrdStatus).getString() == '0' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)

        if self.testCaseID == '7' and message.getField(OrdStatus).getString() == '0' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)            

        if self.testCaseID == '8' and message.getField(OrdStatus).getString() == '0' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelReplaceOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString(),
                message.getField(OrderQty).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)                    

        if self.testCaseID == '9' and message.getField(OrdStatus).getString() == '0' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelReplaceOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString(),
                message.getField(OrderQty).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)       

        if self.testCaseID == '15' and message.getField(OrdStatus).getString() == '1' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)              
            
        if self.testCaseID == '16' and message.getField(OrdStatus).getString() == '1' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)         

        if self.testCaseID == '17' and message.getField(OrdStatus).getString() == '1' and self.exeONE != 0:
            self.exeONE -= 1
            trade = self.cancelReplaceOrder(
                message.getField(ClOrdID).getString(),
                message.getField(Symbol).getString(),
                message.getField(Side).getString(),
                message.getField(OrderQty).getString()
            )
            fix.Session.sendToTarget(trade, self.sessionID)                                   
    
    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def genExecID(self):
        # self.execID = self.execID + 1
        # return str( self.execID )
        return str(int(time.time() * 1000))

    def cancelReplaceOrder(self, OrigClOrdID, Symbol, Side, OrderQty):
        trade = fix.Message()
        header = trade.getHeader()

        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.MsgType("G"))
        trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
        trade.setField(fix.ClOrdID(self.genExecID()))  #11 = Unique order
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

    def cancelOrder(self, OrigClOrdID, Symbol, Side):
        trade = fix.Message()
        header = trade.getHeader()

        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.MsgType("F"))

        trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
        trade.setField(fix.ClOrdID(self.genExecID()))  #11 = Unique order
        trade.setField(fix.OrigClOrdID(OrigClOrdID))    # 41 = 

        dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
        tTag = fix.TransactTime()
        tTag.setString(dnow)
        trade.setField(tTag)  # 60 = 
        trade.setField(fix.Symbol(Symbol))  # 55 = 
        trade.setField(fix.Side(Side))    # 54

        return trade

    def generateOrder(self, iSymbol, iBuySell, iQty):
        trade = fix.Message()
        trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))
        trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  #35 = D

        trade.setField(fix.Account('TRYIKANG'))   #1 = 'TRYIKANG'
        trade.setField(fix.ClOrdID(self.genExecID()))  #11 = Unique order
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

        dnow = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
        tTag = fix.TransactTime()
        tTag.setString(dnow)
        trade.setField(tTag)

        return trade
        # fix.Session.sendToTarget(trade, self.sessionID)

    def Reject_For_Odd_Lot(self):    #1 : Reject for odd lot
        trade = self.generateOrder('MSFT', 'buy', 50)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Reject_For_Sell(self):    #2: Reject for sell
        trade = self.generateOrder('BAC', 'sell', 100)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Order_Reject(self):    #3 : Order reject
        trade = self.generateOrder('NOK', 'buy', 1000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def No_Action(self):    #4 : No action
        trade = self.generateOrder('NOK', 'buy', 2000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Too_Late_To_Cancel(self):    #5 : Too late to cancel
        trade = self.generateOrder('NOK', 'buy', 2300)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Unsolicited_Out(self):    #6 : Unsolicited out
        trade = self.generateOrder('NOK', 'buy', 2400)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Cancel_Reject(self):    #7 : Cancel reject
        trade = self.generateOrder('NOK', 'buy', 2500)
        fix.Session.sendToTarget(trade, self.sessionID)

    def CR_Reject(self):    #8 : Cancel/replace reject
        trade = self.generateOrder('NOK', 'buy', 2500)
        fix.Session.sendToTarget(trade, self.sessionID)

    def CR_Reject_Fill(self):    #9 : Cancel/replace reject
        trade = self.generateOrder('NOK', 'buy', 2550)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Execution_Cancel(self):    #10 : Execution_Cancel
        trade = self.generateOrder('NOK', 'buy', 2600)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Fill_Cancel(self):    #11 : Fill_Cancel     
        trade = self.generateOrder('NOK', 'buy', 2640)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_Bust(self):    #12 : Partial_Bust      
        trade = self.generateOrder('NOK', 'buy', 2644)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_Fill_Correct(self):    #13 : Partial, Fill, Fill correct     
        trade = self.generateOrder('NOK', 'buy', 2645)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Fill_Cancel_Correct(self):    #14 : Fill, Cancel, Cancel correct
        trade = self.generateOrder('NOK', 'buy', 2650)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_Fill(self):    #15 : Partial fill    
        trade = self.generateOrder('NOK', 'buy', 2700)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_Fill_Cancel(self):     #16 : Partial fill cancel
        trade = self.generateOrder('NOK', 'buy', 2800)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_CR_Fill(self):     #17 : Partial CR fill     
        trade = self.generateOrder('NOK', 'buy', 3100)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_Each_CR_Fill(self): #18 : Partials after each C/R until filled    
        trade = self.generateOrder('NOK', 'buy', 3200)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Four_Decimal(self):    #19 : 4 Decimal place execution     
        trade = self.generateOrder('NOK', 'buy', 4321)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Fill_1500(self):    #20 : Fill in 1500 lots     
        trade = self.generateOrder('NOK', 'buy', 4500)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Fill_10(self):    #21 : Fill in 10 lots     
        trade = self.generateOrder('NOK', 'buy', 5000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Fill_100(self):    #22 : Fill in 100 lots       
        trade = self.generateOrder('NOK', 'buy', 6000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_100_500_Fill(self):     #23 : Partial 100, Partial 500, Fill     
        trade = self.generateOrder('NOK', 'buy', 68000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_1000_5000_Fill_24(self):    #24 : Partial 1000, Partial 5000, Fill     
        trade = self.generateOrder('NOK', 'buy', 80000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_1000_5000_Fill_25(self):    # 25 : Partial 1000, Partial 5000, Fill  
        trade = self.generateOrder('NOK', 'buy', 90000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Partial_1000_5000_Fill_26(self):    # 26 : Partial 1000, Partial 5000, Fill     
        trade = self.generateOrder('NOK', 'buy', 100000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Fill_1000(self):    # 27 : Fill in 1000 lots 
        trade = self.generateOrder('NOK', 'buy', 1000000)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Test_A(self):
        trade = self.generateOrder('NOK', 'buy', 1)
        fix.Session.sendToTarget(trade, self.sessionID)

    def Test_B(self):
        trade = self.generateOrder('NOK', 'sell', 1)
        fix.Session.sendToTarget(trade, self.sessionID)
    
    def User_Logout(self):
        trade = fix.Message()
        header = trade.getHeader()

        header.setField(fix.BeginString(fix.BeginString_FIX42))
        header.setField(fix.MsgType('5'))
        fix.Session.sendToTarget(trade, self.sessionID)

    def run(self):
        """Run"""
        while 1:
            time.sleep(1)
            myInput = input('Select your test (h for help) >> ').lower()
            self.testCaseID = myInput
            if myInput == '1':
                print('[Test 1 : Reject for odd lot (50)]')
                self.Reject_For_Odd_Lot()

            if myInput == '2':
                print('[Test 2 : Reject for sell  (100)]')
                self.Reject_For_Sell()

            if myInput == '3':
                print('[Test 3 : Order reject (1,000)]')
                self.Order_Reject()

            if myInput == '4':
                self.exeONE = 1   # Exe one time
                print('[Test 4 : No action (2,000)]')
                self.No_Action()

            if myInput == '5':
                self.exeONE = 1   # Exe one time
                print('[Test 5 : Too late to cancel (2,300)]')
                self.Too_Late_To_Cancel()      

            if myInput == '6':
                print('[Test 6 : Unsolicited out (2,400)]')
                self.Unsolicited_Out()     

            if myInput == '7':
                self.exeONE = 1   # Exe one time
                print('[Test 7 : Cancel reject (2,500)]')
                self.Cancel_Reject()     

            if myInput == '8':
                self.exeONE = 1   # Exe one time
                print('[Test 8 : Cancel/replace reject (2,500)]')
                self.CR_Reject()     

            if myInput == '9':
                self.exeONE = 1   # Exe one time
                print('[Test 9 : C/R reject, fill (2,550)]')
                self.CR_Reject_Fill()     

            if myInput == '10':
                print('[Test 10 : Execution cancel (2,600)]')
                self.Execution_Cancel()     

            if myInput == '11':
                print('[Test 11 : Fill cancel (2,640)]')
                self.Fill_Cancel()     

            if myInput == '12':
                print('[Test 12 : Partial, partial, partial, bust, bust, bust (2,644)]')
                self.Partial_Bust()     

            if myInput == '13':
                print('[Test 13 : Partial, Fill, Fill correct (2,645)]')
                self.Partial_Fill_Correct()     

            if myInput == '14':
                print('[Test 14 : Fill cancel, correct (2,650)]')
                self.Fill_Cancel_Correct()     

            if myInput == '15':
                self.exeONE = 1   # Exe one time
                print('[Test 15 : Partial fill (2,700)]')
                self.Partial_Fill()     

            if myInput == '16':
                self.exeONE = 1   # Exe one time
                print('[Test 16 : Partial fill, cancel req, partial and cancel (2,800)]')
                self.Partial_Fill_Cancel()     

            if myInput == '17':
                self.exeONE = 1   # Exe one time
                print('[Test 17 : Partial, C/R, and fill (3,100)]')
                self.Partial_CR_Fill()     

            if myInput == '18':
                print('[Test 18 : Partials after each C/R until filled (3,200)]')
                self.Partial_Each_CR_Fill()     

            if myInput == '19':
                print('[Test 19 : 4 Decimal place execution (4,321)]')
                self.Four_Decimal()     

            if myInput == '20':
                print('[Test 20 : Fill in 1500 lots (4,500)]')
                self.Fill_1500()     

            if myInput == '21':
                print('[Test 21 : Fill in 10 lots (5,000)]')
                self.Fill_10()     

            if myInput == '22':
                print('[Test 22 : Fill in 100 lots (6,000)]')
                self.Fill_100()       

            if myInput == '23':
                print('[Test 23 : Partial 100, Partial 500, Fill (68,000)]')
                self.Partial_100_500_Fill()     

            if myInput == '24':
                print('[Test 24 : Partial 1000, Partial 5000, Fill (80,000)]')
                self.Partial_1000_5000_Fill_24()     

            if myInput == '25':
                print('[Test 25 : Partial 1000, Partial 5000, Fill (90,000)]')
                self.Partial_1000_5000_Fill_25()     

            if myInput == '26':
                print('[Test 26 : Partial 1000, Partial 5000, Fill (100,000)]')
                self.Partial_1000_5000_Fill_26()     

            if myInput == '27':
                print('[Test 27 : Fill in 1000 lots (1,000,000)]')
                self.Fill_1000()            

            if myInput == 'a':
                print('[Test Order A]')
                self.Test_A()

            if myInput == 'b':
                print('[Test Order B]')
                self.Test_B()

            if myInput == 'exit' or myInput == 'e':
                print('[User exit]')
                self.User_Logout()
                time.sleep(1)
                sys.exit(0)

            if myInput == 'help' or myInput == 'h':
                print('Select Test Cases:')
                print('1: Reject for odd lot (50)')
                print('2: Reject for sell (100)')
                print('3: Order reject (1,000)')
                print('4: No action (2,000)')
                print('5: Too late to cancel (2,300)')
                print('6: Unsolicited out (2,400)')
                print('7: Cancel reject (2,500)')
                print('8: Cancel/replace reject (2,500)')
                print('9: C/R reject, fill (2,550)')
                print('10: Execution cancel (2,600)')
                print('11: Fill cancel (2,640)')
                print('12: Partial, partial, partial, bust, bust, bust (2,644)')
                print('13: Partial, Fill, Fill correct (2,645)')
                print('14: Fill cancel, correct (2,650)')
                print('15: Partial fill (2,700)')
                print('16: Partial fill, cancel req, partial and cancel (2,800')
                print('17: Partial, C/R, and fill (3,100)')
                print('18: Partials after each C/R until filled (3,200)')
                print('19: 4 Decimal place execution (4,321)')
                print('20: Fill in 1500 lots (4,500)')
                print('21: Fill in 10 lots (5,000)')
                print('22: Fill in 100 lots (6,000)')
                print('23: Partial 100, Partial 500, Fill (68,000)')
                print('24: Partial 1000, Partial 5000, Fill (80,000)')
                print('25: Partial 1000, Partial 5000, Fill (90,000)')
                print('26: Partial 1000, Partial 5000, Fill (100,000)')
                print('27: Fill in 1000 lots (1,000,000)')
                print('A: Test A')
                print('B: Test B')
                print('======')

            else:
                # print('Please enter...')
                continue
            