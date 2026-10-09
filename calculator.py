import tkinter as tk
import ast
import math
import operator

# Create the window
window = tk.Tk()
window.title("Calculator")
window.geometry("420x600")
window.configure(bg="#17191f")

# Calculator display
expression = tk.StringVar()

display = tk.Entry(
    window,
    textvariable=expression,
    font=("Arial", 26),
    justify="right",
    bg="#252832",
    fg="white",
    insertbackground="white",
    insertwidth=0,
    relief="flat"
)
display.grid(row=0, column=0, columnspan=4, padx=12, pady=16, ipady=15)

# Operations allowed in calculations
operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow
}

superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
normal_digits = "0123456789"


def calculate_expression(text):
    text = text.replace("×", "*").replace("÷", "/")
    text = text.replace("√(", "sqrt(")
    text = text.replace("²", "**2")

    # Convert superscript digits into a power
    for digit, normal in zip(superscripts, normal_digits):
        text = text.replace(digit, "**" + normal)

    text = text.replace("^", "**")

    tree = ast.parse(text, mode="eval")

    def solve(node):
        if isinstance(node, ast.Expression):
            return solve(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = solve(node.left)
            right = solve(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent too large")

            return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -solve(node.operand)
            if isinstance(node.op, ast.UAdd):
                return solve(node.operand)

        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "sqrt"
                and len(node.args) == 1
                and not node.keywords
            ):
                return math.sqrt(solve(node.args[0]))

        raise ValueError("Invalid calculation")

    result = solve(tree)

    if isinstance(result, complex) or not math.isfinite(float(result)):
        raise ValueError("Invalid result")

    return result


def add_to_display(value):
    text = expression.get()

    # Clear an old error before starting again
    if text in ("Cannot divide by zero!", "Error"):
        expression.set("")
        text = ""

    # Operators that can be replaced by another operator
    operators = ("+", "-", "×", "÷", "^")

    # If the display is empty, start with zero
    if text == "":
        if value in operators or value == "²":
            expression.set("0" + value)
        else:
            expression.set(value)

        display.icursor(tk.END)
        display.focus_set()
        return

    # Replace the last operator instead of adding another
    if value in operators and text[-1] in operators:
        expression.set(text[:-1] + value)
        display.icursor(tk.END)
        display.focus_set()
        return

    # Show exponent digits as superscripts
    if value.isdigit() and text.endswith("^"):
        expression.set(text[:-1] + superscripts[int(value)])
        display.icursor(tk.END)
        display.focus_set()
        return

    # Add the new character
    display.insert(tk.INSERT, value)
    display.icursor(tk.END)
    display.focus_set()


def clear():
    expression.set("")
    display.focus_set()


def delete():
    text = expression.get()

    if text in ("Cannot divide by zero!", "Error"):
        expression.set("")
        return

    pos = display.index(tk.INSERT)

    if pos > 0:
        expression.set(text[:pos - 1] + text[pos:])
        display.icursor(pos - 1)


def calculate():
    try:
        text = expression.get()

        # Support ordinary superscript square notation
        result = calculate_expression(text)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        expression.set(str(result))

    except ZeroDivisionError:
        expression.set("Cannot divide by zero!")

    except (ValueError, SyntaxError, TypeError, OverflowError):
        expression.set("Error")

    display.icursor(tk.END)


# Button layout
buttons = [
    ("C", clear, "#a33b43"),
    ("⌫", delete, "#3b414d"),
    ("(", lambda: add_to_display("("), "#3b414d"),
    (")", lambda: add_to_display(")"), "#3b414d"),

    ("7", lambda: add_to_display("7"), "#303541"),
    ("8", lambda: add_to_display("8"), "#303541"),
    ("9", lambda: add_to_display("9"), "#303541"),
    ("÷", lambda: add_to_display("÷"), "#46536b"),

    ("4", lambda: add_to_display("4"), "#303541"),
    ("5", lambda: add_to_display("5"), "#303541"),
    ("6", lambda: add_to_display("6"), "#303541"),
    ("×", lambda: add_to_display("×"), "#46536b"),

    ("1", lambda: add_to_display("1"), "#303541"),
    ("2", lambda: add_to_display("2"), "#303541"),
    ("3", lambda: add_to_display("3"), "#303541"),
    ("-", lambda: add_to_display("-"), "#46536b"),

    ("0", lambda: add_to_display("0"), "#303541"),
    (".", lambda: add_to_display("."), "#303541"),
    ("x²", lambda: add_to_display("²"), "#3b414d"),
    ("+", lambda: add_to_display("+"), "#46536b"),

    ("√", lambda: add_to_display("√("), "#3b414d"),
    ("xⁿ", lambda: add_to_display("^"), "#3b414d"),
    ("=", calculate, "#238636")
]

for i, (text, command, color) in enumerate(buttons):
    row = i // 4 + 1
    col = i % 4

    button = tk.Button(
        window,
        text=text,
        command=command,
        font=("Arial", 17, "bold"),
        bg=color,
        fg="white",
        activebackground="#626b7c",
        activeforeground="white",
        relief="flat",
        cursor="hand2"
    )

    button.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=4,
        pady=4,
        ipady=8
    )

for col in range(4):
    window.grid_columnconfigure(col, weight=1)

for row in range(1, 7):
    window.grid_rowconfigure(row, weight=1)
    
display = tk.Entry(
    window,
    textvariable=expression,
    font=("Arial", 26),
    justify="right",
    bg="#252832",
    fg="white",
    insertbackground="white",
    insertwidth=0,
    relief="flat"
)

# Keyboard shortcuts
window.bind("<Return>", lambda event: calculate())
window.bind("<Escape>", lambda event: clear())
window.bind("<BackSpace>", lambda event: delete())

window.mainloop()
