import cv2
import numpy as np

import sys
sys.path.append("..") 

from libs import load_files
from libs import search_on_img

patchTestImages = "test_img"
patchFarmingIcons = "../farming_actions"
patchResults = "results"

tolerancy = 0.75

showImg = False

testImages = load_files.get_templates(patchTestImages)

templateImages = load_files.get_templates(patchFarmingIcons)

for imageUrl in testImages:
    test_img = load_files.read_template(imageUrl)

    for templateUrl in templateImages:
        print(f'{patchResults}/{imageUrl.split(".")[0].split("\\")[-1]}-{templateUrl.split("\\")[-1]}')
        template = cv2.imread(templateUrl, cv2.IMREAD_UNCHANGED)

        x, y, tol, dec, match = search_on_img.search_template_on_img(template, test_img, tolerancy)

        if showImg:
            cv2.imshow("Best Match", match)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        if x > 0 and y > 0:
            # Mostrar las coordenadas
            print(f"Better pos detection (x, y): ({x}, {y}); (dec < tol): ({dec},{tol})")
            
            h, w =  template.shape[:2]

            img_copy = test_img.copy()

            cv2.rectangle(img_copy, (x - (w // 2), y - (h // 2)), (x + w, y + h), (0,0,255), 3)
            cv2.putText(img_copy, templateUrl.split("\\")[-1], (x // 1,y // 1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,200), 3)
            cv2.imwrite(f'{patchResults}/{imageUrl.split(".")[0].split("\\")[-1]}-{templateUrl.split("\\")[-1]}', img_copy) 