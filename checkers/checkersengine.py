#-*-coding:utf-8;-*-
#qpy:2

class CheckersEngine:
    O = chr(0xf111)
    X = chr(0xf1db)
    STAR = chr(0xf005)
    HOLE = chr(0xf006)
    MOVE = ('', '', O)
    MSG = '{filled} button{pm} remained.'
    GOAL = '\n[b]Try to achieve three or less to earn stars![/b]'
    COMMENTS = {
    	    3: '\n[b]Not bad![/b]',
    	    2: '\n[b]Well done![/b]',
    	    1: '\n[b]Perfect![/b]'
    	}

    @staticmethod
    def checkGameOver(board, onGameOver):
        if CheckersEngine.isOver(board):
            onGameOver(CheckersEngine.getCountFilled(board))

    @staticmethod
    def isOver(board):
        return not CheckersEngine.any(board, lambda source, _:
            source.text == CheckersEngine.O
            and CheckersEngine.any(board, lambda dest, _: CheckersEngine.isValidMove(board, source, dest)))

    @staticmethod
    def any(board, predicate):
        for cell in board:
            if predicate(board[cell], board): return True
        return False

    @staticmethod
    def isValidMove(board, source, target):
        return CheckersEngine.isEmpty(target) and CheckersEngine.isInRange(source, target) and CheckersEngine.getMiddleCell(board, source, target).text == CheckersEngine.O

    @staticmethod
    def isEmpty(cell):
        return cell.text == ''

    @staticmethod
    def isInRange(source, target):
        return ((source.row == target.row and abs(source.col - target.col) == 2)
            or (source.col == target.col and abs(source.row - target.row) == 2))

    @staticmethod
    def getMiddleCell(board, source, target):
        return board[CheckersEngine.middleKeyOf(source, target)]

    @staticmethod
    def middleKeyOf(source, target):
        return f"cr{CheckersEngine.middleRowOf(source, target)}c{CheckersEngine.middleColOf(source, target)}"

    @staticmethod
    def middleRowOf(source, target):
        return CheckersEngine.middleOf(source.row, target.row)

    @staticmethod
    def middleColOf(source, target):
        return CheckersEngine.middleOf(source.col, target.col)

    @staticmethod
    def middleOf(source, target):
        return int((source + target) / 2)

    @staticmethod
    def getCountFilled(board):
        return CheckersEngine.getCount(board, lambda cell, board: board[cell].text == CheckersEngine.O)

    @staticmethod
    def getCount(board, predicate):
        return CheckersEngine.fold(0, lambda acc, cell, brd: acc + 1 if predicate(cell, brd) else acc, board)

    @staticmethod
    def fold(acc, fn, board):
        a = acc
        for cell in board:
            a = fn(a, cell, board)
        return a

    @staticmethod
    def getStarsResult(filled):
        if filled < 4:
            return (CheckersEngine.STAR * ((4 - filled) % 4)).ljust(3, CheckersEngine.HOLE)
        else:
            return CheckersEngine.HOLE * 3

    @staticmethod
    def getMessage(filled):
        pm = ''
        if filled > 1:
            pm = 's'
        return CheckersEngine.MSG.format(filled = filled, pm = pm) + CheckersEngine.COMMENTS.get(filled, CheckersEngine.GOAL)
