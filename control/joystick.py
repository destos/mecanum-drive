from gevent import monkey; monkey.patch_all()
import gevent

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from mecanum.types import Drive
from hardware.wheels import ServoWheels
from hardware.joysticks import JoystickTwoSticks

drive = None
try:
    from adafruit.pwm import PWM
    pwm = PWM(address=0x40, debug=False)
    pwm.setPWMFreq(50)
    drive = Drive(wheels=ServoWheels(pwm), joystick=JoystickTwoSticks())
except Exception, e:
    print e
finally:
    drive = Drive(joystick=JoystickTwoSticks())


class JoystickPositions(BaseNamespace, BroadcastMixin):
    def on_joystick_update(self, position):
        global drive
        drive.js.pos=position
        drive.calc_speeds()
        print drive.wheels.pos
        
    # def recv_connect(self):
    #     def sendjoy():
    #         while True:
    #             # self.emit('joystick_change', {'point': random.randint(1,100)})
    #             gevent.sleep(0.1)
    #     self.spawn(sendjoy)


class Application(object):
    def __init__(self):
        self.buffer = []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

        if path.startswith('static/') or path == 'index.html':
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/joysticks': JoystickPositions})
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


def main():
    print 'Listening on port http://0.0.0.0:8080 and on port 10843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()

if __name__ == '__main__':
    main()