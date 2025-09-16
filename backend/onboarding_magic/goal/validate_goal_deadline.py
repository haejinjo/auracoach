def validate_goal_deadline(total_loss_lbs, weeks_available):
    """
    Provide user feedback on goal feasibility
    """
    max_sustainable_rate = 1.5  # lbs per week
    min_sustainable_rate = 0.5  # lbs per week
    
    required_rate = total_loss_lbs / weeks_available
    
    if required_rate > 2.0:
        return {
            'feasible': False,
            'message': "This deadline requires over 2lbs/week loss, which risks muscle loss. Consider extending your deadline.",
            'recommended_date': calculate_date_for_rate(total_loss_lbs, 1.5)
        }
    elif required_rate > max_sustainable_rate:
        return {
            'feasible': 'challenging',
            'message': f"This requires {required_rate:.1f}lbs/week. Achievable but demands perfect adherence.",
            'recommended_date': calculate_date_for_rate(total_loss_lbs, 1.0)
        }
    elif required_rate < min_sustainable_rate:
        return {
            'feasible': True,
            'message': "Great! This deadline allows for sustainable progress with flexibility.",
            'could_achieve_by': calculate_date_for_rate(total_loss_lbs, 1.0)
        }
    else:
        return {
            'feasible': True,
            'message': f"Perfect pacing at {required_rate:.1f}lbs/week. Sustainable and effective."
        }