# Forecasting Methods in Fintech 096292

## Project Summary

### Subject: Predicting GBP/JPY Exchange Rate

### Introduction
The objective of this project is to predict the GBP/JPY closing exchange rate using various forecasting techniques. Our approach includes time series analysis and machine learning models to generate daily predictions.

### Project Details:
- **Frequency:** Daily
- **Forecasting Horizon:** One day ahead (evaluated over 80 days)
- **Data Range:** 1st October 2018 - 31st December 2023

### Features Used:
- **Market Data:** Volume, Open, High, Low, and Close prices
- **Technical Indicators:** RSI, Weighted Moving Average, Bollinger Bands
- **Capital Flows:** Nissan, Honda, Barclays, Mitsubishi Motors, Sony
- **Macroeconomic Indicators:**
  - "TONA" (Tokyo Overnight Average Rate)
  - "SONIA" (Sterling Overnight Index Average)
  - Currency Rates: USD/JPY, EUR/JPY, AUD/JPY
  - Crude Oil Prices (USD)

### Data Sources:
- **TONA/SONIA:** Official websites of respective banks
- **Other Market Data:** Dukascopy (https://www.dukascopy.com/), a Swiss banking group and broker

## Statistical Evaluation Metrics
To assess the model's performance, we employed:
- **Mean Absolute Error (MAE):** Measures the average difference between predicted and actual values.
- **Root Mean Square Error (RMSE):** Penalizes larger errors more than MAE.

## Selection of Capital Flows Based on Stock Market Correlations
We conducted correlation analysis between major stocks from Japan's **Nikkei 225** and the UK's **FTSE 100** to determine stocks most relevant to GBP/JPY exchange rate movements. The selected stocks with high correlation were:
- Nissan
- Honda
- Barclays
- Mitsubishi Motors
- Sony

This analysis is documented in **"Find Correlation between Stocks from Japan and England to our rate.ipynb."**

## Data Preprocessing
1. **Handling Missing Data:**
   - Applied forward-fill method for missing values
   - Dropped rows with unfillable NaN values
2. **Feature Engineering:**
   - Structured time series sequences with `sequence_length = 50`
   - Ensured temporal order of data to prevent data leakage
   - Standardized features using **Z-score normalization** (mean = 0, std = 1)
   - Applied normalization only to the training set to avoid data leakage

## Model Training and Overfitting Prevention
To prevent overfitting, we applied:
1. **Early Stopping:** Monitored validation loss to stop training when overfitting was detected.
2. **Dropout Layers:** Randomly dropped connections in neural networks to improve generalization.
3. **Restoring Best Weights:** Saved model weights from the best-performing epoch.

## Prediction Strategy
- Predictions were made exclusively based on training data.
- The model generated test set predictions iteratively, replacing the oldest values in the sequence with newly predicted values.

## Time Series Data Splitting Strategy
- Maintained **temporal integrity** by sequentially splitting data into training, validation, and test sets.
- Ensured **statistical property alignment** by verifying consistency in mean and variance across data splits.
- **Visualization:** Used `plot_close` function to inspect trends and fluctuations.
- **Statistical Analysis:** Used `get_statistics` to check mean, standard deviation, and other descriptive metrics.

## Model Architectures and Hyperparameter Tuning
We experimented with over **650 different LSTM architectures**, testing various hyperparameter configurations:
- **Optimization Strategies:** Learning rate tuning, batch size variations, dropout probabilities
- **Evaluation:** Compared architectures based on MAE and RMSE

## Results and Conclusion
The best-performing model achieved the following results:

**Validation Metrics:**
![image](https://github.com/user-attachments/assets/e6bca0bb-4bdc-4db1-b4b3-feaf1e6fec41)
- **Validation MSE:** 96.713
- **Validation RMSE:** 9.834
- **Validation MAE:** 6.678

![image](https://github.com/user-attachments/assets/db162f6d-cfe1-4cf1-a57e-101fc20c51cf)
**Prediction on Test Set:**
- **Test MSE:** 137.6700
- **Test RMSE:** 11.7332
- **Test MAE:** 9.4284


