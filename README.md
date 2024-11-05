# Battery Arbitrage Strategies

This repository contains example strategies for optimizing battery storage arbitrage. These examples demonstrate how to determine when to sell stored energy based on variables like state of charge (SOC), time of day, and future price forecasts.

## Example Strategies

### 1. Basic SOC Protection

The simplest strategy protects battery life by increasing sell prices as the battery depletes:

```python
min_soc = 5  # Minimum safe state of charge
battery_cost_per_cycle = 0.20  # Example cost per cycle

# Basic protection - price rises as battery depletes
distance_from_charged = 100 * (1 + pow((100 - battery_soc) / (100 - min_soc), 2))

# With wear cost included
distance_from_charged_with_wear = distance_from_charged * battery_cost_per_cycle
```

### 2. Time-Based Pricing

Consider time of day for peak pricing periods:

```python
# Simple peak/off-peak
min_sell_price = base_price * (1.5 if interval_time.hour < 22 and interval_time.hour >= 16 else 1.0)

# More granular based on forecast
peak_buy_price = max(buy_forecast[0:8])  # Look ahead 8 hours
min_sell_price = max(distance_from_charged, peak_buy_price * 0.95)  # Allow for efficiency loss
```

### 3. Arbitrage Opportunity 

When SOC is low but profitable buying opportunity exists:

```python
if battery_soc < 30:
    min_future_buy = min(buy_forecast)  # Lowest upcoming buy price
    sell_revenue = sell_price * 0.95    # Account for round-trip efficiency
    
    if sell_revenue > min_future_buy + distance_from_charged:
        min_sell_price = min_future_buy / 0.95  # Adjust minimum to allow profitable trade
```

## Available Parameters

These examples use various input parameters that might be available from your system:

### Core Pricing 
- `buy_price`: Current buying price (c/kWh)
- `sell_price`: Current feed-in tariff (c/kWh)
- `min_sell_rrp`: Minimum wholesale price to consider selling
- `approx_battery_charge_cost`: Estimated cost to fully charge
- `soc_prod`: Current SOC-based price multiplier

### Battery Status
- `battery_soc`: Current state of charge (%)
- `battery_charge`: Current charge (Wh)
- `battery_capacity`: Total capacity (Wh)

### Forecasting
- `buy_forecast`: Array of future buy prices (c/kWh)
- `sell_forecast`: Array of future sell prices (c/kWh)

### System Metrics
- `house_power`: Current house consumption (W)
- `grid_power`: Grid power flow (W)
- `solar_power`: Current solar production (W)

### Time Context
- `interval_time`: Current time interval
- `sunrise`/`sunset`: Daily sun times

## Example Decision Flows

### 1. Simple Time-of-Day Strategy
```python
def simple_export_decision(interval_time, sell_price, min_sell_price):
    """Basic strategy focusing on peak evening hours"""
    if interval_time.hour >= 16 and sell_price > min_sell_price:
        return 'export'
    return 'idle'
```

### 2. SOC-Aware Strategy
```python
def soc_aware_decision(battery_soc, sell_price, buy_forecast):
    """Considers battery level and future buying opportunities"""
    if battery_soc < 30:
        min_buy = min(buy_forecast)
        if sell_price * 0.95 > min_buy:  # Including efficiency loss
            return 'export'
    return 'idle'
```

### 3. Forecast-Based Strategy
```python
def forecast_based_decision(sell_price, buy_forecast, battery_soc):
    """Uses price forecasts to optimize timing"""
    peak_price = max(buy_forecast[0:8])  # Next 8 hours
    current_margin = sell_price - buy_forecast[0]
    
    if current_margin > 0 and battery_soc > 20:
        if sell_price > peak_price * 0.8:  # Within 20% of peak
            return 'export'
    return 'idle'
```

## Contributing

These examples can be improved in many ways:

- More sophisticated battery wear modelling
- Better forecast integration strategies
- Solar production optimization
- Dynamic time-of-day adjustments
- Grid stability considerations
- Weather forecast integration
- Dynamic efficiency calculations

Pull requests are welcome!

Note: All prices in examples are in cents per kilowatt-hour (c/kWh) unless otherwise specified.
