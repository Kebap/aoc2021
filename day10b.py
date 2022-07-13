# https://adventofcode.com/2021/day/10
import logging
from collections import deque

DAY = "day10"
RELATED_SYMBOLS = {
  ")": "(",
  "]": "[",
  "}": "{",
  ">": "<"}
OPENED_SYMBOLS = RELATED_SYMBOLS.values()
CLOSED_SYMBOLS = RELATED_SYMBOLS.keys()


def identify_b_winner(results: list) -> int:
  """the winner is found by sorting all of the scores and then taking the middle score. (There will always be an odd number of scores to consider.) In this example, the middle score is 288957 because there are the same number of scores smaller and larger than it."""
  results.sort() # Most definitely unsane to modify a list given as parameter. Still will continue like this here, because I know the top-level calling this function will discard the list anyway after this.
  length = len(results)
  middle_item = results[length // 2]
  return middle_item

  
def calculate_score_b(symbols):
  result = 0
  scores_per_character = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4}
  for char in symbols:
    result *= 5
    result += scores_per_character[char]
    logging.debug(f"  Score after {char} is {result}.")
  return result


def solve_b_line(remaining_symbols):
  """
  Figures out how to complete a line and calculate score for part B.
  """
  closing_symbols = list()
  logging.debug(f"Sorting remaining symbols: '{remaining_symbols}'.")
  for symbol in remaining_symbols:
    logging.debug(f"  Opening symbol: '{symbol}'.")
    for key, value in RELATED_SYMBOLS.items():
      if symbol == value:
        closing_symbols.append(key)
        logging.debug(f"    Will be closed by: '{key}'.")
        break
  logging.debug(f"Calculating total remaining score.")
  result = calculate_score_b(closing_symbols)
  logging.debug(f"Total remaining score is: {result}.")
  return result


def check_is_symbol_fitting(pending_symbols, current_symbol):
  logging.debug(f"  Reviewing closing symbol '{current_symbol}'.")
  if len(pending_symbols) == 0:
    logging.warning(f"  Reviewed closing symbol but no more open symbols are pending.")
    return False
  
  if RELATED_SYMBOLS[current_symbol] == pending_symbols[-1]:
    logging.debug(f"  Closing symbol fits the pending opening symbol.")
    return True
  return False


def calculate_score_a(first_illegal_symbol: str) -> int:
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
  remaining_symbols = str()
  for symbol in line:
    if symbol in OPENED_SYMBOLS:
      pending_symbols.append(symbol)
      logging.debug(f"Found opening symbol '{symbol}'.")
    elif symbol in CLOSED_SYMBOLS:
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
    remaining_symbols = str().join(map(str, reversed(pending_symbols)))
    logging.debug(f"The currently still pending symbols are: {remaining_symbols}.")
    symbol = None
  logging.debug(str())
  return calculate_score_a(symbol), remaining_symbols
  

def solve(data, solve_b_as_well: bool):
  """
  Will use other functions and classes (tbd) to solve part A of today.
  """
  running_a_score = 0
  all_b_scores = list()
  for line in data:
    logging.info(f"Reviewing line: {line}.")
    score, remaining_symbols = solve_a_line(line)
    running_a_score += score
    if solve_b_as_well:
      if len(remaining_symbols) > 0:
        # Otherwise we have a completed or a corrupted line, so no score necessary
        score_b = solve_b_line(remaining_symbols)
        all_b_scores.append(score_b)
        logging.info(f"  Found closing score: {score_b}.")
  winning_b_score = identify_b_winner(all_b_scores)
  return running_a_score, winning_b_score
  

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
  partA = False  # If not, do not attempt to solve part A
  partB = True # If not, do not attempt to solve part B
  TestData = True  # If not, do not run with test data
  RealData = False # If not, do not run with real data
  
  logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

  if partA:
    if TestData:
      solution_a, solution_b = solve(get_data(False), partB)
      print(f"Solution for part A with example data is:\n{solution_a}\n")
      if partB:
        print(f"Solution for part B with example data is:\n{solution_b}\n")
        
    if RealData:
      solution_a, solution_b = solve(get_data(True), partB)
      print(f"Solution for part A with real data is:\n{solution_a}\n")
      if partB:
        print(f"Solution for part B with real data is:\n{solution_b}\n")



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
