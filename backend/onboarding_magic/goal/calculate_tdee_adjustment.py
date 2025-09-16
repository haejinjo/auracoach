def calculate_tdee_adjustment(weight_change, user_feedback, current_deficit_type):
    """
    Adjust TDEE based on actual vs expected progress
    """
    expected_loss = (current_deficit * 7) / 3500
    actual_loss = -weight_change  # Convert to positive for loss
    
    variance = actual_loss - expected_loss
    
    if variance < -0.5:  # Losing too slowly
        if user_feedback.feels_recomp:
            return 0  # Body recomposition happening
        else:
            # Increase deficit slightly
            return -100 if current_deficit_type == 'aggressive' else -150
            
    elif variance > 1.0:  # Losing too quickly
        # Protect muscle mass
        return +150
        
    elif abs(variance) <= 0.3:  # On track
        return 0
        
    else:  # Minor adjustment needed
        return -50 if variance < 0 else +50