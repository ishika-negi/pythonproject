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
![Screenshot 2025-04-23 230016](https://github.com/user-attachments/assets/be9d0b27-25c2-4e1d-bb57-d16d479a209e)
![Screenshot 2025-04-23 230016](https://github.com/user-attachments/assets/a9bd9d46-1424-4875-aaa8-c3d77244b0f7)
![Screenshot 2025-04-23 225857](https://github.com/user-attachments/assets/7528a40a-197c-4bc0-aa44-10c6bde1f073)
![Screenshot 2025-04-23 225414](https://github.com/user-attachments/assets/4037a450-9f42-4caa-948a-58718bec97d2)
![Screenshot 2025-04-23 225414](https://github.com/user-attachments/assets/689964c4-65f5-440a-b320-f63fa46f9fdc)
![Screenshot 2025-04-23 224548](https://github.com/user-attachments/assets/1cada070-8884-4185-b6b1-2b50a3e225f4)






---

## 🔮 Future Enhancements

- Add department or store-level filtering
- Integrate promotions, holidays, and other exogenous variables
- Add accuracy metrics like RMSE, MAPE
- Deploy to Heroku, Streamlit Cloud, or Render

---

