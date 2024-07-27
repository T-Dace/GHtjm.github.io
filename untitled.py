import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pmdarima import auto_arima

# Load the dataset
df = pd.read_csv('C:/Users/tjohn/Desktop/PROJECTS/World Population Growth - Python/The_World_Bank_Population_growth_(annual_).csv')


# Melt the dataframe to convert years to a single column
df_melted = pd.melt(df, id_vars=['country_name', 'country_code'], 
                    var_name='year', value_name='growth_rate')

# Convert year to integer
df_melted['year'] = df_melted['year'].astype(int)

# Display basic information
print(df_melted.info())
print(df_melted.describe())

# Check for missing values
print(df_melted.isnull().sum())

# Plot overall growth rate trend
plt.figure(figsize=(12, 6))
df_melted.groupby('year')['growth_rate'].mean().plot()
plt.title('Average World Population Growth Rate')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.show()

# Plot top 10 countries by average growth rate
top_10 = df_melted.groupby('country_name')['growth_rate'].mean().nlargest(10)
sns.barplot(x=top_10.index, y=top_10.values)
plt.title('Top 10 Countries by Average Growth Rate')
plt.xticks(rotation=45)
plt.ylabel('Average Growth Rate')
plt.show()

# Heatmap of growth rates
pivot_df = df_melted.pivot(index='country_name', columns='year', values='growth_rate')
plt.figure(figsize=(20, 10))
sns.heatmap(pivot_df, cmap='YlOrRd')
plt.title('Population Growth Rates by Country and Year Heatmap')
plt.show()


#ARIMA 1

# Pick any country
country = 'United States'
country_data = df_melted[df_melted['country_name'] == country].set_index('year')['growth_rate']

# Check for stationarity
result = adfuller(country_data)
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

# Fit the ARIMA model
model = ARIMA(country_data, order=(1,1,1))
results = model.fit()
print(results.summary())

# Forecast the future growth rates
forecast_steps = 5
forecast = results.forecast(steps=forecast_steps)

# Create a continuous year range
all_years = range(country_data.index.min(), country_data.index.max() + forecast_steps + 1)

# Plot
plt.figure(figsize=(15, 8))

# Plot the historical data
plt.plot(country_data.index, country_data.values, label='Historical')

# Plot the forecast
forecast_years = range(country_data.index.max() + 1, country_data.index.max() + forecast_steps + 1)
plt.plot(forecast_years, forecast.values, color='red', label='Forecast')

# Set the x-axis limits
plt.xlim(1961, all_years[-1])

# Format the x-axis ticks
plt.xticks(range(1961, all_years[-1] + 1, 5))  # Ticks every 5 years

plt.title(f'{country} Growth Rate Forecast')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Rotate and align the tick labels for better presentation
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Print the last few historical values and the forecast
print("\nLast few historical values:")
print(country_data.tail())
print("\nForecast values:")
print(forecast)


#exponential curving

# Pick a country
country = 'United States'
country_data = df_melted[df_melted['country_name'] == country].set_index('year')['growth_rate']

# Fit an Exponential Smoothing model
model = ExponentialSmoothing(country_data, trend='add', seasonal=None)
results = model.fit()

# Forecast the future growth rates
forecast_steps = 5
forecast = results.forecast(forecast_steps)

# Plot
plt.figure(figsize=(15, 8))

# Plot historical data
plt.plot(country_data.index, country_data.values, label='Historical')

# Plot the forecast
forecast_years = range(country_data.index.max() + 1, country_data.index.max() + forecast_steps + 1)
plt.plot(forecast_years, forecast.values, color='red', label='Forecast')

# Set the x-axis limits
plt.xlim(1961, forecast_years[-1])

# Format the x-axis ticks
plt.xticks(range(1961, forecast_years[-1] + 1, 5))  # Ticks every 5 years

plt.title(f'{country} Growth Rate Forecast (Exponential Smoothing)')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Rotate and align the tick labels for better presentation
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Print the last few historical values and the forecast
print("\nLast few historical values:")
print(country_data.tail())
print("\nForecast values:")
print(forecast)

# Print model parameters
print("\nModel Parameters:")
print(f"Alpha (level): {results.params['smoothing_level']}")
print(f"Beta (trend): {results.params['smoothing_trend']}")


#auto arima
# Select a specific country for analysis
country = 'United States'
country_data = df_melted[df_melted['country_name'] == country].set_index('year')['growth_rate']

# Automatically find the best ARIMA parameters
auto_model = auto_arima(country_data, start_p=0, start_q=0, max_p=5, max_q=5, m=1,
                        start_P=0, seasonal=False, d=None, D=None, trace=True,
                        error_action='ignore', suppress_warnings=True, stepwise=True)

print(auto_model.summary())

# Forecast future growth rates
forecast_steps = 5
forecast = auto_model.predict(n_periods=forecast_steps)

# Create a year range for the forecast
last_historical_year = country_data.index[-1]
forecast_years = range(last_historical_year + 1, last_historical_year + forecast_steps + 1)

# Plot
plt.figure(figsize=(15, 8))

# Plot historical data
plt.plot(country_data.index, country_data.values, label='Historical')

# Plot forecast
plt.plot(forecast_years, forecast, color='red', label='Forecast')

# Set x-axis limits
plt.xlim(1961, forecast_years[-1])

# Format x-axis ticks
plt.xticks(range(1961, forecast_years[-1] + 1, 5))  # Ticks every 5 years

plt.title(f'{country} Growth Rate Forecast (Auto ARIMA)')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Rotate and align the tick labels so they look better
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Print the last few historical values and the forecast
print("\nLast few historical values:")
print(country_data.tail())
print("\nForecast values:")
print(forecast)
