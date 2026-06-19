# pip install --upgrade xgboost
# Pip 21.3+ is required : pip install xgboost

# 1- import des librairies
import seaborn as sns
import pandas as pd

# 2- import des données
df = sns.load_dataset('mpg').dropna()
X = df.drop(columns=['mpg'])
y = df['mpg']

# 3- data processing 
X = pd.get_dummies(X, drop_first=True)

# 4- split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# 5- train XGBoost regressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

"""
# Pour classification : 
from xgboost import XGBClassifier
model = XGBClassifier(n_estimators=2, max_depth=2, learning_rate=1, objective='binary:logistic') # create model instance 
"""

model = xgb.XGBRegressor(objective='reg:squarederror',
                         n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f'RMSE: {rmse:.3f}')
print(f'R²: {r2:.3f}')

# 6- hyperparameter tuning - optimization 
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

grid_search = GridSearchCV(
    estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)


# 7- feature plotting - see the important ones
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

importance = model.get_booster().get_score(importance_type='weight')

importance_df = pd.DataFrame({
    'Feature': list(importance.keys()),
    'Importance': list(importance.values())
}).sort_values(by='Importance', ascending=False)

top_n = 20
plt.figure(figsize=(10, 8))
plt.barh(
    importance_df['Feature'].head(top_n)[::-1],
    importance_df['Importance'].head(top_n)[::-1],
    color='skyblue'
)
plt.xlabel('Importance Score')
plt.title(f'Top {top_n} Feature Importance')
plt.tight_layout()
plt.show()