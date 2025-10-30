import pandas as pd
from datetime import timedelta
import joblib
import os

# Load model once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "Electricity_consumption_model.pkl"))

# Feature engineering function
def add_datetime_features(df):
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    return df

# Forecast function
def forecast_power(df_input, minutes_ahead=30):
    df_input = add_datetime_features(df_input.copy())
    
    # Add missing lag features
    for lag in ['lag_1', 'lag_2', 'lag_3']:
        if lag not in df_input.columns:
            df_input[lag] = 0.0

    predictions = []
    current_features = df_input.copy()

    for _ in range(minutes_ahead):
        # Select columns in order expected by the model
        X_input = current_features[['Global_reactive_power', 'Voltage', 'Global_intensity',
                                    'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3',
                                    'year', 'month', 'day', 'hour', 'day_of_week',
                                    'lag_1', 'lag_2', 'lag_3']]

        # Predict next value
        pred_power = model.predict(X_input)[0]
        predictions.append(pred_power)

        # Update features for next iteration
        current_features['Global_reactive_power'] = pred_power
        current_features['timestamp'] = current_features['timestamp'] + timedelta(minutes=1)
        current_features = add_datetime_features(current_features)

    # Prepare result DataFrame
    df_predictions = pd.DataFrame({
        'minute_ahead': range(1, minutes_ahead + 1),
        'predicted_power_kW': predictions,
        'predicted_current_A': [p / df_input['Voltage'].iloc[0] for p in predictions]
    })

    return df_predictions

# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    # Dummy input
    df_test = pd.DataFrame({
        "Global_reactive_power": [4.216],
        "Voltage": [234.84],
        "Global_intensity": [18.4],
        "Sub_metering_1": [0.0],
        "Sub_metering_2": [1.0],
        "Sub_metering_3": [17.0],
        "timestamp": [pd.Timestamp("2025-10-30 14:30")]
    })

    result = forecast_power(df_test, minutes_ahead=30)
    # print(result)
