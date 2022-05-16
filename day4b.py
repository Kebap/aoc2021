# https://adventofcode.com/2021/day/4

# from dataclasses import dataclass
# @dataclass
class Board:
  def __init__(self, values: str):
    """
    Sets up the 5x5 bingo board.
    Accepts 25 numbers (seperated by space character)
    Internally uses one list of 25 items as opposed to 5x5.
    """
    self.values = values
    self.grid = list(map(int, values.split()))
    self.marked = [False] * 25

  
  def __repr__(self):
    """
    Output like:
    40  29  44  17  27
    56  98  83  62  70
    25  91  20  60  84
    42  66  34  77  31
    16  8   6   50  28
    """
    output = []
    for position, number in enumerate(self.grid):
      output.append(str(number))
      output.append("\t")
      if position % 5 == 4:
        output.append("\n")
    return "".join(output)

  
  def test_bingo(self):
    """
    Check all 10 horizontal and vertical lines' status.
    If all 5 numbers there are marked as checked, it's a bingo!
    """
    return any((all(self.marked[0:5]),
                all(self.marked[5:10]),
                all(self.marked[10:15]),
                all(self.marked[15:20]),
                all(self.marked[20:25]),
                all((self.marked[0], 
                     self.marked[5], 
                     self.marked[10], 
                     self.marked[15], 
                     self.marked[20])),
                all((self.marked[1], 
                     self.marked[6], 
                     self.marked[11], 
                     self.marked[16], 
                     self.marked[21])),
                all((self.marked[2], 
                     self.marked[7], 
                     self.marked[12], 
                     self.marked[17], 
                     self.marked[22])),
                all((self.marked[3], 
                     self.marked[8], 
                     self.marked[13], 
                     self.marked[18], 
                     self.marked[23])),
                all((self.marked[4], 
                     self.marked[9], 
                     self.marked[14], 
                     self.marked[19], 
                     self.marked[24]))))
    # Diagonals don't count!
    diagonals = (all((self.marked[0], 
                     self.marked[6], 
                     self.marked[12], 
                     self.marked[18], 
                     self.marked[24])),
                all((self.marked[4], 
                     self.marked[8], 
                     self.marked[12], 
                     self.marked[16], 
                     self.marked[20])))

   
  def mark(self, number: int):
    """
    Accepts any number. Remembers it is now marked. 
    Returns True, if number was found. Returns False otherwise.
    Next hurry to check if you got a bingo now!
    """
    try:
      position = self.grid.index(number)
    except ValueError:
      return False
    self.marked[position] = True
    return True

  def score(self, number_just_called: int) -> int:
    """
    Calculates the score of the winning board like this:
    Start by finding the sum of all unmarked numbers.
    Then, multiply that sum by the number that was just
    called when the board won to get the final score.
    """
    result = 0
    for i, number in enumerate(self.grid):
      if not self.marked[i]:
        result += int(number)
    return result * number_just_called


def setup_boards(data: list) -> list:
  boards = []
  numbers = []
  for line in data:
    if line == "":
      boards.append(Board(" ".join(numbers)))
      numbers = []
    else:
      numbers.append(line)
  boards.append(Board(" ".join(numbers))) # Last 5 lines in data are not followed by an empty line, but still represent a board to be included.
  return boards


def test(position: int = 0) -> Board:
  boards = setup_boards(get_data()[2:])
  board = boards[position]
  return board
  
  
def main():
  data = get_data()
  
  called_numbers = data[0]
  data = data[2:] # Remove called numbers and first empty line

  boards = setup_boards(data)
  called_numbers = called_numbers.split(",") 
  
  for number in called_numbers:
    print(f"Gezogen wurde Nummer {number}.", end=" \t")
    for i, board in enumerate(boards):
      board.mark(int(number))
      if board.test_bingo():
        boards.remove(board)
        last_board = board
    print(f"Noch {len(boards)} Bretter warten auf Bingo!")
    if len(boards) == 0:
      print(f"Das letzte Brett erhält {last_board.score(int(number))} Punkte. Glückwunsch!")
      print(f"So sieht das Brett aus:\n{last_board}")
      print(f"Diese Zahlen sind markiert:\n{last_board.marked}")
      print(f"Diese Zahlen sind im Grid:\n{last_board.grid}")
      break


def get_data() -> list:
  return """
31,50,79,59,39,53,58,95,92,55,40,97,81,22,69,26,6,23,3,29,83,48,18,75,47,49,62,45,35,34,1,88,54,16,56,77,28,94,52,15,0,87,93,90,60,67,68,85,80,51,20,96,61,66,63,91,8,99,70,13,71,17,7,38,44,43,5,25,72,2,57,33,82,78,89,21,30,11,73,84,4,46,14,19,12,10,42,32,64,98,9,74,86,27,24,65,37,41,76,36

31  5 70  8 88
38 63 14 91 56
22 67 17 47 74
93 52 69 29 53
33 66 64 19 73

35 63 17 48 77
25 58 33 14 96
32 87 90 66 70
16  4 98 72 23
19 74 39 29 59
""".strip().split("\n")
  
if __name__ == "__main__":
  main()
