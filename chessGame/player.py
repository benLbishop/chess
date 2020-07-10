"""module containing the Player class."""
class Player:
    """Class representing a user."""
    def __init__(self, player_config):
        self.color = player_config['color']
        self.name = player_config['name']
        self.captured_pieces = []
