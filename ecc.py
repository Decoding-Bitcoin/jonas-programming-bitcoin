from unittest import TestCase


# tag::source1[]
class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:  # <1>
            error = 'Num {} not in field range 0 to {}'.format(
                num, prime - 1)
            raise ValueError(error)
        self.num = num  # <2>
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime  # <3>
    # end::source1[]

    def __ne__(self, other):
        if other is None:
            return False
        return self.num != other.num or self.prime != other.prime

    # tag::source2[]
    def __add__(self, other):
        if self.prime != other.prime:  # <1>
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + other.num) % self.prime  # <2>
        return self.__class__(num, self.prime)  # <3>
    # end::source2[]

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different Fields')
        num = (self.num - other.num) % self.prime  # <2>
        return self.__class__(num, self.prime)  # <3>

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        num = (self.num * other.num) % self.prime  # <2>
        return self.__class__(num, self.prime)  # <3>

    # tag::source3[]
    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)  # <1>
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)
    # end::source3[]

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        num = (self.num * pow(other.num, self.prime-2, self.prime)) % self.prime
        return self.__class__(num, self.prime)

class Point:

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        # end::source1[]
        # tag::source2[]
        if self.x is None and self.y is None:  # <1>
            return
        # end::source2[]
        # tag::source1[]
        if self.y**2 != self.x**3 + a * x + b:  # <1>
            raise ValueError('({}, {}) is not on the curve'.format(x, y))

    def __eq__(self, other):  # <2>
        return self.x == other.x and self.y == other.y \
            and self.a == other.a and self.b == other.b
    # end::source1[]

    def __ne__(self, other):
        # this should be the inverse of the == operator
        return not(self.x == other.x and self.y == other.y \
            and self.a == other.a and self.b == other.b)

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)

    # tag::source3[]
    def __add__(self, other):  # <2>
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format
            (self, other))

        if self.x is None:  # <3>
            return other
        if other.x is None:  # <4>
            return self
        # end::source3[]
        if self.x == other.x and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)
             
        # Case 1: self.x == other.x, self.y != other.y
        # Result is point at infinity
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        
        # Case 2: self.x ≠ other.x
        # Formula (x3,y3)==(x1,y1)+(x2,y2)
        # s=(y2-y1)/(x2-x1)
        # x3=s**2-x1-x2
        # y3=s*(x1-x3)-y1
        if self.x != other.x:
            s = (other.y - self.y)/(other.x - self.x)
            x3 = s**2-self.x-other.x
            y3 = s*(self.x-x3)-self.y
            return self.__class__(x3, y3, self.a, self.b)
        
        # Case 3: self == other
        # Formula (x3,y3)=(x1,y1)+(x1,y1)
        # s=(3*x1**2+a)/(2*y1)
        # x3=s**2-2*x1
        # y3=s*(x1-x3)-y1
        if self.x == other.x:
            s = (3*self.x**2+self.a)/(2*self.y)
            x3 = s**2-2*self.x
            y3 = s*(self.x-x3)-self.y
            return self.__class__(x3, y3, self.a, self.b)