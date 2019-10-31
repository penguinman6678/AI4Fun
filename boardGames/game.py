
from board import Board
from player import Player
from draw_board import Draw

import numpy as np
import utils as UT
import sys

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
        game_log = {'winner':"", 'sequence':{}}
        canvas_for_drawing = Draw()
        is_draw = False

        while self.check_end_status(self.turn) != True:
            print(self.board)

            if self.turn.get_player_type() == Player.PTYPE_HUMAN:
                r_v, c_v = self.validate_input()
            else:
                r_v, c_v = self.a_move_for_agent()

            self.board.set_a_move(r_v, c_v, self.turn)

            canvas_for_drawing.move_and_draw(r_v, c_v, self.turn.get_marker())

            UT.print_as_log(self.board.get_available_positions())
            if self.check_end_status(self.turn):
                print("FinalResult: %s" % (self.turn.get_marker()))
                print(self.board)
                #UT.print_as_log("Winning and so ending this game")
                UT.print_as_log(self.board.sequences_of_movements)
                game_log['winner'] = self.turn.get_marker()
                game_log['sequence'] = self.board.sequences_of_movements

                break

            elif self.is_draw():
                is_draw = True
                print("FinalResult: Draw")
                #UT.print_as_log("Draw.... so, exiting the game")
                print(self.board)
                game_log['winner'] = "D"
                game_log['sequence'] = self.board.sequences_of_movements
                break
            else:
                self.set_to_next_player()
                
        ## for writing a message to the canvas
        result_message = "Game result -- Winner is %s" % (game_log.get("winner"))
        if is_draw:
            result_message = "Game result :  Draw"
        canvas_for_drawing.write_text(result_message)
        canvas_for_drawing.exit_on_click()

        json_str = game_log #json.dumps(game_log)
        return json_str

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

    @staticmethod
    def load_a_game(afile):
        move_sequences = UT.read_a_game(afile)
        if move_sequences:
            Game.parse_history(move_sequences)
    @staticmethod
    def parse_history(adict):


        winner = adict.get("winner", None)
        if winner == None:
            print("Something is wrong")
            sys.exit(1)
        move_sequences = adict.get("sequence", None)

        board_obj_from_history = Board(3, 3, 3)
        # below obj is for drawing the board on a canvas.
        # if you don't like, you can make it comment
        draw_board_obj = Draw()
        for each_move in move_sequences:
            player_marker = each_move.get("turn")
            r_index, c_index = each_move.get("xy")
            p = Player("test", player_marker, 1)
            board_obj_from_history.set_a_move(r_index, c_index, p)
            draw_board_obj.move_and_draw(r_index, c_index, player_marker)
            print(board_obj_from_history)
        draw_board_obj.write_text(("Winner is:  %s" %(player_marker)))
        draw_board_obj.exit_on_click()

if __name__ == "__main__":
    Play_or_Load = 1
    if Play_or_Load == 1:
        board_size = 3
        num_connected = 3
        board = Board(board_size, board_size, num_connected)
        # a player has Player.PTYPE_HUMAN for a human player
        p1 = Player("white", "O", Player.PTYPE_AGENT)
        p2 = Player("black", "X", Player.PTYPE_AGENT)
        players = [p1, p2]
        first_turn_id = 0
        game = Game(players, first_turn_id, board)
        #game.init_game(players,first_turn_id, board)
        json_str = game.play_game()
        UT.write_json_to_file(json_str)

    elif Play_or_Load == 2:
        # this means loading from a file
        Game.load_a_game("./game_output.log")

