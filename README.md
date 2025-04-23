# 🧠 Sales Forecasting Dashboard using Prophet & Dash

An interactive and dynamic web dashboard built using **Dash** and **Prophet** for forecasting **weekly sales** based on historical data. The dashboard features various forecast visualizations and allows users to select custom date ranges for live updates.

---

## 📌 Project Overview

This project visualizes and forecasts retail sales data using the **Facebook Prophet** time series forecasting library. With a stylish UI built in **Dash**, users can:
- View weekly sales forecasts
- Analyze sales trends and seasonality
- Compare forecasted vs. actual sales
- Select custom date ranges for dynamic forecast updates

---

## 📁 Data Requirements and Sources

- `train.csv` – Contains historical weekly sales with `Date`, `Store`, and `Weekly_Sales`.
- `stores.csv` – Optional metadata about stores. Handled gracefully if missing.

All date values are converted to Prophet-friendly format:
- `Date` → `ds`
- `Weekly_Sales` → `y`

---

## 🔧 Tools & Technologies

- **Python**
- **Facebook Prophet** – Forecasting
- **Dash** & **Plotly** – Web dashboard and visualizations
- **Pandas** – Data manipulation

---

## 🚀 Features

- 📆 **Interactive Date Picker** to control the forecast range
- 📊 **Main Forecast Tab** showing predictions with confidence intervals
- 📉 **Trend Analysis Tab** to examine overall trends
- 🌦 **Yearly Seasonality Tab** showing seasonal patterns
- 🔁 **Forecast vs Actual** comparison
- 🌙 **Dark Mode UI** with rich, modern visuals

---

## 🔍 How it Works

1. **Load and preprocess data**:
   - Rename and aggregate weekly sales by date.
   - Convert `Date` to datetime format for Prophet compatibility.
2. **Initialize Prophet**:
   - Fit on the filtered data based on the date range.
   - Generate 52 weeks of future data.
3. **Visualize**:
   - Forecast results
   - Trend component
   - Yearly seasonality
   - Forecast vs. actual comparison

---

## 🛠️ Installation & Running Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/sales-forecast-dashboard.git
   cd sales-forecast-dashboard
   ```

2. **Install Dependencies**:
   ```bash
   pip install pandas prophet dash plotly
   ```

3. **Add your data**:
   - Place `train.csv` (mandatory) and `stores.csv` (optional) in the project directory.

4. **Run the App**:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:8050
   ```

---

## 📸 Dashboard Preview
![image](https://github.com/user-attachments/assets/e1016e7e-fb6c-407f-8ac8-04028bd0aeb8)







---

## 🔮 Future Enhancements

- Add department or store-level filtering
- Integrate promotions, holidays, and other exogenous variables
- Add accuracy metrics like RMSE, MAPE
- Deploy to Heroku, Streamlit Cloud, or Render

---

