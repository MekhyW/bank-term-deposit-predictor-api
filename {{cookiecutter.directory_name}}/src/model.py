import pickle

def load_model():
    with open("../models/model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

def load_encoder():
    with open("../models/ohe.pkl", "rb") as f:
        encoder = pickle.load(f)
    return encoder