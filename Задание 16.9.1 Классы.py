class Rectangle:
    def __init__(self,x, y, width, height ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def __str__(self):
        return f'Rectangle : {self.x}, {self.y}, {self.width}, {self.height}'

    def square(self):
        return self.width * self.height

r1 = Rectangle(5,6,5,5)
print(r1)
print(r1.square())