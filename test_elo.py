from utils import update_egd_rating


# Example usage
if __name__ == "__main__":
    player_rating = 2000
    opponent_rating = 2200
    game_result = 1.0  # player won
    
    player_new_rating = update_egd_rating(player_rating, opponent_rating, game_result)
    opponent_new_rating = update_egd_rating(opponent_rating, player_rating, 1 - game_result)

    print(f"Player's new rating: {player_new_rating:.2f}")
    print(f"Opponent's new rating: {opponent_new_rating:.2f}")