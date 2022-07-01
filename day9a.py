# https://adventofcode.com/2021/day/9
DAY = "day9"


class Point():
  def __init__(self, x, y, height, map_object):
    self.height = int(height)
    self.x = x
    self.y = y
    self.map = map_object

  def __repr__(self):
    return f"Point({self.x}, {self.y}, {self.height})"

  def get_to_know_neighbors(self):
    self.neighbors = list()
    if self.x > 0:
      self.neighbors.append(self.map.get_point(self.x - 1, self.y))
    if self.x < self.map.max_x:
      self.neighbors.append(self.map.get_point(self.x + 1, self.y))
    if self.y > 0:
      self.neighbors.append(self.map.get_point(self.x, self.y - 1))
    if self.y < self.map.max_y:
      self.neighbors.append(self.map.get_point(self.x, self.y + 1))

  def recognize_low_point(self):
    for neighbor in self.neighbors:
      if neighbor.height <= self.height:
        return False
    #print(f"Found low point at {self.x}/{self.y} with height {self.height} and neighbors: {self.neighbors}.")
    return True


class Map():
  def __init__(self, map_data):
    self.map_data = map_data
    self.max_y = len(map_data) - 1
    self.max_x = len(map_data[0]) - 1
    self.points = list()
    self.low_points = None
    for y_index, line in enumerate(map_data):
      for x_index, point in enumerate(line):
        self.points.append(Point(x_index, y_index, point, self))
    for point in self.points:
      point.get_to_know_neighbors()

  def get_point(self, x, y):
    coordinate_in_list = x + (y * (self.max_x + 1))
    return self.points[coordinate_in_list]

  def find_low_points(self):
    self.low_points = [p for p in self.points if p.recognize_low_point()]

  def calculate_risk_level(self):
    if self.low_points is None:
      self.find_low_points()
    total_risk_level = sum(1 + p.height for p in self.low_points)
    return total_risk_level
    

def solve(data):
  m = Map(data)
  output_values = m.calculate_risk_level()
  return f"{output_values} is the soltion here!"
   

def main():  
  print(f"Solution of example data is:\n{solve(get_data(False))}\n")

  if True:
    print(f"Solution of real data is:\n{solve(get_data(True))}\n")
  

def sanitize_data_of_today(data_from_file: list) -> list:
  return data_from_file


def get_data(use_real_input = False) -> list:
  example_input = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
  if not use_real_input:
    used_input = example_input
    
  else:
    with open(f"input_data/{DAY}.txt", "r") as input_file:
      used_input = input_file.read()
      
  used_input = used_input.strip().split("\n")
  return sanitize_data_of_today(used_input)

  
if __name__ == "__main__":
  main()
