import app

def play(input_value):
    decision = make_decision().upper()
    
    if(decision == 'CALL' or decision == 'PUT'):
        print(decision  + ' - value: ' + str(input_value))
        status,id = app.buy(input_value, decision)
        #app.print_result_order(status, id)
        if status:
            result,profit = app.api().check_win_v4(id)
            print('Result: ' + result +' / Profit ' + str(profit))
    else:
        print('pass')

def make_decision():
    return 'CALL' #make your rule

#restul order: win loose