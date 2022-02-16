acts_list = ['+', '-', '*', '/']
while True:
    action = input("Какое действие вы хотите осуществить: 1 это +, 2 это -, 3 это *, 4 это /: ")
    if action in acts_list and len(action) == 1:
        first_number = input('Введи первое число: ')
        second_number = input('Введи второе число: ')
        if first_number.isdigit() and second_number.isdigit():
            first_number = float(first_number)
            second_number = float(second_number)
            if action == '+':
                print("%.2f" % (first_number + second_number))
            elif action == '-':
                print("%.2f" % (first_number - second_number))
            elif action == '*':
                print("%.2f" % (first_number * second_number))
            elif action == '/':
                if second_number != 0:
                    print("%.2f" % (first_number / second_number))
                else:
                    print("Делить на ноль в этом калькуляторе нельзя")
        else:
                print("Ты ввел не число вместо одной из цифр")
    else:
        print('В этом маленьком калькуляторе нет такой операции, выбери снова, только правильно')
