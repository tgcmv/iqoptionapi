from iqoptionapi.stable_api import IQ_Option
import app, rules, json
import time

app.init()

print('Use active: ' + app.actives())
print('Inital balance: ' + str(round(app.current_balance(),2)))
print('Stop loose: ' + str(round(app.stop_loose_balance(),2)))
print('Stop gain: ' +  str(round(app.stop_gain_balance(),2)))

input_value = app.input_value()
strikes = 0

while True:
    if(not rules.it_is_a_good_time()):
        print('it is not a good time for trade')
        break
    if app.stop_loose():
        print('stop loose, current balance: ' + str(round(app.current_balance(),2)))
        break
    if app.stop_gain():
        print('stop gain, current balance: ' + str(round(app.current_balance(),2)))
        break

    if(strikes > 2):
        print('stop strikes, current balance: + ' + str(round(app.current_balance(),2)))
        break

    #print('current balance: + ' + str(round(app.current_balance(),2)))
    time.sleep(1)    
    profit = rules.play_mhi(input_value, app.martin_gale())
    print('current balance: ' + str(round(app.current_balance(),2)))
    if profit < 0:
        strikes += 1

# ------------------------------------------------------------------------------------------------------------------
