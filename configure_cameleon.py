import os

from cv2 import cv2
from flask import Blueprint, render_template, request, send_file


class ConfigureCameleon:
    def __init__(self):
        self.bp = Blueprint('configure', __name__, url_prefix='/configure')
        self.camera = None
        self.recording = False
        self.share = False
        self.camera_list = []
        self.file = []

        self.bp.route('/scan', methods=['GET'])(self.scan)
        self.bp.route('/choose_device', methods=['POST'])(self.choose_device)
        self.bp.route('/files', methods=['GET'])(self.list_video)
        self.bp.route('/files/<filename>', methods=['GET'])(self.get_file)

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
            if record:
                print("Recording")
                self.recording = True
        except KeyError:
            self.recording = False
        try:
            share = request.form['share']
            if share:
                self.share = True
        except KeyError:
            self.share = False
        return render_template('index.html', devices=self.camera_list, device_id=self.camera)

    def list_video(self):
        print(self.camera_list, self.camera)
        self.file = os.listdir('record/')
        if len(self.file) == 0:
            return render_template(template_name_or_list='index.html', files=self.file)
        self.file.sort(reverse=True)
        return render_template(template_name_or_list='index.html', files=self.file)

    def get_file(self, filename):
        file_path = 'record/' + filename
        if not os.path.exists(file_path) or filename == '':
            return render_template('404.html')

            # Check if path is a file and serve
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)

            # Show directory contents
        files = sorted(os.listdir(file_path))
        return render_template('index.html', files=files, devices=self.camera_list, device_id=self.camera)
