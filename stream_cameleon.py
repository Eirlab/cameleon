import cv2
from flask import Blueprint, Response, render_template
from configure_cameleon import ConfigureCameleon

class StreamCameleon:
    def __init__(self):
        self.bp = Blueprint('stream', __name__, url_prefix='/stream')
        self.configuration = ConfigureCameleon()
        self.bp.route('/video_stream/<device>')(self.video_stream)
        self.bp.route('/stop')(self.stop)

    def gen_frames(self):
        self.cap = cv2.VideoCapture(self.device_id)
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video_stream(self, device):
        self.device_id = int(device)
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stop(self):
        self.cap.release()
        return render_template('index.html', success="Stream stopped")