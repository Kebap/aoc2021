# https://adventofcode.com/2021/day/6

from time import process_time_ns


class Pool():
  def __init__(self, fish_list = None):
    if fish_list is None:
      fish_list = get_data()
    self.original_fish = fish_list

    # Forget order, just remember how many fish we have with each timer (maximum of 8 days possible)
    fish_distribution = {
      index: 0 for index in range(9)
    }
    for timer in fish_list:
      if timer in fish_distribution:
        fish_distribution[timer] += 1
      else:
        fish_distribution[timer] = 1
    self.fish = fish_distribution


  def count_fish(self) -> int:
    return sum(self.fish.values())

  
  def calculate_new_day(self) -> None:
    """
    For each Fish known, calculate a day has passed.
  
    Suppose you have a lanternfish with an internal timer value of 3:
    - After one day, its internal timer would become 2.
    - After another day, its internal timer would become 1.
    - After another day, its internal timer would become 0.
    - After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
    - After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
    """
    new_fish = dict()
    for index in range(8):
      new_fish[index] = self.fish[index + 1]
    new_fish[8] = self.fish[0]
    new_fish[6] += self.fish[0]
    self.fish = new_fish
  
  
  def display_fish(self) -> str:
    return ', '.join(f"{n}*{i}d" for i, n in self.fish.items())


def sanitize_data_of_today(data_from_file: list) -> list:
  return [int(d) for d in data_from_file[0].split(",")]


def main():
  days = 80
  debug_contents = True
  debug_time = False

  data = get_data(False)
  pool = Pool(data)
  
  if debug_contents:
    print(f"Initial state: {pool.display_fish()}")

  for day in range(1, days + 1):
    if debug_time: 
      start_time = process_time_ns()

    pool.calculate_new_day()

    if debug_contents:
      print(f"After {day:>2} days: {pool.display_fish()}")

    if debug_time:
      end_time = process_time_ns()
      duration = end_time - start_time
      print(f"Day {day:>2} calculated in {duration//1000:>5} microseconds.")

  result = pool.count_fish()
  print(f"Number of fish after {days} days: {result}.")


def get_data(use_real_input = False) -> list:
  day = "day6"
  example_input = """
3,4,3,1,2
"""
  if not use_real_input:
    used_input = example_input
    
  else:
    with open(f"input_data/{day}.txt", "r") as input_file:
      used_input = input_file.read()
      
  used_input = used_input.strip().split("\n")
  return sanitize_data_of_today(used_input)

  
if __name__ == "__main__":
  main()
