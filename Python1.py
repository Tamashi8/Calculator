# Made by: Andrew Lam
# Date: 6/30/2018

import tkinter as tk
import tkinter.messagebox
from re import findall

# Creating the window
window = tk.Tk()
window.title("Calculator")
window.resizable(False, False)
frame = tk.Frame(window)

# Creating the entry box
input = ""
entry = tk.StringVar()
textbox = tk.Label(window, font=('lucida console', 25), textvariable=entry, bd=10, bg="gainsboro", justify='right', relief="flat", height=2, width=3, anchor="e")

# Button Utility functions
def applyToEntry(key):
    global input
    input = input + key
    entry.set(input)

def getLastNumber():
    global input
    return findall("[0-9]+\.?[0-9]*", input)[-1]        #[-]?[0-9]+\.?[0-9]*

def openParenthesesExist():
    global input
    if input.count('(') > input.count(')'):
        return True
    else:
        return False
    
# Defining button functions
def click(key, event=None):
    global input
    if len(input) == 0 or not input[-1].isdigit() and input[-1] != ')':
        applyToEntry(str(key))
    elif input[-1] == ')' and str(key).isdigit():
        input = input + "*" + str(key)
        entry.set(input)
    else:
        number = getLastNumber()
        if number[0] != '0':
            applyToEntry(str(key))
        elif number.find('.') != -1:
            applyToEntry(str(key))

def zeroClick(event=None):
    global input
    if len(input) == 0:
        click('0')
    else:
        number = getLastNumber()
        if number.find('.') != -1:
            click('0')
        elif number[0] != '0':
            click('0')

def decimalClick(event=None):
    global input
    if len(input) == 0:
        applyToEntry("0.")
    elif input[-1] == ')':
        applyToEntry("*0.")
    elif not input[-1].isdigit() and input[-1] != '.':
        applyToEntry("0.")
    else:
        number = getLastNumber()
        if number.find('.') == -1:
            applyToEntry(".")
    
def operationClick(op, event=None):
    global input
    try:
        last = input[-1]
        if len(input) > 0:
            if last.isdigit() or last == ')' or last == '.':
                applyToEntry(str(op))
    except:
        pass

def parentheses(event=None):
    global input
    if len(input) == 0 or any(x in "(*/+-" for x in input[-1]):
        applyToEntry("(")
    elif (input[-1] == ')' or input[-1].isdigit()) and openParenthesesExist():
        applyToEntry(")")
    elif not any(x in "+-" for x in input[-1]):
        applyToEntry("*(")

def sign():
    global input
    if len(input) > 0 and (input[-1].isdigit() or input[-1] == '.'):
        num = findall("[-]?[0-9]+\.?[0-9]*", input)[-1]
        sign = ""
        if len(num) == len(input):
            sign = str(eval(num + "*-1"))
            if sign == "-0.0" or sign == "0.0":
                sign = sign[:-1]
            input = sign
        elif num[0] == '-' and not any(x in "+-*/()" for x in input[-len(num)-1]):
            sign = str(eval(num[1:] + "*-1"))
            if sign == "-0.0" or sign == "0.0":
                sign = sign[:-1]
            input = input[:-len(num[1:])] + sign
        else:
            sign = str(eval(num + "*-1"))
            if sign == "-0.0" or sign == "0.0":
                sign = sign[:-1]
            input = input[:-len(num)] + sign
        entry.set(input)

def deleteClick(event=None):
    global input
    input = input[:-1]
    entry.set(input)

def clear(event=None):
    global input
    input = ""
    entry.set(input)

def equal(event=None):
    global input
    if openParenthesesExist():
        for openPar in range(input.count('(')-input.count(')')):
            applyToEntry(")")
    try:
        input = str(round(eval(input),10))
        entry.set(input)
    except:
        tk.messagebox.showerror("Error", "An error occurred. Check your formatting.")

# Creating the buttons
def createButton(buttonText):
    return tk.Button(window, text=buttonText, font=('lucida console', 15), bd=2, bg="lightgrey", relief="raised", padx=20, pady=10, width=2, command=lambda:click(buttonText, None))

b1 = createButton(1)
b2 = createButton(2)
b3 = createButton(3)
b4 = createButton(4)
b5 = createButton(5)
b6 = createButton(6)
b7 = createButton(7)
b8 = createButton(8)
b9 = createButton(9)
b0 = createButton(0);       b0.configure(command=lambda:zeroClick())
bAdd = createButton("+");   bAdd.configure(command=lambda:operationClick("+"))
bSub = createButton("-");   bSub.configure(command=lambda:operationClick("-"))
bMul = createButton("×");   bMul.configure(command=lambda:operationClick("*"))
bDiv = createButton("÷");   bDiv.configure(command=lambda:operationClick("/"))
bPar = createButton("( )"); bPar.configure(command=lambda:parentheses())
bDel = createButton("DEL"); bDel.configure(command=lambda:deleteClick())
bClear = createButton("C"); bClear.configure(command=lambda:clear())
bEqual = createButton("="); bEqual.configure(command=lambda:equal())
bSign = createButton("+/-"); bSign.configure(command=lambda:sign())
bDot = createButton(".");   bDot.configure(command=lambda:decimalClick())

# Binding keypresses to respective buttons
frame.bind('1', lambda event: click(1, event))
frame.bind('2', lambda event: click(2, event))
frame.bind('3', lambda event: click(3, event))
frame.bind('4', lambda event: click(4, event))
frame.bind('5', lambda event: click(5, event))
frame.bind('6', lambda event: click(6, event))
frame.bind('7', lambda event: click(7, event))
frame.bind('8', lambda event: click(8, event))
frame.bind('9', lambda event: click(9, event))
frame.bind('0', lambda event: zeroClick(event))
frame.bind('+', lambda event: operationClick("+", event))
frame.bind('-', lambda event: operationClick("-", event))
frame.bind('*', lambda event: operationClick("*", event))
frame.bind('/', lambda event: operationClick("/", event))
frame.bind('(', lambda event: parentheses(event))
frame.bind(')', lambda event: parentheses(event))
frame.bind('<BackSpace>', lambda event: deleteClick(event))
frame.bind('<Delete>', lambda event: deleteClick(event))
frame.bind('<Escape>', lambda event: clear(event))
frame.bind('<Return>', lambda event: equal(event))
frame.bind('.', lambda event: decimalClick(event))

# Placement design
textbox.grid(row = 0, columnspan = 4, sticky = "we")
b1.grid(row = 4, column = 0, sticky = "we")
b2.grid(row = 4, column = 1, sticky = "we")
b3.grid(row = 4, column = 2, sticky = "we")
b4.grid(row = 3, column = 0, sticky = "we")
b5.grid(row = 3, column = 1, sticky = "we")
b6.grid(row = 3, column = 2, sticky = "we")
b7.grid(row = 2, column = 0, sticky = "we")
b8.grid(row = 2, column = 1, sticky = "we")
b9.grid(row = 2, column = 2, sticky = "we")
b0.grid(row = 5, column = 1, sticky = "we")
bAdd.grid(row = 4, column = 3, sticky = "we")
bSub.grid(row = 3, column = 3, sticky = "we")
bMul.grid(row = 2, column = 3, sticky = "we")
bDiv.grid(row = 1, column = 3, sticky = "we")
bPar.grid(row = 1, column = 1, sticky = "we")
bDel.grid(row = 1, column = 2, sticky = "we")
bClear.grid(row = 1, column = 0, sticky = "we")
bEqual.grid(row = 5, column = 3, sticky = "we")
bSign.grid(row = 5, column = 0, sticky = "we")
bDot.grid(row = 5, column = 2, sticky = "we")

# Run program
frame.focus_set()
frame.grid(row = 0, column = 0)
window.mainloop()

