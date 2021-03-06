"""
Game play policies can be defined here.
Policies should inherit from the abstract class Policy.
Note that original Policy code is referred from [1]
, and enhancement and modifications are enhanced
References
[1] https://github.com/boruil/Math381-Project2/blob/master/policies.py

"""

from abc import ABCMeta, abstractmethod
import random
import numpy as np
import operator
import networkx as nx
import copy
from board import Board
#from model_loader import ModelBasedAgent
import utils as UT

EPSILON = 10e-6  # Prevents division by 0 in calculation of UCT


class Policy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self, state):
        pass


class RandomPolicy(Policy):
    def move(self, state):
        """Chooses moves randomly from the legal moves in a given state"""
        legal_moves = state.legal_moves()

        idx = np.random.RandomState().randint(len(legal_moves))
        return legal_moves[idx]
        # return np.random.choice(state.legal_moves())

class ModelPolicy(Policy):
    #def __init__(self, model_dir, model_weight_file, model_json_file):
    def __init__(self, model_obj):
        
        #model_dir = model_dir
        ### "model_2020-01-09-15-15-06_BEST_SO_FAR_WITH_Early_Stop-0.90-upto2-0.924weights.h5"
        #self.model_weight_file = model_dir + model_weight_file
        #### "model_2020-01-09-15-15-06_BEST_SO_FAR_WITH_Early_Stop-0.90-upto2-0.924in_json.json"
        #self.model_json_file = model_dir + model_json_file
        self.model_agent_obj = model_obj #ModelBasedAgent(self.model_weight_file, self.model_json_file)
        self.DEBUG = True
    def set_debug(self, a_flag):
        self.DEBUG = a_flag
    def move(self, state, option_for_pred_structure=2):
        test_instance = state.convert_sequence_moves_to_vector()
        #print(test_instance) #// type of ndarray

        ## below is for regular model
        if option_for_pred_structure == 0:
            predicted_move = self.model_agent_obj.predict_proba(test_instance)[0]
        ## below is for two-tower
        elif option_for_pred_structure == 1:
            predicted_move = self.model_agent_obj.predict([test_instance, test_instance])[0]
        elif option_for_pred_structure == 2:
            # for conv2d
            x_test = test_instance.reshape(1, state.row, state.col, 1)

            predicted_move = self.model_agent_obj.predict_proba(x_test)[0]
        elif option_for_pred_structure == 3:
            # for conv2d and Two-Tower
            x_test = test_instance.reshape(1, state.row, state.col, 1)
            predicted_move = self.model_agent_obj.predict(x_test)[0]

        ####pp = self.model_agent_obj.predict_proba(test_instance)[0]
        if self.DEBUG:
            UT.print_three_arrays(test_instance[0], predicted_move, predicted_move, state.row)
        #mv_indx = np.argmax(predicted_move) + 1  # very important by adding 1
        #r, c = state.indices_to_coordinate(mv_indx)
        r, c, i_v = self.move_validate(state, predicted_move)

        #print("From MOdelPolicy\t R: %d, C:%d for index: %d\t from validate R:%d, C:%d for index:%d"
        #      % (r, c, mv_indx, r_v, c_v, i_v))

        if i_v == -1 :
            print("ModelPolicy based on Model seems not correct -- a move made was generated by the fallback, not by model")
            print("LOG for DEBUG")
            print("DEUBG" + np.round(predicted_move, decimals=2))
            print("DEBUG"+ (-predicted_move).argsort()[:])
            print("From ModelPolicy\t R:%d, C:%d for index:%d"
                  % (r_v, c_v, i_v))
        return r, c
    def move_validate(self, state, a_vec_estimated):
        legal_moves = state.legal_moves()
        ## HACK
        #best_move_from_history_rule = (1, 1)
        #if best_move_from_history_rule in legal_moves:
        #    return 1, 1, 5

        # if this is the first move, then draw a sample from dirchlet
        if len(legal_moves) == state.row * state.col:
            dri_on = False
            if dri_on:
                a_dir_prob = np.random.dirichlet(a_vec_estimated, 1)[0]
                try_outcome = np.random.multinomial(100, list(a_dir_prob))
                best_order = (-a_vec_estimated).argsort()[0]
                r, c = state.indices_to_coordinate(best_order + 1)
                ## or
            else:
                idx = np.random.randint(len(legal_moves))
                best_order = idx-1
                r, c = legal_moves[idx]  #state.indices_to_coordinate(best_order+1)
            return r, c, best_order+1

        print("^^^^^^^^^^^^^")
        print(np.around(a_vec_estimated, decimals=3))
        for best_order in (-a_vec_estimated).argsort()[:]:
            r, c = state.indices_to_coordinate(best_order+1)
            if (r,c) in legal_moves:
                return r, c, best_order+1
        # fall back
        idx = np.random.randint(len(legal_moves))
        return legal_moves[idx], -1

class MCTSPolicy(Policy):

    def __init__(self, playerObj, opponentPlayer, uct_flag=0, board=None):
        """
        Implementation of Monte Carlo Tree Search

        Creates a root of an MCTS tree to keep track of the information
        obtained throughout the course of the game in the form of a tree
        of MCTS nodes

        The data structure of a node consists of:
          - the game state which it corresponds to
          - w, the number of wins that have occurred at or below it in the tree
          - n, the number of plays that have occurred at or below it in the tree
          - expanded, whether all the children (legal moves) of the node have
            been added to the tree

        To access the node attributes, use the following format. For example,
        to access the attribute 'n' of the root node:
          policy = MCTSPolicy()
          current_node = policy.root
          policy.tree.node[current_node]['n']
        """
        self.DEBUG_POLICY = False
        self.digraph = nx.DiGraph()
        self.player = playerObj
        self.oppoent = opponentPlayer
        self.num_simulations = 0
        # Constant parameter to weight exploration vs. exploitation for UCT
        self.uct_c = np.sqrt(2)
        self.uct_flag = uct_flag

        self.node_counter = 0

        empty_board = None #Board(3, 3, 3)
        if board:
            empty_board = Board(board.row, board.col, board.number_of_connected_tobe_win)
        self.digraph.add_node(self.node_counter, attr_dict={'w': 0,
                                                            'n': 0,
                                                            'uct': 0,
                                                            'expanded': False,
                                                            'state': empty_board})
        empty_board_node_id = self.node_counter
        self.node_counter += 1

        self.last_move = None


        if playerObj.get_marker() == 'O':
            for successor in [empty_board.transition_function(*move, opponentPlayer) for move in empty_board.legal_moves()]:
                self.digraph.add_node(self.node_counter, attr_dict={'w': 0,
                                                                    'n': 0,
                                                                    'uct': 0,
                                                                    'expanded': False,
                                                                    'state': successor})
                self.digraph.add_edge(empty_board_node_id, self.node_counter)
                self.node_counter += 1

    def get_player(self):
        return self.player

    def reset_game(self):
        self.last_move = None

    def move(self, starting_state):
        # Make a copy of the starting state so that the MCTS state can't be
        # modified later from the outside
        starting_state = copy.deepcopy(starting_state)
        # todo: is that copy needed?

        starting_node = None

        if self.last_move is not None:
            # Check if the starting state is already in the graph as a child of the last move that we made
            exists = False
            for child in self.digraph.successors(self.last_move):
                # Check if the child has the same state attribute as the starting state
                if self.digraph._node[child]['state'] == starting_state:
                    # If it does, then check if there is a link between the last move and this child state
                    if self.digraph.has_edge(self.last_move, child):
                        exists = True
                        starting_node = child
            if not exists:
                # If it wasn't found, then add the starting state and an edge to it from the last move
                self.digraph.add_node(self.node_counter,
                                      attr_dict={'w': 0,
                                                 'n': 0,
                                                 'uct': 0,
                                                 'expanded': False,
                                                 'state': starting_state})
                self.digraph.add_edge(self.last_move,
                                      self.node_counter)
                starting_node = self.node_counter
                self.node_counter += 1
        else:
            for node in self.digraph.nodes():
                if self.digraph._node[node]['attr_dict']['state'] == starting_state:
                    starting_node = node
        computational_budget = 100
        for i in range(computational_budget):
            self.num_simulations += 1
            if self.DEBUG_POLICY:
                print("Running MCTS from this starting state with node id {}:\n{}".format(starting_node,
                                                                                      starting_state))

            # Until computational budget runs out, run simulated trials
            # through the tree:

            # Selection: Recursively pick the best node that maximizes UCT
            # until reaching an unvisited node
            if self.DEBUG_POLICY:
                print('================ ( selection ) ================')
            selected_node = self.selection(starting_node)
            if self.DEBUG_POLICY:
                print('selected:\n{}'.format(self.digraph._node[selected_node]['attr_dict']['state']))
                print('selected:\n{}'.format(str(selected_node)))
            # Check if the selected node is a terminal state, and if so, this
            # iteration is finished
            if self.digraph._node[selected_node]['attr_dict']['state'].winner():
                break

            # Expansion: Add a child node where simulation will start
            if self.DEBUG_POLICY:
                print('================ ( expansion ) ================')
            new_child_node = self.expansion(selected_node)
            if self.DEBUG_POLICY:
                print('Node chosen for expansion:\n{}'.format(new_child_node))
                print('Node for expansion:\n{}'.format(self.digraph._node[new_child_node]['attr_dict']['state']))
            if self.DEBUG_POLICY:
                # Simulation: Conduct a light playout
                print('================ ( simulation ) ================')
            reward = self.simulation(new_child_node)
            if self.DEBUG_POLICY:
                print('Reward obtained: {}\n'.format(reward))

            # Backpropagation: Update the nodes on the path with the simulation results
            if self.DEBUG_POLICY:
                print('================ ( backpropagation ) ================')
            self.backpropagation(new_child_node, reward)

        move, resulting_node = self.best(starting_node)
        if self.DEBUG_POLICY:
            print('MCTS complete. Suggesting move: {}\n'.format(move))

        self.last_move = resulting_node

        # If we won, reset the last move to None for future games
        if self.digraph._node[resulting_node]['attr_dict']['state'].winner():
            self.last_move = None

        return move

    def best(self, root):
        """
        Returns the action that results in the child with the highest UCT value
        (An alternative strategy could also be used, where the action leading to
        the child with the most number of visits is chosen
        """
        # Todo: explore various strategies for choosing the best action
        children = self.digraph.successors(root)

        # # Option 1: Choose the child with the highest 'n' value
        # num_visits = {}
        # for child_node in children:
        #     num_visits[child_node] = self.digraph.node[child_node]['n']
        # best_child = max(num_visits.items(), key=operator.itemgetter(1))[0]

        # Option 2: Choose the child with the highest UCT value
        uct_values = {}
        for child_node in children:
            uct_values[child_node] = self.uct(child_node)

        # Choose the child node that maximizes the expected value given by UCT
        # If more than one has the same UCT value then break ties randomly
        best_children = [key for key, val in uct_values.items() if val == max(uct_values.values())]
        idx = np.random.randint(len(best_children))
        best_child = best_children[idx]

        # Determine which action leads to this child
        action = self.digraph.get_edge_data(root, best_child)['attr_dict']['action']
        return action, best_child

    def selection(self, root):
        """
        Starting at root, recursively select the best node that maximizes UCT
        until a node is reached that has no explored children
        Keeps track of the path traversed by adding each node to path as
        it is visited
        :return: the node to expand
        """
        # In the case that the root node is not in the graph, add it
        if root not in self.digraph.nodes():
            self.digraph.add_node(self.node_counter,
                                  attr_dict={'w': 0,
                                             'n': 0,
                                             'uct': 0,
                                             'expanded': False,
                                             'state': root})
            self.node_counter += 1
            return root
        elif not self.digraph._node[root]['attr_dict']['expanded']:
            if self.DEBUG_POLICY:
                print('root in digraph but not expanded')
            return root  # This is the node to expand
        else:
            if self.DEBUG_POLICY:
                print('root expanded, move on to a child')
            # Handle the general case
            children = self.digraph.successors(root)
            uct_values = {}
            uct_bernoulli_values = {}
            for child_node in children:
                uct_values[child_node] = self.uct(state=child_node)
                uct_bernoulli_values[child_node] = self.uct_bernoulli(state=child_node)
                #print("Here in Selection\n")
                #print(self.digraph.node[child_node]['attr_dict']['state'])

            # Choose the child node that maximizes the expected value given by UCT
            best_child_node = max(uct_values.items(), key=operator.itemgetter(1))[0]
            best_child_node_bernoulli = max(uct_bernoulli_values.items(), key=operator.itemgetter(1))[0]
            # best_selection_from_bernoulli = self.selection(best_child_node_bernoulli)
            if self.uct_flag == 1:
                return self.selection(best_child_node_bernoulli)
            return self.selection(best_child_node)

    def expansion(self, node):
        # As long as this node has at least one unvisited child, choose a legal move
        children = self.digraph.successors(node)
        legal_moves = self.digraph._node[node]['attr_dict']['state'].legal_moves()
        if self.DEBUG_POLICY:
            print('Legal moves: {}'.format(legal_moves))

        # Select the next unvisited child with uniform probability
        unvisited_children = []
        corresponding_actions = []
        #print("legal moves: {}".format(legal_moves))
        for move in legal_moves:
            if self.DEBUG_POLICY:
                print('adding to expansion analysis with: {}'.format(move))
            child = self.digraph._node[node]['attr_dict']['state'].transition_function(*move, self.player)

            in_children = False
            for child_node in children:
                if self.digraph._node[child_node]['attr_dict']['state'] == child:
                    in_children = True

            if not in_children:
                unvisited_children.append(child)
                corresponding_actions.append(move)
        # Todo: why is it possible for there to be no unvisited children?
        if self.DEBUG_POLICY:
            print('unvisited children: {}'.format(len(unvisited_children)))
        if len(unvisited_children) > 0:
            idx = np.random.randint(len(unvisited_children))
            child, move = unvisited_children[idx], corresponding_actions[idx]

            self.digraph.add_node(self.node_counter,
                                  attr_dict={'w': 0,
                                             'n': 0,
                                             'uct': 0,
                                             'expanded': False,
                                             'state': child})
            self.digraph.add_edge(node, self.node_counter, attr_dict={'action': move})
            child_node_id = self.node_counter
            self.node_counter += 1
        else:
            # Todo:
            # Is this the correct behavior? The issue is, it was getting to the expansion
            # expansion method with nodes that were already expanded for an unknown reason,
            # so here we return the node that was passed. Maybe there is a case where a
            # node had been expanded but not yet marked as expanded until it got here.
            return node

        # If all legal moves are now children, mark this node as expanded.
        if len(list(children)) + 1 == len(legal_moves):
            self.digraph._node[node]['attr_dict']['expanded'] = True
            #print('node is expanded')

        return child_node_id

    def simulation(self, node):
        """
        Conducts a light playout from the specified node
        :return: The reward obtained once a terminal state is reached
        """
        random_policy = RandomPolicy()
        current_state = self.digraph._node[node]['attr_dict']['state']
        players = [self.player, self.oppoent]
        ind_current_player = 1
        # Until reaching to the end of the game, we need to take turns
        while not current_state.winner():
            move = random_policy.move(current_state)
            current_state = current_state.transition_function(*move, players[ind_current_player % 2])
            ind_current_player  += 1

        if current_state.winner() == self.player.get_marker():
            if self.DEBUG_POLICY:
                print("Winner is %s" % current_state.winner())
            return 1000
        elif current_state.winner() == self.oppoent.get_marker():
            if self.DEBUG_POLICY:
                print("Winner is opponent %s" % current_state.winner())
            return -10
        else:
            return 10

    def backpropagation(self, last_visited, reward):
        """
        Walk the path upwards to the root, incrementing the
        'n' and 'w' attributes of the nodes along the way
        """
        current = last_visited
        while True:
            self.digraph._node[current]['attr_dict']['n'] += 1
            self.digraph._node[current]['attr_dict']['w'] += reward

            if self.DEBUG_POLICY:
                print('Updating to n={} and w={}:\n{}'.format(self.digraph._node[current]['attr_dict']['n'],
                                                          self.digraph._node[current]['attr_dict']['w'],
                                                          self.digraph._node[current]['attr_dict']['state']))

            # Terminate when we reach the empty board
            if self.digraph._node[current]['attr_dict']['state'] == Board(3,3,3):
                break
            # Todo:
            # Does this handle the necessary termination conditions for both 'X' and 'O'?
            # As far as we can tell, it does

            # Will throw an IndexError when we arrive at a node with no predecessors
            # Todo: see if this additional check is no longer necessary
            try:
                current = list(self.digraph.predecessors(current))[0]
            except IndexError:
                break

    def uct(self, state):
        """
        Returns the expected value of a state, calculated as a weighted sum of
        its exploitation value and exploration value
        """
        n = self.digraph._node[state]['attr_dict']['n']  # Number of plays from this node
        w = self.digraph._node[state]['attr_dict']['w']  # Number of wins from this node
        t = self.num_simulations
        c = self.uct_c
        epsilon = EPSILON

        exploitation_value = w / (n + epsilon)
        exploration_value = c * np.sqrt(np.log(t) / (n + epsilon))


        value = exploitation_value + 1.0 * exploration_value

        if self.DEBUG_POLICY:
            print(" \ **** ")
            print('exploration_value: {}'.format(exploration_value))
            print(self.digraph.nodes()[state]['attr_dict']['state'])
            print('UCT value {:.3f} for state:\n{}'.format(value, state))
            print(" ****** / ")
        self.digraph._node[state]['uct'] = value

        return value
    def uct_bernoulli(self, state):
        """
        Returns the expected value of a state, calculated as a weighted sum of
        its exploitation value and exploration value
        """
        alpha = 0.6
        beta  = 0.1
        n = self.digraph._node[state]['attr_dict']['n']  # Number of plays from this node
        w = self.digraph._node[state]['attr_dict']['w']  # Number of wins from this node
        t = self.num_simulations
        c = self.uct_c*1.0
        epsilon = EPSILON

        exploitation_value = (w + alpha) / (n + beta) # applying the conjugacy of beta to the observations
        exploration_value = c * np.sqrt(np.log(t) / (n + epsilon))
        gamma = 0.5
        if self.DEBUG_POLICY:
            print('exploration_value: {}'.format(exploration_value))

        value = exploitation_value + exploration_value
        if self.DEBUG_POLICY:
            print('UCT value {:.3f} for state:\n{}'.format(value, state))

        self.digraph._node[state]['uct'] = value

        return value
