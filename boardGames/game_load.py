import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import matplotlib.animation as animation

## belows are for libs cooked by me
from board import Board
from draw_board import Draw
from player import Player
import utils as UT


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
    for each_game in games:
        a_player = each_game.get("winner")
        winning_count[a_player] = winning_count.get(a_player) + 1



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


def draw_heat_map(aMat, T):
    mycmap = sns.cm.rocket_r
    ax = sns.heatmap(np.true_divide(aMat, T), linewidth=0.1, cmap=mycmap)
    ax.text(0.35, 1.05, ("Sample size: %d" % T), transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=dict(boxstyle="round", fc="white", ec="black", pad=0.2))
    # plt.show()


C = 0


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


if __name__ == "__main__":
    file_name = sys.argv[1]
    #analyze_game(file_name)
    # print(first_move_stats_dict)
    # print(a)

    # below is working
    animation_heatmap(file_name)
