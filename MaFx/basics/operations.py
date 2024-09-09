
def root(x:int|float, n:int) -> int|float:
    """
    Returns the n-th root of x
    """
    ans =  x**(1/n)
    if ans%1 == 0:
        return int(ans)
    return ans
    
    
def sqrt(x:int|float) -> int|float:
    """
    Returns the square root of x"""
    return root(x, 2)

def cbrt(x:int|float) -> int|float:
    """
    Returns the cube root of x"""
    
    return root(x, 3)

def square(x:int|float) -> int|float:
    """
    Returns the square of x"""
    
    return x**2

def cube(x:int|float) -> int|float:
    """
    Returns the cube of x"""
    
    return x**3

def power(x:int|float, n:int) -> int|float:
    """
    Returns x raised to the power of n"""
    return x**n

def factorial(n:int) -> int:
    """
    Returns the factorial of n"""
    
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)
    
def inverse(x:int|float) -> int|float:
    """
    Returns the inverse of x
    """
    return 1/x

def absolute(x:int|float) -> int|float:
    """
    Returns the absolute value of x
    """
    return abs(x)

def increment_decimal(x:int|float) -> int:
    """
    Returns the next integer of x if x is a float else returns x
    """
    if x%1 == 0:
        return x
    else:
        str_x = str(x)
        int_part = int(str_x.split('.')[0])
        int_part += 1
        return int_part
    
def decrement_decimal(x:int|float) -> int:
    """
    Returns the previous integer of x if x is a float else returns x
    """
    if x%1 == 0:
        return x
    else:
        str_x = str(x)
        int_part = int(str_x.split('.')[0])
        return int_part
