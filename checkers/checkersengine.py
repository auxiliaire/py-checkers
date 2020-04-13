#-*-coding:utf-8;-*-
#qpy:2

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

def checkGameOver(board, onGameOver):
    if isOver(board):
        onGameOver(getCountFilled(board))

def isOver(board):
    return not any(board, lambda source, _:
        isFilled(source)
        and any(board, lambda dest, _: isValidMove(board, source, dest)))

def isFilled(cell):
    return cell.text == O

def any(board, predicate):
    for cell in board:
        if predicate(board[cell], board): return True
    return False

def isValidMove(board, source, target):
    return isEmpty(target) and isInRange(source, target) and getMiddleCell(board, source, target).text == O

def isEmpty(cell):
    return cell.text == ''

def isInRange(source, target):
    return ((source.row == target.row and abs(source.col - target.col) == 2)
        or (source.col == target.col and abs(source.row - target.row) == 2))

def getMiddleCell(board, source, target):
    return board[middleKeyOf(source, target)]

def middleKeyOf(source, target):
    return f"cr{middleRowOf(source, target)}c{middleColOf(source, target)}"

def middleRowOf(source, target):
    return middleOf(source.row, target.row)

def middleColOf(source, target):
    return middleOf(source.col, target.col)

def middleOf(source, target):
    return int((source + target) / 2)

def getCountFilled(board):
    return getCount(board, lambda cell, board: board[cell].text == O)

def getCount(board, predicate):
    return fold(0, lambda acc, cell, brd: acc + 1 if predicate(cell, brd) else acc, board)

def fold(acc, fn, board):
    a = acc
    for cell in board:
        a = fn(a, cell, board)
    return a

def getStarsResult(filled):
    if filled < 4:
        return (STAR * ((4 - filled) % 4)).ljust(3, HOLE)
    else:
        return HOLE * 3

def getMessage(filled):
    pm = ''
    if filled > 1:
        pm = 's'
    return MSG.format(filled = filled, pm = pm) + COMMENTS.get(filled, GOAL)
