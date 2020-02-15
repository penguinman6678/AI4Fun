
from model_loader import ModelBasedAgent
from policies import ModelPolicy, MCTSPolicy, RandomPolicy

class Player():
    PTYPE_HUMAN = 1
    PTYPE_AGENT = 0

    def __init__(self, str_name, str_marker, ptype=0, policy_type="MCTS"):
        self.name = str_name
        self.marker = str_marker ## in { "x" or "o"}
        self.ptype = Player.PTYPE_HUMAN  # to indicate if a player is human vs. agent

        self.policy_type = policy_type

        if ptype != Player.PTYPE_HUMAN:
            self.ptype = Player.PTYPE_AGENT
        else:
            self.policy_type = "Human"

    def initialize_from_config(self, a_dict):
        self.name = a_dict.get("name")
        self.marker = a_dict.get("marker")
        self.ptype = a_dict.get("ptype")
        self.policy_type = a_dict.get("policy_type")
        self.model_json = a_dict.get("model_json", None)
        self.model_h5 = a_dict.get("model_h5", None)
    def init_model_info(self, a_dict):
        model_dir = a_dict.get("model_dir", None)
        model_json_file = a_dict.get("model_json", None)
        model_w_file = a_dict.get("model_h5", None)
        return ModelBasedAgent(model_dir, model_w_file, model_json_file)

    def set_model_info(self, a_dict):
        self.model_obj = self.init_model_info(a_dict)
        self.model_based_policy = ModelPolicy(self.model_obj)
    def get_model_obj(self):
        return self.model_obj

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

