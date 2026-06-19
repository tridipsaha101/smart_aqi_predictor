import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("final_health_aqi_dataset.csv")

X = df[['aqi','outdoor_hours','age','asthma']]
y = df['risk']

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "risk_model.pkl")

print("Model trained & saved successfully")