# -b+- sqrt(b**2-4ac)/2a
import cmath

a = 1
b = 5
c = 6
d = (b ** 2) - (4 * a * c)

eq1 = (-b + cmath.sqrt(d)) / (2 * a)

eq2 = (-b - cmath.sqrt(d)) / (2 * a)

print(eq1)
print(eq2)
