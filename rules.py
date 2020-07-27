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
        else:
            print('current martingale: ' + str(count_martingale))    

        profit = 0
        print('   -->' + decision  + ' / value: ' + str(input_value))
        if(decision == 'CALL' or decision == 'PUT'):
            now = datetime.now()
            print('   --> buy time: ' + str(now.minute) + ':' + str(now.second))
            result, profit = app.buy(input_value, decision)
            #print('   --> Result: ' + result +' / Profit ' + str(profit))

        if(profit < 0 and (martingale-1) > count_martingale):
            count_martingale += 1
            input_value = input_value*2
        else:
            break
    return profit

def it_is_a_good_time():
    # candle_list = app.get_candles(61)
    # candle_list.pop()

    # qtd_gain = 0
    # qtd_strikes = 0
    # qtd_martingale = 0
    
    # qtd_green = 0
    # qtd_red = 0
    # has_neutral = False
    # martingale = 0
    # nextcandle = False
    # for i in range(len(candle_list)):

    #     if(not nextcandle and not has_neutral and i % 3 == 0):
    #         if (qtd_green > qtd_red):
    #             nextcandle = 'RED'
    #         elif (qtd_green < qtd_red):
    #             nextcandle = 'GREEN'
    #         continue
    #     green = candle_list[i]['close'] > candle_list[i]['open']
    #     red = candle_list[i]['close'] < candle_list[i]['open']
    #     #print(str(i) + ' nextcandle: ' + str(nextcandle) + ' green: ' + str(green) + ' red: ' + str(red))
        
    #     neutral = candle_list[i]['close'] == candle_list[i]['open']
    #     if((nextcandle == 'RED' and green) or (nextcandle == 'GREEN' and red)):
    #         qtd_martingale += 1
    #         martingale += 1
    #         #print('    --> martingale')
    #     elif(neutral):
    #         nextcandle = False
    #         #print('    --> neutral')
    #         continue
    #     elif(nextcandle == 'RED' or nextcandle == 'GREEN'):
    #         nextcandle = False
    #         qtd_gain += 1
        
    #     if(martingale >= 2):
    #         qtd_strikes += 1

    #         martingale = 0 
    #         has_neutral = True
    #         qtd_green = 0
    #         qtd_red = 0
    #         has_neutral = False
    #         nextcandle = False
    #         #print('    --> strike :/')
    #         continue

    #     if(not nextcandle and (i % 4 == 0  or i % 5 == 0)):
    #         #print('    --> nextcandle')
    #         continue

    #     if(green):
    #         qtd_green += 1
    #     elif(red):
    #         qtd_red += 1
    #     else:
    #         has_neutral = True

    # print('last 60 candles (12 gambles): ')
    # print('gain: ' + str(qtd_gain)
    #     + ' strikes: ' + str(qtd_strikes)
    #     + ' martingale: ' +  str(qtd_martingale)
    #     + ' neutral: ' + str(12 - (qtd_gain + qtd_strikes)))


    return True #qtd_strikes > 5 or qtd_martingale > 10 or qtd_gain > 5

def make_decision():
    while True:
        now = datetime.now()
        minute = (now.minute == 0 or now.minute % 5 == 0)
        if (minute and now.second < 3):
            #print('   --> decision start: ' + str(now.minute) + ':' + str(now.second))
            qtd_green, qtd_red, has_neutral = get_status_candles()
            #print('   --> green: ' + str(qtd_green) + ' red: ' + str(qtd_red) + ' has neutral: ' +str(has_neutral))
            if (has_neutral):
                return 'NONE'
            if (qtd_green > qtd_red):
                return 'PUT'
            elif (qtd_green < qtd_red):
                return 'CALL'
        
        time.sleep(1)

def get_status_candles():
    qtd_green = 0
    qtd_red = 0
    has_neutral = False
    candle_list = app.get_candles(6)
    candle_list.pop()
    for candle in candle_list:
        #print(str(candle))
        # print('   --> date: ' 
        #     + ' ' + app.time_ms(candle['from'])
        #     + ' ' + app.time_ms(candle['to'])
        #     + ' delta: ' + 
        #     str(candle['close'] - candle['open']))
        if(candle['close'] > candle['open'] ):
            qtd_green += 1
        elif(candle['close'] < candle['open']):
            qtd_red += 1
        else:
            has_neutral = True
    return qtd_green, qtd_red, has_neutral