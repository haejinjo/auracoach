from .types.activity_level import ActivityLevel

def get_training_load_from_activity(activity_level: ActivityLevel) -> float:
    """
    Estimate training load based on activity level and calorie burn patterns.
    Higher activity levels correlate with more resistance training.
    
    Parameters:
    - activity_level: Calculated activity level
    
    Returns: Training load factor (0.0 to 1.0)
    """
    # Map activity level to estimated training intensity
    # Based on research showing calorie burn correlates with training volume
    training_factors = {
        ActivityLevel.SEDENTARY: 0.0,
        ActivityLevel.LIGHT: 0.1,
        ActivityLevel.MODERATE: 0.3,
        ActivityLevel.ACTIVE: 0.6,
        ActivityLevel.VERY_ACTIVE: 1.0
    }
    
    return training_factors[activity_level]
