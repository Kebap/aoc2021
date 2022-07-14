# https://adventofcode.com/2021/day/11
import logging
DAY = "day11"


class Point():
  def __init__(self, x, y, status, map_object):
    self.status = int(status)
    self.x = x
    self.y = y
    self.map = map_object
    self.flashy = False

  
  def __repr__(self):
    return f"Point({self.x}, {self.y}, {self.status})"

  
  def get_to_know_neighbors(self):
    self.neighbors = list()
    if self.x > 0: # Not the left border
      self.neighbors.append(self.map.get_point(self.x - 1, self.y))
    if self.x < self.map.max_x: # Not the right border
      self.neighbors.append(self.map.get_point(self.x + 1, self.y))
    if self.y > 0: # Not the top border
      self.neighbors.append(self.map.get_point(self.x, self.y - 1))
    if self.y < self.map.max_y: # Not the bottom border
      self.neighbors.append(self.map.get_point(self.x, self.y + 1))
    if self.x > 0 and self.y > 0: # Not the top left corner
      self.neighbors.append(self.map.get_point(self.x - 1, self.y - 1))
    if self.x < self.map.max_x and self.y > 0: # Not the top right corner
      self.neighbors.append(self.map.get_point(self.x + 1, self.y - 1))
    if self.x > 0 and self.y < self.map.max_y: # Not the bottom left corner
      self.neighbors.append(self.map.get_point(self.x - 1, self.y + 1))
    if self.x < self.map.max_x and self.y < self.map.max_y: # Not the bottom right corner
      self.neighbors.append(self.map.get_point(self.x + 1, self.y + 1))



class Map():
  def __init__(self, map_data):
    self.map_data = map_data
    self.max_y = len(map_data) - 1
    self.max_x = len(map_data[0]) - 1
    self.points = list()
    for y_index, line in enumerate(map_data):
      for x_index, point in enumerate(line):
        self.points.append(Point(x_index, y_index, point, self))
    for point in self.points:
      point.get_to_know_neighbors()

  
  def __repr__(self):
    status_represenation = [str(p.status) for p in self.points]
    list_of_lists = list()
    for start_of_line in range(0, len(self.points), self.max_x + 1):
      end_of_line = start_of_line + self.max_x + 1
      partial_list = status_represenation[start_of_line:end_of_line]
      list_of_lists.append(partial_list)
    string_representation = "\n".join("".join(line) for line in list_of_lists)
    return string_representation
    
  
  def get_point(self, x, y):
    coordinate_in_list = x + (y * (self.max_x + 1))
    return self.points[coordinate_in_list]


  def do_a_step(self) -> int:
    """
    Increases all points' status by one.
    Observes how many flashes happen.
    Increases neighbors accordingly, maybe repeats.
    Reports the number of flashes that happened after the whole flashing and the step completed.
    """
    how_many_flashes_happened = 0
    
    # traverse all points
      # increase their status by one
    logging.debug(f"Looping points, increasing their status by one.")
    for point in self.points:
      point.status += 1

    logging.debug(f"Loop #1 done.")
    
    # loop 
      # check all points: is the status >9000 ? and not yet "flashy"
        # if so, set at this point's data a bool value "flashy" 
        # traverse all the point'S neighbors
          # increase their status by one
    logging.debug(f"Looping points, searching and handling flashes.")
    for _ in range(100):
      new_flashes = list(p for p in self.points 
                         if (not p.flashy and p.status > 9))
      logging.debug(f"  Found {len(new_flashes)} new flashes.")
      if len(new_flashes) == 0:
        logging.debug(f"  No more new flashes found, aborting loop.")
        break

      logging.debug(f"  Looping new flashes, increasing their neighbors' status.")
      for point in new_flashes:
        point.flashy = True
        for neighbor in point.neighbors:
          neighbor.status += 1
      logging.debug(f"Loop #2b done.")
          
    logging.debug(f"Loop #2 done.")

    # Remember how many flashes happenend
    points_that_flashed = list(p for p in self.points if p.flashy)
    how_many_flashes_happened += len(points_that_flashed)
    # finally all flashes happened and increased their neighbors, etc.
    # traverse all "flashy" points
      # set these points' values to zero and "flashy" to false again
    logging.debug(f"Looping flashy points, resetting their flashes and status.")
    for point in points_that_flashed:
      point.status = 0
      point.flashy = False

    logging.debug(f"Loop #3 done.")
    return how_many_flashes_happened
    

"""
Remember:
Objects in lists can be mutated from outside as well.
Use this wisely by creating smaller lists to modify some points.
Map will be updated accordingly!

> p = Point(1,2,3, None)
> p
Point(1, 2, 3)
> p.status
3
> a = [p]
> b = 1,2,p
> b
(1, 2, Point(1, 2, 3))
> a
[Point(1, 2, 3)]
> p.status = 5
> p
Point(1, 2, 5)
> a
[Point(1, 2, 5)]
> b
(1, 2, Point(1, 2, 5))
> 
"""
  

def solve_b(data):
  """
  Will use other functions and classes (tbd) to solve part B of today.
  """
  result = ...
  return f"{result} is the soltion here!"


def solve_a(data):
  """
  Will use other functions and classes (tbd) to solve part A of today.
  """
  m = Map(data)
  logging.info("Beginning configuration:")
  logging.info(str(m))
  total_flashes = 0
  for i in range(100):
    flashes = m.do_a_step()
    total_flashes += flashes
    logging.info(f"In this step #{i+1}, {flashes} squids flash, total of {total_flashes}")
  logging.info(str(m))
  return total_flashes
  

def sanitize_data_of_today(data_from_file: list) -> list:
  """
  Can be adjusted to further enhance puzzle data.
  Handy, if the data should not be just a simple string for each line.
  
  For example, consider this line of data coming from puzzle input:
    be cgeb fabcd edb | cefdb gcbe

  Use this function to turn that data into a more handy object:
    {"patterns": ["be", "bceg", "abcdf", "bde"], 
     "outputs": ["bcdef", "bde"]}
  """
  sanitized_data = data_from_file # or modify before
  return sanitized_data 


def main(): 
  """
  Will solve puzzle A and/or B for example and/or real data.
  """
  partA = True  # If not, do not attempt to solve part A
  partB = False # If not, do not attempt to solve part B
  TestData = True  # If not, do not run with test data
  RealData = False # If not, do not run with real data
  
  logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

  if partA:
    if TestData:
      solution = solve_a(get_data(False))
      print(f"Solution for part A with example data is:\n{solution}\n")
    if RealData:
      solution = solve_a(get_data(True))
      print(f"Solution for part A with real data is:\n{solution}\n")
    
  if partB:
    if TestData:
      solution = solve_a(get_data(False))
      print(f"Solution for part B with example data is:\n{solution}\n")
    if RealData:
      solution = solve_a(get_data(True))
      print(f"Solution for part B with real data is:\n{solution}\n")


def get_data(use_real_input = False) -> list:
  """
  Reads either the example data given in this very function,
  or the real puzzle input data given in a file of its own.
  Will return a list of said data with each line as an item.
  """
  example_input = """
11111
19991
19191
19991
11111
"""
  example_input = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
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
