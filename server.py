import queue
import socket
import select
import chess_protocol as cp
import logging

class remoteDevice:
    def __init__(self, connection, address):
        self.conn = connection
        self.address = address
        self.name = ""

    def fileno(self):
        return self.conn.fileno()

    def __del__(self):
        self.conn.close()

class server:
    def __init__(self):
        self.s = socket.socket(cp.ip_prot, cp.tcp_prot)
        self.IP = cp.server_ip
        self.PORT = cp.server_port
        self.MAX_MSG_LENGTH = cp.MAX_MSG_LENGTH
        self.server_name = cp.server_name
        self.device_list = []
        self.ready_to_read = []
        self.ready_to_write = []
        self.in_error = []
        self.server_device = remoteDevice(self.s, self.IP)
        self.requests_queue = queue.SimpleQueue()


        # client logging
        #   Create a custom logger
        self.logger = logging.getLogger(__name__)
        #   Create handlers
        e_handler = logging.FileHandler('serverlogs\error.log')
        e_handler.setLevel(logging.ERROR)

        d_handler = logging.FileHandler('serverlogs\debug.log')
        d_handler.setLevel(logging.DEBUG)

        i_handler = logging.FileHandler('serverlogs\info.log')
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

    def add_conn(self, conn, add):
        new_device = remoteDevice(conn, add)
        self.device_list.append(new_device)

    def disconnect_device(self, device):
        self.logger.info(f"connection with client {device.fileno()} is closed")
        self.device_list.remove(device)

    def print_client_sockets(self):
        for c in self.device_list:
            print("\t", c.conn.getpeername())

    def build_and_send(self, conn, _cmd, _msg):
        built_msg = cp.build_message(_cmd, _msg)
        conn.send(built_msg.encode())

    def recv_and_parse(self, conn):
        raw_msg = conn.recv(self.MAX_MSG_LENGTH).decode()
        (_type, _msg) = cp.parse_message(raw_msg)
        return _type, _msg

    def send_wait(self, conn):
        self.build_and_send(conn, "WAIT", "")

    def send_ok(self, conn):
        self.build_and_send(conn, "OK", "")

    def connect_two_devices(self, dev1, dev2):
        self.send_ok(dev1.conn)
        self.send_ok(dev2.conn)
        self.build_and_send(dev1.conn, "IS_LISTEN", "1")
        self.build_and_send(dev2.conn, "IP_ADDRESS", dev1.address)
<<<<<<< main
=======
        _type, _msg = self.recv_and_parse(dev1.conn)
        if not _type == "LISTENING":
            err_msg = "client didn't send listening"
            print(err_msg)
            self.logger.error(err_msg)
        self.build_and_send(dev2.conn, "ATTEMPT_CONN", "")
        _type, _msg = self.recv_and_parse(dev2.conn)
        if not _type == "CONNECTING":
            err_msg = "client didn't attempt connection"
            print(err_msg)
            self.logger.error(err_msg)
        self.build_and_send(dev1, "ACCEPT_CLIENT", "")
        _type, _msg = self.recv_and_parse(dev2.conn)
        if not _type == "CONT":
            err_msg = "Match orchestration failed"
            print(err_msg)
            self.logger.error(err_msg)
        else:
            msg = (f"successfully orchestrated match between: \n"
                             f"{socket.gethostbyaddr(dev1.address)} and {socket.gethostbyaddr(dev2.address)}")
            print(msg)
            self.logger.info(msg)
>>>>>>> Online WIP

    def match_making(self):
        while self.requests_queue.qsize() > 1:
            dev1 = self.requests_queue.get()
            dev2 = self.requests_queue.get()
            self.connect_two_devices(dev1, dev2)

    def start(self):
        self.s.bind((self.IP, self.PORT))
        run = True
        self.s.listen()
        self.logger.info("Server is up and running...")
        self.logger.info("Listening for clients...")
        print("Server is up and running...")
        print("Listening for clients...")
        while run:
            print(self.requests_queue.qsize())
            self.ready_to_read, self.ready_to_write, self.in_error = select.select([self.server_device] + self.device_list, [], [])
            for current_device in self.ready_to_read:
                    if current_device is self.server_device:
                        (client_socket, client_address) = current_device.conn.accept()
                        self.print_client_sockets()
                        self.logger.info(f"\nNew client joined {client_address}")
                        print(f"\nNew client joined {client_address}")
                        self.add_conn(conn=client_socket, add=client_address)
                    else:
                        self.logger.info( "New data from client" )
                        _type, _msg = self.recv_and_parse(current_device.conn)
                        print( "New data from client " + _type)
                        if _type == "REQUEST_OPPONENT":
                            self.requests_queue.put(current_device)
                            self.send_wait(current_device.conn)
                        if _type == cp.disconnect_msg:
                            self.disconnect_device(device=current_device)
            self.match_making()

    def __del__(self):
        self.s.close()


def main():
    s = server()
    s.start()

main()