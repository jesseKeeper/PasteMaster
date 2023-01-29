import numpy as np
import cv2

class Detector:
    def __init__(self, pad_range, pcb_range, pixels_per_milimeter, offset):
        self.pad_range = pad_range
        self.pcb_range = pcb_range
        self.pixels_per_milimeter = pixels_per_milimeter
        self.offset = offset

    def make_color_mask(self, image, colorRange):
        lower = np.array(colorRange[0])
        upper = np.array(colorRange[1])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        return mask

    def find_and_sort_contours(self, image):
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
        sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)
        return sortedContours, hierarchy

    def isolate_pcb(self, image, pcbColor):
        pcbMask = self.make_color_mask(image, pcbColor)
        cv2.imwrite("PCBmask.jpg", pcbMask)
        sortedContours, _ = self.find_and_sort_contours(pcbMask)
        
        rect = cv2.minAreaRect(sortedContours[0])
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [box], 0, (255, 255, 255), -1)
        cv2.imwrite("PCBmaskContour.jpg", mask)
        out = np.zeros_like(image)
        out[mask == 255] = image[mask == 255]
        cv2.imwrite("IsolatedPCB.jpg", out)
        return out

    def find_pads(self, image, padColor, pcbColor):
        isolatedPCB = self.isolate_pcb(image, pcbColor)
        padMask = self.make_color_mask(isolatedPCB, padColor)
        cv2.imwrite("padMask.jpg", padMask)
        padContours, hierarchy = self.find_and_sort_contours(padMask)
        for i in range(len(padContours)):
            rect = cv2.minAreaRect(padContours[i])
            box = cv2.boxPoints(rect)    
            box = np.intp(box)
            padContours[i] = box
        return padContours, hierarchy

    def filter_by_area(self, pads, minArea):
        filteredPads = []
        for pad in pads:
            if cv2.contourArea(pad) > minArea:
                filteredPads.append(pad)
        return filteredPads

    def get_middle_points(self, pads):
        middlePoints = []
        for i in pads:
            M = cv2.moments(i)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                middlePoints.append((cx, cy))
        return middlePoints

    def pixel_to_printer_coordinate(self, pixelCoordinate, imageOrigin, imageSize):
        centerX = imageSize[0] / 2
        centerY = imageSize[1] / 2
        
        pixelOffsetX = pixelCoordinate[0] - centerX
        pixelOffsetY = pixelCoordinate[1] - centerY

        mmOffsetX = pixelOffsetX / self.pixels_per_milimeter
        mmOffsetY = pixelOffsetY / self.pixels_per_milimeter
        printerX = imageOrigin[0] + mmOffsetY + self.offset[0]
        printerY = imageOrigin[1] + mmOffsetX - self.offset[1]

        return((printerX, printerY))

    def pads_to_printer_coordinates(self, pixelCoordinates, imageOrigin, imageSize):
        coordinates = []
        for coordinate in pixelCoordinates:
            coordinates.append(self.pixel_to_printer_coordinate(coordinate, imageOrigin, imageSize))
        return coordinates

    # callable functions
    def detect(self, image_name, image_origin, image_size):
        image = cv2.imread(image_name)
        pads, hierarchy = self.find_pads(image, self.pad_range, self.pcb_range)
        filteredPads = self.filter_by_area(pads, 100)
        middle_points = self.get_middle_points(filteredPads)
        printer_coordinates = self.pads_to_printer_coordinates(middle_points, image_origin, image_size)
        # cv2.drawContours(image, filteredPads, -1, (0, 0, 0), 5)
        # cv2.imwrite("detected.jpg", image)
        web_coordinates = []
        
        for i in range(len(filteredPads)):
            web_coordinates.append(filteredPads[i].tolist())
            
        return printer_coordinates, web_coordinates