import os
import cv2

class LoadFiles:
    def get_templates(self, path):
        files = os.listdir(path)
        listAbsolute = []

        for file in files:
            listAbsolute.append(os.path.abspath(os.path.join(path, file)))

        return listAbsolute

    def import_templates(self, paths):
        templates = []

        for templateUrl in paths:
            template = self.read_template(templateUrl)
            templates.append(template)
        
        return templates
        
    def read_template(self, templateUrl):
        return cv2.imread(templateUrl, cv2.IMREAD_UNCHANGED)