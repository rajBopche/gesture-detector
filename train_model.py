import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("gesture_dataset.csv")

X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier()

model.fit(X, y)

joblib.dump(model, "gesture_model.pkl")

print("Model trained")