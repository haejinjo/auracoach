
def get_sleep_debt_factor(avg_sleep_last_7_days: float) -> float:
    """
    Calculate sleep debt multiplier based on recent sleep patterns.
    Research shows sleep debt accumulates and requires additional recovery sleep.
    
    Parameters:
    - avg_sleep_last_7_days: Average hours of sleep per night over last 7 days (objective data from sleep tracking)
    
    Returns: Multiplier for additional sleep needed (1.0 = no debt, >1.0 = debt exists)
    """
    optimal_baseline = 7.5  # Research-backed baseline for most adults
    
    if avg_sleep_last_7_days >= optimal_baseline:
        return 1.0  # No sleep debt
    elif avg_sleep_last_7_days >= 6.5:
        return 1.1  # Mild debt
    elif avg_sleep_last_7_days >= 5.5:
        return 1.15  # Moderate debt
    else:
        return 1.2  # Significant debt
