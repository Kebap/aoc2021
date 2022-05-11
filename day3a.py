# https://adventofcode.com/2021/day/3

def main():
  sum_of_columns = [0] * len("100000101101")
  data = get_data()
  lines = len(data)
  for line in data:
    for position, character in enumerate(line):
      sum_of_columns[position] += int(character) # Sum each column
  print(f"{sum_of_columns} from {lines} lines.")
  
  sum_of_columns = [value > lines / 2 for value in sum_of_columns] # Did more than half of the column's bits have the number one?
  
  gamma_rate = [1 * value for value in sum_of_columns] # If so, give the gamma rate a number one as well.
  gamma_rate = "".join([str(value) for value in gamma_rate]) # Create a new bitwise number from the results.
  gamma_rate = int(gamma_rate, base=2) # Need the decimal form though.
  
  epsilon_rate  = [1 * bool(not(value)) for value in sum_of_columns] # The epsilon rate is the boolean opposite of the gamma rate.
  epsilon_rate = "".join([str(value) for value in epsilon_rate]) 
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
