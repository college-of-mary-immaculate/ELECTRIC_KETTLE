import math

# Temperature
def cold(current_temp):
    if current_temp <= 20:
        return 1
    elif 20 < current_temp <= 40:
        return (40 - current_temp) / 20
    else:
        return 0

def warm(current_temp):
    if 30 <= current_temp <= 50:
        return (current_temp - 30) / 20
    elif 50 < current_temp <= 70:
        return (70 - current_temp) / 20
    else:
        return 0

def hot(current_temp):
    if current_temp >= 80:
        return 1
    elif 60 <= current_temp < 80:
        return (current_temp - 60) / 20
    else:
        return 0

# Define membership functions for desired temperature
def low(desired_temp):
    if desired_temp <= 40:
        return 1
    elif 40 < desired_temp <= 60:
        return (60 - desired_temp) / 20
    else:
        return 0

def medium(desired_temp):
    if 50 <= desired_temp <= 65:
        return (desired_temp - 50) / 15
    elif 65 < desired_temp <= 80:
        return (80 - desired_temp) / 15
    else:
        return 0

def high(desired_temp):
    if desired_temp >= 90:
        return 1
    elif 70 <= desired_temp < 90:
        return (desired_temp - 70) / 20
    else:
        return 0

# Amount of water (in liters)
def little(amount_of_water):
    if amount_of_water <= 0.3:
        return 1
    elif 0.3 < amount_of_water <= 0.5:
        return (0.5 - amount_of_water) / 0.2
    else:
        return 0

def slightly_enough(amount_of_water):
    if 0.4 <= amount_of_water <= 0.6:
        return (amount_of_water - 0.4) / 0.2
    elif 0.6 < amount_of_water <= 1.0:
        return (1.0 - amount_of_water) / 0.4
    else:
        return 0

def enough(amount_of_water):
    if 0.9 <= amount_of_water <= 1.5:
        return (amount_of_water - 0.9) / 0.6
    elif 1.5 < amount_of_water <= 2.0:
        return (2.0 - amount_of_water) / 0.5
    else:
        return 0

def plenty(amount_of_water):
    if 1.8 <= amount_of_water <= 2.5:
        return (amount_of_water - 1.8) / 0.7
    elif 2.5 < amount_of_water <= 3.0:
        return (3.0 - amount_of_water) / 0.5
    else:
        return 0

def full(amount_of_water):
    if amount_of_water >= 2.8:
        return 1
    elif 2.5 <= amount_of_water < 2.8:
        return (amount_of_water - 2.5) / 0.3
    else:
        return 0

# Needed time (in minutes)
def short_time(needed_time):
    if needed_time <= 5:
        return 1
    elif 5 < needed_time <= 10:
        return (10 - needed_time) / 5
    else:
        return 0

def medium_time(needed_time):
    if 7 <= needed_time <= 15:
        return (needed_time - 7) / 8
    elif 15 < needed_time <= 20:
        return (20 - needed_time) / 5
    else:
        return 0

def long_time(needed_time):
    if needed_time >= 20:
        return 1
    elif 15 <= needed_time < 20:
        return (needed_time - 15) / 5
    else:
        return 0

def fuzzy_rules_extended_five(current_temp, desired_temp, amount_of_water):
    cold_level = cold(current_temp)
    warm_level = warm(current_temp)
    hot_level = hot(current_temp)

    low_level = low(desired_temp)
    medium_level = medium(desired_temp)
    high_level = high(desired_temp)

    # Fuzzy levels for the amount of water 
    little_level = little(amount_of_water)
    slightly_enough_level = slightly_enough(amount_of_water)
    enough_level = enough(amount_of_water)
    plenty_level = plenty(amount_of_water)
    full_level = full(amount_of_water)

    power_low = max(
        min(cold_level, low_level, little_level),
        min(warm_level, medium_level, slightly_enough_level),
        min(hot_level, low_level, little_level), 
        0.1  
    )

    power_medium = max(
        min(cold_level, medium_level, slightly_enough_level),
        min(warm_level, high_level, enough_level),
        min(hot_level, medium_level, enough_level),
        0.2
    )

    power_high = max(
        min(cold_level, high_level, enough_level),
        min(warm_level, high_level, plenty_level),
        min(hot_level, high_level, full_level),
        0.3  
    )

    return power_low, power_medium, power_high

def defuzzify(power_low, power_medium, power_high):
    if power_low + power_medium + power_high == 0:
        return 0  
    power = (power_low * 20 + power_medium * 50 + power_high * 80) / (power_low + power_medium + power_high)
    
    return max(power, 1)
