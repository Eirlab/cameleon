import os
import time

import cv2
from flask import Blueprint, Response, render_template

from configure_cameleon import ConfigureCameleon


class StreamCameleon:
    def __init__(self):
        self.bp = Blueprint('stream', __name__, url_prefix='/stream')
        self.configuration = ConfigureCameleon()
        self.file_name = None
        self.bp.route('/video_stream/<device>')(self.video_stream)
        self.bp.route('/stop')(self.stop)

    def gen_frames(self):
        self.cap = cv2.VideoCapture(self.device_id)
        if self.configuration.recording:
            frame_width = int(self.cap.get(3))
            frame_height = int(self.cap.get(4))
            time_formatted = time.strftime("%Y_%m_%d_%H_%M")
            self.file_name = str(time_formatted) + '_' + str(self.device_id) + '.mp4'
            out = cv2.VideoWriter('record/' + self.file_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                  (frame_width, frame_height))
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                if self.configuration.recording:
                    out.write(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video_stream(self, device):
        self.device_id = int(device)
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stop(self):
        self.cap.release()
        if self.configuration.share:
            print('share : WIP')
            # self.configuration.share_video(self.file_name)
        return render_template('index.html', success="Stream stopped")
