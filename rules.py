import app, time
from datetime import datetime

def play_mhi(input_value, martingale):
    count_martingale = 0
    profit = 0
    while True:
        if(count_martingale == 0):
            decision = make_decision().upper()
        else:
            print('current martingale: ' + str(count_martingale))    

        profit = 0
        print('   -->' + decision  + ' / value: ' + str(input_value))
        if(decision == 'CALL' or decision == 'PUT'):
            result, profit = app.buy(input_value, decision)
            print('   --> Result: ' + result +' / Profit ' + str(profit))

        if(profit < 0 and (martingale-1) > count_martingale):
            count_martingale += 1
            input_value = input_value*2
        else:
            break
    return profit

def it_is_a_good_time():
    return True

def make_decision():
    while True:
        now = datetime.now()
        minute = (now.minute == 0 or now.minute % 5 == 0)
        if (minute and now.second < 7):
            print(str(now.minute) + ':' + str(now.second))

            qtd_green, qtd_red, has_neutral = get_status_candles(3)
            print('   --> green: ' + str(qtd_green) + ' red: ' + str(qtd_red) + ' has neutral: ' +str(has_neutral))
            if (has_neutral):
                return 'NONE'
            if (qtd_green > qtd_red):
                return 'PUT'
            elif (qtd_green < qtd_red):
                return 'CALL'
        
        time.sleep(1)

def get_status_candles(count):
    qtd_green = 0
    qtd_red = 0
    has_neutral = False
    candle_list = app.get_candles(4)
    candle_list.pop()
    for candle in candle_list:
        #print(str(candle))
        print('   --> date: ' 
            + ' ' + app.time_ms(candle['from'])
            + ' ' + app.time_ms(candle['to'])
            + ' delta: ' + 
            str(candle['close'] - candle['open']))
        if(candle['close'] > candle['open'] ):
            qtd_green += 1
        elif(candle['close'] < candle['open']):
            qtd_red += 1
        else:
            has_neutral = True
    return qtd_green, qtd_red, has_neutral