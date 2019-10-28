from board import Board
from player import Player
import numpy as np
import utils as UT

class Game():
    GAME_STATUS = ["Playing", "End", "Draw"]

    def __init__(self, players, turn_id, board):

        self.board = board
        ## to track of whose turn is now
        self.players = players
        self.turn_id = turn_id
        self.status = Game.GAME_STATUS[0]
        self.turn = self.players[self.turn_id]

    def set_to_next_player(self):
        next_turn = ( self.turn_id + 1) % len(self.players)
        self.turn_id = next_turn
        self.turn = self.players[self.turn_id]

    def check_end_status(self, a_player):
        if self.board.is_win(a_player):
            UT.print_as_log("FinalResult\tWinning by %s" % (a_player))
            return True
        return False

    def get_input(self):
        prompt = "%s 's Turn\n" % (self.turn)
        input_from_user = input(prompt)
        r_c_in_list = input_from_user.split("_")
        r, c = r_c_in_list[0], r_c_in_list[1]
        r_int = ord(r) - ord('a')
        c_int = int(c)
        return r_int, c_int

    def validate_input(self):
        available_pos = self.board.get_available_positions()
        while True:
            r, c = self.get_input()
            if available_pos.get((r, c), 0) == 1:
                break
            Game.print_as_log("Try again. Your input")
        return r, c


    def play_game(self):
        turn_id = 0

        while self.check_end_status(self.turn) != True:
            print(self.board)
            if self.turn.get_player_type() == Player.PTYPE_HUMAN:
                r_v, c_v = self.validate_input()
            else:
                r_v, c_v = self.a_move_for_agent()

            self.board.set_a_move(r_v, c_v, self.turn)
            UT.print_as_log(self.board.get_available_positions())
            if self.check_end_status(self.turn):
                print(self.board)
                UT.print_as_log("Winning and so ending this game")
                return self.turn
            elif self.is_draw():
                print(self.board)
                UT.print_as_log("Draw.... so, exiting the game")
                return None
            self.set_to_next_player()

    def a_move_for_agent(self):
        r, c  = self.a_move_for_agent_helper()
        return r,c

    def a_move_for_agent_helper(self):
        all_available_positions_dict = self.board.get_available_positions()
        random_move_index = np.random.randint(0, len(all_available_positions_dict),1)[0]
        r, c = list(all_available_positions_dict.keys())[random_move_index]
        return r, c
    def is_draw(self):
        if len(self.board.get_available_positions()) < 1:
            return True
        return False

if __name__ == "__main__":
    board_size = 3
    num_connected = 3
    board = Board(board_size, board_size, num_connected)
    p1 = Player("white", "O", Player.PTYPE_AGENT)
    p2 = Player("black", "X", Player.PTYPE_AGENT)
    players = [p1, p2]
    first_turn_id = 0
    game = Game(players, first_turn_id, board)
    #game.init_game(players,first_turn_id, board)
    game.play_game()