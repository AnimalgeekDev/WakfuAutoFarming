import os
import cv2

def get_templates(path):
    files = os.listdir(path)
    listAbsolute = []

    for file in files:
        listAbsolute.append(os.path.abspath(os.path.join(path, file)))

    return listAbsolute

def import_templates(paths):
    templates = []

    for templateUrl in paths:
        template = read_template(templateUrl)
        templates.append(template)
    
    return templates
    
def read_template(templateUrl):
    return cv2.imread(templateUrl)