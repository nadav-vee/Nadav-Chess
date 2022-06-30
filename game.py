import pygame
import os

import piece
from board import Board
from board import minMaxTree
import constants as c
import time


class game:
    def __init__(self, win):
        self.board_sur = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "board_alt.png")), (c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT))
        self.rect = (c.START_X, c.START_Y, c.BOARD_WIDTH, c.BOARD_HEIGHT)
        self.width = c.BOARD_ALT_WIDTH
        self.height = c.BOARD_ALT_HEIGHT
        self.win = win
        pygame.display.set_caption("Chess!!")

        # general variables
        self.color = "w"
        self.turn = "w"
        self.start_time = 0
        self.player_time = 60 * 15
        self.opponent_time = 60 * 15
        self.clock = pygame.time.Clock()

    def redraw_gamewindow(self, win, bo, p1Time, p2Time, showtime=True):
        win.blit(self.board_sur, (0,0))
        bo.draw(win)
        font = pygame.font.SysFont("Arial", 30)
        p1Timemin = int(p1Time // 60)
        p1Timemsec = int(p1Time % 60)
        p2Timemin = int(p2Time // 60)
        p2Timemsec = int(p2Time % 60)
        txt = font.render("Player 1: {:02d}:{:02d}".format(p1Timemin,p1Timemsec), 1, (255, 255, 255))
        txt2 = font.render("Player 2: {:02d}:{:02d}".format(p2Timemin,p2Timemsec), 1, (255, 255, 255))
        if showtime:
            win.blit(txt2, (450, 20))
            win.blit(txt, (450, 720))
        pygame.display.update()

    def online_end_screen(self, win, text):
        pygame.font.init()
        font = pygame.font.SysFont("helvetic", 80)
        txt = font.render(text, 1, (255, 0,0))
        win.blit(txt, (self.width/2 - txt.get_width() / 2, 300))
        pygame.display.update()

        pygame.time.set_timer(pygame.USEREVENT+1, 1)

        run = True
        br = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    br = True
                    break
            if br:
                break

    def end_screen(self, win, text):
        pygame.font.init()
        font = pygame.font.SysFont("helvetic", 80)
        txt = font.render(text, 1, (255, 0,0))
        win.blit(txt, (self.width/2 - txt.get_width() / 2, 300))
        pygame.display.update()

        pygame.time.set_timer(pygame.USEREVENT+1, 1)

        run = True
        br = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    br = True
                    break
            if br:
                break
        self.start()

    def ToolsClick(self, pos):
        rect = (c.START_X - c.SQUARE*2 + 20, c.START_Y, c.SQUARE*2 - 20, c.SQUARE*2)
        x = pos[0]
        y = pos[1]
        if rect[0] < x < rect[0] + rect[2]:
            if rect[1] < y < rect[1] + rect[3]:
                divX = x - rect[0]
                divY = y - rect[1]
                j = int(divX / (rect[2]/2))
                i = int(divY / (rect[3]/2))
                return i, j
        return -1, -1

    def click(self, pos):
        """
        :return: pos  (x, y) in range 0-7 0-7
        """
        x = pos[0]
        y = pos[1]
        if self.rect[0] < x < self.rect[0] + self.rect[2]:
            if self.rect[1] < y < self.rect[1] + self.rect[3]:
                divX = x - self.rect[0]
                divY = y - self.rect[1]
                j = int(divX / (self.rect[2]/8))
                i = int(divY / (self.rect[3]/8))
                return i, j
        return -1, -1

    def invoke_move(self, _move):
        y = _move.start_row
        x = _move.start_col
        _piece = self.board.board[y][x]
        print(f"piece is {_piece}, y is {y}, x is {x}")
        return self.board.authorise_move(_move, _piece)

    def invoke_tooltip_choice(self, _move):
        tool = "queen"
        y = _move.start_row
        x = _move.start_col
        _piece = self.board.board[y][x]
        if _move.index == piece.Piece_Enum.e_Bishop.value:
            tool = "bishop"
        if _move.index == piece.Piece_Enum.e_Knight.value:
            tool = "knight"
        if _move.index == piece.Piece_Enum.e_Queen.value:
            tool = "queen"
        if _move.index == piece.Piece_Enum.e_Rook.value:
            tool = "rook"
        self.board.choose_from_tools(tool, _move.color, _move)

    def init_online_game(self, color):
        self.color = color
        self.board = Board(c.ROWS, c.COLS, color)


    def start(self):
        p1Time = 60 * 15
        p2Time = 60 * 15
        clock = pygame.time.Clock()
        turn = "w"
        self.board = Board(8,8, turn)
        bo = self.board
        run = True
        startTime = time.time()
        while run:
            clock.tick(30)

            if turn == "w":
                p1Time -= (time.time() - startTime)
            else:
                p2Time -= (time.time() - startTime)

            startTime = time.time()


            self.redraw_gamewindow(self.win, bo, p1Time, p2Time)

            if bo.b_is_mated:
                self.end_screen(self.win, "white won!")
            if bo.w_is_mated:
                self.end_screen(self.win, "black won!")
            if bo.b_stalemate or bo.w_stalemate:
                self.end_screen(self.win, "stalemate!")

            if bo.w_tooltip or bo.b_tooltip:
                while bo.w_tooltip or bo.b_tooltip:
                    bo.toolsWin = True
                    _change = False

                    if turn == "w":
                        p1Time -= (time.time() - startTime)
                    else:
                        p2Time -= (time.time() - startTime)

                    startTime = time.time()

                    self.redraw_gamewindow(self.win, bo, p1Time, p2Time)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            quit()
                            pygame.quit()

                        if event.type == pygame.K_ESCAPE:
                            return

                        if event.type == pygame.MOUSEMOTION:
                            pass

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            i, j = self.ToolsClick(pos)
                            _change = bo.choose_tool_from_pos((i,j))

                    if _change:
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                        change = False
                        bo.b_tooltip = False
                        bo.w_tooltip = False
                        bo.toolsWin = False
                        break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                    pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    pass

                if event.type == pygame.K_ESCAPE:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    i, j = self.click(pos)
                    change = bo.move_logic(i, j)

                    if change:
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                        change = False

                if event.type == pygame.KEYUP:
                    bo = Board(8,8, "w")
                    p1Time = 60 * 15
                    p2Time = 60 * 15

    def redraw_gamewindow_ai(self, win, bo, p1Time, chosen_color):
        win.blit(self.board_sur, (0,0))
        bo.draw(win)
        font = pygame.font.SysFont("Arial", 30)
        p1Timemin = int(p1Time // 60)
        p1Timemsec = int(p1Time % 60)
        if chosen_color == "w":
            txt = font.render("Player 1: {:02d}:{:02d}".format(p1Timemin,p1Timemsec), 1, (255, 255, 255))
            win.blit(txt, (450, 720))
        else:
            txt = font.render("Player 2: {:02d}:{:02d}".format(p1Timemin,p1Timemsec), 1, (255, 255, 255))
            win.blit(txt, (450, 20))
        pygame.display.update()

    def startAI(self, chosed_color):
        p1Time = 60 * 15
        clock = pygame.time.Clock()
        turn = "w"
        player = chosed_color
        ai_color = "w"
        if player == "w":
            ai_color = "b"
        bo = Board(8,8, turn)
        ai = minMaxTree(bo)
        run = True
        startTime = time.time()
        while run:
            clock.tick(30)

            if turn == "w":
                if player == "w":
                    p1Time -= (time.time() - startTime)
                else:
                    time.sleep(1)
            else:
                if player == "b":
                    p1Time -= (time.time() - startTime)
                else:
                    time.sleep(1)

            startTime = time.time()

            self.redraw_gamewindow_ai(self.win, bo, p1Time, player)

            if bo.b_is_mated:
                self.end_screen(self.win, "white won!")
            if bo.w_is_mated:
                self.end_screen(self.win, "black won!")
            if bo.b_stalemate or bo.w_stalemate:
                self.end_screen(self.win, "stalemate!")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                    pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    pass

                if event.type == pygame.K_ESCAPE:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    i, j = self.click(pos)
                    if turn == player:
                        change, _move = bo.ai_reaction_move_logic(i, j)
                        if _move:
                            if ai.root.move:
                                if ai.root.move.end != _move.end:
                                    ai.root.move = _move
                                    ai.build_tree(ai.root, 3, ai_color)
                            else:
                                ai.build_tree(ai.root, 3, ai_color)
                    else:
                        is_max = True
                        if player == "w":
                            is_max = False
                        bo.ai_move_logic(ai, is_max)
                        change = True

                    if change:
                        #startTime = time.time()
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                        change = False

                if event.type == pygame.KEYUP:
                    bo = Board(8,8, "w")
                    p1Time = 60 * 15
