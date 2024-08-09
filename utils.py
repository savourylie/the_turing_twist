import math 


def update_egd_rating(r, r_opponent, game_result):
    """
    Update the EGD rating based on the game result and opponent's rating.
    
    Args:
    r (float): Current EGD rating of the player
    r_opponent (float): EGD rating of the opponent
    game_result (float): Actual game result (1.0 = win, 0.5 = jigo, 0.0 = loss)
    
    Returns:
    float: New EGD rating of the player
    """
    
    def beta(rating):
        return -7 * math.log(3300 - rating)
    
    # Calculate Se (expected game result)
    Se = 1 / (1 + math.exp(beta(r_opponent) - beta(r)))
    
    # Calculate con (rating volatility factor)
    con = ((3300 - r) / 200) ** 1.6
    
    # Calculate bonus (to counter rating deflation)
    bonus = math.log(1 + math.exp((2300 - r) / 80)) / 5
    
    # Calculate new rating
    r_new = r + con * (game_result - Se) + bonus
    
    return r_new