from MatchRecorder import MatchRecorder
from TekkenGameState import TekkenGameState
from TekkenGameState import TekkenGameReader
from time import sleep
m = MatchRecorder()
g = TekkenGameState()
g.Update()
sleep(5)
#gr = TekkenGameReader()

#gr.GetUpdatedState()
#gr.WriteMovelistsToFile(gr.p1_movelist, 'test')

for i in range(100):
  g.Update()
  m.Update(g)
  sleep(0.05)
  
m.PrintInputLog()
