import numpy
import constants as c
from piece import move as mv
from piece import B, W
from piece import Piece_Enum as pe

from piece import Bishop
from piece import King
from piece import Knight
from piece import Pawn
from piece import Queen
from piece import Rook

class Node:
    def __init__(self, _value=0, _move=None, _position=None):
        self.value = _value
        self.move = _move
        self.position = _position
        self.children = []

    def set_value(self, _value):
        self.value = _value

class minMaxTree:
    def __init__(self, board, move=None):
        self.root = Node(board.boardScore, move, board)

    def build_tree(self, move_tree, depth, color):
        other_color = move_tree.position.get_other_color(color)
        if len(move_tree.children) == 0:
            color_moves = move_tree.position.ai_danger_moves(other_color)
            for _move in color_moves:
                _position = Board(8,8,color)
                move_tree.position.CopyTo(_position)
                _position.move(_move)
                _score = 0
                _child = Node(_score, _move, _position)
                move_tree.children.append(_child)
        if depth == 0:
            return
        _depth = depth - 1
        for _child in move_tree.children:
            self.build_tree(_child, _depth, other_color)

    def minimax(self, root, depth, maximizing_player):
        root.position.checkMate()
        if depth == 0 or (root.position.is_b_mated or root.position.is_w_mated):
            return root.position.boardScore

        if maximizing_player:
            maxEval = -numpy.inf
            for _child in root.children:
                _eval = self.minimax(_child, depth - 1, False)
                maxEval = max(maxEval, _eval)
            root.set_value(maxEval)
            return maxEval
        else:
            minEval = numpy.inf
            for _child in root.children:
                _eval = self.minimax(_child, depth - 1, True)
                minEval = min(minEval, _eval)
            root.set_value(minEval)
            return minEval

    def get_move_from_eval(self, root, score):
        for _child in root.children:
            if score == _child.value:
                return root.move
        return None

    def set_new_root(self, score):
        for _child in self.root.children:
            if score == _child.value:
                break
        self.root = _child



class Board:
    def __init__(self, rows, cols, turn, is_board_tmp=False):
        self.rows = rows
        self.cols = cols
        self.currentColor = turn
        self.toolsWin = False
        self.w_tooltip = False
        self.b_tooltip = False
        self.w_tooltip_ind = (-1, -1)
        self.b_tooltip_ind = (-1, -1)
        self.ToggleTurns = True
        self.w_stalemate = False
        self.b_stalemate = False
        self.w_is_mated = False
        self.b_is_mated = False
        self.w_checked = False
        self.b_checked = False
        self.TogglePawns = True
        self.boardScore = 0
        self.is_board_tmp = is_board_tmp

        self.b_right_rook_moved = False
        self.b_left_rook_moved = False
        self.b_king_moved = False
        self.w_right_rook_moved = False
        self.w_left_rook_moved = False
        self.w_king_moved = False


        self.board = [[0 for x in range(cols)] for _ in range(rows)]
        if self.is_board_tmp == False:
            self.board[0][0] = Rook(0,0,"b")
            self.board[0][1] = Knight(0,1,"b")
            self.board[0][2] = Bishop(0,2,"b")
            self.board[0][3] = Queen(0,3,"b")
            self.board[0][4] = King(0,4,"b")
            self.board[0][5] = Bishop(0,5,"b")
            self.board[0][6] = Knight(0,6,"b")
            self.board[0][6] = Knight(0,6,"b")
            self.board[0][7] = Rook(0,7,"b")
            if self.TogglePawns:
                for j in range(8):
                    self.board[1][j] = Pawn(1, j, "b")
            self.board[7][0] = Rook(7,0,"w")
            self.board[7][1] = Knight(7,1,"w")
            self.board[7][2] = Bishop(7,2,"w")
            self.board[7][3] = Queen(7,3,"w")
            self.board[7][4] = King(7,4,"w")
            self.board[7][5] = Bishop(7,5,"w")
            self.board[7][6] = Knight(7,6,"w")
            self.board[7][7] = Rook(7,7,"w")
            if self.TogglePawns:
                for j in range(8):
                    self.board[6][j] = Pawn(6, j, "w")

            self.update_init_moves()

    def evaluate_move(self, move):
        move_score = 0
        p = self.board[move.end[0]][move.end[1]]
        if p != 0:
            if p.color == "w":
                move_score = p.score
            else:
                move_score = -p.score
        return move_score

    def CopyTo(self, board):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    continue
                else:
                    self.board[i][j].copy(board)


    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)
        if self.toolsWin:
            if self.currentColor == "w":
                bishop = W[pe.e_Bishop.value]
                knight = W[pe.e_Knight.value]
                queen = W[pe.e_Queen.value]
                rook = W[pe.e_Rook.value]
            else:
                bishop = B[pe.e_Bishop.value]
                knight = B[pe.e_Knight.value]
                queen = B[pe.e_Queen.value]
                rook = B[pe.e_Rook.value]
            bishop_des = (c.START_X - c.SQUARE*2 + 20, c.START_Y)
            knight_des = (c.START_X - c.SQUARE, c.START_Y)
            queen_des = (c.START_X - c.SQUARE*2 + 20, c.START_Y + c.SQUARE)
            rook_des = (c.START_X - c.SQUARE, c.START_Y + c.SQUARE)
            win.blit(bishop, bishop_des)
            win.blit(knight, knight_des)
            win.blit(queen, queen_des)
            win.blit(rook, rook_des)

    def update_init_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].UpdateValidMoves(self.board)

    def is_move_a_threat(self, danger_move, my_move):
        if danger_move.end == my_move.end:
            y = danger_move.start_row
            x = danger_move.start_col
            if self.board[y][x]:
                if self.board[y][x].pawn:
                    if danger_move.end_col - my_move.end_col == 0:
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return False
        return False

    def UpdateKingMoves(self):
        Wmoves_without, Bmoves_without = self.get_all_moves_without_kings()
        w_king = self.get_king("w")
        w_king_actual_moves = []
        for _move in w_king.move_list:
            w_king_actual_moves.append(_move)
        for w_move in w_king.move_list:
            for w_secret_move in Bmoves_without:
                if self.is_move_a_threat(w_secret_move, w_move):
                    w_king_actual_moves.remove(w_move)
                    break
        w_king.move_list = w_king_actual_moves
        if len(w_king.move_list) == 0:
            w_king.can_move = False

        b_king = self.get_king("b")
        b_king_actual_moves = []
        for _move in b_king.move_list:
            b_king_actual_moves.append(_move)
        for b_move in b_king.move_list:
            for b_secret_move in Wmoves_without:
                if self.is_move_a_threat(b_secret_move, b_move):
                    b_king_actual_moves.remove(b_move)
                    break
        b_king.move_list = b_king_actual_moves
        if len(b_king.move_list) == 0:
            b_king.can_move = False

    def UpdateBoard(self):
        self.update_init_moves()
        self.update_pinned_moves()
        self.UpdateKingMoves()
        self.is_checked("w")
        self.is_checked("b")

    def get_danger_moves(self, color):
        danger_moves = []
        _pieces = self.get_all_pieces_by_color(self.get_other_color(color))
        for _piece in _pieces:
            for _move in _piece.move_list:
                danger_moves.append(_move)
        return danger_moves

    def ai_danger_moves(self, color):
        self.UpdateBoard()
        danger_moves = []
        _pieces = self.get_all_pieces_by_color(self.get_other_color(color))
        for _piece in _pieces:
            for _move in _piece.move_list:
                danger_moves.append(_move)
        return danger_moves

    def get_all_pieces(self):
        _pieces = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    _pieces.append(self.board[i][j])
        return _pieces

    def get_all_pieces_by_color(self, color):
        _pieces = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == color:
                        _pieces.append(self.board[i][j])
        return _pieces

    def get_danger_moves_by_king(self, king_color):
        _danger_moves = []
        _king_pos = self.GiveKingPos(king_color)
        _pieces = self.get_all_pieces()
        for _piece in _pieces:
            if _piece.color != king_color:
                for _move in _piece.move_list:
                    if _king_pos == _move.end:
                        _danger_moves.append(_move)
        return _danger_moves

    def get_other_color(self, color):
        _color = "w"
        if color == "w":
            _color = "b"
        return _color

    def get_danger_moves_by_piece(self, by_piece):
        danger_moves = []
        other_color = self.get_other_color(by_piece.color)
        _pieces = self.get_all_pieces_by_color(other_color)
        for _piece in _pieces:
            for _move in _piece.move_list:
                if by_piece.position == _move.end:
                    danger_moves.append(_move)
        return danger_moves

    def get_pinned_pieces(self, color):
        pinned_pieces = []
        _pieces = self.get_all_pieces_by_color(color)
        _king = self.get_king(color)
        for _piece in _pieces:
            secret_danger_moves = self.get_danger_moves_without_piece(_piece)
            for _move in secret_danger_moves:
                if _king.position == _move.end:
                    pinned_pieces.append(_piece)
        return pinned_pieces

    def is_move_dangerous(self, move, color):
        tmp = Board(8,8,"w", is_board_tmp=True)
        self.CopyTo(tmp)
        tmp.move(move)
        tmp.update_init_moves()
        return tmp.is_checked(color)

    def update_pinned_moves(self):
        w_pinned = self.get_pinned_pieces("w")
        for w_piece in w_pinned:
            w_actual_moves = []
            for w_move in w_piece.move_list:
                if not self.is_move_dangerous(w_move, "w"):
                    w_actual_moves.append(w_move)
            w_piece.move_list = w_actual_moves

        b_pinned = self.get_pinned_pieces("b")
        for b_piece in b_pinned:
            b_actual_moves = []
            for b_move in b_piece.move_list:
                if not self.is_move_dangerous(b_move, "b"):
                    b_actual_moves.append(b_move)
            b_piece.move_list = b_actual_moves

    def get_all_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)
        return danger_moves

    def remove_piece_from_board(self, piece):
        if piece.img_ind == pe.e_King:
            return None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == piece:
                    returned_piece = self.board[i][j]
                    self.board[i][j] = 0
                    return returned_piece
        return None

    def get_danger_moves_without_piece(self, by_piece):
        tmp = Board(8,8,self.currentColor, is_board_tmp=True)
        self.CopyTo(tmp)
        piece_to_remove = tmp.board[by_piece.row][by_piece.col]
        tmp.remove_piece_from_board(piece_to_remove)
        tmp.update_init_moves()
        moves_without_piece = tmp.get_danger_moves(by_piece.color)
        return moves_without_piece

    def get_danger_moves_with_piece_in_new_pos(self, by_piece, move):
        tmp = Board(8,8, self.currentColor, is_board_tmp=True)
        self.CopyTo(tmp)
        tmp.move(move)
        tmp.update_init_moves()
        new_moves = tmp.get_danger_moves(by_piece.color)
        return new_moves

    def is_checked_with_piece_in_new_pos(self, color, move):
        tmp = Board(8,8, self.currentColor, is_board_tmp=True)
        self.CopyTo(tmp)
        tmp.move(move)
        tmp.update_init_moves()
        return tmp.is_checked(color)

    def get_all_moves_without_kings(self):
        tmp = Board(8,8,self.currentColor, is_board_tmp=True)
        self.CopyTo(tmp)
        tmp_white_king = tmp.get_king("w")
        tmp_black_king = tmp.get_king("b")
        wy = tmp_white_king.row
        wx = tmp_white_king.col
        by = tmp_black_king.row
        bx = tmp_black_king.col
        tmp.board[wy][wx] = 0
        tmp.board[by][bx] = 0
        tmp.update_init_moves()
        w_moves_without = tmp.get_danger_moves("b")
        b_moves_without = tmp.get_danger_moves("w")

        return w_moves_without, b_moves_without

    def dangerous_pieces(self, piece):
        attacking_pieces = []
        _pieces = self.get_all_pieces_by_color(self.get_other_color(piece.color))
        for _piece in _pieces:
            for _move in _piece.move_list:
                if _move.end == piece.position:
                    attacking_pieces.append(_piece)
        return attacking_pieces


    def can_king_be_defended(self, color): # all moves here are legal
        color_pieces = self.get_all_pieces_by_color(color)
        _king = self.get_king(color)
        newer_moves = []
        attacking_pieces = self.dangerous_pieces(_king)
        for _piece in color_pieces:
            for _move in _piece.move_list:
                new_moves = self.get_danger_moves_with_piece_in_new_pos(_piece, _move)
                for _move in new_moves:
                    newer_moves.append(_move)
                for new_move in new_moves:
                    if _king.position != new_move.end:
                        newer_moves.remove(new_move)
                if len(newer_moves) == 0:
                    return True
        return False

    def checkMate(self):
        black = "b"
        white = "w"
        if self.b_is_mated or self.w_is_mated:
            return True
        w_danger_moves = self.get_danger_moves(white)
        b_danger_moves = self.get_danger_moves(black)
        w_king = self.get_king(white)
        b_king = self.get_king(black)

        w_king_moves = w_king.move_list
        w_king_actual_moves = w_king_moves
        for w_move in w_king_moves:
            for w_danger_move in w_danger_moves:
                if w_move.end == w_danger_move.end:
                    w_king_actual_moves.remove(w_move)
                    break
        w_king.move_list = w_king_actual_moves

        b_king_moves = b_king.move_list
        b_king_actual_moves = b_king_moves
        for b_move in b_king_moves:
            for b_danger_move in b_danger_moves:
                if b_move.end == b_danger_move.end:
                    b_king_actual_moves.remove(b_move)
                    break
        b_king.move_list = b_king_actual_moves

        if self.w_checked:
            if len(w_king_actual_moves) == 0:
                w_king.can_move = False
                if self.can_king_be_defended(white) == False:
                    self.w_is_mated = True
                    return True

        if self.b_checked:
            if len(b_king_actual_moves) == 0:
                b_king.can_move = False
                if self.can_king_be_defended(black) == False:
                    self.b_is_mated = True
                    return True

        overall_w_moves, overall_b_moves = self.get_all_moves_without_kings()
        if len(overall_b_moves) == 0:
            if len(b_king_actual_moves) == 0:
                self.b_stalemate = True
                return False

        if len(overall_w_moves) == 0:
            if len(w_king_actual_moves) == 0:
                self.w_stalemate = True
                return False

        return False


    def get_king(self, color):
        _pieces = self.get_all_pieces()
        for _piece in _pieces:
            if _piece.king and _piece.color == color:
                return _piece
        return None


    def is_checked(self, color):
        danger_moves = self.get_danger_moves(color) # other color all moves
        _king = self.get_king(color)
        self.w_checked = False
        self.b_checked = False
        _king.isChecked = False
        for _move in danger_moves:
            if _king.position == _move.end:
                _king.isChecked = True
                if color == "w":
                    self.w_checked = True
                else:
                    self.b_checked = True
                return True
        return False


    def select(self, y, x):
        if self.ToggleTurns:
            toselect = False
            if self.board[y][x].selected == False:
                if self.currentColor == self.board[y][x].color:
                    toselect = True
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] != 0:
                        self.board[i][j].selected = False
            if toselect:
                self.board[y][x].selected = True
                self.UpdateBoard()
        else:
            toselect = False
            if(self.board[y][x].selected == False):
                toselect = True
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] != 0:
                        self.board[i][j].selected = False
            if(toselect):
                self.board[y][x].selected = True
                self.UpdateBoard()

    def castle(self, move, side):
        if side:
            if move.color == "w":
                self.move(move)
                m = mv((7,7), (7,5), pe.e_Rook.value, move.color)
                self.move(m)
            else:
                self.move(move)
                m = mv((0,7), (0,5), pe.e_Rook.value, move.color)
                self.move(m)
        else:
            if move.color == "w":
                self.move(move)
                m = mv((7,0), (7,3), pe.e_Rook.value, move.color)
                self.move(m)
            else:
                self.move(move)
                m = mv((0,0), (0,3), pe.e_Rook.value, move.color)
                self.move(m)

    def authorise_move(self, move, piece):
        if self.checkMate():
            return False
        if self.is_checked_with_piece_in_new_pos(piece.color, move):
            return False
        self.check_tooltip(move)
        if self.b_tooltip or self.w_tooltip:
            return False
        if not self.check_can_castle(move):
            self.move(move)
        self.UpdateBoard()
        self.checkMate()
        self.currentColor = self.get_other_color(piece.color)
        piece.selected = False
        return True


    def ai_move_logic(self, tree, is_maximizing):
        _color = "w"
        if not is_maximizing:
            _color = "b"
        self.UpdateBoard()
        _score = tree.minimax(self.tree.root, 4, is_maximizing)
        _move = tree.get_move_from_eval(self.tree.root, _score)
        _piece = self.board[_move.start_row][_move.start_col]
        if self.authorise_move(_move, _piece):
            tree.set_new_root(_score)
            tree.build_tree(self.tree, 4, _color)


    def ai_reaction_move_logic(self, i, j):
        if(0 <= i < 8 and 0 <= j < 8):
            IsSelected = self.IsSelected()
            y = IsSelected[1]
            x = IsSelected[2]
            _piece = self.board[y][x]
            self.UpdateBoard()
            if IsSelected[0]:
                if self.IsValid((i, j), _piece):
                    _move = self.get_move((i, j), _piece)
                    if self.authorise_move(_move, _piece):
                        return True, _move
                else:
                    if(self.board[i][j] != 0):
                        self.select(i,j)
            else:
                if(self.board[i][j] != 0):
                    self.select(i,j)
        return False, None

    def move_logic(self, i, j):
        change = False
        if(0 <= i < 8 and 0 <= j < 8):
            IsSelected = self.IsSelected()
            y = IsSelected[1]
            x = IsSelected[2]
            _piece = self.board[y][x]
            self.UpdateBoard()
            if IsSelected[0]:
                if self.IsValid((i, j), _piece):
                    _move = self.get_move((i, j), _piece)
                    if self.authorise_move(_move, _piece):
                        change = True
                else:
                    if(self.board[i][j] != 0):
                        self.select(i,j)
            else:
                if(self.board[i][j] != 0):
                    self.select(i,j)
        return change


    def update_moved_bools(self, p):
        if p.img_ind == pe.e_Rook.value:
            if p.moved == False:
                p.moved = True
                if p.color == "w":
                    if p.side:
                        self.w_right_rook_moved = True
                    else:
                        self.w_left_rook_moved = True
                else:
                    if p.side:
                        self.b_right_rook_moved = True
                    else:
                        self.b_left_rook_moved = True
        if p.img_ind == pe.e_King.value:
            if p.moved == False:
                p.moved = True
                if p.color == "w":
                    self.w_king_moved = True
                else:
                    self.b_king_moved = True

    def check_can_castle(self, move):
        p = self.board[move.start_row][move.start_col]
        if not p.img_ind == pe.e_King.value:
            return False
        if move.color == "w":
            if not self.w_king_moved:
                if move.start_col - move.end_col < -1:
                    if not self.w_right_rook_moved:
                        if not p.isChecked:
                            self.castle(move, True)
                            return True
                else:
                    if not self.w_left_rook_moved:
                        if not p.isChecked:
                            self.castle(move, False)
                            return True
        else:
            if not self.b_king_moved:
                if move.start_col - move.end_col < -1:
                    if not self.b_right_rook_moved:
                        if not p.isChecked:
                            self.castle(move, True)
                            return True
                else:
                    if not self.b_left_rook_moved:
                        if not p.isChecked:
                            self.castle(move, False)
                            return True
        return False

    def move(self, move):
        self.check_tooltip(move)
        p = self.board[move.start_row][move.start_col]
        self.update_moved_bools(p)
        p = self.board[move.end_row][move.end_col]
        if p != 0:
            if p.color == "b":
                self.boardScore -= p.score
            else:
                self.boardScore += p.score
        self.board[move.start_row][move.start_col].UpdatePos((move.end_row, move.end_col))
        self.board[move.end_row][move.end_col] = self.board[move.start_row][move.start_col]
        self.board[move.start_row][move.start_col] = 0


    def get_move(self, end, piece):
        for _move in piece.move_list:
            if end == _move.end:
                return _move
        return None


    def IsValid(self, pos, piece):
        y = pos[0]
        x = pos[1]
        for _move in piece.move_list:
            if y == _move.end_row and x == _move.end_col:
                return True
        return False

    def IsSelected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                     return True, i, j
        return False, -1, -1

    def choose_from_tools(self, tool, color, move):
        self.move(move)
        y = move.end_row
        x = move.end_col
        if tool == "bishop":
            self.board[y][x] = Bishop(y,x, color)
        if tool == "queen":
            self.board[y][x] = Queen(y,x, color)
        if tool == "knight":
            self.board[y][x] = Knight(y,x, color)
        if tool == "rook":
            self.board[y][x] = Rook(y,x, color)
        self.UpdateBoard()
        self.checkMate()
        self.currentColor = self.get_other_color(color)
        self.board[y][x].selected = False

    def choose_tool_from_pos(self, pos):
        if pos == (-1, -1):
            return False
        if pos == (0,0):
            tool = "bishop"
        if pos == (0,1):
            tool = "knight"
        if pos == (1,0):
            tool = "queen"
        if pos == (1,1):
            tool = "rook"
        if self.currentColor == "w":
            self.choose_from_tools(tool, "w", self.w_tooltip_ind)
        else:
            self.choose_from_tools(tool, "b", self.b_tooltip_ind)
        return True

    def check_tooltip(self, move):
        for _pawn in self.get_all_pieces():
            if _pawn.img_ind == pe.e_Pawn.value:
                _pawn.inPassing = False
        y = move.start_row
        x = move.start_col
        ey = move.end_row
        ex = move.end_col
        self.w_tooltip = False
        self.b_tooltip = False
        if self.board[y][x].img_ind == pe.e_Pawn.value:
            if self.board[y][x].color == "b":
                if ey == 7:
                    self.b_tooltip = True
                    self.b_tooltip_ind = move
                else:
                    if ex != x:
                        p = self.board[ey][ex]
                        if p == 0:
                            r = self.board[ey+1][ex]
                            self.board[ey+1][ex] = 0
                    else:
                        if abs(ey - y) > 1:
                            if self.board[y][x].first:
                                self.board[y][x].inPassing = True
                        else:
                            self.board[y][x].inPassing = False
            else:
                if ey == 0:
                    self.w_tooltip = True
                    self.w_tooltip_ind = move
                else:
                    if ex != x:
                        p = self.board[ey][ex]
                        if p == 0:
                            r = self.board[ey+1][ex]
                            self.board[ey+1][ex] = 0
                    else:
                        if abs(ey - y) > 1:
                            if self.board[y][x].first:
                                self.board[y][x].inPassing = True
                        else:
                            self.board[y][x].inPassing = False