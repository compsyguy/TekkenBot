"""
Class for holding move states for TekkenBot
"""

class MoveStates:
    def __init__(self):
        self.Position = None
        self.Start = None
        self.Message = None
        self.FailMessage = ""
        
    def GoToStart(self, Message = ""):
        if(Message != ""):
            print(Message)
        self.FailMessage = ""
        self.Position = self.Start

    def MoveToEdge(self, edgeName):
        if(self.Position is not None):
            if(self.Position.EdgeExists(edgeName)):
                edge = self.Position.GetEdge(edgeName)
                self.Message = edge.Message
                self.Position = edge.State
                if(edge.FailMessage != ""):
                    self.FailMessage = edge.FailMessage
                return True
            else:
                self.Position = None
                return False
            
    def LoadBDC(self):
        #Initial state - Neutral
        self.Start = MoveState('Universal_32769')
        self.Position = self.Start
        
        #First B
        FirstB = MoveState('Co_Dummy_620')
        edge = Edge(FirstB, "FirstB")
        self.Position.AddEdge(edge)

        #Neutral
        Neutral = MoveState('Co_Dummy_621')
        edge = Edge(Neutral, "Neutral")
        FirstB.AddEdge(edge)
        
        #Second B type 1
        SecondB1a = MoveState('Co_Dummy_623')
        edge = Edge(SecondB1a, "SecondB1a")
        Neutral.AddEdge(edge)
        SecondB1b = MoveState('Co_Dummy_624')
        edge = Edge(SecondB1b, "SecondB1b")
        SecondB1a.AddEdge(edge)

        #Second B
        SecondB2 = MoveState('Co_Dummy_625')
        edge = Edge(SecondB2, "SecondB2")
        Neutral.AddEdge(edge)
        
        #Too Slow to DB after second B
        TooSlow = MoveState('Co_Dummy_620')
        edge = Edge(TooSlow, "Too Slow to D/B", "Too Slow to D/B")
        SecondB1a.AddEdge(edge)
        
        #First DB
        FirstDB = MoveState('cYOKE_00B')
        edge = Edge(FirstDB, "First DB")
        SecondB1a.AddEdge(edge)
        SecondB1b.AddEdge(edge)
        SecondB2.AddEdge(edge)
        
        #A slow DB
        SlowDB1 = MoveState('He_sDASHBLp')
        edge = Edge(SlowDB1, "Slow DB", "WARN: Slow DB")
        FirstDB.AddEdge(edge)
        
        SlowDB2 = MoveState('sJUMP_00_SF')
        edge = Edge(SlowDB2, "Slow DB", "WARN: Slow DB")
        SlowDB1.AddEdge(edge)
        
        SlowDB3 = MoveState('cWALK_10BL')
        edge = Edge(SlowDB3, "Slow DB", "WARN: Slow DB")
        SlowDB2.AddEdge(edge)
        
        edge = Edge(SecondB1a, "Slow DB Finish")
        SlowDB3.AddEdge(edge)
        
        #A quick db
        StandingFromDB1 = MoveState('He_cWALKB')
        edge = Edge(StandingFromDB1, 'Back to N1')
        FirstDB.AddEdge(edge)
        
        edge = Edge(FirstB, 'Subsequent BDC b')
        StandingFromDB1.AddEdge(edge)
        
        StandingFromDB3 = MoveState('cWALK_00F')
        edge = Edge(StandingFromDB3, 'Back to N3')
        StandingFromDB1.AddEdge(edge)
        
        StandingFromDB2 = MoveState('Universal_32769')
        edge = Edge(StandingFromDB2, 'Back to N2')
        StandingFromDB1.AddEdge(edge)
        StandingFromDB3.AddEdge(edge)
        
        edge = Edge(SecondB1a, 'Back to N2a')
        StandingFromDB2.AddEdge(edge)
        
        edge = Edge(SecondB2, 'Back to N2b')
        StandingFromDB2.AddEdge(edge)
        
        self.GoToStart()
        
        #BDCMoveNames = ['Universal_32769', 'Co_Dummy_620', 'Co_Dummy_621', 'Co_Dummy_625', 'cYOKE_00B', 'He_cWALKB', 'cWALK_00F', 'Universal_32769', 'Co_Dummy_625', 'He_sKAM00_', 'Universal_32769']

class MoveState:
    def __init__(self, StateName):
        self.StateName = StateName
        self.Edges = []

    def AddEdge(self, edge):
        self.Edges.append(edge)
		
    def EdgeExists(self, edgeName):
        for edge in self.Edges:
            if(edge.State.StateName == edgeName):
                return True
        return False
      
    def GetEdge(self, edgeName):
        for edge in self.Edges:
            if(edge.State.StateName == edgeName):
                return edge
		
class Edge:
    def __init__(self, state, message, failMessage = ""):
        self.State = state
        self.Message = message
        self.FailMessage = failMessage
		
if __name__ == "__main__":
    print("Here")
    a = MoveState("a")
    b = MoveState("b")
    c = MoveState("c")
    ab = Edge(b, "Woot")
    a.AddEdge(ab)
    ac = Edge(c, "Meh")
    a.AddEdge(ac)
    print(a.EdgeExists("b").Message)
    print(a.EdgeExists("c").Message)
    print(b.EdgeExists("a").Message)