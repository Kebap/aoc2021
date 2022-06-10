# https://adventofcode.com/2021/day/6

from time import process_time_ns

# class Fish():
#   def __init__(self, days_left = 8: int):
# self.days_left = days_left


def calculate_new_day(fishes: list) -> list:
  """
  For each Fish in list, calculate a day has passed.
  Any new fish spawned are added to the end of the fishes list.

  Suppose you have a lanternfish with an internal timer value of 3:
  - After one day, its internal timer would become 2.
  - After another day, its internal timer would become 1.
  - After another day, its internal timer would become 0.
  - After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
  - After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
  """
  new_fishes = [f for f in fishes]
  for index, fish_timer in enumerate(fishes):
    if fish_timer > 0:
      new_fishes[index] -= 1
    elif fish_timer == 0:
      new_fishes[index] = 6
      new_fishes.append(8)
    else:
      assert False, "Why do we have negative fish timers?"
  return new_fishes
  
  
def fish_str(fishes: list) -> str:
  return ','.join(str(d) for d in fishes)


def sanitize_data_of_today(data_from_file: list) -> list:
  return [int(d) for d in data_from_file[0].split(",")]


def main():
  data = get_data()
  days = 80
  debug_contents = False
  debug_time = True

  if debug_contents: 
    print(f"Initial state: {fish_str(data)}")

  for day in range(1, days + 1):
    if debug_time: 
      start_time = process_time_ns()

    data = calculate_new_day(data)

    if debug_contents:
      print(f"After {day:>2} days: {fish_str(data)}")

    if debug_time:
      end_time = process_time_ns()
      duration = end_time - start_time
      print(f"Day {day:>2} calculated in {duration//1000:>5} ms.")

  result = len(data)
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
