#Getting the partial differential of a given function using Sympy

from sympy import symbols, sin, cos, diff, pi
from numpy import sqrt

#Initializing the variables
x, y = symbols('x y',real=True)

#The formula
f = x*(y**2) * (sin(pi * x) +cos(2 * pi * y))

#Partial differential wrt to each variable
result_x = diff(f,x)
result_y = diff(f,y)

#Plugging in the values
result_x = result_x.subs({x:1,y:1})
result_y = result_y.subs({x:1,y:1})

#Converting value to float and printing the values
result_x = float(result_x)
result_y = float(result_y)
print(result_x)
print(result_y)

#Getting the scalar magnitude
scalar = sqrt((result_x**2) + (result_y**2))
print(scalar)