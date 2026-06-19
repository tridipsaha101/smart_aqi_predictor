import pandas as pd
import glob
import random

files = glob.glob("*.csv")
df_list = []

for f in files:
    df = pd.read_csv(f)
    df.columns = [c.lower().strip() for c in df.columns]

    # Possible AQI column names
    aqi_cols = ['aqi', 'air_quality_index', 'pm2.5', 'pm25', 'pm_2_5', 'pm10']

    found = None
    for col in aqi_cols:
        if col in df.columns:
            found = col
            break

    if found:
        temp = df[[found]].copy()
        temp.rename(columns={found: 'aqi'}, inplace=True)
        df_list.append(temp)

final_df = pd.concat(df_list, ignore_index=True)

# Drop invalid values
final_df = final_df.dropna()
final_df = final_df[(final_df['aqi'] > 0) & (final_df['aqi'] < 600)]

# Generate synthetic health data
data = []
for aqi in final_df['aqi']:
    outdoor = random.randint(1,6)
    age = random.randint(10,70)
    asthma = random.choice([0,1])

    # Risk logic
    if aqi < 50:
        risk = 0
    elif aqi < 100:
        risk = 1
    elif aqi < 200:
        risk = 2
    else:
        risk = 3

    data.append([aqi, outdoor, age, asthma, risk])

final = pd.DataFrame(data, columns=['aqi','outdoor_hours','age','asthma','risk'])

final.to_csv("final_health_aqi_dataset.csv", index=False)

print("FINAL DATASET CREATED: final_health_aqi_dataset.csv")