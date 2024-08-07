import pandas as pd

df = pd.read_csv("data/bank.csv")

dep_mapping = {"yes": 1, "no": 0}
df["deposit"] = df["deposit"].astype("category").map(dep_mapping) # Convert the column to category and map the values
df = df.drop(labels = ["default", "contact", "day", "month", "pdays", "previous", "loan", "poutcome", "poutcome"], axis=1)

df.to_csv("data/processed_data.csv", index=False)