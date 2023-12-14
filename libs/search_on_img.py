import cv2
import numpy as np

class SearchOnImg:
    bf = None

    threshold = 0
    match_type = '1'
    max_result = 0

    line_color = (0,0,255)
    line_size = cv2.LINE_4

    groupThreshold=0
    eps=0

    def __init__(self):
        self.bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    def search_template_on_img(self, img, template):
        img_mod = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        template_mod = cv2.cvtColor(template, cv2.COLOR_RGBA2GRAY)

        img_match = img.copy()
        img_multi_mach = img.copy()

        resource_w = template_mod.shape[1]
        resource_h = template_mod.shape[0]

        if self.match_type == '1':
            result = cv2.matchTemplate(img_mod, template_mod, cv2.TM_SQDIFF_NORMED)
            locations = np.where(result <= self.threshold)
        elif self.match_type == '2':
            result = cv2.matchTemplate(img_mod, template_mod, cv2.TM_CCORR_NORMED)
            locations = np.where(result >= self.threshold)
        elif self.match_type == '3':
            result = cv2.matchTemplate(img_mod, template_mod, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= self.threshold)
        
        locations = list(zip(*locations[::-1]))

        center_x = 0
        center_y = 0

        if len(locations) < self.max_result:
            rectangles = []
            for loc in locations:
                rect = [int(loc[0]), int(loc[1]), resource_w, resource_h]
                rectangles.append(rect)
                rectangles.append(rect)
            
            rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=self.groupThreshold, eps=self.eps)

            if len(rectangles):
                for (x, y, w, h) in rectangles:
                    center_x = x + w//2
                    center_y = y + h//2
                    
                    top_left = (x , y)
                    bottom_right = (x+w , y+h)

                    img_multi_mach = cv2.rectangle(img_multi_mach, top_left, bottom_right, self.line_color, self.line_size)

                x, y, w, h = rectangles[0]
                center_x = x + w//2
                center_y = y + h//2

                top_left = (x , y)
                bottom_right = (x+w , y+h)
                
                img_match = cv2.rectangle(img_match, top_left, bottom_right, self.line_color, self.line_size)

        return center_x, center_y, img_match, img_multi_mach, (result * 255).astype(np.uint8), len(locations)
    
def main():
    img = cv2.imread('debugger/test_img/cerca.png', cv2.IMREAD_UNCHANGED)
    template = cv2.imread('resource_img/girasol.png', cv2.IMREAD_UNCHANGED)

    searcher = SearchOnImg()
    
    searcher.threshold = 0.075
    searcher.match_type = '1'

    x, y, match, multi_math, result_match, _ = searcher.search_template_on_img(img, template)

    cv2.imshow('match', match)
    cv2.imshow('multi_math', multi_math)
    cv2.imshow('result_match', result_match)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()