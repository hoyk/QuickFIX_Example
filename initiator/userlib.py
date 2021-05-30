
def OrdType_Match(data):
    result = ''
    if data == 'Market':
        result = '1'
    elif data == 'Limit':
        result = '2'
    elif data == 'Stop':
        result = '3'
    elif data == 'Stop Limit':
        result = '4'
    elif data == 'Market On Close':
        result = '5'
    elif data == 'Limit On Close':
        result = 'B'
    elif data == 'Trailing Stop':
        result = 'P'
    return result

def Side_Match(data):
    result = ''
    if data == 'Buy':
        result = '1'
    elif data == 'Sell':
        result = '2'
    elif data == 'Sell short':
        result = '5'
    return result

def TimeInForce_Match(data):
    result = ''
    if data == 'Day':
        result = '0'
    elif data == 'GTC':
        result = '1'
    elif data == 'At the opening':
        result = '2'
    elif data == 'GTD':
        result = '6'
    elif data == 'IOC':
        result = '3'
    elif data == 'FOK':
        result = '4'
    return result

