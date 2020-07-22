import app, time
from datetime import datetime

def play(input_value):
    decision = make_decision().upper()
    print('decision: ' + decision)
    profit = 0
    if(decision == 'CALL' or decision == 'PUT'):
        print(decision  + ' / value: ' + str(input_value))
        result, profit = app.buy(input_value, decision)
        print('Result: ' + result +' / Profit ' + str(profit))
    else:
        print('pass')        

def it_is_a_good_time():
    return True

def make_decision():
    while True:
        now = datetime.now()
        if ((now.minute == 0 or (now.minute-3) % 5 == 0)): #and now.second < 5):
            qtd_green, qtd_red, has_neutral = get_status_candles(3)
            print('green: ' + str(qtd_green) + ' red: ' + str(qtd_red) + ' none: ' +str(has_neutral))
            if (has_neutral):
                return 'NONE'
            if (qtd_green > qtd_red):
                return 'CALL'
            elif (qtd_green < qtd_red):
                return 'PUT'
        
        print(str(now.minute) + ':' + str(now.second))
        time.sleep(1)

def get_status_candles(count):
    qtd_green = 0
    qtd_red = 0
    has_neutral = False
    candle_list = app.get_candles(4)
    candle_list.pop()
    for candle in candle_list:
        #print(str(candle))
        #print(app.time_converter(candle['from']))
        #print(app.time_converter(candle['to']))
        if(candle['close'] > candle['open'] ):
            qtd_green += 1
        elif(candle['close'] < candle['open']):
            qtd_red += 1
        else:
            has_neutral = True
    return qtd_green, qtd_red, has_neutral