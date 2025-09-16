def calculate_initial_deficit(
    current_weight_kg, 
    current_bf_pct,
    goal_weight_kg, 
    goal_bf_pct,
    goal_date, 
    sex,
    estimated_tdee
):
    """
    Calculate personalized caloric deficit based on latest research and body composition.
    
    This algorithm incorporates findings from recent meta-analyses and studies on optimal
    fat loss while preserving muscle mass. Key research improvements over conservative approaches:
    
    
    ALGORITHM STRENGTHS
    ============================================
    Body composition focus: Calculates fat loss rather than just weight loss
    Sex-specific considerations: Different BF% thresholds for males vs females
    Minimum calorie protection: Uses lean mass (25 kcal/kg) + absolute minimums
    Timeline realism: Flags unrealistic goals and extends timelines appropriately
    Fat mass energy availability: Considers metabolic constraints of available fat
    
    RESEARCH-BASED IMPROVEMENTS:
    ============================
    Primary metric: Weekly weight loss percentage (0.5-0.7% optimal range)
    500 kcal maximum: Research-backed threshold, not arbitrary caps
    Less conservative BF% limits: Aligned with actual muscle loss risk data
    Nuanced warning system: Green/Yellow/Red zones based on weekly loss rates
    Body recomposition recognition: Deficits <300 kcal flagged for potential muscle gain

    Primary Research Findings:
    - Murphy et al. (2021): Energy deficits >500 kcal/day significantly impair lean mass gains
    - Garthe et al. (2011): 0.7% weekly weight loss optimizes muscle retention vs 1.4% weekly loss
    - Longland et al. (2016): 2.4g protein/kg bodyweight superior to 1.2g/kg during deficits
    - Helms et al. (2021): 0.5-1.0% weekly weight loss recommended for resistance-trained athletes
    - Stronger by Science analysis (2024): Body fat % should guide deficit aggressiveness
    
    Key Thresholds Applied:
    - 500 kcal/day: Critical threshold above which muscle loss accelerates significantly
    - 0.5-0.7% weekly weight loss: Optimal range for fat loss with muscle preservation
    - Body fat scaling: Higher BF% allows more aggressive deficits without muscle loss risk
    
    Parameters:
    -----------
    current_weight_kg : float
        Current body weight in kilograms
    current_bf_pct : float
        Current body fat percentage (1-50)
    goal_weight_kg : float
        Target body weight in kilograms
    goal_bf_pct : float
        Target body fat percentage
    goal_date : datetime or None
        Target completion date (None for optimal timeline)
    sex : str
        'male' or 'female'
    estimated_tdee : int
        Total Daily Energy Expenditure in calories
        
    Returns:
    --------
    dict : Comprehensive deficit calculation with research-based recommendations
    
    Research Citations:
    ------------------
    - Murphy, C. et al. (2021). Energy deficiency impairs resistance training gains
    - Garthe, I. et al. (2011). Effect of two different weight-loss rates on body composition
    - Longland, T. et al. (2016). Higher protein during energy deficit promotes lean mass
    - Helms, E. et al. (2021). Achieving optimal fat loss phase in resistance-trained athletes
    """
    from datetime import datetime
    
    # Calculate current body composition
    current_lean_mass_kg = current_weight_kg * (1 - current_bf_pct/100)
    current_fat_mass_kg = current_weight_kg * (current_bf_pct/100)
    
    # Calculate goal body composition
    goal_lean_mass_kg = goal_weight_kg * (1 - goal_bf_pct/100)
    goal_fat_mass_kg = goal_weight_kg * (goal_bf_pct/100)
    
    # Calculate required FAT loss (not just weight loss)
    fat_to_lose_kg = current_fat_mass_kg - goal_fat_mass_kg
    fat_to_lose_lbs = fat_to_lose_kg * 2.205
    
    def get_weekly_loss_target(bf_pct, sex):
        """
        Calculate safe weekly weight loss as % of bodyweight based on research.
        
        Based on Garthe et al. (2011) and Stronger by Science analysis:
        - Higher BF% allows more aggressive deficits
        - 0.7% weekly is optimal for most individuals
        - Very lean individuals should be more conservative
        """
        if sex == 'male':
            if bf_pct >= 20:
                return 0.007  # 0.7% per week - research optimal
            elif bf_pct >= 15:
                return 0.006  # 0.6% per week
            elif bf_pct >= 12:
                return 0.005  # 0.5% per week
            else:
                return 0.004  # 0.4% per week - contest lean
        else:  # female
            if bf_pct >= 28:
                return 0.007  # 0.7% per week
            elif bf_pct >= 25:
                return 0.006  # 0.6% per week
            elif bf_pct >= 22:
                return 0.005  # 0.5% per week
            else:
                return 0.004  # 0.4% per week
    
    def get_max_safe_deficit(bf_pct, fat_mass_kg, tdee, sex):
        """
        Calculate maximum safe deficit using research-based thresholds.
        
        Primary limit: 500 kcal/day (Murphy et al. 2021 critical threshold)
        Secondary limits: Body fat availability and TDEE percentage
        """
        # Research-based 500 kcal threshold with BF% scaling
        if sex == 'male':
            if bf_pct >= 20:
                base_limit = 500  # Full research threshold
            elif bf_pct >= 15:
                base_limit = 450  # 90% of threshold
            elif bf_pct >= 12:
                base_limit = 400  # 80% of threshold
            else:
                base_limit = 300  # Very lean - conservative
        else:  # female
            if bf_pct >= 28:
                base_limit = 500
            elif bf_pct >= 25:
                base_limit = 450
            elif bf_pct >= 22:
                base_limit = 400
            else:
                base_limit = 300
        
        # Fat mass energy availability (22 kcal/lb fat/day - metabolic constraint)
        fat_mass_lbs = fat_mass_kg * 2.205
        max_from_fat = fat_mass_lbs * 22
        
        # TDEE percentage safety (max 25% to maintain metabolic function)
        max_from_tdee = tdee * 0.25
        
        # Use most restrictive limit for safety
        return min(base_limit, max_from_fat, max_from_tdee)
    
    # Calculate research-based targets
    optimal_weekly_loss_rate = get_weekly_loss_target(current_bf_pct, sex)
    max_safe_deficit = get_max_safe_deficit(current_bf_pct, current_fat_mass_kg, estimated_tdee, sex)
    
    # Calculate optimal deficit based on weekly loss rate
    optimal_weekly_loss_kg = current_weight_kg * optimal_weekly_loss_rate
    optimal_daily_deficit = (optimal_weekly_loss_kg * 2.205 * 3500) / 7  # Convert to daily calories
    
    # Timeline-based calculations
    if goal_date:
        today = datetime.now().date()
        weeks_to_goal = (goal_date - today).days / 7
        
        # Calculate required deficit for timeline
        required_daily_deficit = (fat_to_lose_lbs * 3500) / (weeks_to_goal * 7)
        required_weekly_loss_rate = (fat_to_lose_kg / weeks_to_goal) / current_weight_kg
        
        # Determine deficit strategy and risk level
        if required_daily_deficit > max_safe_deficit:
            # Exceeds research-based maximum
            deficit = max_safe_deficit
            deficit_type = 'max_safe_limited'
            realistic_weeks = (fat_to_lose_lbs * 3500) / (max_safe_deficit * 7)
            risk_level = 'high_risk_timeline'
            warnings = [
                f'Timeline requires {required_daily_deficit:.0f} kcal/day deficit (exceeds {max_safe_deficit:.0f} kcal research maximum)',
                f'Extended to {realistic_weeks:.0f} weeks to preserve muscle mass',
                f'Original timeline would likely cause significant muscle loss'
            ]
            
        elif required_weekly_loss_rate > 0.010:  # >1.0% weekly
            # Exceeds 1% weekly - high muscle loss risk
            deficit = min(required_daily_deficit, max_safe_deficit)
            deficit_type = 'high_risk'
            risk_level = 'red_zone'
            warnings = [
                f'Timeline requires {required_weekly_loss_rate*100:.1f}% weekly weight loss (research recommends <1.0%)',
                'High risk of muscle loss - consider extending timeline',
                'Requires perfect adherence to training and protein targets'
            ]
            
        elif required_weekly_loss_rate > 0.007:  # >0.7% weekly
            # Above optimal but manageable
            deficit = required_daily_deficit
            deficit_type = 'aggressive'
            risk_level = 'yellow_zone'
            warnings = [
                f'Aggressive but manageable {required_weekly_loss_rate*100:.1f}% weekly loss rate',
                'Strict adherence to resistance training and protein required'
            ]
            
        elif required_weekly_loss_rate >= 0.005:  # 0.5-0.7% weekly - optimal range
            deficit = required_daily_deficit
            deficit_type = 'optimal'
            risk_level = 'green_zone'
            warnings = []
            
        else:  # <0.5% weekly - potential recomposition
            deficit = required_daily_deficit
            deficit_type = 'recomposition'
            risk_level = 'green_zone_recomp'
            warnings = ['Conservative rate may allow muscle gain while losing fat (body recomposition)']
    
    else:
        # No deadline - use optimal research-based approach
        deficit = min(optimal_daily_deficit, max_safe_deficit)
        
        if deficit < 300:
            deficit_type = 'recomposition'
            risk_level = 'green_zone_recomp'
            warnings = ['Small deficit optimized for body recomposition (gain muscle, lose fat)']
        elif deficit <= 400:
            deficit_type = 'conservative'
            risk_level = 'green_zone'
            warnings = []
        elif deficit <= 500:
            deficit_type = 'optimal'
            risk_level = 'green_zone'
            warnings = []
        else:
            deficit_type = 'aggressive'
            risk_level = 'yellow_zone'
            warnings = ['Approaching maximum research-based deficit']
        
        estimated_weeks = (fat_to_lose_lbs * 3500) / (deficit * 7)
    
    # Calculate minimum safe calories (research-based: 25 kcal/kg lean mass)
    min_calories_lean_mass = current_lean_mass_kg * 25
    min_calories_absolute = 1200 if sex == 'female' else 1500
    min_calories = max(min_calories_lean_mass, min_calories_absolute)
    
    # Ensure deficit doesn't drop below minimum calories
    target_calories = estimated_tdee - deficit
    if target_calories < min_calories:
        deficit = estimated_tdee - min_calories
        warnings.append(f'Deficit reduced to maintain minimum {min_calories:.0f} calories for metabolic health')
        if 'high_risk' not in deficit_type:
            deficit_type += '_calorie_limited'
    
    # Calculate expected outcomes
    weekly_fat_loss_kg = (deficit * 7) / (3500 / 2.205)
    weekly_weight_loss_rate = (weekly_fat_loss_kg / current_weight_kg)
    
    # Research-based protein recommendations
    if deficit >= 400:
        protein_per_kg = 2.4  # Longland et al. 2016 - high deficit optimal
    elif deficit >= 300:
        protein_per_kg = 2.2  # Moderate deficit
    else:
        protein_per_kg = 2.0  # Recomposition/conservative
    
    recommended_protein_g = current_weight_kg * protein_per_kg
    
    # Muscle retention priority based on research
    if current_bf_pct < 12 and sex == 'male' or current_bf_pct < 22 and sex == 'female':
        muscle_retention_priority = 'critical'
    elif current_bf_pct < 15 and sex == 'male' or current_bf_pct < 25 and sex == 'female':
        muscle_retention_priority = 'high'
    else:
        muscle_retention_priority = 'moderate'
    
    return {
        'daily_deficit': round(deficit),
        'target_calories': round(estimated_tdee - deficit),
        'deficit_type': deficit_type,
        'risk_level': risk_level,
        'max_safe_deficit': round(max_safe_deficit),
        'optimal_daily_deficit': round(optimal_daily_deficit),
        'weekly_fat_loss_kg': round(weekly_fat_loss_kg, 3),
        'weekly_weight_loss_rate_pct': round(weekly_weight_loss_rate * 100, 1),
        'estimated_weeks': round(weeks_to_goal if goal_date else estimated_weeks, 1),
        'muscle_retention_priority': muscle_retention_priority,
        'recommended_protein_g': round(recommended_protein_g),
        'min_calories': round(min_calories),
        'warnings': warnings,
        'research_notes': {
            'deficit_basis': '500 kcal/day research threshold (Murphy et al. 2021)',
            'weekly_rate_basis': '0.5-0.7% optimal range (Garthe et al. 2011)',
            'protein_basis': f'{protein_per_kg}g/kg based on deficit magnitude (Longland et al. 2016)',
            'risk_assessment': 'Green: <0.7%/week, Yellow: 0.7-1.0%/week, Red: >1.0%/week'
        }
    }