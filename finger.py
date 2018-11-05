import serial
from gevent import select
import gevent
import lock
import buzzer

SUCCESS, FAIL, FULL, NOUSER, USER_OPD, FIN_OPD, TIMEOUT = (0, 1, 4, 5, 6, 7, 8)

ACK_ERROR = {
    1: "FAIL",
    4: "FULL",
    5: "NOUSER",
    6: "USER_OPD",
    7: "TIMEOUT"
}


class _Finger:
    _ser = None
    _buf = None
    _running = False

    def refresh(self):
        self._buf = bytearray(8)
        self._buf[0] = 0xf5
        self._buf[7] = 0xf5

    def loop(self):
        while (True):
            print("running")
            self.judgefinger()
            select.select([self._ser], [], [])
            if self.isrunning() is False:
                return
            id, auth = self.checkfinger()
            if auth > 3:
                print("Finger error", ACK_ERROR[auth])
                buzzer.ring()
                continue
            print("id = ", id)
            lock.unlock()

    def isrunning(self):
        return self._running

    def start(self):
        if self._running is True:
            return
        self._running = True
        gevent.spawn(self.loop)

    def stop(self):
        self._running = False

    def __init__(self):
        self._ser = serial.Serial()
        self._ser.baudrate = 19200

    def open(self, port):
        self._ser.port = port
        self._ser.open()

    def _getchk(self):
        ret = 0
        for num in range(self._buf[1:5]):
            ret ^= num
        return ret

    def send(self):
        data = self._buf[1]
        for item in self._buf[2:5]:
            data = data ^ item
        self._buf[6] = data
        self._ser.write(self._buf)

    def read(self):
        data = self._ser.read(8)
        if (data[0] != 0xf5) or (data[0] != 0xf5):
            raise Exception("read error")
        return data

    def sleep(self):
        self.stop()
        self.refresh()
        self._buf[1] = 0x2c
        self.send()

        self.read()
        return True

    def addfinger(self, num, id, auth):
        self.stop()
        self.refresh()
        self._buf[1] = int(num)
        self._buf[2] = 0xff & (id >> 8)
        self._buf[3] = 0xff & id
        self._buf[4] = auth
        self.send()

        return self.read()[4]

    def delfinger(self, id):
        self.stop()
        self.refresh()
        self._buf[1] = 4
        self._buf[2] = 0xff & (id >> 8)
        self._buf[3] = 0xff & id
        self.send()

        return self.read()[4]

    def delallfinger(self):
        self.stop()
        self.refresh()
        self._buf[1] = 5
        self.send()

        return self.read()[4]

    def getusernum(self):
        self.stop()
        self.refresh()
        self._buf[1] = 9
        self.send()

        data = self.read()

        if data[4] == FAIL:
            return -1
        return int(data[2]) << 8 | int(data[3])

    def getuserauth(self, id):
        self.stop()
        self.refresh()
        self._buf[1] = 0x0a
        self._buf[2] = 0xff & id >> 8
        self._buf[3] = 0xff & id
        self.send()

        return self.read()[4]

    def judgefinger(self):
        self.refresh()
        self._buf[1] = 0x0c
        self.send()

    def checkfinger(self):
        data = self.read()
        id = int(data[2]) << 8 | data[3]
        auth = data[4]
        return id, auth
