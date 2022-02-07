import questionary
from questionary import Separator, Choice, prompt

def ask_order(**kwargs):
    questions = [
        {
            "type": "select",
            "name": "OrdType",
            "message": "(40) Select order type: ",
            "choices": ["Market","Limit","Stop","Stop Limit", "Market On Close","Limit On Close","Trailing Stop"],
            "default": "Market",
        },
        {
            "type": "text",
            "name": "Symbol",
            "message": "(55) Input symbol: ",
        },
        {
            "type": "select",
            "name": "Side",
            "message": "(54) Select side: ",
            "choices": ["Buy","Sell","Sell short"],
            "default": "Buy",
        },
        {
            "type": "text",
            "name": "Price",
            "when": lambda x: x['OrdType'] in ['Limit', 'Stop Limit', 'Limit On Close'],
            "message": "(44) Limit price: ",
        },
        {
            "type": "text",
            "name": "CashOrderQty",
            "message": "(152) Dollor order amount: ",
            # "when": lambda x: x['OrdType'] == 'Market',
        },
        {
            "type": "text",
            "name": "OrderQty",
            "message": "(38) Order quentity: ",
            "default": "1"
        },
        {
            "type": "select",
            "name": "TimeInForce",
            "message": "(59) Select TimeInForce: ",
            "choices": ["Day","GTC","At the opening","GTD","IOC","FOK"],
            "default": "Day",
        },
        {
            "type": "text",
            "name": "StopPx",
            "when": lambda x: x["OrdType"] == "Stop" or x["OrdType"] == "Stop Limit",
            "message": "(99) Input stop price: ",
        },
        {
            "type": "confirm",
            "name": "prepost",
            "message": "Pre & Post Market? ",
            "default": False
        },
        {
            "type": "select",
            "name": "NoTradingSessions",
            "choices": ["1", "2", "3"],
            "when": lambda x: x['prepost'],
            "message": "(386) NoTradingSessions: ",            
        },
        # ==== TradingSessionID 3 ====
        {
            "type": "select",
            "name": "TradingSessionID1",
            "message": "(336) TradingSessionID (1): ",
            "when": lambda x: x['prepost'] and x['NoTradingSessions'] == "3",
            "choices": ["PRE","CORE","POST","ALL"],
        },
        {
            "type": "select",
            "name": "TradingSessionID2",
            "message": "(336) TradingSessionID (2): ",
            "when": lambda x: x['prepost'] and x['NoTradingSessions'] == "3",
            "choices": ["PRE","CORE","POST","ALL"],
        },
        {
            "type": "select",
            "name": "TradingSessionID3",
            "message": "(336) TradingSessionID (3): ",
            "when": lambda x: x['prepost'] and x['NoTradingSessions'] == "3",
            "choices": ["PRE","CORE","POST","ALL"],
        },
        # ==== TradingSessionID 2 ====
        {
            "type": "select",
            "name": "TradingSessionID1",
            "message": "(336) TradingSessionID (1): ",
            "when": lambda x: x['prepost'] and x['NoTradingSessions'] == "2",
            "choices": ["PRE","CORE","POST","ALL"],
        },
        {
            "type": "select",
            "name": "TradingSessionID2",
            "message": "(336) TradingSessionID (2): ",
            "when": lambda x: x['prepost'] and x['NoTradingSessions'] == "2",
            "choices": ["PRE","CORE","POST","ALL"],
        },
        # ==== TradingSessionID 1 ====
        {
            "type": "select",
            "name": "TradingSessionID1",
            "message": "(336) TradingSessionID (1): ",
            "when": lambda x: x['prepost'] and x['NoTradingSessions'] == "1",
            "choices": ["PRE","CORE","POST","ALL"],
        }
    ]

    return prompt(questions, **kwargs)

if __name__ == "__main__":
    answer = ask_order()
    print(answer)

