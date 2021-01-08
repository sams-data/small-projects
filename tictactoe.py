# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 20:09:00 2019

@author: sdste
"""

from IPython.display import clear_output


def display_board(board):
    print(f'   |   |   ')
    print(f' {board[0]} | {board[1]} | {board[2]} ')
    print(f'   |   |   ')
    print(f'-----------')
    print(f'   |   |   ')
    print(f' {board[3]} | {board[4]} | {board[5]} ')
    print(f'   |   |   ')
    print(f'-----------')
    print(f'   |   |   ')
    print(f' {board[6]} | {board[7]} | {board[8]} ')
    print(f'   |   |   ')
    
def player_input():
    players = {'O':'','X':''}
    #need to randomize
    from random import shuffle
    xo = ['X','O']
    shuffle(xo)
    players[xo.pop()] = input('Player 1, enter your name:')
    players[xo.pop()] = input('Player 2, enter your name:')
    print(f"Selecting...\n{players['O']}, you go first with marker 'O'")
    return players

def choose_position(board, player, marker):
    valid_pos = [x+1 for x in range(9)]
    valid_check = False
    #clear_output()
    display_board(board)
    position = int(input(f"{player}, choose a position:"))
    while not valid_check:
        if not position in valid_pos:
            #clear_output()
            display_board(board)
            position = int(input(f'{position} is not an option. Try again, {player}:'))
        elif (board[position-1] == 'X') or (board[position-1] == 'O'):
            #clear_output()
            display_board(board) 
            position = int(input(f'{position} is already taken. Try again, {player}:'))
        else:
            valid_check = True
            board[position-1] = marker
            return board
        
def win_check(board, mark):
    possib = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    for set in possib:
        if board[set[0]-1] == board[set[1]-1] == board[set[2]-1] == mark:
            return True
    return False

def full_board_check(board):
    for position in board:
        if (position == 'X') or (position == 'O'):
            continue
        else:
            return False
    return True

def replay():
    val_inpt = False
    while not val_inpt:
        plyagn = str(input('Do you want to play again? (y/n)')).lower()
        if plyagn == 'y':
            return True
            val_inpt = True
        elif plyagn == 'n':
            return False
            val_inpt = True
        else:
            print("I don't understand")
    

##################################################
clear_output()
print('Welcome to Tic Tac Toe!')
players = player_input()

while True:
    
    game_on = True
    board = ['1','2','3','4','5','6','7','8','9']
    pass

    while game_on:

        ox = ['O','X']
        for mark in ox:
            board = choose_position(board,players[mark],mark)
            if win_check(board,mark):
                print(f'{players[mark]}, you win!')
                game_on = False
                break
            if full_board_check(board):
                print('Tie game!')
                game_on = False
                break


    if not replay():
        break


