import app, time
from datetime import datetime

def play_mhi(input_value, martingale):
    count_martingale = 0
    profit = 0
    while True:
        if app.stop_loose():
            break
        if(count_martingale == 0):
            decision = make_decision().upper()
            print('decision: ' + str(decision))
        else:
            print('martingale: ' + str(count_martingale))    

        profit = 0
        print('   -->' + str(input_value))
        if(decision == 'CALL' or decision == 'PUT'):
            now = datetime.now()
            print('   --> buy time: ' + str(now.minute) + ':' + str(now.second))
            result, profit = app.buy(input_value, decision)
            print('   --> Result: ' + str(result) +' / Profit ' + str(profit))

            if(profit < 0 and martingale > count_martingale):
                count_martingale += 1
                input_value = input_value*2
            else:
                break
    return profit

def it_is_a_good_time():
    full_list = app.get_candles(121)
    full_list.pop()
    candle_list = []

    qtd_neutral = 0
    qtd_win = 0
    qtd_loose = 0
    qtd_martingale = 0

    for i in range(len(full_list)):

        candle_list.append(full_list[i])
        if(len(candle_list) == 5):
            qtd_green, qtd_red, has_neutral = get_status_candles(candle_list[:3])
            decision = analisys_candles_decision(qtd_green, qtd_red, has_neutral)
            if(decision == 'NONE'):
                qtd_neutral += 1
            else:
                for martin in range(3):
                    if(martin == 2):
                        qtd_loose += 1
                        break
                    
                    green, red, neutral = get_status_candle(candle_list[3 + martin])
                    win = (decision == 'CALL' and green) or (decision == 'PUT' and red)
                    
                    if(win):
                        qtd_win += 1
                        break;
                    else:
                        qtd_martingale += 1
            candle_list = []

    print('qtd_martingale: ' + str(qtd_martingale) + ' qtd_neutral: ' + str(qtd_neutral) + ' qtd_win: ' + str(qtd_win) + ' qtd_loose: ' + str(qtd_loose))
    return qtd_loose < 5 and qtd_martingale < 10 and qtd_neutral < 5

def analisys_candles_decision(qtd_green, qtd_red, has_neutral):
    if (has_neutral):
        return 'NONE'
    if (qtd_green > qtd_red):
        return 'PUT'
    elif (qtd_green < qtd_red):
        return 'CALL'

def make_decision():
    while True:
        now = datetime.now()
        minute = (now.minute == 0 or now.minute % 5 == 0)
        if (minute and now.second < 2):
            candle_list = app.get_candles(6)
            candle_list.pop()
            qtd_green, qtd_red, has_neutral = get_status_candles(candle_list)
            return analisys_candles_decision(qtd_green, qtd_red, has_neutral)
        time.sleep(1)

def get_status_candles(candle_list):
    qtd_green = 0
    qtd_red = 0
    has_neutral = False

    for candle in candle_list:
        green, red, neutral = get_status_candle(candle)    
        qtd_green += green
        qtd_red += red
        if(neutral):
           has_neutral = True
    return qtd_green, qtd_red, has_neutral

def get_status_candle(candle):
    green = 0
    red = 0
    neutral = False
    if(candle['close'] > candle['open'] ):
        green += 1
    elif(candle['close'] < candle['open']):
        red += 1
    else:
        neutral = True
    return green, red, neutral