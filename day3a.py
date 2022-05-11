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
  
def main():
  data = get_data()
  most_common_bits = calculate_most_common_bits(data) # Did more than half of the column's bits have the number one?

  assert 0 not in most_common_bits # Not sure how to react if any column had the same exact number of 1 and 0 in it. Luckily it wasn't the case.
  
  gamma_rate = ["1" if value == 1 else "0" for value in most_common_bits] # If so, give the gamma rate a number one as well.
  gamma_rate = "".join(gamma_rate) # Create a new bitwise number from the results.
  gamma_rate = int(gamma_rate, base=2) # Need the decimal form though.

  epsilon_rate  = ["0" if value == 1 else "1" for value in most_common_bits] # The epsilon rate is the boolean opposite of the gamma rate.
  epsilon_rate = "".join(epsilon_rate) 
  epsilon_rate = int(epsilon_rate, base=2)

  print(f"\nDay3a multiplicative result: {gamma_rate * epsilon_rate}")

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
