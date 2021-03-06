# https://adventofcode.com/2021/day/5

class Field():
  def __init__(self, coordinates: list):
    self.coordinates = coordinates

    # Find out maximum values for x and y in the field
    max_x = max_y = 0
    for line in coordinates:
      x1, y1, x2, y2 = line
      if max(x1, x2) > max_x:
        max_x = max(x1, x2)
      if max(y1, y2) > max_y:
        max_y = max(y1, y2)
    self.max_x = max_x
    self.max_y = max_y

    # Implement x*y field as a one-dimensional list 
    points_required = (max_x + 1) * max_y
    #print(f"Found dimensions: max_x: {max_x}, max_y: {max_y}, grid_size; {points_required}.")
    self.grid = [0] * points_required

    # Populate grid with information from coordinates
    self.populate_grid(self.coordinates)


  def print_grid(self, from_x = 0, from_y = 0, to_x = 5, to_y = 5):
    """
    Prints the grid to the screen so you can review it.
    For starters, only prints a small 5x5 subset of it.
    """
    pass

    
  def populate_grid_xy(self, x: int, y: int) -> None:
    """
    Translates x,y coordinates into one-dimensional grid.
    Then increases that position by one.
    
    That means, point 0,0 is item 0 in grid
    Meanwhile, point 0,1 is item 1 in grid
    Meanwhile, point 1,0 is item max_x in grid
    Meanwhile, point 1,1 is item max_x + 1 in grid   
    """
    #print(f"Populating grid coordinates: {x}/{y} at ")
    self.grid[x * self.max_x + y] += 1
    return

  
  def populate_grid(self, coordinates):
    for line in coordinates:
      # Decide kind of current line 
      horizontal = False
      vertical = False
      x1, y1, x2, y2 = line
      if x1 == x2:
        horizontal = True
      if y1 == y2:
        vertical = True
        
      if not horizontal and not vertical:
        # For now, ignore all other diagonal lines!
        continue

      # Fill start-point of line
      self.populate_grid_xy(x1, y1)
      
      if horizontal and vertical:
        # Start point is also end, so we are done here
        continue

      # Fill end-point of line
      self.populate_grid_xy(x2, y2)
      
      # Calculate and fill all points in between
      if horizontal:
        y_max, y_min = max(y1, y2), min(y1, y2)
        delta = y_max - y_min
        for i in range(1, delta):
          self.populate_grid_xy(x1, y_min + i)
          
      elif vertical:
        x_max, x_min = max(x1, x2), min(x1, x2)
        delta = x_max - x_min
        for i in range(1, delta):
          self.populate_grid_xy(x_min + i, y1)

  
  def count_interesting_spots(self):
    """
    Determine the number of points where at least two lines overlap. In the grid will be a 2 or larger 
    """
    return len(tuple(s for s in self.grid if s >= 2))
    

  def __repr__(self):
    return f"A {self.max_x}/{self.max_y} grid with {len(self.coordinates)} known lines"

def get_coordinates_from_data(data: list) -> list:
  lines = []
  arrow = " -> "
  for line in data:
    # line == "0,9 -> 5,9"
    arrow_start_position = line.index(arrow)
    first_part = line[:arrow_start_position]
    arrow_end_position = arrow_start_position + len(arrow)
    last_part = line[arrow_end_position:]
    # (first_part, last_part) == ('0,9', '5,9')
    x1, y1 = first_part.split(",")
    x2, y2 = last_part.split(",")
    coordinates = [int(a) for a in (x1, y1, x2, y2)]
    # coordinates == [0, 9, 5, 9]
    lines.append(coordinates)
  return lines


def review_lines(lines: list) -> list:
  return lines


def main():
  data = get_data()
  coordinates = get_coordinates_from_data(data)
  result = Field(coordinates).count_interesting_spots()
  print(f"Das Ergebnis lautet {result}. Gl??ckwunsch!")


def get_data(use_real_input = False) -> list:
  day = "day5a"
  example_input = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
  if not use_real_input:
    used_input = example_input
  else:
    with open(f"input_data/{day}.txt", "r") as input_file:
      used_input = input_file.read()
  used_input = used_input.strip().split("\n")
  return used_input
  
if __name__ == "__main__":
  main()
