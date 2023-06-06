
def validate_credit_card(card_number):

    if len(card_number) < 13 or len(card_number) > 16:
        print('Invalid Credit Card')
        return False

    first_digit = card_number[:2]
    card_type = ''
    print(first_digit, len(card_number))

    if int(first_digit[0]) == 4 and len(card_number) == 13:
        card_type = 'VISA'
    elif int(first_digit[0]) == 5 and len(card_number) == 13:
        card_type = 'Master'
    elif int(first_digit[0]) == 3 and int(first_digit[1]) == 7 and len(card_number) == 16:
        card_type = 'American Express'
    elif int(first_digit[0]) == 6 and len(card_number) == 15:
        card_type = 'Discover'
    else:
        print('Invalid Credit Card')
        return False

    digits = [int(digit) for digit in str(card_number)][::-1]
    multiplied_digits = [digit * 2 if i % 2 == 1 else digit for i, digit in enumerate(digits)]
    summed_digits = [sum(int(digit) for digit in str(x)) for x in multiplied_digits]
    total_sum = sum(summed_digits)
    
    if total_sum % 10 == 0:
        print('card is valid and type is ', card_type)
        return True
    else:
        print("Invalid Credit Card")
        return False


card_number = input("Enter card number : ")
validate_credit_card(card_number)
