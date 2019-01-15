import movelist
import NotationParser
from NotationParser import ParseMoveList
from movelist import MoveList

gp = MoveList(22)

moves = gp.getGameplan(1)

for move in gp.gameplan:
    try:
        command = ParseMoveList(gp.getMoveCommand(move))
    except:
        print(move[0].text)