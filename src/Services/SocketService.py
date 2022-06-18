import socket, random
import logging

class SocketService():

    def __init__(self, excludePorts: list = None, host: str = None, port: int = None):
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        if port is None:
            self.port = self.__generatePort(excludePorts)
        else:
            self.port = port
        self.hostName = socket.gethostname()
        if host is None:
            self.hostIp = socket.gethostbyname(self.hostName)
        else:
            self.hostIp = host
        self._continue = True
        self.sock = None

    def listen(self, queue: list):
        self.sock = socket.socket()
        self.__bindSock()
        self.sock.listen(30)  # указываем сколько может сокет принимать соединений
        self.log.debug('start listening host: ' + self.hostIp + ', port: ' + str(self.port))
        while self._continue:
            try:
                conn, addr = self.sock.accept()  # начинаем принимать соединения
                # print('connected:', addr)  # выводим информацию о подключении
                data = conn.recv(1024)  # принимаем данные от клиента, по 1024 байт
                data = data.decode("utf-8")
                self.log.debug('receive message: ' + str(data))
                queue.append(data)
                conn.close()
            except Exception as ex:
                if self._continue:
                    self.log.error(str(type(ex)) + " : " + str(ex))
        self.sock.close()

    def listenAndSend(self, methodToCall):
        self.sock = socket.socket()
        self.__bindSock()
        self.sock.listen(30)  # указываем сколько может сокет принимать соединений
        self.log.debug('start listening host: ' + self.hostIp + ', port: ' + str(self.port))
        while self._continue:
            try:
                conn, addr = self.sock.accept()  # начинаем принимать соединения
                data = conn.recv(1024)  # принимаем данные от клиента, по 1024 байт
                data = data.decode("UTF-8")
                self.log.debug('receive message: ' + str(data))
                ans = methodToCall(data)
                self.log.debug('send answer: ' + ans)
                conn.send(bytes(ans, encoding = 'UTF-8'))
                conn.close()
            except socket.error as ex:
                if self._continue:
                    self.log.error(str(type(ex)) + " : " + str(ex))
        self.sock.close()

    def send(self, hostIp, port, msg):
        self.log.debug('send to host ' + hostIp + ', port ' + str(port) + ' message: ' + msg)
        sock = socket.socket()  # создаем сокет
        sock.connect((hostIp, port))  # подключемся к серверному сокету
        sock.send(bytes(msg, encoding = 'UTF-8'))  # отправляем сообщение
        sock.close()  # закрываем соединение

    def sendAndReceive(self, hostIp, port, msg):
        self.log.debug('send to host ' + hostIp + ', port ' + str(port) + ' message: ' + msg)
        sock = socket.socket()  # создаем сокет
        sock.connect((hostIp, port))  # подключемся к серверному сокету
        sock.send(bytes(msg, encoding = 'UTF-8'))  # отправляем сообщение
        data = sock.recv(1024)  # читаем ответ от серверного сокета
        data = data.decode("UTF-8")
        self.log.debug('receive answer: ' + str(data))
        sock.close()  # закрываем соединение
        return data

    def __generatePort(self, excludePorts: list):
        port = random.randint(4000, 10000)
        while port in excludePorts:
            port = random.randint(4000, 10000)
        return port

    def __bindSock(self):
        try:
            self.sock.bind((self.hostIp, self.port))  # связываем сокет с портом, где он будет ожидать сообщения
        except OSError as ex:
            realHostIp = socket.gethostbyname(self.hostName)
            if (realHostIp != self.hostIp):
                self.log.error("incorrect host was passed through the config file\nassigned host is " + realHostIp)
                self.hostIp = realHostIp
                self.sock.bind((self.hostIp, self.port))
            else:
                raise ex

    def __exit__(self):
        self._continue = False
        if not self.sock is None:
            self.log.debug("close socket connection")
            self.sock.close()
        