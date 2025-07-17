from typing import Annotated

from fastapi.params import Depends

from shared import repositories

UsersRepository = Annotated[repositories.UsersRepository, Depends()]
