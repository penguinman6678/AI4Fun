

class Player():
    PTYPE_HUMAN = 1
    PTYPE_AGENT = 0
    def __init__(self, str_name, str_marker, ptype=0):
        self.name = str_name
        self.marker = str_marker ## in { "x" or "o"}
        self.ptype = Player.PTYPE_HUMAN  # to indicate if a player is human vs. agent
        if ptype != Player.PTYPE_HUMAN:
            self.ptype = Player.PTYPE_AGENT

        self.movements = []


    def __str__(self):
        return "Player: " + self.get_marker()

    def add_movement(self, indx_in_board):
        self.movements.append(indx_in_board)

    def get_movements(self):
        return self.movements
    def get_marker(self):
        return self.marker
    def get_player_type(self):
        return self.ptype