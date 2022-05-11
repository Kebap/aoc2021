def main():
  pos_x = 0 # horizontal position
  pos_y = 0 # depth
  aim = 0

  for item in get_data():
    command, size = item.split(" ")
    size = int(size)

    if command == "down":
      aim += size
    elif command == "up":
      aim -= size
    elif command == "forward":
      pos_x += size
      pos_y += aim * size
    else:
      print(f"Unexpected data: {command}, {size}")
      break

    print(f"Moving '{command:<7}' by '{size}'.\t"
          f"New position: {pos_x}/{pos_y} and aim: {aim}.")
  print(f"\nFinal multiplicative result: {pos_x * pos_y}")

def get_data():
  return """
forward 7
down 2
forward 7
down 6
forward 1
forward 7
down 3
up 5
forward 7
forward 6
down 8
down 1
up 5
up 1
down 2
forward 8
etc. -1
""".strip().split("\n")
  
if __name__ == "__main__":
  main()
