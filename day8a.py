# https://adventofcode.com/2021/day/8

from parse import parse # requires: pip install parse 
# from parse import *   # would yield: parse(), search(), findall(), and with_pattern() 

EASY_DIGITS_LEGTHS = [2, 4, 3, 7] # for digits 1, 4, 7, or 8

DISPLAY = """
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""


def solve_display(display):
  easy_digits_displayed = [d for d in display["outputs"] if len(d) in EASY_DIGITS_LEGTHS]
  return len(easy_digits_displayed)    


def solve(data):
  ammount_of_easy_digits = 0
  for display in data:
    ammount_of_easy_digits += solve_display(display)
  return f"{ammount_of_easy_digits} easy digits found."
    


def main():
  data = get_data(False)
  print(f"Solution of example data is: \n{solve(data)}\n")

  data = get_data(True)
  print(f"Solution of real data is: \n{solve(data)}\n")
  

def sanitize_data_of_today(data_from_file: list) -> list:
  displays = []
  for display in data_from_file:
    unique_patterns, output_values = parse("{} | {}", display)
    unique_patterns = unique_patterns.split(" ")
    output_values = output_values.split(" ")
    displays.append({"patterns": unique_patterns, "outputs": output_values})
  return displays


def get_data(use_real_input = False) -> list:
  day = "day8"
  example_input = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
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
