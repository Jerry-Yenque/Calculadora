import tkinter as ttk
import tkinter
import math


new_operand = False
brackets = 0
expression = ""
memory = ""
inverted = False

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


def arc_angle_value(value):
    if degreeUnit.get() == 0:
        # converts radians to degrees
        return math.degrees(value)

    elif degreeUnit.get() == 1:
        # leaves value as radians
        return value

    else:
        # converts radians to grad
        return value * 63.662


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
                if val != ".":
                    if abs(float(acc.get() + str(val))) >= 1:
                        acc.set((acc.get() + str(val)).lstrip("0"))
                    else:
                        acc.set(acc.get() + str(val))

        else:
            acc.set(val)
            if expression:
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


def invert():
    global inverted

    if buttonInv.config("relief")[-1] == "raised" and inverted is False:
        buttonInv.config(relief="sunken")
        inverted = True

    else:
        buttonInv.config(relief="raised")
        inverted = False

    if inverted:
        buttonLn.config(text="e\u02E3")
        buttonInt.config(text="Frac")
        buttonSinh.config(text="sinh\u207B\u00B9")
        buttonSin.config(text="sin\u207B\u00B9")
        buttonDms.config(text="deg")
        buttonCosh.config(text="cosh\u207B\u00B9")
        buttonCos.config(text="cos\u207B\u00B9")
        buttonPi.config(text="2*\u03C0")
        buttonTanh.config(text="tanh\u207B\u00B9")
        buttonTan.config(text="tan\u207B\u00B9")
    else:
        buttonLn.config(text="ln")
        buttonInt.config(text="Int")
        buttonSinh.config(text="sinh")
        buttonSin.config(text="sin")
        buttonDms.config(text="dms")
        buttonCosh.config(text="cosh")
        buttonCos.config(text="cos")
        buttonPi.config(text="\u03C0")
        buttonTanh.config(text="tanh")
        buttonTan.config(text="tan")


def mod_memory(action):
    global memory

    if action == "clear":
        memory = ""

    elif action == "recall":
        if memory:
            acc.set(memory)

    elif action == "save":
        memory = acc.get()

    elif action == "add":
        if memory:
            memory = str(eval(memory) + eval(acc.get()))
        else:
            memory = acc.get()

    elif action == "sub":
        if memory:
            memory = str(eval(memory) - eval(acc.get()))
        else:
            memory = "-" + acc.get()


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
        if not inverted:
            try:
                expressionDisplay.set(expressionDisplay.get() + f"ln({value})")
                acc.set(round(math.log(value), 10))
            except ValueError:
                acc.set("Math Error")
        else:
            expressionDisplay.set(expressionDisplay.get() + f"powe({value})")
            acc.set(round(math.pow(math.e, value), 10))
        new_operand = True

    elif function == "sinh":
        if not inverted:
            expressionDisplay.set(expressionDisplay.get() + f"sinh({value})")
            acc.set(round(math.sinh(angle_value(value)), 10))
        else:
            expressionDisplay.set(expressionDisplay.get() + f"asinh({value})")
            acc.set(round(math.asinh(value), 10))
        new_operand = True

    elif function == "sin":
        if not inverted:
            expressionDisplay.set(expressionDisplay.get() + f"sin({value})")
            acc.set(round(math.sin(angle_value(value)), 10))
        else:
            expressionDisplay.set(expressionDisplay.get() + f"asin({value})")
            acc.set(round(arc_angle_value(math.asin(value)), 10))
        new_operand = True

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
        if not inverted:
            expressionDisplay.set(expressionDisplay.get() + f"cosh({value})")
            acc.set(round(math.cosh(angle_value(value)), 10))
        else:
            expressionDisplay.set(expressionDisplay.get() + f"acosh({value})")
            acc.set(round(math.acosh(value), 10))
        new_operand = True

    elif function == "cos":
        if not inverted:
            expressionDisplay.set(expressionDisplay.get() + f"cos({value})")
            acc.set(round(math.cos(angle_value(value)), 10))
        else:
            expressionDisplay.set(expressionDisplay.get() + f"acos({value})")
            acc.set(round(arc_angle_value(math.acos(value)), 10))
        new_operand = True

    elif function == "pi":
        if not inverted:
            acc.set(round(math.pi, 10))
        else:
            acc.set(round(math.pi * 2, 10))

    elif function == "tanh":
        if not inverted:
            expressionDisplay.set(expressionDisplay.get() + f"tanh({value})")
            acc.set(round(math.tanh(angle_value(value)), 10))
        else:
            expressionDisplay.set(expressionDisplay.get() + f"atanh({value})")
            acc.set(round(math.atanh(value), 10))
        new_operand = True

    elif function == "tan":
        if not inverted:
            expressionDisplay.set(expressionDisplay.get() + f"tanh({value})")
            acc.set(round(math.tan(angle_value(value)), 10))
        else:
            expressionDisplay.set(expressionDisplay.get() + f"atan({value})")
            acc.set(round(arc_angle_value(math.atan(value)), 10))
        new_operand = True

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

    elif function == "dms":
        if not inverted:
            degree, ms = int(value // 1), value % 1
            minutes, seconds = int((ms * 60) // 1), ((ms * 60) % 1) * 60
            new_val = f"{degree}.{minutes}" + str(seconds).replace(".", "")
            expressionDisplay.set(expressionDisplay.get() + f"dms({value})")
            acc.set(round(eval(new_val), 10))
        else:
            degree, ms = int(value // 1), value % 1
            minutes, seconds = ((ms // 0.01) / 60), (((ms % 0.01) * 1000) / 3600)
            new_val = degree + minutes + seconds
            expressionDisplay.set(expressionDisplay.get() + f"degrees({value})")
            acc.set(round(new_val), 10)
        new_operand = True

    elif function == "int":
        expressionDisplay.set(expressionDisplay.get() + f"Int({value})")
        new_operand = True
        acc.set(int(value))


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
    standardFrame.grid(row=1, column=6, rowspan=6, padx=(0, 3), pady=(0, 5))

    buttonMC = ttk.Button(standardFrame, text="MC", command=lambda: mod_memory("clear")).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
    buttonMR = ttk.Button(standardFrame, text="MR", command=lambda: mod_memory("recall")).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
    buttonMS = ttk.Button(standardFrame, text="MS", command=lambda: mod_memory("save")).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
    buttonMp = ttk.Button(standardFrame, text="M+", command=lambda: mod_memory("add")).grid(row=0, column=3, sticky="ew", padx=2, pady=2)
    buttonMm = ttk.Button(standardFrame, text="M-", command=lambda: mod_memory("sub")).grid(row=0, column=4, sticky="ew", padx=2, pady=2)
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

    buttonNull = ttk.Button(functionFrame, text="", state="disabled", relief="groove", bg="#acd8db").grid(row=0, column=0, sticky="ew", padx=2, pady=2)
    buttonInv = ttk.Button(functionFrame, text="Inv", command=invert)
    buttonInv.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
    buttonLn = ttk.Button(functionFrame, text="ln", command=lambda: func("ln"))
    buttonLn.grid(row=0, column=2, sticky="ew", padx=2, pady=2)
    buttonBraL = ttk.Button(functionFrame, text="(", command=lambda: operate("(")).grid(row=0, column=3, sticky="ew", padx=2, pady=2)
    buttonBraR = ttk.Button(functionFrame, text=")", command=lambda: operate(")")).grid(row=0, column=4, sticky="ew", padx=2, pady=2)
    buttonInt = ttk.Button(functionFrame, text="Int", command=lambda: func("int"))
    buttonInt.grid(row=1, column=0, sticky="ew", padx=2, pady=2)
    buttonSinh = ttk.Button(functionFrame, text="sinh", command=lambda: func("sinh"))
    buttonSinh.grid(row=1, column=1, sticky="ew", padx=2, pady=2)
    buttonSin = ttk.Button(functionFrame, text="sin", command=lambda: func("sin"))
    buttonSin.grid(row=1, column=2, sticky="ew", padx=2, pady=2)
    buttonSqr = ttk.Button(functionFrame, text="x\u00B2", command=lambda: func("sqr")).grid(row=1, column=3, sticky="ew", padx=2, pady=2)
    buttonFact = ttk.Button(functionFrame, text="n!", command=lambda: func("fact")).grid(row=1, column=4, sticky="ew", padx=2, pady=2)
    buttonDms = ttk.Button(functionFrame, text="dms", command=lambda: func("dms"))
    buttonDms.grid(row=2, column=0, sticky="ew", padx=2, pady=2)
    buttonCosh = ttk.Button(functionFrame, text="cosh", command=lambda: func("cosh"))
    buttonCosh.grid(row=2, column=1, sticky="ew", padx=2, pady=2)
    buttonCos = ttk.Button(functionFrame, text="cos", command=lambda: func("cos"))
    buttonCos.grid(row=2, column=2, sticky="ew", padx=2, pady=2)
    buttonPow = ttk.Button(functionFrame, text="x\u02B8", command=lambda: operate("^")).grid(row=2, column=3, sticky="ew", padx=2, pady=2)
    buttonRoot = ttk.Button(functionFrame, text="y\u221Ax", command=lambda: operate("root")).grid(row=2, column=4, sticky="ew", padx=2, pady=2)
    buttonPi = ttk.Button(functionFrame, text="\u03C0", command=lambda: func("pi"))
    buttonPi.grid(row=3, column=0, sticky="ew", padx=2, pady=2)
    buttonTanh = ttk.Button(functionFrame, text="tanh", command=lambda: func("tanh"))
    buttonTanh.grid(row=3, column=1, sticky="ew", padx=2, pady=2)
    buttonTan = ttk.Button(functionFrame, text="tan", command=lambda: func("tan"))
    buttonTan.grid(row=3, column=2, sticky="ew", padx=2, pady=2)
    buttonCube = ttk.Button(functionFrame, text="x\u00B3", command=lambda: func("cube")).grid(row=3, column=3, sticky="ew", padx=2, pady=2)
    buttonCrt = ttk.Button(functionFrame, text="\u00B3\u221Ax", command=lambda: func("crt")).grid(row=3, column=4, sticky="ew", padx=2, pady=2)
    buttonFE = ttk.Button(functionFrame, text="F-E", command=lambda: acc.set(Format(acc.get()).exp_format())).grid(row=4, column=0, sticky="ew", padx=2, pady=2)
    buttonExp = ttk.Button(functionFrame, text="Exp", command=exponential).grid(row=4, column=1, sticky="ew", padx=2, pady=2)
    buttonMod = ttk.Button(functionFrame, text="Mod", command=lambda: operate("mod")).grid(row=4, column=2, sticky="ew", padx=2, pady=2)
    buttonLog = ttk.Button(functionFrame, text="log", command=lambda: func("log")).grid(row=4, column=3, sticky="ew", padx=2, pady=2)
    buttonALog = ttk.Button(functionFrame, text="10\u02E3", command=lambda: func("alog")).grid(row=4, column=4, sticky="ew", padx=2, pady=2)

    calculator.mainloop()
