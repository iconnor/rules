min_soc = 5  # This is an option min state of charge as a safety limit to prevent deep discharge
distance_from_charged = 100 * (1 + pow((100 - battery_soc) / (100 - min_soc), 2))

min_sell_price = distance_from_charged * approx_battery_charge_cost

if battery_soc < 30:
    # Current potential sell revenue
    sell_revenue = sell_price * 0.9  # Assuming 90% round-trip efficiency

    # Find cheapest buy price in next 7 hours
    min_buy_price = min(buy_forecast)

    # If we can sell high now and buy back lower, might still want to export
    if sell_revenue > min_buy_price:
        # Modify our minimum sell price to be more lenient
        min_sell_price = min_buy_price / 0.9  # Account for efficiency loss

if interval_time.hour > 16 or interval_time.hour < 8:
    if action == 'export' and sell_price < min_sell_price:
        action = 'auto'
        reason = 'west: auto if sell price less than soc pow(1.3) factor'

if interval_time.hour >= 16 and sell_price > min_sell_price:
    action = 'export'
