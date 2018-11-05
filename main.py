import finger
import web

if __name__ == '__main__':
    web.fing.open("/dev/ttyAMA0")
    # web.fing.getusernum()

    web.start()
