import tkinter as ttk
import tkinter
import math


new_operand = False
brackets = 0
expression = ""

# Todo: if F-E is toggled, use exp_format, else use decimal format.
# Todo: if value is in exp format, change it to decimal.


class Format:
    def __init__(self, value: str):
        self.value = str(value)

    def __add__(self, other):
        return self.value + other

    def __str__(self):
        return self.result_format()

    def exp_format(self):
        if all(True if char.isdigit() or char == "." else False for char in self.value):
            if eval(self.value) > 1:
                new_val = self.value[0] + "."
                dp_count = 0
                for char in self.value[1:]:
                    if char != "0":
                        new_val += char
                    else:
                        if int(self.value[self.value.index(char):]) == 0:
                            break
                        new_val += "0"
                    if dp_count == 5:
                        break
                    dp_count += 1
                new_val += "e+" + str(len(self.value[1:]))

            else:
                decimal = self.value.split(".")[1]
                first = str(int(decimal))[0]
                first_ind = decimal.index(first)
                new_val = first + "."
                dp_count = 0
                for char in decimal[first_ind + 1:]:
                    if char != "0":
                        new_val += char
                    else:
                        if int(self.value[self.value.index(char):]) == 0:
                            break
                        new_val += "0"
                    if dp_count == 5:
                        break
                    dp_count += 1
                new_val += "e-" + str(len(decimal[:first_ind + 1]))
            return new_val
        return self.value

    def result_format(self):
        if '.' in self.value and "e" not in self.value:
            whole, decimal = self.value.split(".")
            decimal = "".join(decimal)
            if len(decimal) == 1 and decimal == "0":
                value = "".join(whole)
            else:
                value = ".".join([whole, decimal])

        elif len(self.value) > 19:
            value = self.exp_format()

        else:
            value = self.value

        return value

    # ! Deprecated method, made redundant by python's eval()
    @staticmethod
    def decimal_format(value):
        e_ind = value.index("e")
        if "e+" in value:
            value = float(value[:e_ind]) * (10 ** int(value[e_ind + 2:]))

        elif "e-" in value:
            value = float(value[:e_ind]) / (10 ** int(value[e_ind + 2:]))
        return value


def angle_value(value):
    if degreeUnit.get() == 0:
        # converts degree to radians
        return math.radians(value)

    elif degreeUnit.get() == 1:
        # leaves value as radians
        return value

    else:
        # converts grad to radians
        return value * 0.0157


def clear_expression():
    global expression
    expression = ""
    expressionDisplay.set("")


def expression_append(val):
    if new_operand is not True:
        expressionDisplay.set(expressionDisplay.get() + acc.get() + val)
    else:
        expressionDisplay.set(expressionDisplay.get() + val)


def get_result():
    try:
        if expression[-1] == "(":
            return 0
        elif expression[-1] == ")":
            return eval(expression)
        elif expression[-2] in ("/", "*"):
            if brackets == 0:
                return eval(expression + "1")
        elif expression[-2] in ("+", "-"):
            if brackets == 0:
                return eval(expression + "0")
        return acc.get()
    except ZeroDivisionError:
        acc.set("Math Error")


def press(val):
    global new_operand
    global expression
    global brackets

    if len(acc.get()) < 19 or new_operand is True:
        if new_operand is False:
            if "e" in acc.get() and acc.get()[-1] == "0":
                acc.set(acc.get()[:-1])
            if val == 0 and acc.get()[0] == "0" and len(acc.get()) == 1:
                acc.set("0")
            elif val == "." and acc.get()[0] == "0":
                acc.set(acc.get() + val)
            if expression:
                if expression[-1] == ")":
                    expression = expression[:-1] + str(val) + ")"
            else:
                if abs(float(acc.get() + str(val))) >= 1:
                    acc.set((acc.get() + str(val)).lstrip("0"))
                else:
                    acc.set(acc.get() + str(val))

        else:
            acc.set(val)
            if expression[-2] == "/":
                expression += acc.get() + ")"
                brackets -= 1
            new_operand = False


def evaluate():
    global expression
    global brackets
    try:
        if expression:
            if expression[-1] == ")":
                result = round(get_result(), 10)
            else:
                if brackets == 1:
                    expression += acc.get() + ")"
                    brackets -= 1
                    result = round(eval(expression), 10)
                else:
                    result = round(eval(expression + acc.get()), 10)
            acc.set(Format(result))
            clear_expression()

        else:
            if "e" in acc.get():
                acc.set(Format(str(eval(acc.get()))).result_format())
            clear_expression()

    except ZeroDivisionError:
        acc.set("Math Error")


def clear(case):
    if case == 1:
        if len(acc.get()) > 1:
            acc.set(acc.get()[:-1])

        elif len(acc.get()) == 1:
            acc.set("0")

    elif case == 2:
        acc.set("0")
        if len(expressionDisplay.get().split()) == 1:
            clear_expression()

    else:
        acc.set("0")
        clear_expression()


def operate(operator):
    global new_operand
    global brackets
    global expression

    if expression:
        if expression[-1] == ")":
            acc.set("")

    if operator == "+":
        expression += acc.get() + " + "
        expression_append(" + ")

    elif operator == "-":
        expression += acc.get() + " - "
        expression_append(" - ")

    elif operator == "/":
        expression += acc.get() + " / "
        expression_append(" / ")

    elif operator == "*":
        expression += acc.get() + " * "
        expression_append(" * ")

    elif operator == "mod":
        expression += acc.get() + " % "
        expression_append(" mod ")

    elif operator == "^":
        expression += acc.get() + " ** "
        expression_append(" ^ ")

    elif operator == "root":
        brackets += 1
        expression += acc.get() + " ** (1 / "
        expression_append(" yroot ")

    elif operator == "(":
        expression += "("
        expression_append("(")
        brackets += 1

    elif operator == ")":
        expression += acc.get() + ")"
        expression_append(")")
        brackets -= 1

    if operator != "root":
        acc.set(get_result())

    new_operand = True


def exponential():
    acc.set(acc.get() + "e+0")


def func(function):
    global new_operand

    value = eval(acc.get())

    if function == "neg":
        acc.set(-value)

    elif function == "sqrt":
        expressionDisplay.set(expressionDisplay.get() + f"sqrt({value}) ")
        new_operand = True
        acc.set(round(math.sqrt(value), 10))

    elif function == "per":
        acc.set(value / 100)

    elif function == "rec":
        expressionDisplay.set(expressionDisplay.get() + f"reciproc({value})")
        new_operand = True
        acc.set(round((1 / value), 10))

    elif function == "ln":
        try:
            expressionDisplay.set(expressionDisplay.get() + f"ln({value})")
            new_operand = True
            acc.set(round(math.log(value), 10))
        except ValueError:
            acc.set("Math Error")

    elif function == "sinh":
        expressionDisplay.set(expressionDisplay.get() + f"sinh({value})")
        new_operand = True
        acc.set(round(math.sinh(angle_value(value)), 10))

    elif function == "sin":
        expressionDisplay.set(expressionDisplay.get() + f"sin({value})")
        new_operand = True
        acc.set(round(math.sin(angle_value(value)), 10))

    elif function == "sqr":
        expressionDisplay.set(expressionDisplay.get() + f"sqr({value})")
        new_operand = True
        acc.set(round(math.pow(value, 2), 10))

    elif function == "fact":
        try:
            expressionDisplay.set(expressionDisplay.get() + f"fact({value})")
            new_operand = True
            acc.set(Format(str(math.factorial(value))))
        except ValueError:
            acc.set("Math Error")

    elif function == "cosh":
        expressionDisplay.set(expressionDisplay.get() + f"cosh({value})")
        new_operand = True
        acc.set(round(math.cosh(angle_value(value)), 10))

    elif function == "cos":
        expressionDisplay.set(expressionDisplay.get() + f"cos({value})")
        new_operand = True
        acc.set(round(math.cos(angle_value(value)), 10))

    elif function == "pi":
        acc.set(round(math.pi, 10))

    elif function == "tanh":
        expressionDisplay.set(expressionDisplay.get() + f"tanh({value})")
        new_operand = True
        acc.set(round(math.tanh(angle_value(value)), 10))

    elif function == "tan":
        expressionDisplay.set(expressionDisplay.get() + f"tanh({value})")
        new_operand = True
        acc.set(round(math.tan(angle_value(value)), 10))

    elif function == "cube":
        expressionDisplay.set(expressionDisplay.get() + f"cube({value})")
        new_operand = True
        acc.set(round(math.pow(value, 3), 10))

    elif function == "crt":
        expressionDisplay.set(expressionDisplay.get() + f"crt({value})")
        new_operand = True
        acc.set(round(math.pow(value, 1 / 3), 10))

    elif function == "alog":
        expressionDisplay.set(expressionDisplay.get() + f"powerten({value})")
        new_operand = True
        acc.set(round(math.pow(10, value)))

    elif function == "log":
        try:
            expressionDisplay.set(expressionDisplay.get() + f"log({value})")
            new_operand = True
            acc.set(round(math.log10(value), 10))
        except ValueError:
            acc.set("Math Error")


def create_num_button(val, row, col):
    return tkinter.Button(standardFrame, text=str(val), relief="groove", bg="#ffffff", command=lambda: press(val)).grid(row=row, column=col, sticky="ew", padx=2, pady=2)


if __name__ == "__main__":

    calculator = ttk.Tk()
    calculator.title("Calculator")
    calculator.resizable(0, 0)
    calculator.configure(bg="#acd8db")

    displayFrame = ttk.Frame(calculator, borderwidth=3, relief="sunken", padx=2, pady=2)
    displayFrame.grid(row=0, column=0, columnspan=10, sticky="ew")

    expressionDisplay = ttk.StringVar()
    displayLabel1 = ttk.Entry(displayFrame, state="disabled", disabledbackground="white", justify="right", font="segoeui 10", highlightthickness=0, borderwidth=0, textvariable=expressionDisplay)

    acc = ttk.StringVar()
    acc.set("0")
    displayLabel2 = ttk.Entry(displayFrame, state="disabled", disabledbackground="white", justify="right", font="segoeui 25", highlightthickness=0, borderwidth=0, textvariable=acc)

    displayLabel1.grid(row=0, sticky="ew")
    displayLabel2.grid(row=1, sticky="ew")

    radioFrame = ttk.Frame(calculator, borderwidth=1, relief="solid")
    radioFrame.grid(row=1, column=0, columnspan=5, padx=2, pady=2)

    degreeUnit = ttk.IntVar()

    ttk.Radiobutton(radioFrame, text="Degrees", variable=degreeUnit, value=0).grid(row=0, column=0)

    ttk.Radiobutton(radioFrame, text="Radians", variable=degreeUnit, value=1).grid(row=0, column=1)

    ttk.Radiobutton(radioFrame, text="Grads", variable=degreeUnit, value=2).grid(row=0, column=2)

    standardFrame = ttk.Frame(calculator, borderwidth=1, bg="#acd8db")
    standardFrame.grid(row=1, column=6, rowspan=6)

    buttonMC = ttk.Button(standardFrame, text="MC").grid(row=0, column=0, sticky="ew", padx=2, pady=2)
    buttonMR = ttk.Button(standardFrame, text="MR").grid(row=0, column=1, sticky="ew", padx=2, pady=2)
    buttonMS = ttk.Button(standardFrame, text="MS").grid(row=0, column=2, sticky="ew", padx=2, pady=2)
    buttonMp = ttk.Button(standardFrame, text="M+").grid(row=0, column=3, sticky="ew", padx=2, pady=2)
    buttonMm = ttk.Button(standardFrame, text="M-").grid(row=0, column=4, sticky="ew", padx=2, pady=2)
    buttonDel = ttk.Button(standardFrame, text="\u2190", command=lambda: clear(1)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
    buttonCE = ttk.Button(standardFrame, text="CE", command=lambda: clear(2)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
    buttonC = ttk.Button(standardFrame, text="C", command=lambda: clear(3)).grid(row=1, column=2, sticky="ew", padx=2, pady=2)
    buttonNeg = ttk.Button(standardFrame, text="\u00B1", command=lambda: func("neg")).grid(row=1, column=3, sticky="ew", padx=2, pady=2)
    buttonSqrt = ttk.Button(standardFrame, text="\u221A", command=lambda: func("sqrt")).grid(row=1, column=4, sticky="ew", padx=2, pady=2)
    buttonDiv = ttk.Button(standardFrame, text="/", command=lambda: operate("/")).grid(row=2, column=3, sticky="ew", padx=2, pady=2)
    buttonPer = ttk.Button(standardFrame, text="%", command=lambda: func("per")).grid(row=2, column=4, sticky="ew", padx=2, pady=2)
    buttonMul = ttk.Button(standardFrame, text="*", command=lambda: operate("*")).grid(row=3, column=3, sticky="ew", padx=2, pady=2)
    buttonRec = ttk.Button(standardFrame, text="1/x", command=lambda: func("rec")).grid(row=3, column=4, sticky="ew", padx=2, pady=2)
    buttonSub = ttk.Button(standardFrame, text="-", command=lambda: operate("-")).grid(row=4, column=3, sticky="ew", padx=2, pady=2)
    buttonAdd = ttk.Button(standardFrame, text="+", command=lambda: operate("+")).grid(row=5, column=3, sticky="ew", padx=2, pady=2)
    buttonEval = ttk.Button(standardFrame, text="=", command=evaluate).grid(row=4, column=4, rowspan=2, sticky="nsew", padx=2, pady=2)

    button7 = create_num_button(7, 2, 0)
    button8 = create_num_button(8, 2, 1)
    button9 = create_num_button(9, 2, 2)
    button4 = create_num_button(4, 3, 0)
    button5 = create_num_button(5, 3, 1)
    button6 = create_num_button(6, 3, 2)
    button1 = create_num_button(1, 4, 0)
    button2 = create_num_button(2, 4, 1)
    button3 = create_num_button(3, 4, 2)

    button0 = ttk.Button(standardFrame, text="0", relief="groove", bg="#ffffff", command=lambda: press(0)).grid(row=5, column=0, columnspan=2, sticky="ew", padx=2, pady=2)

    buttonDec = ttk.Button(standardFrame, text=".", relief="groove", bg="#ffffff", command=lambda: press(".")).grid(row=5, column=2, sticky="ew", padx=2, pady=2)

    functionFrame = ttk.Frame(calculator, borderwidth=1, bg="#acd8db")
    functionFrame.grid(row=2, column=0, columnspan=5)

    # Todo: Rewrite all these statements with a loop

    buttonNull = ttk.Button(functionFrame, text="", state="disabled", relief="groove", bg="#acd8db").grid(row=0, column=0, sticky="ew", padx=2, pady=2)
    buttonInv = ttk.Button(functionFrame, text="Inv").grid(row=0, column=1, sticky="ew", padx=2, pady=2)
    buttonLn = ttk.Button(functionFrame, text="ln", command=lambda: func("ln")).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
    buttonBraL = ttk.Button(functionFrame, text="(", command=lambda: operate("(")).grid(row=0, column=3, sticky="ew", padx=2, pady=2)
    buttonBraR = ttk.Button(functionFrame, text=")", command=lambda: operate(")")).grid(row=0, column=4, sticky="ew", padx=2, pady=2)
    buttonInt = ttk.Button(functionFrame, text="Int").grid(row=1, column=0, sticky="ew", padx=2, pady=2)
    buttonSinh = ttk.Button(functionFrame, text="sinh", command=lambda: func("sinh")).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
    buttonSin = ttk.Button(functionFrame, text="sin", command=lambda: func("sin")).grid(row=1, column=2, sticky="ew", padx=2, pady=2)
    buttonSqr = ttk.Button(functionFrame, text="x\u00B2", command=lambda: func("sqr")).grid(row=1, column=3, sticky="ew", padx=2, pady=2)
    buttonFact = ttk.Button(functionFrame, text="n!", command=lambda: func("fact")).grid(row=1, column=4, sticky="ew", padx=2, pady=2)
    buttonDms = ttk.Button(functionFrame, text="dms").grid(row=2, column=0, sticky="ew", padx=2, pady=2)
    buttonCosh = ttk.Button(functionFrame, text="cosh", command=lambda: func("cosh")).grid(row=2, column=1, sticky="ew", padx=2, pady=2)
    buttonCos = ttk.Button(functionFrame, text="cos", command=lambda: func("cos")).grid(row=2, column=2, sticky="ew", padx=2, pady=2)
    buttonPow = ttk.Button(functionFrame, text="x\u02B8", command=lambda: operate("^")).grid(row=2, column=3, sticky="ew", padx=2, pady=2)
    buttonRoot = ttk.Button(functionFrame, text="y\u221Ax", command=lambda: operate("root")).grid(row=2, column=4, sticky="ew", padx=2, pady=2)
    buttonPi = ttk.Button(functionFrame, text="\u03C0", command=lambda: func("pi")).grid(row=3, column=0, sticky="ew", padx=2, pady=2)
    buttonTanh = ttk.Button(functionFrame, text="tanh", command=lambda: func("tanh")).grid(row=3, column=1, sticky="ew", padx=2, pady=2)
    buttonTan = ttk.Button(functionFrame, text="tan", command=lambda: func("tan")).grid(row=3, column=2, sticky="ew", padx=2, pady=2)
    buttonCube = ttk.Button(functionFrame, text="x\u00B3", command=lambda: func("cube")).grid(row=3, column=3, sticky="ew", padx=2, pady=2)
    buttonCrt = ttk.Button(functionFrame, text="\u00B3\u221Ax", command=lambda: func("crt")).grid(row=3, column=4, sticky="ew", padx=2, pady=2)
    buttonFE = ttk.Button(functionFrame, text="F-E", command=lambda: acc.set(Format(acc.get()).exp_format())).grid(row=4, column=0, sticky="ew", padx=2, pady=2)
    buttonExp = ttk.Button(functionFrame, text="Exp", command=exponential).grid(row=4, column=1, sticky="ew", padx=2, pady=2)
    buttonMod = ttk.Button(functionFrame, text="Mod", command=lambda: operate("mod")).grid(row=4, column=2, sticky="ew", padx=2, pady=2)
    buttonLog = ttk.Button(functionFrame, text="log", command=lambda: func("log")).grid(row=4, column=3, sticky="ew", padx=2, pady=2)
    buttonALog = ttk.Button(functionFrame, text="10\u02E3", command=lambda: func("alog")).grid(row=4, column=4, sticky="ew", padx=2, pady=2)

    calculator.mainloop()
