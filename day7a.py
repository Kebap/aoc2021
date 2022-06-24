# https://adventofcode.com/2021/day/7
from statistics import median


def calculate_fuel_consumption(data, target_position):
  fuel_required = 0
  for crab_position in data:
    fuel_required += abs(crab_position - target_position)
  return fuel_required
    

def solve(data):
  bounds = range(min(data), max(data)) # Missing max bound
  
  # Calculate for maximum bound as a starting point
  minimum_fuel = calculate_fuel_consumption(data, max(data))
  best_position = max(data)

  # Compare all other possible positions to find better ones
  for possible_position in bounds:
    fuel_required = calculate_fuel_consumption(data, possible_position)
    if fuel_required < minimum_fuel:
      minimum_fuel = fuel_required
      best_position = possible_position

  return best_position, minimum_fuel


def main():
  data = get_data(True)
  print(f"Der Median lautet {median(data)}. Ist das auch immer das optimale Ergebnis? Wieviel Sprit braucht man dorthin?")
  print(f"Insgesamt haben wir {len(data)} Datenpunkte zwischen {min(data)} und {max(data)}.")
  zp, f = solve(data)
  print(f"Survey says, die beste Zielposition wird {zp} sein, denn dorthin braucht man nur {f} Treibstoff.")


def sanitize_data_of_today(data_from_file: list) -> list:
  return [int(d) for d in data_from_file[0].split(",")]


def get_data(use_real_input = False) -> list:
  day = "day7"
  example_input = """
  16,1,2,0,4,2,7,1,2,14
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
