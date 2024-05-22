import random
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from forecast import auto_arima, forecast

# Set random seed for reproducibility
random.seed(123)

# Simulated Time Series Data
time = np.arange('2022-01-01', '2023-01-01', dtype='datetime64[W]')
value = np.sin(2 * np.pi * np.arange(1, 53) / 12) + np.random.normal(0, 0.5, 52)
ts_data = pd.Series(value, index=time)

# Data Preprocessing: Smoothing
# You can add smoothing techniques here

# Plot Simulated Time Series Data
plt.plot(ts_data)
plt.title("Simulated Time Series Data")
plt.xlabel("Year")
plt.ylabel("Value")
plt.show()

# Augmented Dickey-Fuller Test
adf_test = adfuller(ts_data)
print(adf_test)

# Auto ARIMA Model
# You might need to fine-tune the parameters for better accuracy
arima_model = auto_arima(ts_data)
print(arima_model)

# Forecasting
forecast_values = forecast(arima_model, h=12)
print(forecast_values)

# Plot Forecasted Time Series Data
plt.plot(forecast_values)
plt.title("Forecasted Time Series Data")
plt.xlabel("Year")
plt.ylabel("Value")
plt.show()

def calculate_safety_stock(avg_demand, demand_std, avg_lead_time, lead_time_std, service_level):
    """
    Calculate safety stock using the given parameters.

    Args:
    - avg_demand: Average weekly demand
    - demand_std: Standard deviation of weekly demand
    - avg_lead_time: Average lead time (days)
    - lead_time_std: Standard deviation of lead time (days)
    - service_level: Service level coefficient (safety factor)

    Returns:
    - safety_stock: Calculated safety stock
    """
    term1 = demand_std ** 2 * avg_lead_time
    term2 = lead_time_std ** 2 * avg_demand ** 2
    safety_stock = service_level * np.sqrt(term1 + term2)
    return safety_stock

def calculate_resilience_index(safety_stock, avg_lead_time):
    """
    Calculate resilience index using safety stock and average lead time.

    Args:
    - safety_stock: Safety stock level
    - avg_lead_time: Average lead time (days)

    Returns:
    - resilience_index: Calculated resilience index
    """
    resilience_index = safety_stock / avg_lead_time
    return resilience_index

# Data for Supplier A
avg_demand_A = 1000  # Average weekly demand
demand_std_A = 100  # Standard deviation of weekly demand
avg_lead_time_A = 14  # Average lead time (days)
lead_time_std_A = 2  # Standard deviation of lead time (days)
service_level = 1.96  # Service level coefficient (safety factor)

# Calculate safety stock for Supplier A
safety_stock_A = calculate_safety_stock(avg_demand_A, demand_std_A, avg_lead_time_A, lead_time_std_A, service_level)

# Calculate resilience index for Supplier A
avg_lead_time_supplier_A = 10  # Average lead time (days) for Supplier A
resilience_index_supplier_A = calculate_resilience_index(safety_stock_A, avg_lead_time_supplier_A)

print("Supplier A - Safety Stock:", safety_stock_A)
print("Supplier A - Resilience Index:", resilience_index_supplier_A)

# Data for plot
categories = ['Safety Stock', 'Resilience Index']
values = [safety_stock_A, resilience_index_supplier_A]

# Create bar plot
plt.bar(categories, values, color=['blue', 'green'])

# Add title and labels
plt.title('Supplier A Inventory Analysis')
plt.xlabel('Metrics')
plt.ylabel('Values')

# Show plot
plt.show()
