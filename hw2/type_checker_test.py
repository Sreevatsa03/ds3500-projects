from type_checker import TypeChecker

import math


@TypeChecker.check
def add(x: int, y: int) -> int:
    return x+y


print(add(2,'3')) # This should raise an exception!



