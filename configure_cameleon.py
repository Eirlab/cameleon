from cv2 import cv2
from flask import Blueprint, render_template, request


class ConfigureCameleon:
    def __init__(self):
        self.bp = Blueprint('configure', __name__, url_prefix='/configure')
        self.camera = None
        self.recording = False
        self.share = False
        self.camera_list = []

        self.bp.route('/scan', methods=['GET'])(self.scan)
        self.bp.route('/choose_device', methods=['POST'])(self.choose_device)

    def scan(self):
        # Find availables cameras
        self.camera_list = []
        for i in range(0, 10):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    self.camera_list.append(i)
                    cap.release()
            except:
                pass
        if len(self.camera_list) == 0:
            return render_template('index.html')
        return render_template('index.html', devices=self.camera_list)

    def choose_device(self):
        # Choose device
        try:
            device = int(request.form['device_id'])
        except KeyError:
            return render_template('index.html', alert='No device selected')
        self.camera = device
        try:
            record = request.form['record']
            if record == 'true':
                self.recording = True
        except KeyError:
            self.recording = False
        try:
            share = request.form['share']
            if share == 'true':
                self.share = True
        except KeyError:
            self.share = False
        return render_template('index.html', devices=self.camera_list, device_id=self.camera, recording=self.recording,
                               share=self.share)
