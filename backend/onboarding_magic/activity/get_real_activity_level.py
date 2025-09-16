def get_real_activity_level(weight_kg, avg_daily_burn_last_30_days):
    """
    Determine activity level based on calories burned per kg of body weight
    
    Parameters:
    - weight_kg: User's weight in kilograms
    - avg_daily_burn_last_30_days: Average daily calories burned from activity in last 30 days
    
    Returns: Dictionary with activity level 
    """
    
    # Calculate calories burned per kg of body weight
    calories_per_kg = avg_daily_calories_burned / weight_kg
    
    # Classify based on research-backed thresholds
    if calories_per_kg < 3:
        activity_level = "Sedentary"
    elif calories_per_kg < 6:
        activity_level = "Lightly Active"
    elif calories_per_kg < 10:
        activity_level = "Moderately Active"
    elif calories_per_kg < 15:
        activity_level = "Very Active"
    else:  # >= 15 calories/kg
        activity_level = "Athlete/Extreme"
    
    return {
        'activity_level': activity_level,
    }
