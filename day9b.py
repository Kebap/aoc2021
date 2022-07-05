# https://adventofcode.com/2021/day/9
import logging

DAY = "day9"


class Point():
  def __init__(self, x, y, height, map_object):
    self.height = int(height)
    self.x = x
    self.y = y
    self.map = map_object
    self.basin = None

  
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

  
  def find_adjacent_basins(self):
    basins = set()
    for neighbor in self.neighbors:
      if not neighbor.basin is None:
        if len(basins) == 0:
          self.basin = neighbor.basin
          basins.add(self.basin)
        else:
          first_basin = min(self.basin, neighbor.basin)
          self.basin = first_basin
          basins.add(self.basin)
          basins.add(neighbor.basin)
    if len(basins) == 0:
      new_basin = self.map.add_basin()
      new_basin.add(self)
      self.basin = new_basin.number
      basins.add(self.basin)
    return basins


class Basin():
  def __init__(self, number):
    self.number = number
    self.points = list()

  def __repr__(self):
    return f"Basin #{self.number} with {len(self.points)} points."

  
  def add(self, point):
    """Adds a point to this basin."""
    if not point in self.points:
      self.points.append(point)

  
  def remove(self, point):
    """Remove a point from this basin."""
    self.points.remove(point)



class Map():
  def __init__(self, map_data):
    self.map_data = map_data
    self.max_y = len(map_data) - 1
    self.max_x = len(map_data[0]) - 1
    self.points = list()
    self.low_points = None
    self.basins = None
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


  def add_basin(self):
    new_basin = Basin(len(self.basins))
    self.basins.append(new_basin)
    return new_basin


  def calculate_top_basin_sizes(self):
    """Find the three largest basins and multiply their sizes together."""
    basin_sizes = [len(b.points) for b in self.basins]
    basin_sizes.sort(reverse = True)
    print(f"Found basin sizes like: {basin_sizes}.")
    product = 1
    for basin_size in basin_sizes[:3]:
      print(f"  Multiplying: {basin_size}.")
      product *= basin_size
    return product

  
  def find_basins(self):
    self.basins = list()
    for point in self.points:
      logging.debug(f"")
      logging.debug(f"Betrachte Punkt {point.x}/{point.y}/{point.height}...")
      if point.height == 9:
        logging.debug(f"  Höhe 9 gefunden. Ignoriere Punkt.")
        continue
      logging.debug(f"  Betrachte benachbarte Punkte...")
      found_basins = point.find_adjacent_basins()
      logging.debug(f"  Fand dabei folgende Basins: {found_basins}.")
      if len(found_basins) == 0:
        assert False, "The point did not find nor create any basins!?"
        new_basin = self.add_basin()
        new_basin.add(point)
      elif len(found_basins) == 1:
        logging.debug(f"  Das ist das einzige Basin im Umkreis.")
        logging.debug(f"  Füge diesen Punkt hinzu!")
        this_basin = self.basins[point.basin]
        this_basin.add(point)
        logging.debug(f"  Basin #{this_basin.number} enthält nun {len(this_basin.points)} Punkte.")
      elif len(found_basins) > 1:
        # Need to merge basins, then get rid of obsolete basins contents
        logging.debug(f"  Es gibt hier mehrere Basins im Umkreis!")
        chosen_basin = min(found_basins)
        logging.debug(f"  Behalte davon nur Basin #{chosen_basin}.")
        logging.debug(f"  Füge diesen Punkt hinzu!")
        this_basin = self.basins[point.basin]
        this_basin.add(point)
        logging.debug(f"  Basin #{this_basin.number} enthält nun {len(this_basin.points)} Punkte.")
        logging.debug(f"  Verschiebe Rest...")
        found_basins.remove(chosen_basin)
        for other_basin in found_basins:
          logging.debug(f"    Verschiebe aus Basin #{other_basin}...")
          points_to_be_moved = self.basins[other_basin].points[:]
          for other_point in points_to_be_moved:
            logging.debug(f"      Verschiebe Punkt {other_point.x}/{other_point.y}.")
            other_point.basin = chosen_basin
            self.basins[chosen_basin].add(other_point)
            self.basins[other_basin].remove(other_point)
        logging.debug(f"  Basin #{this_basin.number} enthält nun {len(this_basin.points)} Punkte.")
        
    
def solve_b(data):
  m = Map(data)
  m.find_basins()
  result = m.calculate_top_basin_sizes()
  return f"{result} is the soltion here!"


def solve_a(data):
  m = Map(data)
  result = m.calculate_risk_level()
  return f"{result} is the soltion here!"
  

def main():  
  logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
  
  if True:
    print(f"Solution of example data is:\n{solve_b(get_data(False))}\n")
    
  if False:
    print(f"Solution of real data is:\n{solve_b(get_data(True))}\n")
    # 902880 is too low.
  

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
  example_input = """
98997
49896
98765
69896
""" # This snippet has more backtracking in that the merged basin is larger.
  if not use_real_input:
    used_input = example_input
    
  else:
    with open(f"input_data/{DAY}.txt", "r") as input_file:
      used_input = input_file.read()
      
  used_input = used_input.strip().split("\n")
  return sanitize_data_of_today(used_input)

  
if __name__ == "__main__":
  main()
