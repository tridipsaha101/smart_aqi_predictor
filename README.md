# 🌍 Smart AQI Health Predictor

An AI-powered web application that predicts **Air Quality Index (AQI)** and provides **health risk assessments and recommendations** based on pollution levels. The project uses machine learning techniques and air quality datasets to help users understand environmental health risks.

---

## 📌 Features

- 📊 Predict Air Quality Index (AQI)
- 🩺 Assess health risks based on AQI levels
- 🌫️ Analyze air pollution parameters
- 📈 Interactive data visualization
- ⚡ User-friendly Streamlit web interface
- 🤖 Machine Learning-based predictions

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Pickle
- Matplotlib/Plotly

---

## 📂 Project Structure

```
AQI APP/
│
├── app.py                      # Streamlit web application
├── model.py                    # Machine learning model training script
├── merge_clean_dataset.py      # Dataset preprocessing and merging
├── risk_model.pkl              # Trained ML model
│
├── city_day.csv                # City-wise daily AQI dataset
├── city_hour.csv               # City-wise hourly AQI dataset
├── station_day.csv             # Station-wise daily AQI dataset
├── station_hour.csv            # Station-wise hourly AQI dataset
├── stations.csv                # Air quality station information
├── final_health_aqi_dataset.csv # Final processed dataset
│
└── README.md                   # Project documentation
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/Smart-AQI-Health-Predictor.git
cd Smart-AQI-Health-Predictor
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open your browser and visit:

```
http://localhost:8501
```

---

## 📊 AQI Categories

| AQI Range | Category | Health Impact |
|-----------|-----------|----------------|
| 0-50 | Good | Minimal impact |
| 51-100 | Moderate | Acceptable air quality |
| 101-150 | Unhealthy for Sensitive Groups | Breathing discomfort |
| 151-200 | Unhealthy | Increased health effects |
| 201-300 | Very Unhealthy | Serious health warnings |
| 301-500 | Hazardous | Emergency conditions |

---

## 💡 Health Recommendations

- Wear a mask during high AQI conditions.
- Avoid outdoor activities when AQI is unhealthy.
- Use air purifiers indoors.
- Stay hydrated and monitor respiratory symptoms.
- Sensitive groups should take extra precautions.

---

## 📈 Dataset Sources

- City-wise AQI Data
- Station-wise AQI Data
- Air Pollution Monitoring Stations
- Processed Health-AQI Dataset

---

## 🔮 Future Enhancements

- Real-time AQI API integration
- Location-based predictions
- AQI forecasting using time-series models
- Personalized health recommendations
- Mobile application deployment

---

## 👨‍💻 Author

**Tridip Saha**  
B.Sc. in Data Science Student  
Aspiring Data Analyst | Machine Learning Enthusiast | Web Developer

---

## 📜 License

This project is licensed under the MIT License.

⭐ If you found this project useful, please give it a star on GitHub!
