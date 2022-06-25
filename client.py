import random
import time
import pygame
from pygame.locals import *
import game
import constants as c
import chess_protocol as cp
import os
import socket
import logging

import piece


class Client:
    def __init__(self):

        # pygame
        self.win = pygame.display.set_mode((c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT))
        self.font = pygame.font.SysFont("Arial", 30)

        # game options
        self.game = game.game(self.win)
        self.game_running = False
        self.game_over = False

        # client general
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = cp.server_port
        self.SERVER_IP = cp.server_ip
        self.IP = socket.getaddrinfo(socket.gethostname(), self.CL_PORT)[-1][-1][0]
        self.CL_PORT = cp.client_port
        self.CL_IP = cp.server_ip
        print(self.IP, self.CL_PORT)
        self.MAX_MSG_LENGTH = cp.MAX_MSG_LENGTH
        self.can_connect = False
        self.in_charge = False
        self.connected = False

        # client logging
        #   Create a custom logger
        self.logger = logging.getLogger(__name__)
        #   Create handlers
        e_handler = logging.FileHandler('logs\error.log')
        e_handler.setLevel(logging.ERROR)

        d_handler = logging.FileHandler('logs\debug.log')
        d_handler.setLevel(logging.DEBUG)

        i_handler = logging.FileHandler('logs\info.log')
        i_handler.setLevel(logging.INFO)
        #   Create formatters and add it to handlers
        e_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        e_handler.setFormatter(e_format)

        d_format = logging.Formatter('%(asctime)s - %(name)s \n %(levelname)s - %(message)s\n\n\n')
        d_handler.setFormatter(d_format)

        i_format = logging.Formatter('%(message)s')
        i_handler.setFormatter(i_format)
        #   Add handlers to the logger
        self.logger.addHandler(e_handler)
        self.logger.addHandler(d_handler)
        self.logger.addHandler(i_handler)

        # design
        self.pvp_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "pvp.png")), (c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT/3))
        self.ai_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "ai.png")), (c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT/3))
        self.online_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "internet.png")), (c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT/3))
        self.pvp_hover = False
        self.online_hover = False
        self.ai_hover = False
        self.pvp_rect = (0, 0, c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT/3)
        self.ai_rect = (0, c.BOARD_ALT_HEIGHT/3, c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT/3)
        self.online_rect = (0, c.BOARD_ALT_HEIGHT*2/3, c.BOARD_ALT_WIDTH, c.BOARD_ALT_HEIGHT/3)
        self.to_choose = False
        self.toggle_ai = False
        self.choose_txt = self.font.render("choose color!", True, (255, 255, 255))
        self.black_txt = self.font.render("black", True, (255, 255, 255))
        self.white_txt = self.font.render("white", True, (255, 255, 255))
        self.black_txt_hitbox = (c.BOARD_ALT_WIDTH/3 - 70, c.BOARD_ALT_HEIGHT/3 - 100, 50, 30)
        self.white_txt_hitbox = (c.BOARD_ALT_WIDTH/3, c.BOARD_ALT_HEIGHT/3 - 100, 50, 30)

    def __del__(self):
        self.conn.close()

    def build_and_send(self, _cmd, _msg):
        built_msg = cp.build_message(_cmd, _msg)
        self.client_conn.send(built_msg.encode())

    def recv_and_parse(self):
        raw_msg = self.client_conn.recv(self.MAX_MSG_LENGTH).decode()
        (_type, _msg) = cp.parse_message(raw_msg)
        return _type, _msg

    def build_and_send_server(self, _cmd, _msg):
        built_msg = cp.build_message(_cmd, _msg)
        self.conn.send(built_msg.encode())

    def recv_and_parse_server(self):
        raw_msg = self.conn.recv(self.MAX_MSG_LENGTH).decode()
        (_type, _msg) = cp.parse_message(raw_msg)
        return _type, _msg

    def send_wait(self):
        self.build_and_send("WAIT", "")

    def send_ok(self):
        self.build_and_send("OK", "")

    def recv_is_wait_or_ok(self):
        _type, _msg = self.recv_and_parse()
        if _type == "OK":
            return True
        elif _type == "WAIT":
            return False
        else:
            self.logger.error(f"in wait or ok question got different type : {_type} - {_msg}")
            return False

    def connect_to_opponent(self, _listen):
        if not _listen:
            try:
<<<<<<< main
                self.logger.info(f"attempting to connect to %s:%d {self.CL_IP, self.CL_PORT}")
                _type, _msg = self.recv_and_parse_server()
                if _type != "ATTEMPT_CONN":
                    err_msg = f"server didn't communicated attempt connect instead : {_type}"
                    print(err_msg)
                    self.logger.error(err_msg)
                self.logger.info(f"attempting to connect to %s:%d {self.CL_IP, self.CL_PORT}")
                self.build_and_send_server("CONT", "")
                self.client_conn.connect((self.CL_IP, self.CL_PORT))
            except Exception as e:
                self.logger.error("something's wrong with %s:%d. Exception is %s" % (self.IP, self.CL_PORT, e), exc_info=True)
        else:
            self.client_conn.bind((self.IP, self.CL_PORT))
            self.logger.info(f"listening in port %d ...{self.CL_PORT}")
            self.client_conn.listen()
            self.build_and_send_server("LISTENING", "")
            _type, _msg = self.recv_and_parse_server()
            if _type != "ACCEPT_CLIENT":
                err_msg = f"server didn't tell client to accept, instead : {_type}"
                print(err_msg)
                self.logger.error(err_msg)
            (self.opp_socket, self.opp_address) = self.client_conn.accept()
            self.logger.info("Opponent connected")

    def request_connection(self):
        self.logger.info("requesting opponent from server...")
        self.build_and_send_server("REQUEST_OPPONENT", "")
        _type, _res = self.recv_and_parse_server()
        waiting = True
        while waiting:
            print(_type)
            if _type == "WAIT":
                _type, _res = self.recv_and_parse_server()
                continue
            if _type == "OK":
                self.logger.info("server found opponent")
                raw_sec_res = self.conn.recv(self.MAX_MSG_LENGTH).decode()
                (sec_type, sec_res) = cp.parse_message(raw_sec_res)
                print(sec_type, sec_res)
                if sec_type == "IS_LISTEN":
                    if sec_res == "1":
                        self.in_charge = True
                        self.logger.info(f"client {self.IP} is in listen mode")
                elif sec_type == "IP_ADDRESS":
                    self.CL_IP = sec_res
                    print(f"client {self.IP} is in connect mode to {self.CL_IP}")
                    self.logger.info(f"client {self.IP} is in connect mode to {self.CL_IP}")
                else:
                    self.conn.close()
            waiting = False
        try:
            self.connect_to_opponent(self.in_charge)
            msg_close_conn = cp.build_message("CLOSE", "")
            self.conn.send(msg_close_conn.encode())
            self.conn.close()
            self.logger.info("connection with server is closed. start playing!")
        except Exception as e:
            self.logger.error(f"connection failed : {e}")

    def init_game(self):
        if self.in_charge:
            if random.random() % 2 == 0:
                _color = "w"
            else:
                _color = "b"
            (_type, _msg) = self.recv_and_parse()
            if _type == "OK":
                self.game.init_online_game(c.dif_clr(_color))
        else:

            (_type, _color) = self.recv_and_parse()
            if _type == "INIT_GAME":
                self.game.init_online_game(_color)
            self.build_and_send("OK", "")

    def handle_sync_connect(self):
        if self.game_running:
            return True
        else:
            try:
                self.request_connection()
                self.logger.info("handle sync - connected")
                self.init_game()
                self.logger.info("handle sync - game initialized")
            except Exception as e:
                return False
            finally:
                self.game_running = True

    def handle_abrupt_disconnection(self):
        self.game.end_screen(self.win, "abruptly disconnected")
        self.logger.error("abruptly disconnected")
<<<<<<< main

    def sync_current_time(self):
        if self.in_charge:
            (_type, _msg) = self.recv_and_parse()
            if _type == "SET_START_TIME":
                self.game.start_time = float(_msg)
        else:
            self.game.start_time = time.time()
            self.build_and_send("START_TIME", f"{self.game.start_time}")

    def alert_mate(self, _color):
        if self.game.turn == self.game.color:
            self.build_and_send("GAME_OVER", _color)
            self.game.end_screen(self.win, f"{c.clr(_color)} won!")
        else:
            _type, _msg = self.recv_and_parse()
            if _type == "GAME_OVER":
                self.game.end_screen(self.win, f"{c.clr(_msg)} won!")

    def alert_stalemate(self):
        if self.game.turn == self.game.color:
            self.build_and_send("STALEMATE", "")
            self.game.end_screen(self.win, "Stalemate!")
        else:
            _type, _msg = self.recv_and_parse()
            if _type == "STALEMATE":
                self.game.end_screen(self.win, "Stalemate!")

    def send_move(self, _move):
        move_msg = self.build_move_msg(_move, _move.index, _move.color)
        self.build_and_send("PENDING_MOVE", move_msg)

    def recv_move(self):
        _move = None
        _type, _msg = self.recv_and_parse()
        if _type == "PENDING_MOVE":
            _move = self.parse_move_msg(_msg)
        return _move

    def build_move_msg(self, _move, _ind, _color):
        i = _move.start_row
        j = _move.start_col
        y = _move.end_row
        x = _move.end_col
        g = _ind
        c = _color
        return "%s%s%s%s%s%s" % (str(i), str(j), str(y), str(x), str(g), c)

    def parse_move_msg(self, msg):
        i = msg[0]
        j = msg[1]
        y = msg[2]
        x = msg[3]
        g = msg[4]
        c = msg[5]
        m = piece.move((int(i),int(j)), (int(y),int(x)), int(g), c)
        return m

    def reset_time(self):
        self.game.player_time = 60 * 15
        self.game.opponent_time = 60 * 15
        self.sync_current_time()

    def sync_current_time(self):
        if self.in_charge:
            (_type, _msg) = self.recv_and_parse()
            if _type == "SET_START_TIME":
                self.game.start_time = float(_msg)
        else:
            self.game.start_time = time.time()
            self.build_and_send("START_TIME", f"{self.game.start_time}")

    def alert_mate(self, _color):
        if self.game.turn == self.game.color:
            self.build_and_send("GAME_OVER", _color)
            self.game.end_screen(self.win, f"{c.clr(_color)} won!")
        else:
            _type, _msg = self.recv_and_parse()
            if _type == "GAME_OVER":
                self.game.end_screen(self.win, f"{c.clr(_msg)} won!")

    def alert_stalemate(self):
        if self.game.turn == self.game.color:
            self.build_and_send("STALEMATE", "")
            self.game.end_screen(self.win, "Stalemate!")
        else:
            _type, _msg = self.recv_and_parse()
            if _type == "STALEMATE":
                self.game.end_screen(self.win, "Stalemate!")

    def send_move(self, _move):
        move_msg = self.build_move_msg(_move, _move.index, _move.color)
        self.build_and_send("PENDING_MOVE", move_msg)

    def recv_move(self):
        _move = None
        _type, _msg = self.recv_and_parse()
        if _type == "PENDING_MOVE":
            _move = self.parse_move_msg(_msg)
        return _move

    def build_move_msg(self, _move, _ind, _color):
        i = _move.start_row
        j = _move.start_col
        y = _move.end_row
        x = _move.end_col
        g = _ind
        c = _color
        return "%s%s%s%s%s%s" % (str(i), str(j), str(y), str(x), str(g), c)

    def parse_move_msg(self, msg):
        i = msg[0]
        j = msg[1]
        y = msg[2]
        x = msg[3]
        g = msg[4]
        c = msg[5]
        m = piece.move((int(i),int(j)), (int(y),int(x)), int(g), c)
        return m

    def reset_time(self):
        self.game.player_time = 60 * 15
        self.game.opponent_time = 60 * 15
        self.sync_current_time()

    def online_start(self):
        run = True
        change = False
        self.sync_current_time()
        while run:
            self.game.clock.tick(30)

            if self.game.turn == self.game.color:
                self.game.player_time -= (time.time() - self.game.start_time)
            else:
                self.game.opponent_time -= (time.time() - self.game.start_time)

            self.sync_current_time()


            self.game.redraw_gamewindow(self.game.win, self.game.board, self.game.player_time, self.game.opponent_time)

            if self.game.board.b_is_mated:
                self.alert_mate("w")
            if self.game.board.w_is_mated:
                self.alert_mate("b")
            if self.game.board.b_stalemate or self.game.board.w_stalemate:
                self.alert_stalemate()

            if self.game.board.w_tooltip or self.game.board.b_tooltip:
                if self.game.turn == self.game.color:
                    while self.game.board.w_tooltip or self.game.board.b_tooltip:
                        self.game.board.toolsWin = True
                        _change = False

                        if self.game.turn == self.game.color:
                            self.game.player_time -= (time.time() - self.game.start_time)
                        else:
                            self.game.opponent_time -= (time.time() - self.game.start_time)

                        self.sync_current_time()

                        self.game.redraw_gamewindow(self.game.win, self.game.board, self.game.player_time, self.game.opponent_time)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                quit()
                                pygame.quit()

                            if event.type == pygame.K_ESCAPE:
                                self.client_conn.close()
                                self.handle_abrupt_disconnection()

                            if event.type == pygame.MOUSEMOTION:
                                pass

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                i, j = self.game.ToolsClick(pos)
                                _change, tt_tool, tt_color, tt_move = self.game.board.choose_tool_from_pos((i,j))
                                if _change:
                                    self.send_ok()
                                    move_msg = self.build_move_msg(tt_move, tt_tool, tt_color)
                                    self.build_and_send("CHOSEN_TOOL", move_msg)

                        if _change:
                            if self.game.turn == "w":
                                self.game.turn = "b"
                            else:
                                self.game.turn = "w"
                            _change = False
                            self.game.board.b_tooltip = False
                            self.game.board.w_tooltip = False
                            self.game.board.toolsWin = False
                            break
                        else:
                            self.send_wait()
                else:
                    while self.game.turn != self.game.color:
                        if self.game.turn == self.game.color:
                            self.game.player_time -= (time.time() - self.game.start_time)
                        else:
                            self.game.opponent_time -= (time.time() - self.game.start_time)
                        self.sync_current_time()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                quit()
                                pygame.quit()

                            if event.type == pygame.K_ESCAPE:
                                pass

                            if event.type == pygame.MOUSEMOTION:
                                pass
                        try:
                            _change = self.recv_is_wait_or_ok()
                        except Exception as e:
                            self.logger.error(f"error : {e}")
                            self.handle_abrupt_disconnection()

                        if _change:
                            try:
                                _type, _msg = self.recv_and_parse()
                            except Exception as e:
                                self.logger.error(f"error : {e}")
                                self.handle_abrupt_disconnection()
                            if _type == "CHOSEN_TOOL":
                                _move = self.parse_move_msg(_msg)
                                self.game.invoke_tooltip_choice(_move)
                            if self.game.turn == "w":
                                self.game.turn = "b"
                            else:
                                self.game.turn = "w"
                            _change = False
                            self.game.board.b_tooltip = False
                            self.game.board.w_tooltip = False
                            self.game.board.toolsWin = False
                            break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                    pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    pass

                if event.type == pygame.K_ESCAPE:
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    i, j = self.game.click(pos)
                    if self.game.turn == self.game.color:
                        change, _move = self.game.board.comm_move_logic(i, j)
                        if change:
                            self.send_ok()
                            self.send_move(_move)
                        else:
                            self.send_wait()
                    else:
                        if self.recv_is_wait_or_ok():
                            _move = self.recv_move()
                            self.game.invoke_move(_move)
                            change = True

                    if change:
                        if self.game.turn == "w":
                            self.game.turn = "b"
                        else:
                            self.game.turn = "w"
                        change = False

    def start_script(self):
        try:
            self.conn.connect((self.SERVER_IP, self.PORT))
            self.logger.info("connected to %s:%d successfully" % (self.SERVER_IP, self.PORT))
            self.request_connection()
            self.online_start()
        except Exception as e:
            self.logger.error("something's wrong with %s:%d. Exception is %s" % (self.SERVER_IP, self.PORT, e))
            self.conn.close()


    def debug_start(self):
        try:
            self.conn.connect((self.IP, self.PORT))
            while True:
                msg = input("enter message\n")
                self.conn.send(msg.encode())
                data = self.conn.recv(self.MAX_MSG_LENGTH).decode()
                print("THE SERVER SENT: " + data)
                if data == "bye":
                    break
        except Exception as e:
            self.logger.error("something's wrong with %s:%d. Exception is %s" % (self.IP, self.PORT, e))
            self.conn.close()

    def redraw(self, win):
        win.blit(self.pvp_img, (0,0))
        win.blit(self.ai_img, (0, c.BOARD_ALT_HEIGHT/3))
        win.blit(self.online_img, (0, c.BOARD_ALT_HEIGHT*2/3))
        if self.pvp_hover:
            pygame.draw.rect(win, [255,255,255], self.pvp_rect, 5)
        elif self.ai_hover:
            pygame.draw.rect(win, [255,255,255], self.ai_rect, 5)
        elif self.online_hover:
            pygame.draw.rect(win, [255,255,255], self.online_rect, 5)
        if self.to_choose:
            win.blit(self.choose_txt, (c.BOARD_ALT_WIDTH/3 - 80, c.BOARD_ALT_HEIGHT/3))
            win.blit(self.black_txt, (c.BOARD_ALT_WIDTH/3 - 70, c.BOARD_ALT_HEIGHT/3 - 100))
            win.blit(self.white_txt, (c.BOARD_ALT_WIDTH/3, c.BOARD_ALT_HEIGHT/3 - 100))
        pygame.display.update()


    def intersects(self, rect, pos):
        if pos[0] >= rect[0] and pos[0] <= (rect[2] + rect[0]) and pos[1] >= rect[1] and pos[1] <= (rect[3] + rect[1]):
            return True
        return False

    def start(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)

            self.redraw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                    pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    if not self.to_choose:
                        pos = pygame.mouse.get_pos(self.win)
                        if self.intersects(self.ai_rect, pos):
                            self.ai_hover = True
                        else:
                            self.ai_hover = False
                        if self.intersects(self.pvp_rect, pos):
                            self.pvp_hover = True
                        else:
                            self.pvp_hover = False
                        if self.intersects(self.online_rect, pos):
                            self.online_hover = True
                        else:
                            self.online_hover = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos(self.win)
                    if not self.to_choose:
                        if self.intersects(self.pvp_rect, pos):
                            #self.clientg.startAI("w")
                            self.game.start()
                        if self.intersects(self.ai_rect, pos):
                            if self.toggle_ai:
                                self.to_choose = True
                        if self.intersects(self.online_rect, pos):
                            self.start_script()
                    else:
                        if self.intersects(self.white_txt_hitbox, pos):
                            self.game.startAI("w")
                        if self.intersects(self.black_txt_hitbox, pos):
                            self.game.startAI("b")
                        self.to_choose = False

pygame.init()
pygame.font.init()
m = Client()
m.start()


'''







import socket
import like_a_rolling_project.chatlib_skeleton as ch #  To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    msg = str(ch.build_message(code, data))
    nmsg = str(msg).encode()
    conn.send(nmsg)
"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
"""
# Implement Code


def recv_message_and_parse(conn):
    full_msg = conn.recv(ch.MAX_MSG_LENGTH).decode()
    cmd, data = ch.parse_message(full_msg)
    return cmd, data
"""
Recieves a new message from given socket,
then parses the message using chatlib.
Paramaters: conn (socket object)
Returns: cmd (str) and data (str) of the received message. 
If error occured, will return None, None
"""

def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    (msg_code, msg) = recv_message_and_parse(conn)
    return msg_code, msg

def get_score(conn):
    code, msg = build_send_recv_parse(conn, ch.PROTOCOL_CLIENT["get_score"],"")
    if(code == "ERROR"):
        print("ERROR")
    else:
        print(msg)

def get_highscore(conn):
    code, msg = build_send_recv_parse(conn, ch.PROTOCOL_CLIENT["get_score_table"], "")
    if(code == "ERROR"):
        print("ERROR")
    else:
        print("Your score: " + msg)

def menu():
    print("\nq\tQuit\ns\tScore\n"
          "h\tHigh Score\np\tPlay Question\nl\tGet all logged users\n")
    option = input("Please choose an option: ")
    return option

def play_question(conn):
    while True:
        code, msg = build_send_recv_parse(conn, ch.PROTOCOL_CLIENT["get_question"], "")
        if code == "ERROR":
            print("ERROR with getting the question")
        if code == "NO_QUESTIONS":
            print("No more questions\n Game Over\n")
        question_info = ch.split_data(msg, 6)
        id = question_info[0]
        question = question_info[1]
        answers = question_info[2:6]
        print("Q: " + question + "\n")
        for i in range(4):
            print("\t" + str(i+1) + ": " + answers[i])
        ans = input("Please choose an answer [1-4]: ")
        answer_to_send = ch.join_data((id, str(ans)))
        code, msg = build_send_recv_parse(conn, ch.PROTOCOL_CLIENT["send_answer"], answer_to_send)
        if code == "ERROR":
            print("ERROR with getting the right answer")
        if code == "CORRECT_ANSWER":
            print("Yes!!!")
        if code == "WRONG_ANSWER":
            print("wrong :(\nThe correct answer is: " + msg)
        if(input("Would you like to continue\ny/n\n") == "n"):
            break


def get_logged_users(conn):
    code, msg = build_send_recv_parse(conn, ch.PROTOCOL_CLIENT["get_logged_users"], "")
    if code == "ERROR":
        print("ERROR with getting the logged users")
    else:
        print(msg)

def connect():
    # Implement Code
    my_socket = socket.socket()
    my_socket.connect((SERVER_IP, SERVER_PORT))
    pass
    return my_socket


def error_and_exit(error_msg):
    # Implement code
    print(error_msg)
    exit()
    pass

def encrypt(password):
    return password

def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = ch.join_data((username,encrypt(password)))

        code, data = build_send_recv_parse(conn, ch.PROTOCOL_CLIENT["login_msg"], data)
        if code == "ERROR":
            print("login unsuccessful")
        else:
            print("logged in!")
            return


    pass

def logout(conn):
    build_and_send_message(conn, ch.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")
    pass

def main():
    conn = connect()
    login(conn)
    while True:
        op = menu()
        if(op == "s"):
            get_score(conn)
        if(op == "q"):
            logout(conn)
            break
        if(op == "h"):
            get_highscore(conn)
        if op == "p":
            play_question(conn)
        if op == "l":
            get_logged_users(conn)
    conn.close()
    exit()
    pass

if __name__ == '__main__':
    main()
'''