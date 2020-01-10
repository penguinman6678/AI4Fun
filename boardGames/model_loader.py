
from keras.models import model_from_json
import json

import sys
from os import path

class ModelBasedAgent():
    def __init__(self, filename_for_model, filename_for_json):
        if not path.exists(filename_for_model):
            print("%s does not exist. Check again"
                  % (filename_for_model))
            sys.exit(1)
        if filename_for_model.strip().split(".")[-1] != "h5":
            print("%s does not seem to be h5 format -- no h5 as file extension"
                  % (filename_for_model))
            sys.exit(1)

        self.model = None
        json_from_file = open(filename_for_json, 'r')
        loaded_model_json = json_from_file.read()
        json_from_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights(filename_for_model)

    def get_model(self):
        return self.model
    def predict(self, avec):
        return self.model.predict(avec)
    def predict_proba(self, avec):
        return self.model.predict_proba(avec)


