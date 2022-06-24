import socket
import select
import chess_protocol as cp

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

    def add_conn(self, conn, add):
        new_device = remoteDevice(conn, add)
        self.device_list.append(new_device)

    def parse(self):
        pass

    def build_msg(self):
        pass

    def disconnect_device(self, device):
        print(f"connection with client {device.fileno()} is closed")
        device.conn.send(cp.disconnect_msg.encode())
        self.device_list.remove(device)
        device.conn.close()

    def print_client_sockets(self):
        for c in self.device_list:
            print("\t", c.conn.getpeername())

    def start(self):
        self.s.bind((self.IP, self.PORT))
        msg = ""
        data = ""
        run = True
        self.s.listen()
        print("Server is up and running...")
        print("Listening for clients...")
        while run:
            self.ready_to_read, self.ready_to_write, self.in_error = select.select([self.server_device] + self.device_list, [], [])
            for current_device in self.ready_to_read:
                    if current_device is self.server_device:
                        (client_socket, client_address) = current_device.conn.accept()
                        self.print_client_sockets()
                        print("\nNew client joined!", client_address)
                        self.add_conn(conn=client_socket, add=client_address)
                    else:
                        print( "New data from client" )
                        data = current_device.conn.recv(self.MAX_MSG_LENGTH).decode()
                        if data == cp.disconnect_msg:
                            self.disconnect_device(device=current_device)
                        elif data == cp.kill_server_msg:
                            self.disconnect_device(device=current_device)
                            run = False
                        else:
                            print(data)
                            current_device.conn.send(data.encode())

    def __del__(self):
        self.s.close()


def main():
    s = server()
    s.start()

main()