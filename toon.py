
class Toon:
    """
    A toon object. Handles all toon related information.
    """
    def __init__(self, _start_playground):
        """
        CONSTRUCTOR
        """
        self.pies = 3
        self.current_location = _start_playground
        self.last_playground = _start_playground
        self.laff = [17, 17]
    
    def throw_pie(self):
        """
        Throws a pie.
        Returns: True if a pie was thrown. False if no pies left.
        """
        if self.pies:
            self.pies -= 1
            return True
        else:
            return False
    
    def set_playground(self, _playground):
        """
        Sets the passed in vertex to the last
        playground the toon visited.
        """
        self.last_playground = _playground

    def take_damage(self, _dmg):
        """
        Remove the passed in damage from the toons laff.
        Input: _dmg as int
        Returns: tuple with (laff remaining, total toon laff)
        """
        self.laff[0] = (self.laff[0] - _dmg) if self.laff[0] >= _dmg else 0
        return (self.laff[0], self.laff[1])
    
    def set_location(self, _location):
        """
        Set the toons current location to the passed in vertex.
        """
        if _location.is_playground: # If this is  a playground
            self.set_playground(_location) # Save this to our toon so we can respawn here
        self.current_location = _location
    
    def get_location(self):
        """
        Returns the toons location.
        """
        return self.current_location