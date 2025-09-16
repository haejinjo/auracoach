from typing import Dict, Union

from .types.sex import Sex
from .types.activity_level import ActivityLevel
from .types.goal import Goal

from .get_sleep_debt_factor import get_sleep_debt_factor
from .activity.get_training_load_from_activity import get_training_load_from_activity

def get_optimal_sleep(age: int,
                          sex: Sex,
                          activity_level: ActivityLevel,
                          goal: Goal = Goal.MUSCLE_GAIN_RECOMP,
                          avg_sleep_last_7_days: float) -> Dict[str, Union[float, str]]:
    """
        Calculate optimal sleep duration using age, sex, real activity level, goal, and recent sleep patterns.
        
        Based on research for muscle growth and resistance training performance:
        - Sleep needs vary by age and sex (hormonal differences)
        - You need more sleep to recover if you have a higher activity level
        - Sleep debt must be accounted for
        
        Key Studies:
        - Dattilo et al. (2011): Sleep and muscle recovery in athletes
        - Reilly & Edwards (2007): Sleep restriction impairs muscle glycogen synthesis
        - Spiegel et al. (2009): Sleep debt and metabolic consequences
        - Mah et al. (2011): Sleep extension improves athletic performance 
        - Hirshkowitz et al. (2015): National Sleep Foundation age-based recommendations
        - Bonnet & Arand (2003): Sleep debt accumulation and recovery patterns
        - Driver & Taylor (2000): Sex differences in sleep architecture and needs
        - Fullagar et al. (2015): Sleep and athletic recovery systematic review
        - Simpson et al. (2017): Sleep and muscle protein synthesis review

        Parameters:
        - age: User's age in years
        - sex: Sex (affects hormonal recovery patterns)
        - activity_level: ActivityLevel from calories burned calculation
        - goal: Goal (muscle_gain_recomp or muscle_retain_recomp or maintain)
        - avg_sleep_last_7_days: Average sleep duration last week (from sleep tracking)
        
        Returns: Dictionary with sleep recommendations
        """
    
    # Base sleep requirement by age and sex
    # Research shows sex differences in sleep needs, especially during reproductive years
    if age < 26:
        base_sleep = 8.2 if sex == Sex.FEMALE else 8.0  # Young adults need more
    elif age < 40:
        base_sleep = 7.7 if sex == Sex.FEMALE else 7.5  # Peak years, slight female advantage
    elif age < 55:
        base_sleep = 7.6 if sex == Sex.FEMALE else 7.4  # Hormonal considerations
    else:
        base_sleep = 7.3 if sex == Sex.FEMALE else 7.1  # Post-reproductive/andropause
    
    # Goal-specific adjustments
    if goal == Goal.MUSCLE_GAIN_RECOMP:
        sleep_target += 0.3  # Additional sleep for anabolic processes
    
    # Factor in current sleep debt (objective measurement)
    debt_factor = get_sleep_debt_factor(avg_sleep_last_7_days)
    sleep_target *= debt_factor
    
    # Training load estimation from activity patterns
    training_load = get_training_load_from_activity(activity_level)
    sleep_target += training_load * 0.4  # Up to 0.4 hours additional for high training loads
    
    # Age-related efficiency adjustment (objective biological factor)
    if age > 60:
        sleep_target += 0.3  # Decreased sleep efficiency with age
    elif age > 45:
        sleep_target += 0.1  # Slight efficiency decline
    
    # Calculate range (±0.4 hours for individual biological variation)
    min_sleep = max(6.5, sleep_target - 0.4)
    max_sleep = min(9.5, sleep_target + 0.4)