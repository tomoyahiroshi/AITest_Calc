import unittest

from calculator import CalculatorEngine


class CalculatorEngineTest(unittest.TestCase):
    def test_basic_operations(self):
        engine = CalculatorEngine()
        for key in ["1", "2"]:
            engine.input_digit_or_dot(key)
        engine.input_operator("+")
        engine.input_digit_or_dot("7")
        engine.input_operator("*")
        engine.input_digit_or_dot("3")
        engine.evaluate()
        self.assertEqual(engine.display, "33")

    def test_division_by_zero_error(self):
        engine = CalculatorEngine()
        engine.input_digit_or_dot("1")
        engine.input_operator("/")
        engine.input_digit_or_dot("0")
        engine.evaluate()
        self.assertEqual(engine.display, "Error: Division by zero")

    def test_error_then_new_input_starts_fresh(self):
        engine = CalculatorEngine()
        engine.input_digit_or_dot("1")
        engine.input_operator("/")
        engine.input_digit_or_dot("0")
        engine.evaluate()
        engine.input_digit_or_dot("9")
        self.assertEqual(engine.expression, "9")
        self.assertEqual(engine.display, "9")

    def test_backspace_and_clear_entry(self):
        engine = CalculatorEngine()
        for key in ["1", "2", "+", "3", "4"]:
            if key in "+-*/":
                engine.input_operator(key)
            else:
                engine.input_digit_or_dot(key)

        engine.backspace()
        self.assertEqual(engine.expression, "12+3")

        engine.clear_entry()
        self.assertEqual(engine.expression, "12+")
        self.assertEqual(engine.display, "0")


if __name__ == "__main__":
    unittest.main()
