# -*- coding: utf-8 -*-

import sys, os ,re
import numpy as np
from player import Player
#from component import Component

"""
class Player():
    def __init__(self, str_name, str_marker):
        self.name = str_name
        self.marker = str_marker ## in { "x" or "o"}
        self.movements = []
    def add_movement(self, r, c):
        self.movements.append((r,c))
    def get_movements(self):
        return self.movements
    def get_marker(self):
        return self.marker
"""

class Board():
    def __init__(self, row, col, number_to_be_connected):
        self.row = row
        self.col = col
        self.board = np.chararray(shape=[self.row, self.col], unicode=True)
        self.board[:] = "-"
        self.row_index = "abcdefghijklmnopqrstuvwxyz"
        self.number_of_connected_tobe_win = number_to_be_connected
        self.winning_value = 1000
        self.available_position = {}
        self.init_available_positions()
        self.components = {}

    def __str__(self):
        strings = ""
        index_row = 0
        print("   " + " ".join(map(str, range(self.col))))
        for each_row in range(self.row):
            strings += self.row_index[index_row] + ": " + " ".join(map(str, self.board[each_row, :]))
            index_row += 1
            strings += "\n"
        return strings.encode('utf-8').decode('utf-8')

    def init_available_positions(self):
        for r in range(self.row):
            for c in range(self.col):
                self.available_position[(r, c)] = 1
    def update_available_positions(self, r, c):
        self.available_position[(r,c)] = 0


    def set_a_move(self, r_index, c_index, player):

        self.board[r_index][c_index] = player.get_marker()
        self.update_available_positions(r_index, c_index)
        index_in_board = self.coordinate_to_indices(r_index, c_index)
        player.add_movement(index_in_board)


    def get_available_positions(self):
        return self.available_position


    def is_win(self, player):
        which_turn = player.get_marker()
        print("Checking for the winning state for player: " + which_turn)

        connected_number = 1
        stack_for_current_player = []
        cell_index = 0
        win_status = False

        print("Board status")
        stack_for_current_player = player.get_movements()[:] # return a sequence of cell indices (which are converted from (r, c))
        stack_for_current_player.sort(reverse=False)
        print(stack_for_current_player)

        if len(stack_for_current_player) < self.number_of_connected_tobe_win:
            # print "Total number of stones for this player is less than the required,  " \
            #      "and so don't even bother to see if the game is winning"

            return win_status

        for index in range(len(stack_for_current_player) - 1):
            focused_ind = stack_for_current_player[index] #self.coordinate_to_indices(stack_for_current_player[index])
            stack_for_current_player_excluding_focus = stack_for_current_player[index + 1:]
            if len(stack_for_current_player_excluding_focus) < (self.number_of_connected_tobe_win - 1):
                break
            win_status = self.is_win_helper(focused_ind,
                                            stack_for_current_player_excluding_focus,
                                            self.row, self.col)
            if win_status:
                break

        return win_status

    def is_win_helper(self, afocused_index, a_list_of_stones_in_a_board, r, c):
        """given r and c, we can make inferences of indices from the list to see if
           stones are connected
        """

        # First check right-straight
        flag_win = self.check_win_right_straight(afocused_index, a_list_of_stones_in_a_board)
        if flag_win:
            return True
        # Second check bottom-straight
        flag_win = self.check_win_down_straight(afocused_index, a_list_of_stones_in_a_board, c)

        if flag_win:
            return True
        # third, check down-right-diagnal
        flag_win = self.check_win_down_right_diagnal(afocused_index, a_list_of_stones_in_a_board, c)
        if flag_win:
            return True

        # fourth, check down-left-diagnoal
        flag_win = self.check_win_down_left_diagnal(afocused_index, a_list_of_stones_in_a_board, c)
        return flag_win

    def check_win_right_straight(self, focused_index, list_of_stones_in_board):
        # First check right-straight
        flag_win = True
        so_far_connected = 1
        for index, item in enumerate(list_of_stones_in_board):
            estimated_next_value = focused_index + index + 1

            if item != estimated_next_value or \
                    int(focused_index / (self.col+1)) != int(estimated_next_value / (self.col+1)):
                flag_win = False
                break
            if so_far_connected == (self.number_of_connected_tobe_win - 1):
                break
            so_far_connected += 1
        return flag_win

    def check_win_down_straight(self, focused_index, list_of_stones_in_board, c):
        # Second check bottom-straight
        a_list_in_dict = dict(zip((list_of_stones_in_board), range(len(list_of_stones_in_board))))
        flag_win = False
        so_far_connected = 1
        for index in range(self.number_of_connected_tobe_win - 1):
            estimated_next_value = focused_index + (index + 1) * c
            if estimated_next_value in a_list_in_dict:
                so_far_connected += 1
            if so_far_connected == self.number_of_connected_tobe_win:
                flag_win = True
                return flag_win

        return flag_win

    def check_win_down_right_diagnal(self, focused_index, list_of_stones_in_board, c):
        a_list_in_dict = dict(zip((list_of_stones_in_board), range(len(list_of_stones_in_board))))
        flag_win = False
        so_far_connected = 1
        for index in range(self.number_of_connected_tobe_win - 1):
            estimated_next_value = focused_index + (index + 1) * (c + 1)
            if estimated_next_value in a_list_in_dict:
                so_far_connected +=1
            if so_far_connected == self.number_of_connected_tobe_win:
                flag_win = True
                return flag_win

        return flag_win

    def check_win_down_left_diagnal(self, focused_index, list_of_stones_in_board, c):
        a_list_in_dict = dict(zip((list_of_stones_in_board), range(len(list_of_stones_in_board))))
        flag_win = False
        so_far_connected  = 1
        for index in range(self.number_of_connected_tobe_win - 1):
            estimated_next_value = focused_index + (index + 1) * (c - 1)
            if estimated_next_value in a_list_in_dict:
                so_far_connected +=1

            if so_far_connected == self.number_of_connected_tobe_win:
                flag_win = True
                return flag_win
        return flag_win


    @staticmethod
    def is_connected(r_1, c_1, r_2, c_2):
        ## given two indices, tell if two are connected in a board
        return abs(r_2 - r_1) <= 1 and abs(c_2-c_1) <= 1


    def coordinate_to_indices(self, r, c):
        return r * self.col + (c + 1)
    def indices_to_coordinate(self, indices):
        r = an_index / self.col
        c = an_index % self.col
        return r, c

## to test class Board...
if __name__ == "__main__":
    board = Board(3, 3, 3)
    print(board)
    p1 = Player("white", "O")
    p2 = Player("black", "X")

    board.set_a_move(0, 0, p1)
    print(board)

    board.set_a_move(2, 0, p1)
    print(board)
    print(board.is_win(p1))

    board.set_a_move(1, 0, p2)
    print(board)

    print(board.is_win(p1))