# 📊 Forecasting Methods in Fintech

## 🧠 Project Summary

### 🎯 Subject: Predicting GBP/JPY Exchange Rate

---

### 📌 Introduction

The goal of this project is to forecast the **GBP/JPY closing exchange rate** using a combination of **time series analysis** and **machine learning models**. Our approach focuses on daily predictions based on historical market data, technical indicators, and macroeconomic features.

---

### 🔍 Project Details

- **Data Frequency:** Daily
- **Forecasting Horizon:** One day ahead (evaluated over 80 days)
- **Date Range:** 1st October 2018 – 31st December 2023

---

### 📈 Features Used

- **Market Data:**
  - Volume, Open, High, Low, and Close prices
- **Technical Indicators:**
  - RSI, Weighted Moving Average, Bollinger Bands
- **Capital Flows:**
  - Stock prices of Nissan, Honda, Barclays, Mitsubishi Motors, Sony
- **Macroeconomic Indicators:**
  - TONA (Tokyo Overnight Average Rate)
  - SONIA (Sterling Overnight Index Average)
  - Currency rates: USD/JPY, EUR/JPY, AUD/JPY
  - Crude Oil Prices (USD)

---

### 🗂️ Data Sources

- **TONA / SONIA:** Official websites of respective central banks
- **Market Data:** [Dukascopy](https://www.dukascopy.com/) (Swiss banking group and broker)

---

## 📏 Evaluation Metrics

To evaluate model performance, we used the following metrics:

- **Mean Absolute Error (MAE):** Measures average absolute difference between predictions and actual values.
- **Root Mean Square Error (RMSE):** Penalizes larger errors more heavily, emphasizing outliers.

---

## 🔄 Capital Flow Selection via Correlation Analysis

We analyzed correlations between major stocks from Japan's **Nikkei 225** and the UK's **FTSE 100** to identify companies most correlated with GBP/JPY movements.

The selected stocks:
- Nissan
- Honda
- Barclays
- Mitsubishi Motors
- Sony

📁 *See:* `Find Correlation between Stocks from Japan and England to our rate.ipynb`

---

## 🧹 Data Preprocessing

1. **Handling Missing Values**
   - Forward-fill method applied
   - Rows with unfillable NaNs were dropped

2. **Feature Engineering**
   - Constructed time series sequences with `sequence_length = 50`
   - Maintained chronological order to prevent data leakage
   - Standardized features using **Z-score normalization** (mean = 0, std = 1)
   - Normalization applied only to the training set to avoid leakage

---

## 🏋️ Model Training & Overfitting Prevention

To ensure robust training and avoid overfitting:

1. **Early Stopping**
   - Training halted when validation loss stopped improving

2. **Dropout Layers**
   - Randomly disabled neurons to enhance generalization

3. **Best Weight Restoration**
   - Restored weights from the epoch with the best validation performance

---

## 🔁 Prediction Strategy

- The model was trained solely on the training data.
- Test predictions were generated in a **rolling fashion**, replacing the oldest time step with each new prediction.

---

## ⏱️ Time Series Splitting Strategy

- Data was **sequentially** split into training, validation, and test sets to preserve temporal structure.
- Ensured alignment of statistical properties (mean, variance) across splits.

### Tools:
- `plot_close`: Visualized closing price trends
- `get_statistics`: Verified distribution consistency

---

## 🧪 Model Architecture & Hyperparameter Tuning

We explored **over 650 LSTM architectures** by varying hyperparameters such as:

- Learning rate
- Batch size
- Dropout probability

Models were evaluated based on MAE and RMSE to identify the best configuration.

---

## 📊 Results & Conclusion

The best-performing model achieved the following metrics:

### ✅ Validation Performance

![Validation Metrics](https://github.com/user-attachments/assets/e6bca0bb-4bdc-4db1-b4b3-feaf1e6fec41)

- **MSE:** 96.713  
- **RMSE:** 9.834  
- **MAE:** 6.678  

---

### 🧾 Test Set Performance

![Test Prediction](https://github.com/user-attachments/assets/db162f6d-cfe1-4cf1-a57e-101fc20c51cf)

- **MSE:** 137.6700  
- **RMSE:** 11.7332  
- **MAE:** 9.4284  
---

## ✅ Conclusions

This project demonstrates the effectiveness of using time series modeling and LSTM-based neural networks to forecast the GBP/JPY exchange rate. Through careful data preprocessing, thoughtful feature engineering, and extensive experimentation with over 650 LSTM architectures, we were able to build a model that generalizes well despite the complexities of financial data.

Key takeaways include:

- Incorporating macroeconomic indicators and capital flow features (e.g., stock correlations) improved model performance by capturing broader economic patterns.
- Maintaining temporal integrity throughout the pipeline (e.g., sequential data splitting, rolling prediction windows) was essential to avoid data leakage and ensure realistic evaluation.
- Hyperparameter tuning had a significant impact on results. Dropout rate, batch size, and learning rate were especially influential.
- The final model achieved a **Validation MAE of 6.678** and a **Test MAE of 9.428**, demonstrating strong predictive capabilities over an 80-day test window.

While the model didn't perfectly capture all fluctuations, it effectively followed general trends. With more data, additional feature engineering, and model ensemble techniques, future work could further improve accuracy.
This project lays a solid foundation for real-world forecasting in fintech applications and showcases the power of combining statistical rigor with deep learning techniques.

---

## 📌 Final Notes

This repository includes both code and documentation.  
For a quick overview of the implementation, use the lightweight version of the notebook.  
To dive into all experiments and results, refer to the full notebook.

---

Feel free to reach out for questions or collaboration!
