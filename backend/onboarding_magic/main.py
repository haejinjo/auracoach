from .types.goal import Goal
from .protein.get_optimal_protein import get_optimal_protein
from .sleep.get_optimal_sleep import get_optimal_sleep
from .activity.get_real_activity_level import get_real_activity_level

def get_complete_recommendation(weight_kg, avg_daily_calories_burned):
    """
    Get complete activity level and protein recommendation
    """
    activity_data = get_real_activity_level(weight_kg, avg_daily_calories_burned)
    protein_data = get_optimal_protein(weight_kg, activity_data['activity_level'], Goal.MUSCLE_GAIN_RECOMP)
    sleep_data = get_optimal_sleep(weight_kg, activity_data['activity_level'], Goal.MUSCLE_GAIN_RECOMP)

    return {
        **activity_data, # Based on real calorie burn data
        **protein_data, # Protein needs based on current weight, activity level, and goal
        **sleep_data # Sleep needs based on recent sleep and current age, sex, goal, and activity level
    }