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


# declare default variables
board_length = 4
board_width = 4 # Max 26
num_turns = 4
num_ships = 1
num_players = 1
max_ship_length = 4 # At most board length/width


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
                print('\nDone\n')
            elif user_input == '2':
                num_players = 2
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
            user_input = input()
            if user_input.isdigit():
                if int(user_input) >= 1:
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
    # generate board
    for player in players:
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
            print('\nTurn: {}'.format(turn+1))
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
                                print('You guessed that one already.')
                            else:
                                break
    
    
    
            print( '\n{}\n'.format('-'*10) )
            # check for hit
            for ship in players[i]['ships']:
                if guess in ship:
                    players[i]['board'][guess_row][guess_col] = 'X'
                    ship.remove(guess)
                    if not ship:
                        players[i]['ships'].remove([])
                        if not players[i]['ships']:
                            print('\nYou have sunk all the battleships!\n')
                            if num_players != 1:
                                print('\n{} wins!\n'.format(players[i]['name']) )
                        else:
                            print('\nYou sunk a battleship!\n')
                            players[i]['ships_sunk'] += 1
                    else:
                        print ('\nYou hit a battleship!\n')
                        players[i]['shots_hit'] += 1
        
            if players[i]['board'][guess_row][guess_col] != 'X':
                    print ('\nYou missed!\n')
                    players[i]['board'][guess_row][guess_col] = 'M'
    

            if turn == num_turns-1 and i == 1 or not players[i]['ships']:
                print_board(players[0]['board'], players[1]['board'])
                print('\nGame Over\n')
                if num_players == 1:
                    print(' '*10 + 'Statistics')
                    print('-'*30)
                    print('Shots fired: {}'.format(str(num_turns)))
                    print('Shots hit: {}'.format(str(players[0]['shots_hit'])))
                    print('Ships sunk: {}'.format(str(players[0]['ships_sunk'])))
                    print('Ships remaining: {}'.format(str(players[0]['num_ships']-players[0]['ships_sunk'])))
                    print('Accuracy: {}'.format(str((players[0]['shots_hit']//num_turns)*100)+'%'))
                while 1:
                    rematch = input('Play again? (Y/N)').upper()
                    if rematch != 'Y' and rematch != 'N':
                        print('Please enter Y or N')
                    else:
                        break


print('\nGoodbye!')


"""
1) Work on effciency
  - generate just 1 board, and 1 board of ships for single player
2) More ships
  - names for ships, can put in new list with corresponding indexes
3) Allow player to place ships themselves
4) Create a proper interface with pygame
5) More features
  - ship specials
  - fix statistics
  - custom names for ships
6) each player goes once during 1 turn, not each one on alternate turns
7) fix broken single player(game not ending)
8) fix number of turns to min turns needed to sink ships, and max is number of squares
"""
