from enum import StrEnum
from operator import add, sub, mul, truediv
from typing import Literal

Op = Literal["+", "-", "*", "/"]

class OpsEnum(StrEnum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class Calculator:
    """
    Пример сложной команды, реализация которой требует создания класса.

    Непосредственно команда Typer выступает в роли запускалки
    """
    ops = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": truediv,
    }

    def __init__(self, num1: int, num2: int, op: OpsEnum):
        self.num1 = num1
        self.num2 = num2
        self.op = op

    def calculate(self):
        op = self.ops[self.op]
        return op(self.num1, self.num2)
