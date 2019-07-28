import calculator_input as calc

print("""
Hi there! I am your calculator robot. I can add, subtract, multiply and divide.
 Enter a for addition.
 Enter s for substraction
 Enter m for mulitiplication
 Enter d for division
Provide your choice:
""")

choice = input()
operator = " "
if choice == "a":
    operator = "addition"
elif choice == "s":
    operator = "subtraction"
elif choice == "m":
    operator = "multiplication"
elif choice == "d":
    operator = "division"
else:
    operator = "unknown"

print("Nice choice, we will do " + operator)
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
result = 0
if choice == "a":
    result = calc.addition(num1, num2)
elif choice == "s":
    result = calc.subtraction(num1, num2)
elif choice == "m":
    result = calc.multiplication(num1, num2)
elif choice == "d":
    result = calc.division(num1, num2)
else:
    result = 0
print("the result of your calculation is " + str(result))
