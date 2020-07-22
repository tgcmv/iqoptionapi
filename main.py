import app, rules

app.api()

print('Use active: ' + app.actives())
print('Inital balance: ' + str(round(app.api().get_balance(),2)))
print('Stop loose: ' + str(round(app.stop_loose_balance(),2)))
print('Stop gain: ' +  str(round(app.stop_gain_balance(),2)))

input_value = 200

while True:
    if app.stop_loose():
        print('stop loose, current balance: + ' + str(round(app.api().get_balance(),2)))
        break
    if app.stop_gain():
        print('stop gain, current balance: + ' + str(round(app.api().get_balance(),2)))
        break
        
    rules.play(input_value)
