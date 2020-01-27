
import TekkenGameState

#Abstract class for various condtions
class condition:
    def __init__(self):
        pass
        
    def is_condition_met(self, gameState: TekkenGameState):
        pass

class max_distance_condition(condition):
    def __init__(self, distance):
        self.distance = distance
        
    def is_condition_met(self, gameState: TekkenGameState):
        if gameState.GetDist() <= self.distance:
            return True
        else:
            return False

class min_distance_condition(condition):
    def __init__(self, distance):
        self.distance = distance
        
    def is_condition_met(self, gameState: TekkenGameState):
        if gameState.GetDist() >= self.distance:
            return True
        else:
            return False


class situation:
    def __init__(self, c: condition):
        self.condition = c
        self.command = None
        self.success_condition = None
        
    def is_condition_met(self, gameState: TekkenGameState):
        if self.condition != None:
            return self.condition.is_condition_met(gameState)
        else:
            return True
            
            
    def get_command(self):
        return command.get_command()
        
    def is_successful(self, gameState: TekkenGameState):
        if self.success_condition != None:
            return self.success_condition.is_successful(gameState)
        else:
            return True
            
            


            
if __name__ == "__main__":
    c = max_distance_condition(1)
    s = situation(c)
    print("Here")
    s.is_condition_met("asdf")