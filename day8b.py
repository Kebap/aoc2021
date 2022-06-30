# https://adventofcode.com/2021/day/8

from parse import parse # requires: pip install parse 
# from parse import *   # would yield: parse(), search(), findall(), and with_pattern() 

UNIQUE_DIGITS_LENGTHS = [2, 4, 3, 7] # for digits 1, 4, 7, or 8
UNIQUE_LENGTHS_TRANSLATIONS = {2: 1, 4: 4, 3: 7, 7: 8}
UNIQUE_SLOT_OCCURENCES_TRANSLATIONS = {4: "e", 6: "b", 9: "f"}
GENERAL_PATTERN_DECRYPTIONS = {
  "abcefg": 0,
  "cf": 1,
  "acdeg": 2,
  "acdfg": 3,
  "bcdf": 4,
  "abdfg": 5,
  "abdefg": 6,
  "acf": 7,
  "abcdefg": 8,
  "abcdfg": 9
} # Could remove patterns with unique length from here, they are handled otherwise already! 

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

PLAN = """
Skizze:
  A	
B		C
	D	
E		F
	G	

Zusammensetzung:
n	A	B	C	D	E	F	G	s	unique?
0	X	X	X		X	X	X	6	Set 6
1			X			X		2	WAHR
2	X		X	X	X		X	5	Set 5
3	X		X	X		X	X	5	Set 5
4		X	X	X		X		4	WAHR
5	X	X		X		X	X	5	Set 5
6	X	X		X	X	X	X	6	Set 6
7	X		X			X		3	WAHR
8	X	X	X	X	X	X	X	7	WAHR
9	X	X	X	X		X	X	6	Set 6
#	8	6	8	7	4	9	7		
u	2	1	2	2	1	1	2		

Legende:
Spalten:
- n: Zahlen 0-9
- A-G: Slots
- s: Summe der Slots für diese Zahl
- unique?: Ist s unique und Zahl damit in UNIQUE_DIGITS_LENGTH
Zeilen:
- 0-9: Zusammensetzung der Slots für diese Zahl
- #: Anzahl der Einsätze für diesen Slot
- u: Einsätze unique? Dann Slot darüber identifizierbar!

Zahlen:		
0  	?  	Set 6: C, D oder E fehlt
1	  OK	1, 4, 7, or 8: Unique über Länge erkannt
2	  ?	  Set 5: [B, E], [B, F] oder [C, E] fehlen
3	  ?	  Set 5: [B, E], [B, F] oder [C, E] fehlen
4	  OK	1, 4, 7, or 8: Unique über Länge erkannt
5	  ?	  Set 5: [B, E], [B, F] oder [C, E] fehlen
6	  ?	  Set 6: C, D oder E fehlt
7	  OK	1, 4, 7, or 8: Unique über Länge erkannt
8	  OK	1, 4, 7, or 8: Unique über Länge erkannt
9	  ?	  Set 6: C, D oder E fehlt

Slots:		
A	todo	noch ableiten über 1 und 7 (sind bekannt)
B	todo	B, E, F: unique über Häufigkeit erkannt
C	todo	noch ableiten über Set 5 (Rest bekannt)
D	todo	noch ableiten über Set 6 (Rest bald bekannt aus Set 5 und C)
E	todo	B, E, F: unique über Häufigkeit erkannt
F	todo	B, E, F: unique über Häufigkeit erkannt
G	todo	verbleibt als letztes, wenn obiges umgesetzt ist
Alle Slots erkannt? Dann kann auch alle Zahlen erkennen!
"""


def solve_display_8a(display):
  easy_digits_displayed = [d for d in display["outputs"] if len(d) in UNIQUE_DIGITS_LENGTHS]
  return len(easy_digits_displayed)    


def solve_display(display) -> int:
  """
  Review one display and return its output value translated into integer.
  """
  patterns = display["patterns"]
  outputs = display["outputs"]
  
  # For solving the display, I need to decrypt each pattern into a number 
  # Then: decryption("cdeg") == 4
  decryptions = dict()  

  # Maybe slot "e" in this display was called "B" in the general modell
  # Then: slot_translations["e"] == "B"
  slot_translations = dict()
  
  # When I have translated enough slots, I can translate signal patterns
  # Then pattern_translations["cdeg"] == "abef"
  # Where "abef" is the name the pattern would have in the general modell
  # And "cdeg" is the encrypted name the pattern has in the current display
  pattern_translations = dict()
  # Is this step even necessary or can't I immediately use decryptions at that time?

  # Remember or even decypher patterns via their (maybe unique) lengths
  set5 = list(p for p in patterns if len(p) == 5) # will be 3 different patterns
  set6 = list(p for p in patterns if len(p) == 6) # will be 3 different patterns
  for pattern in patterns:  
    # Is this a pattern that can already be identified by its unique length?
    if len(pattern) in UNIQUE_LENGTHS_TRANSLATIONS:
      decryptions[pattern] = UNIQUE_LENGTHS_TRANSLATIONS[len(pattern)]
      
  # Looking at each slot/signal/wire now.
  # How often (and for which patterns) is each slot used?
  slot_names = list("abcdefg")
  slot_usage = dict()
  for slot in slot_names:
    slot_usage[slot] = [p for p in patterns if slot in p]
  slot_usage_count = {k: len(v) for k, v in slot_usage.items()}
  # slot_usage_count has the following values once: 4, 6, 9, and twice: 7, 8 
  assert "".join(sorted(map(str, slot_usage_count.values()))) == "4677889", "unexpected slots"

  # The slots with unique number of occurrences can be identified immediately.
  # Where 4x used is called E in the general model, 6x used is B, 9x used is F.
  for slot, occurrences in slot_usage_count.items():
    if occurrences in UNIQUE_SLOT_OCCURENCES_TRANSLATIONS:
      slot_translations[slot] = UNIQUE_SLOT_OCCURENCES_TRANSLATIONS[occurrences]

  # We can identify the slot that is called A in the general model as well.
  # It is the slot that is used in number 7 but not used in number 1 and we know those.
  for p, n in decryptions.items():
    if n == 1: 
      slots_used_in_one = list(p)
    elif n == 7:
      slots_used_in_seven = list(p)
  assert not slots_used_in_one is None, "Pattern for number one not found"
  assert not slots_used_in_seven is None, "Pattern for number seven not found"
  # Find the slot that is used in 7 but not used in 1. It translates to A in general
  for slot in slots_used_in_seven:
    if not slot in slots_used_in_one:
      slot_translations[slot] = "a"
      break

  # Find slot C via set5 (which are the 3 patterns represented with exactly 5 slots)
  # Two of their slots are used in 2 of the 3 patterns. One slot I know as F, the other is C.
  slots_used_in_set5 = set5[0] + set5[1] + set5[2]
  slots_used_twice_in_set5 = list(s for s in set(slots_used_in_set5) 
                                  if slots_used_in_set5.count(s) == 2)  # O(n) ?
  for slot in slots_used_twice_in_set5:
    if not slot in slot_translations:
      slot_translations[slot] = "c"
      break
  
  # Find slot D via set6 (which are the 3 patterns represented with exactly 6 slots)
  # Three of their slots are used in 2 of the 3 patterns. One slot is still unknown. It is D.
  slots_used_in_set6 = set6[0] + set6[1] + set6[2]
  slots_used_twice_in_set6 = list(s for s in set(slots_used_in_set6) 
                                  if slots_used_in_set6.count(s) == 2)  # O(n) ?
  for slot in slots_used_twice_in_set6:
    if not slot in slot_translations:
      slot_translations[slot] = "d"
      break

  # Only one slot remains without a translation to its general name. It is G.
  for slot in slot_names:
    if not slot in slot_translations:
      slot_translations[slot] = "g"

  # All slots can now be translated to their general name. Great!
  # Now I can translate the slot name in the display

  # Decrypt all six remaining unknown numbers (with non-unique lengths).
  # This will use the now known slots, as all translations are known.
  for pattern in set5 + set6:
    if all(bool(slot in slot_translations) for slot in pattern):
      pattern_translation = "".join(sorted(slot_translations[slot] for slot in pattern))
      decryptions[pattern] = GENERAL_PATTERN_DECRYPTIONS[pattern_translation]
      pattern_translations[pattern] = pattern_translation

  # Finally I can decrypt the numbers shown in this display
  decrypted_output_numbers = tuple(decryptions.get(p, 0) for p in outputs)
  # The 0 here was a place holder during a time when some decryptions were unknown still!
  
  decrypted_value = int("".join(str(n) for n in decrypted_output_numbers))
  
  print(f"{decrypted_value:>4}", 
        outputs, 
        sep="\t")
  return decrypted_value


def solve(data):
  sum_of_output_values = sum(solve_display(d) for d in data)
  return f"{sum_of_output_values} is the sum of all output values."
   


def main():
  print(f"Solution of example data is:\n{solve(get_data(False))}\n")
  print(f"Solution of real data is:\n{solve(get_data(True))}\n")
  

def sanitize_data_of_today(data_from_file: list) -> list:
  displays = []
  for display in data_from_file:
    unique_patterns, output_values = parse("{} | {}", display)
    
    unique_patterns = unique_patterns.split(" ")
    # In each pattern, sort the letters alphabetically lexicographically
    unique_patterns = ["".join(sorted(s)) for s in unique_patterns]
    # Sort the patterns, the shortest first, then lexicographically
    unique_patterns.sort(key = lambda x: (len(x), x))
    
    output_values = output_values.split(" ")
    output_values = ["".join(sorted(s)) for s in output_values]
    
    displays.append({"patterns": unique_patterns, "outputs": output_values})
    
  return displays


def get_data(use_real_input = False) -> list:
  day = "day8"
  example_input = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
  """
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
