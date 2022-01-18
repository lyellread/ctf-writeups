AF_INET = 1
SOCK_STREAM = 1


class socket:
    def __init__(self, a, b):
        pass

    def socket(self, a, b):
        pass

    def connect(self, a):
        pass

    def shutdown(self):
        pass

    def close(self):
        pass

    def sendall(self, x):
        print(f"Stubbed Socket Send: {x}")

    def recv(self, x):
        print(f"Stubbed Socket Recv Count: {x}")
        return b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
