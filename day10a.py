# https://adventofcode.com/2021/day/10
import logging
from collections import deque

DAY = "day10"


def solve_b(data):
  """
  Will use other functions and classes (tbd) to solve part B of today.
  """
  result = ...
  return f"{result} is the soltion here!"


def check_is_symbol_fitting(pending_symbols, current_symbol):
  related_symbols = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
  }
  logging.debug(f"  Reviewing closing symbol '{current_symbol}'.")
  if len(pending_symbols) == 0:
    logging.warning(f"  Reviewed closing symbol but no more open symbols are pending.")
    return False
  
  if related_symbols[current_symbol] == pending_symbols[-1]:
    logging.debug(f"  Closing symbol fits the pending opening symbol.")
    return True
  return False


def calculate_score(first_illegal_symbol: str) -> int:
  if first_illegal_symbol is None:
    return 0
  scores_per_character = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
  }
  try:
    return scores_per_character[first_illegal_symbol]
  except KeyError:
    assert False, "Trying to calculate score for an unknown symbol."


def solve_a_line(line):
  pending_symbols = deque()
  opened_symbols = "([{<"
  closed_symbols = ")]}>"
  for symbol in line:
    if symbol in opened_symbols:
      pending_symbols.append(symbol)
      logging.debug(f"Found opening symbol '{symbol}'.")
    elif symbol in closed_symbols:
      logging.debug(f"Found closing symbol '{symbol}'.")
      if check_is_symbol_fitting(pending_symbols, symbol):
        symbol_closed = pending_symbols.pop()
        logging.debug(f"  Closed open symbol '{symbol_closed}'.")
      else:
        logging.warning(f"Found a non-fitting closing symbol '{symbol}' in line: {line}.")
        break
    else:
      logging.warning(f"Found an unknown symbol '{symbol}' in line: {line}.")
      break
  else:
    logging.info(f"Arrived safely at the end of the line.")
    logging.debug(f"The currently still pending symbols are: {str().join(map(str, reversed(pending_symbols)))}.")
    symbol = None
  logging.debug(str())
  return calculate_score(symbol)
  

def solve_a(data):
  """
  Will use other functions and classes (tbd) to solve part A of today.
  """
  running_score = 0
  for line in data:
    logging.info(f"Reviewing line: {line}.")
    running_score += solve_a_line(line)
  return running_score
  

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
  sanitized_data = data_from_file
  # sanitized_data = [list(d) for d in data_from_file]
  #  Actually string works like list as well and is easier to read.
  return sanitized_data 

  
def main(): 
  """
  Will solve puzzle A and/or B for example and/or real data.
  """
  partA = True  # If not, do not attempt to solve part A
  partB = False # If not, do not attempt to solve part B
  TestData = True  # If not, do not run with test data
  RealData = True # If not, do not run with real data
  
  logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

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
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
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
