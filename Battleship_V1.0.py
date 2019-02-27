from random import randint
import string


def random_row(board, vert_shiplength):
    return randint(0, board_length - vert_shiplength)


def random_col(board, hori_shiplength):
    return randint(0, board_width - hori_shiplength)

# print_board still requires both boards as input even in solo mode for simplicity sake
# player 1 and player 2 board are flipped, to make it easier to toggle between solo and duo play
def print_board(board1, board2):
    index = 1
    if num_players == 2:
        print(' '*2 + ' '.join(letters[:board_width]) + ' '*10 + ' '*2 + ' '.join(letters[:board_width]))
        for row1, row2 in zip(board1, board2):
            print(str(index) + ' ' + ' '.join(row2) + ' '*10 + str(index) + ' ' + ' '.join(row1))
            index += 1
        print(' '+' '*(board_width-4)+ 'Player 1' + ' '*11 +  ' '*2*(board_width-4) + 'Player 2')

    else:
        print( ' '*2 + ' '.join(letters[:board_width]) )
        for row in board1:
            print(str(index) + ' ' + ' '.join(row))
            index += 1

def print_stats(n):
    print('Shots fired: {}'.format(str(turn+1)))
    print('Shots missed: {}'.format(str(turn+1-players[n]['shots_hit'])))
    print('Shots hit: {}'.format(str(players[n]['shots_hit'])))
    print('Ships sunk: {}'.format(str(players[n]['ships_sunk'])))
    print('Ships remaining: {}'.format(str(num_ships-players[n]['ships_sunk'])))
    print('Accuracy: {}'.format(str((players[n]['shots_hit']/(turn+1))*100)+'%'))

# declare default variables
board_length = 4
board_width = 4 # Min 4, Max 26
num_ships = board_width - 2
num_players = 1
max_ship_length = 4 # At most board length/width
num_turns = max_ship_length*num_ships + 2


# think of board and ship as 
# 'board player is firing at' and 'ships player needs to sink'
players = [
{  'name': 'Player 1',
   'board': [],
   'ships': [],
   'occupied_coords': [],
   'ships_sunk': 0,
   'shots_hit': 0
},

{  'name': 'Player 2',
   'board': [],
   'ships': [],
   'occupied_coords': [],
   'ships_sunk': 0,
   'shots_hit': 0
}

]

letters = string.ascii_uppercase

#menu start

menu_selection = '0'
while menu_selection != '1':
    while menu_selection == '0':
        print(' '*4 + 'Welcome to Battleship!\n' + '-'*30 + '\n')
        print(' '*9 + '1 - Play\n')
        print(' '*9 + '2 - Settings')
        menu_selection = input()
        
    while menu_selection == '2':
        settings_selection = '0'
        while settings_selection == '0':
            print('\n' + ' '*11 + 'Settings\n' + '-'*30 + '\n')
            print(' '*7 + '1 - Game modes\n')
            print(' '*7 + '2 - Size of boards\n')
            print(' '*7 + '3 - No. of ships\n')
            print(' '*7 + '4 - No. of turns\n')
            print(' '*7 + '5 - Back\n')
            settings_selection = input()

        while settings_selection == '1':
            print(' '*11 + 'Settings\n' + '-'*30 + '\n') 
            print(' '*11 + '1 - Solo\n')
            print(' '*11 + '2 - 2 Player Vs.\n')
            print(' '*11 + '3 - Back')
            user_input = input()
            if user_input == '1':
                num_players = 1
                settings_selection = '0'
                print('\nDone\n')
            elif user_input == '2':
                num_players = 2
                settings_selection = '0'
                print('\nDone\n')
            elif user_input == '3':
                settings_selection = '0'
            else:
                print('please enter a valid input')

        while settings_selection == '2':
            print(' '*11 + 'Settings\n' + '-'*30 + '\n') 
            print(' '*7 + 'Enter board size\n' +' '*10 + '(4 to 9)\n')
            user_input = input()
            if user_input.isdigit():
                if 4 <= int(user_input) <= 9:
                    board_width = int(user_input)
                    board_length = int(user_input)
                    print('\nDone\n')
                    settings_selection = '0'
                else:
                    print('Enter a valid board size')
            else:
                print('Enter a valid board size')

        while settings_selection == '3':
            print(' '*11 + 'Settings\n' + '-'*30 + '\n') 
            print(' '*6 + 'Enter no. of ships\n' +' '*11 + '(1 to {})\n'.format(board_width - 2))
            user_input = input()
            if user_input.isdigit():
                if 1 <= int(user_input) <= board_width - 2:
                    num_ships = int(user_input)
                    print('\nDone\n')
                    settings_selection = '0'
                else:
                    print('Enter a valid number of ships')
            else:
                print('Enter a valid number of ships')
                
        while settings_selection == '4':
            print(' '*11 + 'Settings\n' + '-'*30 + '\n') 
            print(' '*6 + 'Enter no. of turns\n')
            print(' '*11 + '{} to {}'.format(str(num_ships*max_ship_length), str(board_width*board_length)) )
            user_input = input()
            if user_input.isdigit():
                if num_ships*max_ship_length <= int(user_input) <= board_width*board_length:
                    num_turns = int(user_input)
                    print('\nDone\n')
                    settings_selection = '0'
                else:
                    print('Enter a valid number of turns')
            else:
                print('Enter a valid number of turns')

        if settings_selection == '5':
            menu_selection = '0'


rematch = 'Y'
while rematch == 'Y':
    # generate board and wipe stats, ships
    for player in players:
        player['shots_hit'] = 0
        player['ships_sunk'] = 0
        player['ships'] = []
        for x in range(board_length):
            try:
                player['board'][x] = (['O'] * board_width)
            except IndexError:
                player['board'].append(['O'] * board_width)
        

    # generate ships

    print('Generating ships...')

    for shipnum in range(num_ships):
        ship_length = randint(1, max_ship_length)

        for player in players:
            player['ships'].append( [] )
            while len(player['ships'][shipnum]) != ship_length:
                ship_orientation = randint(0, 1)
                if ship_orientation == 0:  # horizontal
                    ship_row = random_row(player['board'], 1)
                    ship_col = random_col(player['board'], ship_length)
                    for num in range(ship_length):
                        coords = (ship_row, ship_col + num)
                        if coords in player['occupied_coords']:
                            player['ships'][shipnum].clear()
                            player['occupied_coords'] = player['occupied_coords'][:len(player['occupied_coords'])-num]
                            break
                        player['occupied_coords'].append(coords)
                        player['ships'][shipnum].append(coords)


                else:  # vertical
                    ship_row = random_row(player['board'], ship_length)
                    ship_col = random_col(player['board'], 1)
                    for num in range(ship_length):
                        coords = (ship_row + num, ship_col)
                        if coords in player['occupied_coords']:
                            player['ships'][shipnum].clear()
                            player['occupied_coords'] = player['occupied_coords'][:len(player['occupied_coords'])-num]
                            break
                        player['occupied_coords'].append(coords)
                        player['ships'][shipnum].append(coords)
    



    print('Done!\n' + '-' * 30)


    # Game start
    for turn in range(num_turns):
        for i in range(num_players):
        # get guess
            print_board(players[0]['board'], players[1]['board'])
            print('\nTurn: {} of {}'.format(turn+1, num_turns))
            while 1:
                guess = input( '{} input coordinates: '.format(players[i]['name']) )
                if not guess:
                    print('Please input coordinates')
                else:
                    if not guess[0].isalpha() or not guess[1:].isdigit():  # Only works for letters up till Z
                        print('Please input coordinates in the format (letter)(number), A1 for example')
                    else:
                        guess_col = letters.index(guess[0].upper())
                        guess_row = int(guess[1:]) - 1
    
                        if not 0 <= guess_row < board_length or not 0 <= guess_col < board_width:
                            print("Oops, that's not even in the ocean. Guess again!")
            
                        else:
                            tile = players[i]['board'][guess_row][guess_col]
                            guess = (guess_row,guess_col)
    
                            if tile == 'M' or tile == 'X':
                                print('Yo1u guessed that one already.')
                            else:
                                break
    
    
    
            print( '\n{}\n'.format('-'*10) )
            # check for hit
            for ship in players[i]['ships']:
                if guess in ship:
                    players[i]['board'][guess_row][guess_col] = 'X'
                    ship.remove(guess)
                    players[i]['shots_hit'] += 1
                    if not ship:
                        players[i]['ships'].remove([])
                        players[i]['ships_sunk'] += 1
                        if not players[i]['ships']:
                            print('\nYou have sunk all the battleships!\n')
                            if num_players != 1:
                                print('\n{} wins!\n'.format(players[i]['name']) )
                        else:
                            print('\nYou sunk a battleship!\n')
                    else:
                        print ('\nYou hit a battleship!\n')

        
            if players[i]['board'][guess_row][guess_col] != 'X':
                    print ('\nYou missed!\n')
                    players[i]['board'][guess_row][guess_col] = 'M'
    

            if not players[i]['ships']:
                break
            
        if turn == num_turns-1 or not players[i]['ships']:
            print_board(players[0]['board'], players[1]['board'])
            print('\nGame Over\n')
            if num_players == 1:
                print(' '*10 + 'Statistics')
                print('-'*30)
                print_stats(0)
            else:
                print(' '*10 + 'Statistics')
                print('-'*30)
                print('\nPlayer 1:\n')
                print_stats(0)
                print('\nPlayer 2:\n')
                print_stats(1)
            while 1:
                rematch = input('Play again? (Y/N)').upper()
                if rematch != 'Y' and rematch != 'N':
                    print('Please enter Y or N')
                else:
                    break
            break
        


print('\nGoodbye!')


"""
1) Work on stucture
  - efficiency, generate just 1 board, and 1 board of ships for single player
  - improve readability
2) More ships
  - names for ships, can put in new list with corresponding indexes
3) Allow player to place ships themselves
4) Create a proper interface with pygame
5) More features
  - ship specials
  - custom names for ships
6) make sure variables dont break the game

"""
