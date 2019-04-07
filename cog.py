
class Cog:
    """
    Cog object.
    """
    def __init__(self, _start_location):
        """
        CONSTRUCTOR
        """
        self.location = _start_location
    
    def change_location(self, _location):
        """
        Set the cogs location to the passed in location.
        """
        self.location = _location
