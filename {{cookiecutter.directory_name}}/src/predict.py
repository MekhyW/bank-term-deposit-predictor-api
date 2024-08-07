import pandas as pd
import pickle

df = pd.read_csv("data/bank.csv")
df.to_csv("data/bank_predict.csv", index=False)
df = pd.read_csv("data/bank_predict.csv")

X = df.drop("deposit", axis=1)
df["y_pred"] = 0
y = df["y_pred"]

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/ohe.pkl", "rb") as f:
    one_hot_enc = pickle.load(f)
    
X = one_hot_enc.transform(X)
X = pd.DataFrame(X, columns=one_hot_enc.get_feature_names_out())

y_pred = model.predict(X)
df["y_pred"] = y_pred
df["y_pred"] = df["y_pred"].map({1: "yes", 0: "no"})

df.to_csv("data/bank_predict.csv", index=False)