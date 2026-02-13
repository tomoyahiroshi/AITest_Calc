import tkinter as tk
from tkinter import ttk


class CalculatorEngine:
    def __init__(self) -> None:
        self.expression = ""
        self.display = "0"
        self.error_state = False

    def _reset_on_error_if_needed(self, value: str) -> None:
        if self.error_state and (value.isdigit() or value == "."):
            self.all_clear()

    def input_digit_or_dot(self, value: str) -> None:
        self._reset_on_error_if_needed(value)
        if value == ".":
            token = self._current_token()
            if "." in token:
                return
            if token == "":
                self.expression += "0"
        self.expression += value
        self.display = self._current_token() or "0"

    def input_operator(self, op: str) -> None:
        if self.error_state:
            return
        if not self.expression:
            if self.display and self.display != "0":
                self.expression = self.display
            else:
                return
        if self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op

    def toggle_sign(self) -> None:
        if self.error_state:
            return
        token = self._current_token()
        if token == "":
            self.expression += "-"
            return

        start = self._current_token_start_index()
        if token.startswith("-"):
            self.expression = self.expression[:start] + token[1:]
        else:
            self.expression = self.expression[:start] + "-" + token
        self.display = self._current_token() or "0"

    def backspace(self) -> None:
        if self.error_state:
            self.all_clear()
            return
        if not self.expression:
            return
        self.expression = self.expression[:-1]
        self.display = self._current_token() or "0"

    def clear_entry(self) -> None:
        if self.error_state:
            self.all_clear()
            return
        if not self.expression:
            self.display = "0"
            return
        idx = self._current_token_start_index()
        self.expression = self.expression[:idx]
        self.display = "0"

    def all_clear(self) -> None:
        self.expression = ""
        self.display = "0"
        self.error_state = False

    def evaluate(self) -> None:
        if self.error_state:
            return
        if not self.expression:
            return
        expr = self.expression
        if expr[-1] in "+-*/":
            expr = expr[:-1]
        if not expr:
            return
        try:
            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display = str(result)
            self.expression = str(result)
        except ZeroDivisionError:
            self.display = "Error: Division by zero"
            self.expression = ""
            self.error_state = True
        except Exception:
            self.display = "Error"
            self.expression = ""
            self.error_state = True

    def expression_for_display(self) -> str:
        return self.expression.replace("*", "×").replace("/", "÷")

    def _current_token_start_index(self) -> int:
        i = len(self.expression) - 1
        while i >= 0 and self.expression[i] not in "+*/":
            if self.expression[i] == "-":
                if i == 0 or self.expression[i - 1] in "+-*/":
                    i -= 1
                    continue
                break
            i -= 1
        return i + 1

    def _current_token(self) -> str:
        if not self.expression:
            return ""
        return self.expression[self._current_token_start_index():]


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.minsize(280, 360)

        self.engine = CalculatorEngine()

        self.expr_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        self._build_ui()
        self._bind_keys()

    def _build_ui(self) -> None:
        main = ttk.Frame(self, padding=8)
        main.grid(sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        display = ttk.Frame(main)
        display.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        display.columnconfigure(0, weight=1)

        ttk.Label(display, textvariable=self.expr_var, anchor="e", font=("Arial", 12)).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Label(display, textvariable=self.result_var, anchor="e", font=("Arial", 24, "bold")).grid(
            row=1, column=0, sticky="ew"
        )

        buttons = [
            ["AC", "C", "⌫", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]

        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=1, column=0, sticky="nsew")
        main.rowconfigure(1, weight=1)
        main.columnconfigure(0, weight=1)

        for r in range(5):
            btn_frame.rowconfigure(r, weight=1)
        for c in range(4):
            btn_frame.columnconfigure(c, weight=1)

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                button = tk.Button(
                    btn_frame,
                    text=label,
                    font=("Arial", 14),
                    relief="raised",
                    bg="#f7d9a8" if label in {"÷", "×", "-", "+"} else "#f5f5f5",
                    activebackground="#ffd28a" if label in {"÷", "×", "-", "+", "="} else "#e8e8e8",
                )
                if label == "=":
                    button.configure(bg="#ffad42", fg="white", activebackground="#ff970f")
                button.configure(command=lambda v=label: self._handle_button(v))
                button.grid(row=r, column=c, sticky="nsew", padx=2, pady=2, ipadx=4, ipady=10)

    def _bind_keys(self) -> None:
        for key in "0123456789":
            self.bind(key, lambda event, v=key: self._handle_button(v))
        for key in ["+", "-", "*", "/", "."]:
            self.bind(key, lambda event, v=key: self._handle_key_operator(v))
        self.bind("<Return>", lambda event: self._handle_button("="))
        self.bind("<KP_Enter>", lambda event: self._handle_button("="))
        self.bind("<BackSpace>", lambda event: self._handle_button("⌫"))
        self.bind("<Escape>", lambda event: self._handle_button("AC"))

    def _handle_key_operator(self, key: str) -> None:
        mapping = {"*": "×", "/": "÷", "+": "+", "-": "-"}
        self._handle_button(mapping.get(key, key))

    def _handle_button(self, label: str) -> None:
        if label.isdigit() or label == ".":
            self.engine.input_digit_or_dot(label)
        elif label in {"+", "-", "×", "÷"}:
            mapping = {"×": "*", "÷": "/", "+": "+", "-": "-"}
            self.engine.input_operator(mapping[label])
        elif label == "+/-":
            self.engine.toggle_sign()
        elif label == "⌫":
            self.engine.backspace()
        elif label == "C":
            self.engine.clear_entry()
        elif label == "AC":
            self.engine.all_clear()
        elif label == "=":
            self.engine.evaluate()

        self.expr_var.set(self.engine.expression_for_display())
        self.result_var.set(self.engine.display)


def main() -> None:
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
