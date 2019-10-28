"""
Experimental class to be implemented, after design...
"""

class Component():
    def __init__(self):
        self.sequence_of_cells = []
        self.direction = None
    def add_cell(self, r, c, direction_str):
        if self.direction == None:
            self.direction = direction_str
        self.sequence_of_cells.append((r,c))

    def get_cells(self):
        return self.sequence_of_cells
    def is_single_component(self):
        return len(self.sequence_of_cells) == 1
    def get_direction_helper(self, r_ind, c_ind):
        last_r_idx, last_c_indx = self.sequence_of_cells[-1]
        if Board.is_connected(last_r_idx, last_c_indx, r_ind, c_ind) == True:
            # direction -- right diagonal, left diagonal, horizontal, vertical
            # Check RD
            if r_ind - last_r_idx == 1 and c_ind - last_c_indx == 1:
                return "RD"
            elif r_ind - last_r_idx == 1 and c_ind == last_c_indx:
                return "VT"
            elif r_ind == last_r_idx and c_ind- last_c_indx == 1:
                return "HT"
    def get_direction(self, r_index, c_index):
        if self.direction == "Single":
            pass

