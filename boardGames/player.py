

class Player():
    PTYPE_HUMAN = 1
    PTYPE_AGENT = 0
    def __init__(self, str_name, str_marker, ptype=0, policy_type="MCTS"):
        self.name = str_name
        self.marker = str_marker ## in { "x" or "o"}
        self.ptype = Player.PTYPE_HUMAN  # to indicate if a player is human vs. agent

        if ptype != Player.PTYPE_HUMAN:
            self.ptype = Player.PTYPE_AGENT
        self.policy_type = policy_type


        #self.movements = []


    def __str__(self):
        return "Player: " + self.get_marker()
    def get_policy_mode(self):
        return self.policy_type

    def get_marker(self):
        return self.marker
    def get_player_type(self):
        return self.ptype
    def reset(self):
        self.__init__(self.name, self.marker, self.ptype)

