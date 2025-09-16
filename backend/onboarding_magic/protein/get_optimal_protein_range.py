from .types.activity_level import ActivityLevel
from .types.goal import Goal
from .activity.get_real_activity_level import get_real_activity_level

def get_optimal_protein(weight_kg, activity_level: ActivityLevel, goal: Goal):
    """
        Calculate optimal protein intake based on weight, activity level, and goal.
        
        Research Foundation:
        - Sedentary adults: 0.8g/kg (RDA minimum for nitrogen balance)
        - Active individuals: 1.2-1.6g/kg for endurance, 1.6-2.2g/kg for strength training
        - Muscle protein synthesis peaks at ~1.6g/kg but benefits continue to ~2.2-2.4g/kg
        - Muscle gain: Higher protein supports anabolic processes and training adaptations
        - Muscle retention: Adequate protein prevents catabolism during maintenance/cutting
        - Individual variation: ±0.4g/kg accounts for genetic differences in protein utilization
        
        Key Studies:
        - Helms et al. (2014): 1.8-2.7g/kg for physique athletes
        - Morton et al. (2018): Meta-analysis showing 1.6g/kg optimizes muscle protein synthesis
        - Antonio et al. (2014-2020): High protein (>2.2g/kg) safe and potentially beneficial
        - Phillips & Van Loon (2011): Activity-dependent protein requirements
        - Pasiakos et al. (2015): Protein needs during energy deficit
        - Jäger et al. (2017): ISSN position stand on protein and exercise
        - Campbell et al. (2007): Protein intake and lean body mass in older adults
        - Tang et al. (2009): Muscle protein synthesis response to protein intake
        - Witard et al. (2014): Protein dose-response in resistance-trained individuals
        
        Algorithm Logic:
        - Base multiplier scales with activity level (calorie burn indicates training volume/intensity)
        - Muscle gain goal adds 0.2g/kg for enhanced anabolic signaling
        - Range accounts for individual genetic variation in protein metabolism
        - Upper limit prevents excessive intake while maximizing benefits
        
        Parameters:
        - weight_kg: User's weight in kilograms (lean body mass proxy)
        - activity_level: ActivityLevel Enum from get_real_activity_level() 
                        (objective measure based on calories burned per kg bodyweight)
        - goal: Goal Enum (muscle_gain_recomp or muscle_retain_recomp or maintain)
                - muscle_gain_recomp: Building new muscle tissue (anabolic priority)
                - muscle_retain_recomp: Maintaining muscle during maintenance/deficit
        
        Returns: 
        Dictionary with protein recommendations:
        - protein_multiplier: Base g/kg multiplier used
        - min_protein_g: Lower bound of optimal range
        - max_protein_g: Upper bound of optimal range  
        - protein_range_g: Formatted string range for user display
        """

    # Map activity level to protein multiplier (g per kg body weight)
    activity_dependent_protein_multipliers = {
        ActivityLevel.SEDENTARY: 0.8,
        ActivityLevel.LIGHT: 1.2,
        ActivityLevel.MODERATE: 1.6,
        ActivityLevel.ACTIVE: 2.0,
        ActivityLevel.VERY_ACTIVE: 2.4
    }
    protein_multiplier = activity_dependent_protein_multipliers[activity_level]

    # Adjust multiplier based on goal
    if goal == Goal.MUSCLE_GAIN_RECOMP:
        protein_multiplier += 0.2
    # For muscle_retain_recomp, no change

    # Calculate protein range
    min_protein = weight_kg * protein_multiplier
    max_protein = weight_kg * (protein_multiplier + 0.4)

    return {
        'protein_multiplier': protein_multiplier,
        'min_protein_g': int(min_protein),
        'max_protein_g': int(max_protein),
        'protein_range_g': f"{int(min_protein)}-{int(max_protein)}g"
    }
