#  From article 1

import pandas as pd 
import numpy as np 
from statsmodels.tsa.arima.model import ARIMA 
import matplotlib.pyplot as plt  

# Simulated daily demand dataset 
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D') 
data  =  100  +  np.sin(np.arange(len(dates))  /  20)  * 10 + np.random.normal(0, 5, len(dates)) 
df = pd.DataFrame({'Date': dates, 'Demand': data}) 
df.set_index('Date', inplace=True) 

# Fit ARIMA model
model = ARIMA(df['Demand'], order=(5,1,0)) 
model_fit = model.fit()  
# Forecast next 30 days 
forecast = model_fit.forecast(steps=30) 

# Plot results 
plt.figure(figsize=(10,4)) 
plt.plot(df.index, df['Demand'], label='Observed') 
plt.plot(pd.date_range(df.index[-1], periods=31, freq='D')[1:], forecast, label='Forecast', color='red') 
plt.legend() 
plt.title('Inventory Demand Forecast using ARIMA') 
plt.show() 