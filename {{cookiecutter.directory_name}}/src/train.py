import pandas as pd
import pickle
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("data/processed_data.csv")

X = df.drop("deposit", axis=1)
y = df["deposit"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1912)

cat_cols = ["job", "marital", "education", "housing"]
num_cols = ["age", "balance", "duration", "campaign"]

one_hot_enc = make_column_transformer(
    (OneHotEncoder(handle_unknown="ignore", drop="first"),
    cat_cols),
    remainder="passthrough")
X_train = one_hot_enc.fit_transform(X_train)
X_train = pd.DataFrame(X_train, columns=one_hot_enc.get_feature_names_out())
X_test = pd.DataFrame(one_hot_enc.transform(X_test), columns=one_hot_enc.get_feature_names_out())

model = LGBMClassifier()
model.fit(X_train, y_train)

with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("models/ohe.pkl", "wb") as f:
    pickle.dump(one_hot_enc, f)