from map_layout import Toontown_Map
from toon import Toon
from cog import Cog
import random


class Game_Controller:
    def __init__(self):
        """
        Constructor:
        Creates our Game Controller.
        -    Creates the toontown map (Graph)
        -    Sets current location of the toon to Toontown Central
        -    Starts the cog in Bossbot Headquarters
        -    Picks three random (non playground) spots for bananas
        -    Picks another three different spots for black holes
        """
        self.map = Toontown_Map()
        self.toon = Toon(self.map.get_vertex('Toontown Central'))
        self.cog = Cog(self.map.get_vertex('Bossbot Headquarters')) # This is where the cog will start off

        self.banana_locations = set(self.map.get_random_nodes(3))
        # print(''.join([str(x) for x in self.banana_locations])) # Uncomment to see where bananas are put
        self.black_hole_locations = set(self.map.get_random_nodes(3, _exclude=self.banana_locations))
        # print(''.join([str(x) for x in self.black_hole_locations])) # Uncomment to see where black holes are put

        # Number of rounds till the cog moves.
        self.ROUNDS_TO_MOVE_COG = 5
    
    def round_generator(self):
        """
        A generator method. Each time this method is called a new
        round of the game is started. (I.e. allows player to make
        another move).
        """
        # Prime the counter till we move our cog.
        rounds_till_cog_moves = self.ROUNDS_TO_MOVE_COG

        while True:
            print('')
            print("You are in {}.".format(self.toon.get_location().get_name()))

            # Check if we are near a cog.
            near_cog = self.check_near_cog()
            # Check if we are near a banana.
            near_banana = self.check_near_banana()
            # Check if we are near a black hole.
            near_hole = self.check_near_black_hole()            

            print("Where would you like to go?")
            print(self.info_tip())

            # Wait for a valid input
            while True:
                location = input("Enter Location (Ex: {}): ".format(next(iter(self.toon.get_location().neighbors)).get_name()))
                # If location is not within the number of locations we have.
                next_location = self.map.get_vertex(location)
                if next_location: break
                print("This location is not valid.")
                print("Please try again.")

            if near_cog: 
                next_location = self.cog_logic(next_location) # If we hit a cog we get a new location
            if near_banana: 
                if self.banana_logic(next_location): # If we went sad from to many bananas
                    break
            if near_hole: 
                if self.black_hole_logic(next_location): # If we hit a black whole
                    break

            self.toon.set_location(next_location) # Move our location to the picked spot
            
            # ------------------------------------------------------------
            # Handle moving the cog every few rounds.
            # ------------------------------------------------------------
            if rounds_till_cog_moves is 0: # If it is time to move the cog
                self.change_cog_location()
                rounds_till_cog_moves = self.ROUNDS_TO_MOVE_COG # Reprime counter
            else:
                rounds_till_cog_moves -= 1

            yield # Return to main method

    def check_near_cog(self):
        """
        Checks if the toon is one tunnel away from a cog.
        """
        if self.cog.location in self.toon.get_location().neighbors:
            print("WARNING: A cog is nearby.")
            return True
        return False
    
    def cog_logic(self, _next_location):
        """
        Handles the input and output logic if for dealing with a cog.
        """
        print('')
        print("Would you like to throw a pie in the tunnel incase there is a cog?")
        print("You have {} pies left.".format(self.toon.pies))
        while True:
            confirmation = input("Throw Pie? (y or n): ")
            # If location is not within the number of locations we have.
            if confirmation is 'y' or confirmation is 'n': break
            print("Not a valid input.")
            print("Please try again.")
        
        print('')
        if confirmation is 'y' and self.toon.throw_pie():
            if _next_location is self.cog.location:
                print("You hit the cog.")
                self.change_cog_location()
        elif confirmation is 'y':
            print("You were out of pies")
            if _next_location is self.cog.location:
                print("There was a cog there.")
                print("You got sent back to the last playground.")
                _next_location = self.toon.last_playground
        else:
            if _next_location is self.cog.location:
                print("There was a cog there.")
                print("You got sent back to the last playground.")
                _next_location = self.toon.last_playground
        return _next_location
    
    def check_near_banana(self):
        """
        Checks if the toon is one tunnel away from a banana.
        """
        if self.toon.get_location().neighbors.isdisjoint(self.banana_locations):
            return False
        else:
            print("WARNING: A banana is nearby.")
            return True
    
    def banana_logic(self, _next_location):
        """
        Handles the input and output logic if for dealing with a banana.
        """
        # If our next location is a banana location.
        if _next_location in self.banana_locations:
            print("You hit a banana!")
            print("Your laff has been reduced by 9.")
            left, total = self.toon.take_damage(9) # Take damage
            print("Current laff {}/{}".format(left, total))
            if left is 0: # If we have no laff left.
                print("You ran out of laff and went sad.")
                print("Better luck next time!")
                return True
        return False
    
    def check_near_black_hole(self):
        """
        Checks if the toon is one tunnel away from a balck hole.
        """
        if self.toon.get_location().neighbors.isdisjoint(self.black_hole_locations):
            return False
        else:
            print("WARNING: A black hole is nearby.")
            print("If you hit a black hole it will be game over.")
            return True
    
    def black_hole_logic(self, _next_location):
        """
        Handles the input and output logic if for dealing with a black hole.
        """
        if _next_location in self.black_hole_locations:
            print("You hit a black hole and logged off!")
            print("Better luck next time!")
            return True
        return False

    def change_cog_location(self):
        """
        Move the cog to a different non playground location.
        """
        new_location = self.map.get_random_nodes()[0]
        self.cog.change_location(new_location)
        # print("Moving cog to {}.".format(new_location)) # Comment out to watch when and where cog moves

    def info_tip(self):
        """
        Returns the info tip for the current location.
        Such as where the player can go or what they can do.
        """
        return "Options {}".format(self.toon.get_location().get_info_tip())
    
g = Game_Controller() # Create our game
game_play = g.round_generator() # Create our round generator
while True: # Start playing
    try:
        next(game_play)
    except StopIteration: # If the game ends.
        print("END GAME.")
        break

