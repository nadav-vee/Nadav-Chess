import pygame
import os
import constants as c
import enum

b_bishop =  pygame.image.load(os.path.join("Assets", "black_bishop.png"))
b_king =    pygame.image.load(os.path.join("Assets", "black_king.png"))
b_knight =  pygame.image.load(os.path.join("Assets", "black_knight.png"))
b_pawn =    pygame.image.load(os.path.join("Assets", "black_pawn.png"))
b_queen =   pygame.image.load(os.path.join("Assets", "black_queen.png"))
b_rook =    pygame.image.load(os.path.join("Assets", "black_rook.png"))

w_bishop =  pygame.image.load(os.path.join("Assets", "white_bishop.png"))
w_king =    pygame.image.load(os.path.join("Assets", "white_king.png"))
w_knight =  pygame.image.load(os.path.join("Assets", "white_knight.png"))
w_pawn =    pygame.image.load(os.path.join("Assets", "white_pawn.png"))
w_queen =   pygame.image.load(os.path.join("Assets", "white_queen.png"))
w_rook =    pygame.image.load(os.path.join("Assets", "white_rook.png"))

class Piece_Enum(enum.Enum):
    e_Bishop = 0
    e_King = 1
    e_Knight = 2
    e_Pawn = 3
    e_Queen = 4
    e_Rook = 5

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (c.SQUARE - c.PADDING, c.SQUARE - c.PADDING)))

for img in w:
    W.append(pygame.transform.scale(img, (c.SQUARE - c.PADDING, c.SQUARE - c.PADDING)))

class move:
    def __init__(self, start, end, index, color):
        self.start_row = start[0]
        self.start_col = start[1]
        self.start = start
        self.end_row = end[0]
        self.end_col = end[1]
        self.end = end
        self.piece = index
        self.color = color

class Piece:
    img_ind = -1
    rect = (c.START_X, c.START_Y, c.BOARD_WIDTH, c.BOARD_HEIGHT)
    startX = rect[0]
    startY = rect[1]

    def __init__ (self, row, col, color):
        self.row = row
        self.col = col
        self.position = (row, col)
        self.color = color
        self.selected = False
        self.move_list = []
        self.inPassing = False
        self.isChecked = False
        self.king = False
        self.pawn = False
        self.moved = False
        self.can_move = True
        self.black_pov = False

    def copy(self, board):
        if self.img_ind == Piece_Enum.e_Bishop.value:
            board.board[self.row][self.col] = Bishop(self.row, self.col, self.color)
        elif self.img_ind == Piece_Enum.e_King.value:
            board.board[self.row][self.col] = King(self.row, self.col, self.color)
            board.board[self.row][self.col].moved = self.moved
            board.board[self.row][self.col].can_move = self.can_move
        elif self.img_ind == Piece_Enum.e_Knight.value:
            board.board[self.row][self.col] = Knight(self.row, self.col, self.color)
        elif self.img_ind == Piece_Enum.e_Pawn.value:
            board.board[self.row][self.col] = Pawn(self.row, self.col, self.color)
            board.board[self.row][self.col].first = self.first
            board.board[self.row][self.col].pawn = self.pawn
        elif self.img_ind == Piece_Enum.e_Queen.value:
            board.board[self.row][self.col] = Queen(self.row, self.col, self.color)
        elif self.img_ind == Piece_Enum.e_Rook.value:
            board.board[self.row][self.col] = Rook(self.row, self.col, self.color)
            board.board[self.row][self.col].moved = self.moved

    def set_black_pov(self):
        self.black_pov = True

    def UpdateValidMoves(self, board):
        self.move_list = self.valid_moves(board)

    def RemoveMove(self, move):
        for m in self.move_list:
            if m.end == move.end:
                self.move_list.remove(m)

    def getPiece(self):
        return (self.row, self.col)

    def IsSelected(self):
        return self.selected

    def UpdatePos(self, pos):
        self.row = pos[0]
        self.col = pos[1]
        self.position = pos
        if self.img_ind == Piece_Enum.e_Pawn.value:
            self.first = False

    def draw(self, win):
        if self.color == "w":
            if not self.black_pov:
                drawThis = W[self.img_ind]
            else:
                drawThis = B[self.img_ind]
        else:
            if not self.black_pov:
                drawThis = B[self.img_ind]
            else:
                drawThis = W[self.img_ind]

        x = c.PADDING/2 + self.startX + (self.col * self.rect[2]/8)
        y = c.PADDING/2 + self.startY + (self.row * self.rect[3]/8)

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x - c.PADDING/2, y - c.PADDING/2, c.SQUARE, c.SQUARE), 5)

        win.blit(drawThis, (x, y))

        if self.isChecked:
            checkRect = c.CHECKED
            win.blit(checkRect, (x - c.PADDING/2, y - c.PADDING/2), None, pygame.BLEND_MIN)

        if self.selected:
            moves = self.move_list

            for move in moves:
                x = 33 + self.startX + (move.end_col * self.rect[2]/8)
                y = 33 + self.startY + (move.end_row * self.rect[3]/8)
                pygame.draw.circle(win, (255, 0 ,0), (x, y), 11)


class Bishop(Piece):
    score = 3
    img_ind = Piece_Enum.e_Bishop.value


    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        # left up
        count = j
        for y in range(i,-1,-1):
            p = board[y][count]
            if p == 0:
                m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count - 1
            if(count < 0):
                break

        # left down
        count = j
        for y in range(i,8,1):
            p = board[y][count]
            if p == 0:
                m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count - 1
            if(count < 0):
                break

        # right up
        count = j
        for y in range(i,-1,-1):
            p = board[y][count]
            if p == 0:
                m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count + 1
            if(count > 7):
                break

        # right down
        count = j
        for y in range(i,8,1):
            p = board[y][count]
            if p == 0:
                m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((self.row, self.col), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count + 1
            if(count > 7):
                break


        return moves

class King(Piece):
    score = 50
    img_ind = Piece_Enum.e_King.value

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True
        self.moved = False


    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                canAppend = True
                if 0 <= (i - y) <= 7 and 0 <= (j - x) <= 7:
                    p = board[i - y][j - x]
                    if p == 0:
                        m = move((i, j), (i - y, j - x), self.img_ind, self.color)
                        moves.append(m)
                    else:
                        if p.color != self.color:
                            m = move((i, j), (i - y, j - x), self.img_ind, self.color)
                            moves.append(m)
        if self.color == "w" and self.moved == False:
            if board[i][j-1] == 0 and board[i][j-2] == 0 and board[i][j-3] == 0:
                m = move((i, j), (i, j-2), self.img_ind, self.color)
                moves.append(m)
            if board[i][j+1] == 0 and board[i][j+2] == 0:
                m = move((i, j), (i, j+2), self.img_ind, self.color)
                moves.append(m)
        if self.color == "b" and self.moved == False:
            if board[i][j-1] == 0 and board[i][j-2] == 0 and board[i][j-3] == 0:
                m = move((i, j), (i, j-2), self.img_ind, self.color)
                moves.append(m)
            if board[i][j+1] == 0 and board[i][j+2] == 0:
                m = move((i, j), (i, j+2), self.img_ind, self.color)
                moves.append(m)

        return moves


class Knight(Piece):
    score = 3
    img_ind = Piece_Enum.e_Knight.value

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = [] # [[pos], is_killing]
        # down left
        if i < 6 and j > 0:
            p = board[i+2][j-1]
            if p == 0:
                m = move((i, j), (i+2, j-1), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i+2, j-1), self.img_ind, self.color)
                    moves.append(m)

        # down right
        if i < 6 and j < 7:
            p = board[i+2][j+1]
            if p == 0:
                m = move((i, j), (i+2, j+1), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i+2, j+1), self.img_ind, self.color)
                    moves.append(m)

        # up left
        if i > 1 and j > 0:
            p = board[i-2][j-1]
            if p == 0:
                m = move((i, j), (i-2, j-1), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i-2, j-1), self.img_ind, self.color)
                    moves.append(m)

        # up right
        if i > 1 and j < 7:
            p = board[i-2][j+1]
            if p == 0:
                m = move((i, j), (i-2, j+1), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i-2, j+1), self.img_ind, self.color)
                    moves.append(m)

        # left up
        if i > 0 and j > 1:
            p = board[i-1][j-2]
            if p == 0:
                m = move((i, j), (i-1, j-2), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i-1, j-2), self.img_ind, self.color)
                    moves.append(m)

        # left down
        if i < 7 and j > 1:
            p = board[i+1][j-2]
            if p == 0:
                m = move((i, j), (i+1, j-2), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i+1, j-2), self.img_ind, self.color)
                    moves.append(m)

        # right up
        if i > 0 and j < 6:
            p = board[i-1][j+2]
            if p == 0:
                m = move((i, j), (i-1, j+2), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i-1, j+2), self.img_ind, self.color)
                    moves.append(m)

        # right down
        if i < 7 and j < 6:
            p = board[i+1][j+2]
            if p == 0:
                m = move((i, j), (i+1, j+2), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i+1, j+2), self.img_ind, self.color)
                    moves.append(m)



        return moves

class Pawn(Piece):
    score = 1
    img_ind = Piece_Enum.e_Pawn.value
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.pawn = True

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []
        if self.color == "b":
            TwoRowsOpening = True
            if i + 1 < 8:
                p = board[i+1][j]
                if p == 0:
                    m = move((i, j), (i+1, j), self.img_ind, self.color)
                    moves.append(m)
                else:
                    TwoRowsOpening = False
                if j + 1 < 8 and j - 1 >= 0:
                    p = board[i+1][j+1]
                    if p != 0:
                        if p.color != self.color:
                            m = move((i, j), (i+1, j+1), self.img_ind, self.color)
                            moves.append(m)
                    p = board[i+1][j-1]
                    if p != 0:
                        if p.color != self.color:
                            if p.color != self.color:
                                m = move((i, j), (i+1, j-1), self.img_ind, self.color)
                                moves.append(m)
                if j + 1 < 8:
                    p = board[i][j+1]
                    if p != 0:
                        if p.inPassing:
                            if p.color != self.color:
                                m = move((i, j), (i+1, j+1), self.img_ind, self.color)
                                moves.append(m)
                if j - 1 >= 0:
                    p = board[i][j-1]
                    if p != 0:
                        if p.inPassing:
                            if p.color != self.color:
                                m = move((i, j), (i+1, j-1), self.img_ind, self.color)
                                moves.append(m)
            if self.first and TwoRowsOpening:
                if i + 2 < 8:
                    p = board[i+2][j]
                    if p == 0:
                        m = move((i, j), (i+2, j), self.img_ind, self.color)
                        moves.append(m)
        else:
            TwoRowsOpening = True
            if i >= 0:
                p = board[i-1][j]
                if p == 0:
                    m = move((i, j), (i-1, j), self.img_ind, self.color)
                    moves.append(m)
                else:
                    TwoRowsOpening = False
                if j + 1 < 8 and j - 1 >= 0:
                    p = board[i-1][j+1]
                    if p != 0:
                        if p.color != self.color:
                            m = move((i, j), (i-1, j+1), self.img_ind, self.color)
                            moves.append(m)
                    p = board[i-1][j-1]
                    if p != 0:
                        if p.color != self.color:
                            m = move((i, j), (i-1, j-1), self.img_ind, self.color)
                            moves.append(m)
                if j + 1 < 8:
                    p = board[i][j+1]
                    if p != 0:
                        if p.inPassing:
                            if p.color != self.color:
                                m = move((i, j), (i-1, j+1), self.img_ind, self.color)
                                moves.append(m)
                if i - 1 >= 0:
                    p = board[i][j-1]
                    if p != 0:
                        if p.inPassing:
                            if p.color != self.color:
                                m = move((i, j), (i-1, j-1), self.img_ind, self.color)
                                moves.append(m)
            if self.first and TwoRowsOpening:
                if i > 1:
                    p = board[i-2][j]
                    if p == 0:
                        m = move((i, j), (i-2, j), self.img_ind, self.color)
                        moves.append(m)




        return moves


class Queen(Piece):
    score = 9
    img_ind = Piece_Enum.e_Queen.value

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        # left up
        count = j
        for y in range(i,-1,-1):
            p = board[y][count]
            if p == 0:
                m = move((i, j), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count - 1
            if(count < 0):
                break

        # left down
        count = j
        for y in range(i,8,1):
            p = board[y][count]
            if p == 0:
                m = move((i, j), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count - 1
            if(count < 0):
                break

        # right up
        count = j
        for y in range(i,-1,-1):
            p = board[y][count]
            if p == 0:
                m = move((i, j), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count + 1
            if(count > 7):
                break

        # right down
        count = j
        for y in range(i,8,1):
            p = board[y][count]
            if p == 0:
                m = move((i, j), (y, count), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (y, count), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif y != self.row or count != self.col:
                    break
            count = count + 1
            if(count > 7):
                break

        # up
        for x in range(i,-1,-1):
            p = board[x][j]
            if p == 0:
                m = move((i, j), (x, j), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (x, j), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif x != self.row or j != self.col:
                    break

        # down
        for x in range(i,8,1):
            p = board[x][j]
            if p == 0:
                m = move((i, j), (x, j), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (x, j), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif x != self.row or j != self.col:
                    break

        # left
        for x in range(j,-1,-1):
            p = board[i][x]
            if p == 0:
                m = move((i, j), (i, x), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i, x), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif i != self.row or x != self.col:
                    break

        # right
        for x in range(j,8,1):
            p = board[i][x]
            if p == 0:
                m = move((i, j), (i, x), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i, x), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif i != self.row or x != self.col:
                    break

        return moves

class Rook(Piece):
    score = 5
    img_ind = Piece_Enum.e_Rook.value

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.moved = False
        self.side = False
        if col > 0:
            self.side = True

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        # up
        for x in range(i,-1,-1):
            p = board[x][j]
            if p == 0:
                m = move((i, j), (x, j), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (x, j), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif x != self.row or j != self.col:
                    break

        # down
        for x in range(i,8,1):
            p = board[x][j]
            if p == 0:
                m = move((i, j), (x, j), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (x, j), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif x != self.row or j != self.col:
                    break

        # left
        for x in range(j,-1,-1):
            p = board[i][x]
            if p == 0:
                m = move((i, j), (i, x), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i, x), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif i != self.row or x != self.col:
                    break

        # right
        for x in range(j,8,1):
            p = board[i][x]
            if p == 0:
                m = move((i, j), (i, x), self.img_ind, self.color)
                moves.append(m)
            else:
                if p.color != self.color:
                    m = move((i, j), (i, x), self.img_ind, self.color)
                    moves.append(m)
                    break
                elif i != self.row or x != self.col:
                    break

        return moves
