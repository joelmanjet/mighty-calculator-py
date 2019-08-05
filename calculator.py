def addition(num1, num2):
    return speakable(float(num1) + float(num2))


def subtraction(num1, num2):
    return speakable(float(num1) - float(num2))


def multiplication(num1, num2):
    return speakable(float(num1) * float(num2))


def division(num1, num2):
    return speakable(float(num1) / float(num2))


def speakable(x):
    y = round(x, 1)
    z = int(y)
    if y == z:
        return z
    else:
        return y
