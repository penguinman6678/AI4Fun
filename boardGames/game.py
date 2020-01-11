
from board import Board
from player import Player
from draw_board import Draw

import numpy as np
import utils as UT
import sys
import turtle
from policies import RandomPolicy, MCTSPolicy, ModelPolicy
import uuid
import time


from keras.models import load_model
from keras.models import model_from_json
import json

class Game():
    GAME_STATUS = ["Playing", "End", "Draw"]

    def __init__(self, players, turn_id, board):

        self.board = board
        ## to track of whose turn is now
        self.players = players
        self.turn_id = turn_id
        self.status = Game.GAME_STATUS[0]
        self.turn = self.players[self.turn_id]
        self.flag_for_drawing_canvas = False

        # in case a move needs to be made through Random
        self.random_policy = RandomPolicy()
        ## MCTSPolicy(a, b) -- a is player, b is for an opponent

        self.mctsObj_X = MCTSPolicy(self.players[0], self.players[1])
        self.mctsObj_O = MCTSPolicy(self.players[1], self.players[0])

        self.mctsObjs = [self.mctsObj_X, self.mctsObj_O]

        model_dir = "/Users/chihoon/works/mlBooks/introML/simple_template/AI4Fun/boardGames/analysis-tools/models_ex/"
        model_w_file = "model_2020-01-09-15-15-06_BEST_SO_FAR_WITH_Early_Stop-0.90-upto2-0.924weights.h5"
        model_json_file = "model_2020-01-09-15-15-06_BEST_SO_FAR_WITH_Early_Stop-0.90-upto2-0.924in_json.json"

        self.model_based_policy = ModelPolicy(model_dir, model_w_file, model_json_file)

        self.game_id = uuid.uuid1()


    def show_progress_on_canvas(self, a_boolean_flag):
        self.flag_for_drawing_canvas = a_boolean_flag
    def set_to_next_player(self):
        next_turn = ( self.turn_id + 1) % len(self.players)
        self.turn_id = next_turn
        self.turn = self.players[self.turn_id]

    def is_end(self):
        if self.is_draw():
            return True

        for each_player in self.players:
            if self.check_end_status(each_player):
                return True
        return False

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
            print("Try again. Your input")
        return r, c

    # def convert_sequence_moves_to_vector(self):
    #     individual_sequence = [0] * 9
    #     for item in self.board.sequences_of_movements:
    #         turn_for_this_move = item.get("turn")
    #         move_made_for_this_move = item.get("position")
    #         individual_sequence[move_made_for_this_move - 1] = 1 if turn_for_this_move == "X" else 2
    #
    #     return np.array([individual_sequence])


    def play_game(self):
        turn_id = 0
        game_log = {'game_uuid': self.get_game_id(), 'play_modes': {'X': self.players[0].get_policy_mode(),
                                                                    'O': self.players[1].get_policy_mode()},
                    'winner':"", 'sequence':{}}
        canvas_for_drawing = None

        if self.flag_for_drawing_canvas:
            #turtle.setup(500, 500)
            canvas_for_drawing = Draw()
        is_draw_gametie = False

        from model_loader import ModelBasedAgent
        model_dir = "/Users/chihoon/works/mlBooks/introML/simple_template/AI4Fun/boardGames/analysis-tools/models_ex/"
        model_w_file = model_dir + "current_best.h5" #"model_2020-01-09-15-15-06_BEST_SO_FAR_WITH_Early_Stop-0.90-upto2-0.924weights.h5"
        model_json_file = model_dir + "current_best.json" #model_2020-01-09-15-15-06_BEST_SO_FAR_WITH_Early_Stop-0.90-upto2-0.924in_json.json"
        model_agent_obj = ModelBasedAgent(model_w_file, model_json_file)
        mlModel = model_agent_obj.get_model()

        while self.check_end_status(self.turn) != True:
            print(self.board)
            test_instance = self.board.convert_sequence_moves_to_vector()
            print(test_instance)
            if self.turn.get_player_type() == Player.PTYPE_HUMAN:
                # TODO -- this part is just to make a simplified interface of modelbased movement
                # later, this will be the part of Policy as a ModelPolicy class
                # for now, we assume player O would be model.. as X is always starting first

                #test_instance = np.array([an_instance])

                prediction_move = mlModel.predict_proba(test_instance)[0]
                pp = model_agent_obj.predict_proba(test_instance)[0]
                UT.print_three_arrays(test_instance[0], pp, prediction_move)
                move_by_prediction = np.argmax(pp) + 1
                r_e, c_e = self.board.indices_to_coordinate(move_by_prediction)

                r_v, c_v = self.validate_input()
                print("R:%d C:%d \t i_e:%d R_e:%d C_e:%d" % (r_v, c_v, move_by_prediction, r_e, c_e))
            else:  # when Player is an agent
                if self.turn.get_policy_mode() == "MODEL":
                    r_v, c_v = self.model_based_policy.move(self.board)
                elif self.turn.get_policy_mode() == "MCTS":
                    if self.turn.get_marker() == "O":
                        r_v, c_v = self.mctsObj_O.move(self.board)
                        # TODO -- this part is just to make a simplified interface of modelbased movement
                        # This could be a place for ModelBased action
                    elif self.turn.get_marker() == "X":
                        if self.turn.get_policy_mode() == "Random":
                            self.random_policy = RandomPolicy()
                            r_v, c_v = self.random_policy.move(self.board)
                            # print("AM I HERE FOR RANDOM")
                        else:
                            r_v, c_v = self.mctsObj_X.move(self.board)
                elif self.turn.get_policy_mode() == "Random":
                    self.random_policy = RandomPolicy()
                    r_v, c_v = self.random_policy.move(self.board)


            self.board.set_a_move(r_v, c_v, self.turn)
            UT.print_as_log(self.board.get_available_positions())
            ## Drawing on canvas
            if self.flag_for_drawing_canvas:
                canvas_for_drawing.move_and_draw(r_v, c_v, self.turn.get_marker())

            if self.check_end_status(self.turn):
                print("FinalResult: %s" % (self.turn.get_marker()))
                print(self.board)
                print(self.board.convert_sequence_moves_to_vector())
                #UT.print_as_log("Winning and so ending this game")
                UT.print_as_log(self.board.sequences_of_movements)
                game_log['winner'] = self.turn.get_marker()
                game_log['sequence'] = self.board.sequences_of_movements

                break

            elif self.is_draw():
                is_draw_gametie = True
                print("FinalResult: Draw")
                #UT.print_as_log("Draw.... so, exiting the game")
                print(self.board)
                print(self.board.convert_sequence_moves_to_vector())
                game_log['winner'] = "D"
                game_log['sequence'] = self.board.sequences_of_movements
                break
            else:
                self.set_to_next_player()

        ## for writing a message to the canvas
        if self.flag_for_drawing_canvas:
            result_message = "Game result -- Winner is %s" % (game_log.get("winner"))
            if is_draw_gametie:
                result_message = "Game result :  Draw"
            canvas_for_drawing.write_text(result_message)
            canvas_for_drawing.exit_on_click()

            #canvas_for_drawing.reset_canvas()
            #turtle.TurtleScreen._RUNNING = True
        json_str = game_log #json.dumps(game_log)
        return json_str

    def a_move_for_agent(self):
        r, c  = self.a_move_for_agent_helper()
        return r,c
    ## this is the function for an agent to come up with a smarter decision
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
    def parse_history(adict, message_str=None):

        winner = adict.get("winner", None)
        if winner == None:
            print("Something is wrong")
            sys.exit(1)
        move_sequences = adict.get("sequence", None)
        turtle.hideturtle()
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

        draw_board_obj.write_text(("Winner is:  %s -- sampled %s" %(winner, str(message_str))))
        time.sleep(3)
        draw_board_obj.turtle_obj.getpen().clear()
        draw_board_obj.turtle_obj.getscreen().clearscreen()

        # draw_board_obj.exit_on_click()
        # or

    def get_game_id(self):
        return str(self.game_id)


## since this is the simulation based, we will use agent vs agent
def run_n_simulations(n):
    board_size = 3
    num_connected = 3
    for i in range(n):
        p1 = Player("white", "X", Player.PTYPE_AGENT)
        p2 = Player("black", "O", Player.PTYPE_AGENT)
        players = [p1, p2]
        first_turn_id = 0  # np.random.choice([0, 1])
        board = Board(board_size, board_size, num_connected)
        each_game = Game(players, first_turn_id, board)
        each_game.show_progress_on_canvas(False)
        json_str  = each_game.play_game()
        UT.write_json_to_file(json_str)
        p1.reset()
        p2.reset()

def human_vs_MCTS():
    board_size = 3
    num_connected = 3
    p1 = Player("black", "X", Player.PTYPE_HUMAN)
    p2 = Player("white", "O", Player.PTYPE_AGENT)

    players = [p1, p2]
    board = Board(board_size, board_size, num_connected)
    each_game = Game(players, 0, board)
    each_game.show_progress_on_canvas(True)
    json_str  = each_game.play_game()
    UT.write_json_to_file(json_str)

def MCTS_vs_MODEL(n):

    board_size = 3
    num_connected = 3

    for i in range(n):
        p1 = Player("black", "X", Player.PTYPE_AGENT, "MCTS")
        #p2 = Player("white", "O", Player.PTYPE_HUMAN)
        p2 = Player("white", "O", Player.PTYPE_AGENT, "MODEL")
        players = [p1, p2]
        board = Board(board_size, board_size, num_connected)
        each_game = Game(players, 0, board)
        each_game.show_progress_on_canvas(False)
        json_str  = each_game.play_game()
        UT.write_json_to_file(json_str)
        p1.reset()
        p2.reset()

def MCTS_vs_MCTS():
    board_size = 3
    num_connected = 3
    p1 = Player("black", "X", Player.PTYPE_AGENT)
    p2 = Player("white", "O", Player.PTYPE_AGENT)

    players = [p1, p2]
    board = Board(board_size, board_size, num_connected)
    each_game = Game(players, 0, board)
    each_game.show_progress_on_canvas(True)
    json_str  = each_game.play_game()
    UT.write_json_to_file(json_str)

def humans_vs_model_agent():
    pass
DO_PLAY = 1
LOAD_PLAY = 2

if __name__ == "__main__":

    #GAME_MODE = DO_PLAY
    GAME_MODE = LOAD_PLAY
    if GAME_MODE == DO_PLAY:
        #run_n_simulations(100000)
        #human_vs_MCTS()
        MCTS_vs_MODEL(200)
        #MCTS_vs_MCTS()
    elif GAME_MODE == LOAD_PLAY:
        all_games = UT.read_games("./game_output.log")
        sampled_games = np.random.choice(all_games, 3)
        c = 0
        print(len(sampled_games))
        for index, each_item in enumerate(sampled_games):
            Game.parse_history(each_item, index)
            print(c)
