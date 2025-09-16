# WIP might need to make an API call

# takes in number of days and user timezone
# returns average of total daily burn in this period starting from today
def get_avg_daily_burn(daily_burns, days, timezone):
    """
    Calculate average daily calorie burn over a specified number of days.
    Research shows that average daily burn is a key metric for assessing activity level.
    
    Parameters:
    - daily_burns: List of tuples (date, calories burned) for each day
    - days: Number of days to average over (e.g., 30)
    - timezone: User's timezone for accurate date handling
    
    Returns: Average daily calories burned over the period
    """
    from datetime import datetime, timedelta
    import pytz

    # Get today's date in user's timezone
    user_tz = pytz.timezone(timezone)
    today = datetime.now(user_tz).date()
    
    # Calculate the start date
    start_date = today - timedelta(days=days - 1)
    
    # Filter burns within the date range and sum calories
    total_burn = 0
    count_days = 0
    for date_str, calories in daily_burns:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if start_date <= date <= today:
            total_burn += calories
            count_days += 1
    
    # Avoid division by zero
    if count_days == 0:
        return 0.0
    
    avg_daily_burn = total_burn / count_days
    return avg_daily_burn