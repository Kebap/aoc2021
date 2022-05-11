# https://adventofcode.com/2021/day/3

def calculate_most_common_bits(data):
  """
  Takes a list of same-length strings containing of 1 and 0.
  For each position of the string, calculates which is the case:
    a. Most have the number 1?
    b. Most have the number 0?
    c. The same ammount of 1 and 0 were found?
  Results are codified as 1, -1, or 0 respectively.
  Returns a single list of these results (same length as string).
  """
  sum_of_columns = [0] * len(data[0])
  lines = len(data)
  for line in data:
    for position, character in enumerate(line):
      sum_of_columns[position] += int(character) # Sum each column
  print(f"{sum_of_columns} from {lines} lines.")

  result = []
  for value in sum_of_columns:
    if value > lines / 2:
      result.append(1)
    elif value == lines / 2:
      result.append(0)
    elif value < lines / 2:
      result.append(-1)
  return result

def calculate_oxygen_generator_rating(data):
  for position in range(len(data[0])):
    most_common_bits = calculate_most_common_bits(data)
    if most_common_bits[position] in [1, 0]:
      data = [d for d in data if d[position] == "1"]
    elif most_common_bits[position] == -1:
      data = [d for d in data if d[position] == "0"]
    if len(data) == 1:
      break
  return data[0]

def calculate_co2_scrubber_rating(data):
  for position in range(len(data[0])):
    most_common_bits = calculate_most_common_bits(data)
    if most_common_bits[position] in [1, 0]:
      data = [d for d in data if d[position] == "0"]
    elif most_common_bits[position] == -1:
      data = [d for d in data if d[position] == "1"]
    if len(data) == 1:
      break
  return data[0]

def main():
  data = get_data()

  oxygen_rating_as_bin = calculate_oxygen_generator_rating(data)
  oxygen_rating_as_dec = int(oxygen_rating_as_bin, base = 2)
  print(f"Oxygen generator rating: {oxygen_rating_as_bin} aka {oxygen_rating_as_dec}")
      
  co2_rating_as_bin = calculate_co2_scrubber_rating(data)
  co2_rating_as_dec = int(co2_rating_as_bin, base = 2)
  print(f"CO2 scrubber rating: {co2_rating_as_bin} aka {co2_rating_as_dec}")
  
  print(f"\nDay3b multiplicative result: {oxygen_rating_as_dec * co2_rating_as_dec}")

def get_data():
  return """
100000101101
011011010101
000000111000
110101110111
110000001100
""".strip().split("\n")
  
if __name__ == "__main__":
  main()
