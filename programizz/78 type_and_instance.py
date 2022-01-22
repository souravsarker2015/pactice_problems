class Polygon:
    def side_no(self):
        pass


class Triangle(Polygon):
    def area(self):
        pass


p1 = Polygon()
t1 = Triangle()

print(type(t1) == Triangle)
print(type(p1) == Triangle)
print(isinstance(p1, Polygon))
print(isinstance(t1, Polygon))

# class Polygon:
#     def sides_no(self):
#         pass
# class Triangle(Polygon):
#     def area(self):
#         pass
# obj_polygon = Polygon()
# obj_triangle = Triangle()
# print(type(obj_triangle) == Triangle)  # true
# print(type(obj_triangle) == Polygon)  # false
# print(isinstance(obj_polygon, Polygon))  # true
# print(isinstance(obj_triangle, Polygon))
