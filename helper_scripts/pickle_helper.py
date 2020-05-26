import os
import pickle
from config import output_directory


def load_pickle(pickle_key):
    path = output_directory + "/" + pickle_key + ".p"
    if os.path.isfile(path):
        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except Exception:  # so many things could go wrong, can't be more specific.
                pass
    return None


def save_pickle(object_to_save, pickle_key):
    path = output_directory + "/" + pickle_key + ".p"
    pickle.dump(object_to_save, open(path, "wb"))
