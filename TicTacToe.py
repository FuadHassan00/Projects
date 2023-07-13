##Assigning X and O to players
player1_symbol = 'X '
player2_symbol = 'O '

## creating the interface
interface = [
  ["A1", "B1", "C1"],
  ["A2", "B2", "C2"],
  ["A3", "B3", "C3"]
]

## Creating a dictionary to represent the positions on the interface
d = {
    "A1": 0,
    "B1": 1,
    "C1": 2,
    "A2": 3,
    "B2": 4,
    "C2": 5,
    "A3": 6,
    "B3": 7,
    "C3": 8
}

### Displaying the board
def display_board():
  print()
  for i in range(3):
    print(' '.join(interface[i]))


### Creating a funtion that takes on players turn and also the while loop is used to prompt players to enter
### valid inputs
def player_turn():
  turn = input('Please enter a valid input: ')
  while turn not in d:
    print('Invalid input')
    turn = input('Please enter a valid input: ')
  location = d[turn]
  row, col  = location // 3, location % 3
  return row, col


## funtion to determine winner

def is_winner(player):
  if (any([all([cell == player for cell in row]) for row in interface])
      or
      (
        (interface[0][0] == player and interface[1][0] == player and interface[2][0] == player) 
        or
        (interface[0][1] == player and interface[1][1] == player and interface[2][1] == player)
        or
        (interface[0][2] == player and interface[1][2] == player and interface[2][2] == player)
      )
      or
      (
        (interface[0][0] == player and interface[1][1] == player and interface[2][2] == player) 
        or
        (interface[2][0] == player and interface[1][1] == player and interface[0][2] == player)
      )
  ):
    return True
  return False

## Function to determine tie
def is_tie():
  return all([all([cell in (player1_symbol, player2_symbol) for cell in row]) for row in interface])
  
### Funtion that checks the board if player 1 wins, player 2 wins or it is a tie
def check_board():
  if is_winner(player1_symbol):
    return 'Player1'
  elif is_winner(player2_symbol):
    return 'Player2'
  elif is_tie():
    return 'Tie'
  return None

## Function that starts the game
def start_game():
  turn  = 0
  while True:
    display_board()
    status = check_board()
    if status == 'Player1':
      print('Player 1 won the game')
      return
    elif status == 'Player2':
      print('Player 2 won the game')
      return
    elif status == 'Tie':
      print('The game tied')
      return
    row, col = player_turn()
    if turn % 2 == 0:
      interface[row][col] = player1_symbol
    else:
      interface[row][col] = player2_symbol
    turn += 1
start_game()