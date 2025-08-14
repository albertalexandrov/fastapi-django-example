import logging
from typing import Annotated

from typer import Typer, Argument

from management.commands.calculator import OpsEnum, Calculator

typer = Typer(help="Набор команд непосредственно приложения")
logger = logging.getLogger(__name__)


@typer.command()
def calculate(
    num1: Annotated[int, Argument(help="Первое число")],
    num2: Annotated[int, Argument(help="Второе число")],
    op: Annotated[OpsEnum, Argument(help="Операция")],
):
    """
    Калькулятор
    """
    calc = Calculator(num1, num2, op)
    res = calc.calculate()
    logger.warning(f"{num1} {op} {num2} = {res}")
