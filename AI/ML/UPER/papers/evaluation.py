# From Article 3

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

def calculate_smape(y_true, y_pred):
    """
    Calculate Symmetric Mean Absolute Percentage Error (SMAPE)
    Formula: 100/n * sum(|y_pred - y_true| / ((|y_true| + |y_pred|)/2))
    """
    numerator = np.abs(y_pred - y_true)
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    # Avoid division by zero
    smape = np.mean(numerator / np.maximum(denominator, 1e-8)) * 100
    return smape

def evaluate_metrics(y_true, y_pred):
    """
    Section 3.2: Model Performance Evaluation
    Calculate and print the 4 error metrics mentioned in the paper:
    MAE, RMSE, MAPE, and SMAPE.
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100 # Expressed as percentage
    smape = calculate_smape(y_true, y_pred)
    
    print(f"Model Performance Evaluation:")
    print(f"MAE   : {mae:.4f}")
    print(f"RMSE  : {rmse:.4f}")
    print(f"MAPE  : {mape:.4f}%")
    print(f"SMAPE : {smape:.4f}%")
    return {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'SMAPE': smape
    }

def plot_prediction_results(y_true, y_pred, time_index=None):
    """
    Figure 2: Prediction Results Using XGBoost
    Line chart comparing actual vs predicted values over time.
    """
    plt.figure(figsize=(12, 6))
    if time_index is None:
        time_index = np.arange(len(y_true))
        
    plt.plot(time_index, y_true, label='Aktual', color='#1f77b4') 
    plt.plot(time_index, y_pred, label='Prediksi', color='#ff7f0e', linestyle='--')
    plt.title('Hasil Prediksi Demand Menggunakan XGBoost')
    plt.xlabel('Indeks Waktu')
    plt.ylabel('Jumlah Penjualan')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_error_distribution(y_true, y_pred):
    """
    Figure 4: Error Distribution
    Histogram of the errors (Actual - Predicted).
    """
    errors = y_true - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=50, color='#1f77b4')
    plt.title('Distribusi Error')
    plt.axvline(x=0, color='r', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_error_vs_prediction(y_true, y_pred):
    """
    Figure 5: Error vs Prediction Results
    Scatter plot of predicted values vs errors.
    """
    errors = y_true - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, errors, alpha=0.6, color='#7fb3d5')
    plt.axhline(y=0, color='r', linestyle='-', alpha=0.7)
    plt.title('Error vs Prediksi')
    plt.xlabel('Prediksi')
    plt.ylabel('Error (Actual - Prediction)')
    plt.tight_layout()
    plt.show()

def plot_absolute_error_over_time(y_true, y_pred, time_index=None):
    """
    Figure 6: Absolute Error Against Time
    Line chart of absolute errors over time.
    """
    absolute_errors = np.abs(y_true - y_pred)
    
    plt.figure(figsize=(12, 6))
    if time_index is None:
        time_index = np.arange(len(absolute_errors))
        
    plt.plot(time_index, absolute_errors, color='#1f77b4')
    plt.title('Absolute Error terhadap Waktu')
    plt.xlabel('Indeks Waktu')
    plt.ylabel('Absolute Error')
    plt.tight_layout()
    plt.show()

def plot_feature_importance(model, feature_names=None):
    """
    Figure 7: Feature Importance
    Bar chart showing the importance of each feature in the XGBoost model.
    """
    # This expects an XGBoost model or any sklearn-compatible model with feature_importances_
    if not hasattr(model, 'feature_importances_'):
        raise ValueError("Model does not have feature_importances_ attribute.")
        
    importance = model.feature_importances_
    
    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(len(importance))]
        
    # Sort features by importance
    sorted_idx = np.argsort(importance)[::-1]
    sorted_importance = importance[sorted_idx]
    sorted_features = np.array(feature_names)[sorted_idx]
    
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_features, sorted_importance, color='#1f77b4')
    plt.title('Feature Importance')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def run_full_evaluation(y_true, y_pred, model=None, feature_names=None, time_index=None):
    """
    Runs all evaluation steps from the paper sequentially.
    """
    print("--- 1. Evaluating Metrics ---")
    metrics = evaluate_metrics(y_true, y_pred)
    
    print("\n--- 2. Generating Plots ---")
    plot_prediction_results(y_true, y_pred, time_index)
    plot_error_distribution(y_true, y_pred)
    plot_error_vs_prediction(y_true, y_pred)
    plot_absolute_error_over_time(y_true, y_pred, time_index)
    
    if model is not None:
        plot_feature_importance(model, feature_names)
    else:
        print("\nNote: Model not provided, skipping Feature Importance plot.")
        
    return metrics

if __name__ == "__main__":
    # Example mock execution to test the functions
    print("Running example evaluation with mock data...")
    np.random.seed(42)
    y_true_mock = np.random.poisson(100, 200)
    y_pred_mock = y_true_mock + np.random.normal(0, 15, 200)
    
    class MockModel:
        feature_importances_ = np.array([0.38, 0.14, 0.08, 0.08, 0.06, 0.06, 0.06, 0.05, 0.05])
        
    mock_features = ['lag_1', 'dayofweek', 'estoque', 'lag_7', 'month', 'year', 'lag_14', 'day', 'preco']
    
    run_full_evaluation(y_true_mock, y_pred_mock, model=MockModel(), feature_names=mock_features)
