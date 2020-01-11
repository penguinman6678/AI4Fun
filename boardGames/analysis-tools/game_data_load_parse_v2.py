import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sys.path.insert(0, "/Users/chihoon/works/mlBooks/introML/simple_template/AI4Fun/boardGames/")
import matplotlib.animation as animation

## belows are for libs cooked by me
from board import Board
from draw_board import Draw
from player import Player
import utils as UT


C = 0

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
    draw_board_obj.write_text(("Winner is:  %s" % (winner)))
    draw_board_obj.exit_on_click()




def analyze_game(file_name):
    games = UT.read_games(file_name)
    winning_count = {}
    for i  in range(len(games)):
        each_game = games[i]
        a_player = each_game.get("winner")
        winning_count[a_player] = winning_count.get(a_player, 0) + 1
    move_tree = build_session_second_degree(games)
    return winning_count, move_tree

def build_session_second_degree(games):

    move_tree ={}
    for each_game in games:
        # analyze the subsequent movements
        moves = each_game.get('sequence')
        winner = each_game.get('winner')
        weight = 1

        for each_move_i in range(len(moves)-2):
            curr_turn = moves[each_move_i].get("turn")
            next_turn = moves[each_move_i+1].get("turn")
            curr_move = tuple(moves[each_move_i].get("xy"))
            next_move = tuple(moves[each_move_i+1].get("xy"))
            next_next_move = tuple(moves[each_move_i+2].get("xy"))
            discount = 1 if next_turn == winner else 0

            if curr_move in move_tree:
                if next_move in move_tree[curr_move]:
                    if next_next_move in move_tree[curr_move][next_move]:
                        move_tree[curr_move][next_move][next_next_move] += (weight*discount)
                    else:
                        move_tree[curr_move][next_move][next_next_move] = (weight*discount)
                else:
                    move_tree[curr_move][next_move]={next_next_move:weight*discount}
            else:
                move_tree[curr_move] = {next_move:{next_next_move:(weight*discount)}}

    return sorted(move_tree.items(), key=lambda item: item[0])

def build_session_first_degree(games):

    move_tree ={}
    for each_game in games:
        # analyze the subsequent movements
        moves = each_game.get('sequence')
        winner = each_game.get('winner')
        weight = 1

        for each_move_i in range(len(moves)-1):
            curr_turn = moves[each_move_i].get("turn")
            next_turn = moves[each_move_i+1].get("turn")
            curr_move = tuple(moves[each_move_i].get("xy"))
            next_move = tuple(moves[each_move_i+1].get("xy"))
            discount = 1 if next_turn == winner else 0
            if curr_move in move_tree:
                if next_move in move_tree[curr_move]:
                    move_tree[curr_move][next_move] += (weight*discount)
                else:
                    move_tree[curr_move][next_move] = (weight*discount)
            else:
                move_tree[curr_move] = {next_move:(weight*discount)}

    return sorted(move_tree.items(), key=lambda item: item[0])

def init_second_degree(move_tree, T):
    two_level_dict = {}
    count = 0
    for i in range(T):
        each_starting = move_tree[i]
        curr_move = each_starting[0]
        next_moves_given_curr_move =  list(each_starting[1].keys())
        next_next_moves_given_opponent = list(each_starting[1].values())
        for each_next in next_moves_given_curr_move:
            k = (curr_move, each_next)
            v = each_starting[1][each_next]
            two_level_dict[k] = v
            count += 1
    return sorted(two_level_dict.items(), key=lambda item: item[0]), count

def draw_sequences_heatmap(move_tree, opt_id= 1):
    fig = plt.figure()
    move_next_next_tree = None
    T = len(move_tree)
    if opt_id == 2:
        move_next_next_tree, T = init_second_degree(move_tree, T)

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)

    A = 0
    def animate(i):
        each_starting = move_tree[i]
        plt.clf()
        a = np.zeros((3,3))
        count_local = 0
        current_move = each_starting[0]
        plt.title(str(current_move))
        for k, v in each_starting[1].items():
            r, c = k[0], k[1]
            a[r][c] = v
        count_local = sum(list(each_starting[1].values()))
        sample_flag = False
        draw_heat_map(a, count_local)

    def animate_second_degree(i, move_next_next_tree):
        each_curr_next = move_next_next_tree[i]
        curr_next = each_curr_next[0]
        a = np.zeros((3,3))
        plt.clf()
        #for each_next_next, each_next_next_possible_moves_dict in .items():
        total_c = 0
        for next_next_move, w in sorted(each_curr_next[1].items(), key=lambda item: item[0]):
            r, c = next_next_move
            a[r][c] = w
            total_c += w
        draw_heat_map(a,total_c, str(curr_next))

    if opt_id == 1:
        anim = animation.FuncAnimation(fig, animate, frames=T, interval=5)
        anim.save('sub_sequent_move.mp4', writer=writer)
    elif opt_id == 2:
        anim = animation.FuncAnimation(fig, animate_second_degree, fargs=(move_next_next_tree,),
                                       frames=T, interval=5)
        anim.save('sub_sub_sequent_move.mp4', writer=writer)
    print("Total frames: %d" % (T))

"""
below function is deprecated by function animation_heatmap
"""
def analyze_game_first_move_working_version_for_heatmap_animation(file_name):
    a = np.zeros((3, 3))
    games = UT.read_games(file_name)
    first_move_stats_dict = {}
    T = 0

    m = 0
    fig = plt.figure()
    for each_game in games:
        if each_game.get("winner") != "D":
            r, c = each_game.get("sequence")[0].get("xy")
            rc_move = (r, c)
            first_move_stats_dict[rc_move] = first_move_stats_dict.get(rc_move, 0) + 1
            a[r][c] += 1
            T += 1
            if m % 10 == 0:
                draw_heat_map(a, T)
                plt.draw()
                plt.pause(0.01)
                plt.clf()

    print("Total Count: %d" % T)
    plt.show()
    # plt.imshow(a, cmap='hot', interpolation='nearest')

    return first_move_stats_dict, a



def draw_heat_map(aMat, T, text_msg= None):
    mycmap = sns.cm.rocket_r
    ax = sns.heatmap(np.true_divide(aMat, T), linewidth=0.1, cmap=mycmap)
    if text_msg != None:
        ax.text(0.35, 1.05, str(text_msg), transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=dict(boxstyle="round", fc="white", ec="black", pad=0.2))



def animation_heatmap(file_name):
    a = np.zeros((3, 3))
    games = UT.read_games(file_name)
    games_win_by_O = []
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    T = len(games)
    focused_result = "O"
    fig = plt.figure()

    skip_by = 1
    c_ = 0
    for each_game in games:
        if each_game.get("winner") == focused_result:  # and c_ % skip_by == 0 :
            games_win_by_O.append(each_game)
            c_ += 1

    T = len(games_win_by_O)

    def animate(i):
        global C
        each_game = games_win_by_O[i]  # games[i]
        #print("focused player: %s, this_game_player: %s" % (focused_result, each_game.get("winner")))

        plt.clf()

        if each_game.get("winner") == focused_result:
            r, c = each_game.get("sequence")[0].get("xy")
            a[r][c] += 1
            C += 1
            draw_heat_map(a, C)


    anim = animation.FuncAnimation(fig, animate, frames=T, interval=10)
    anim.save('first_move_winningRate_animation.mp4', writer=writer)
    print("Total Win: %d" % C)
    # plt.show()


def visualize_historical_games(filename):
    for each_game in UT.read_games(file_name):
        parse_history(each_game)

def parse_data_example(filename):
    # games is a list, an array, where each cell in the array holds a dictionary format for each game per line from the filename
    games = UT.read_games(filename)
    winning_count = {}
    x_wins = 0
    o_wins = 0
    ties = 0

    winning_count_dict = {}

    for i  in range(len(games)):
        ## each i holds a game log, which is represented in a dictionary format
        each_game = games[i]
        # once you have a dictionary obj, you can retrieve a value for a key by
        # adict.get("mykey") <-- adict is a dictionary obj; "mykey" is a key name000
        player_winner = each_game.get("winner")


        winning_count_dict[player_winner] = winning_count_dict.get(player_winner, 0) + 1

        if player_winner == "X":
            x_wins+=1
        elif player_winner == "O":
            o_wins += 1
        elif player_winner == "D":
            ties += 1

        game_sequence_in_list = each_game.get("sequence")
        play_modes = each_game.get("play_modes")

        print("Winner is: %s. First move: %s." % (player_winner, game_sequence_in_list[0].get("turn")))
    print("X win-rate:", winning_count_dict.get("X")/len(games))
    print("O win-rate:", o_wins/len(games))
    print("Draw rate:", ties/len(games))

def parse_jsons_example(filename):
    # games is a list, an array, where each cell in the array holds a dictionary format for each game per line from the filename
    games_in_jsons = UT.read_games(filename)
    list_of_dic = []
    training_samples =[]
    weight_of_lost_samples_from_x = 10
    weight_of_winning_samples_from_o = 20
    move_to_prevent_losing = []
    move_to_enhance_winning = []
    for i  in range(len(games_in_jsons)):
        # TO-DO
        # 1) create an-empty list for init-game
        # 2) create list of list

        dict_move_set = {}
        dict_move_set["move_sequence"] = None
        dict_move_set["player_winner"] = None

        individual_sequence = ["_"] * 9
        list_of_individual_sequence = []

        ## each i holds a game log, which is represented in a dictionary format
        each_game_in_a_json = games_in_jsons[i]
        # once you have a dictionary obj, you can retrieve a value for a key by
        # adict.get("mykey") <-- adict is a dictionary obj; "mykey" is a key name000

        player_winner = each_game_in_a_json.get("winner")
        moves_in_sequence_per_game = each_game_in_a_json.get("sequence")

        copy_list = individual_sequence[:]
        list_of_individual_sequence.append(updated_list_parse(copy_list))

        for each_move_dict in range(len(moves_in_sequence_per_game)):

            #list_of_individual_sequence.append(individual_sequence)
            turn_for_this_move = moves_in_sequence_per_game[each_move_dict].get("turn")
            move_made_for_this_move = moves_in_sequence_per_game[each_move_dict].get("position")
            # for this game and movements so far, a list is created... and then
            # need to be appended to the list of list
            individual_sequence[move_made_for_this_move - 1] = turn_for_this_move
            copy_list = individual_sequence[:]
            current_state = updated_list_parse(copy_list)
            list_of_individual_sequence.append(current_state)

            # for moves from each game, we can generate training data for player O
            # every even index from the sequence is for player O, except 0
            if player_winner == "O":
                if each_move_dict > 0 and each_move_dict % 2 == 1:
                    # then each_move_dict-1 is x; and each_move_dict is y indices
                    x = list_of_individual_sequence[-2]
                    y = list_of_individual_sequence[-1]
                    multi_y = np.subtract(y, x)
                    a_max = np.amax(multi_y)
                    multi_y = np.true_divide(multi_y, a_max).astype(int)
                    training_samples.append((x, y, multi_y))
            
        # Now we can collect another data by replacing a winning position made by X with O
        # that is, final third position becomes x; and the final postion made by X becomes Y
        # we can work on the "list_of_individual_sequence", not above for loop
        if player_winner == "X":
            x = list_of_individual_sequence[-3]
            ## y_1 will contains 2 and 1 -- 2 for O and 1 for X;
            ## so we only need to find a position of 1 for y
            y_1 = list_of_individual_sequence[-1] 
            multi_y = np.subtract(y_1, x)
            final_position_made_by_x = np.where(multi_y == 1)[0][0]
            y = x[:]
            y[final_position_made_by_x] = 2
            multi_y = get_multi_class_format(x, y)
            move_to_prevent_losing.append((x, y, multi_y))
            for a_weight in range(weight_of_lost_samples_from_x):
                training_samples.append((x, y, multi_y))

        # Now I can add more weight to winner of "O" for the last two movements
        # to let the game know the winning position explicitly
        if player_winner == "O":
            x = list_of_individual_sequence[-2]
            y = list_of_individual_sequence[-1]
            multi_y = get_multi_class_format(x, y)
            for a_weight in range(weight_of_winning_samples_from_o):
                training_samples.append((x, y, multi_y))

        dict_move_set["player_winner"] = player_winner
        dict_move_set["move_sequence"] = list_of_individual_sequence
        #(list_of_individual_sequence)
        list_of_dic.append(dict_move_set)
    return list_of_dic, training_samples

def get_multi_class_format(x, y):
    multi_y = np.subtract(y, x)
    a_max = np.amax(y)
    multi_y = np.true_divide(multi_y, a_max).astype(int)
    return multi_y

def updated_list_parse(individualSequence):

    for count in range(len(individualSequence)):
        if individualSequence[count] == "_":
            individualSequence[count] = 0
        elif individualSequence[count] == "X":
            individualSequence[count] = 1
        elif individualSequence[count] =="O":
            individualSequence[count] = 2

    return individualSequence


def select_games_winning(a_list_of_dict, a_target_winner="O"):
    sub_set = []
    for each_game_log in a_list_of_dict:
        if each_game_log.get('player_winner') == a_target_winner:
            sub_set.append(each_game_log)
    return sub_set

def print_sequence_for_a_game(aDict):
    for each_move in aDict.get("move_sequence", None):
        print(each_move)
        print(np.reshape(each_move, (3, 3)))
def print_training_samples(alist, file_out_name=None):
    if file_out_name:
        import sys
        sys.stdout = open(file_out_name, "w+")
    for each_sample in alist:
        print(",".join(map(str, each_sample[0]))+"\t"+
        ",".join(map(str, each_sample[1])) + "\t"+
        ",".join(map(str, each_sample[2]))
        )
if __name__ == "__main__":
    file_name = sys.argv[1]
    #parse_data_example(file_name)
    list_of_dict_for_games, training_samples = parse_jsons_example(file_name)
    #sub_set_by_O = select_games_winning(list_of_dict_for_games ,"X")
    #print_sequence_for_a_game(sub_set_by_O[2])
    #print(len(sub_set_by_O))
    print_training_samples(training_samples, "./testing_write_for_training.txt")
