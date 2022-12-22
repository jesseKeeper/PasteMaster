import cv2 
import numpy as np
padRange = [[2, 0, 0], [60, 255, 255]]
bluePcbRange = [[100, 100, 40], [130, 255, 255]]

greenPadRange = [[2, 0, 0], [40, 255, 255]]
greenPcbRange = [[60, 100, 40], [90, 255, 255]]

def makeColorMask(image, colorRange):
    lower = np.array(colorRange[0])
    upper = np.array(colorRange[1])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    return mask

def findAndSortContours(image):
    contours, hierarchy = cv2.findContours(
        image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)
    return sortedContours, hierarchy

def isolatePCB(image, pcbColor):
    pcbMask = makeColorMask(image, pcbColor)
    cv2.imwrite("PCBmask.jpg", pcbMask)
    sortedContours, _ = findAndSortContours(pcbMask)
    
    rect = cv2.minAreaRect(sortedContours[0])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    mask = np.zeros_like(image)
    cv2.drawContours(mask, [box], 0, (255, 255, 255), -1)
    cv2.imwrite("PCBmaskContour.jpg", mask)
    out = np.zeros_like(image)
    out[mask == 255] = image[mask == 255]
    cv2.imwrite("IsolatedPCB.jpg", out)
    cv2.imshow("PCB", out)
    return out

def findPads(image, padColor, pcbColor):
    isolatedPCB = isolatePCB(image, pcbColor)
    padMask = makeColorMask(isolatedPCB, padColor)
    cv2.imwrite("padMask.jpg", padMask)
    padContours, hierarchy = findAndSortContours(padMask)
    for i in range(len(padContours)):
        rect = cv2.minAreaRect(padContours[i])
        box = cv2.boxPoints(rect)    
        box = np.int0(box)
        padContours[i] = box
    return padContours, hierarchy

def classifyThtPads(pads, hierarchy):
    numOfPads = len(pads)
    thtPads = []
    for i in range(numOfPads):
        if hierarchy[0][i][2] > 0:
            thtPads.append(pads[i])
    return thtPads
    
image = cv2.imread("test7.jpg")

pads, hierarchy = findPads(image, padRange, bluePcbRange)


print(pads)
cv2.drawContours(image, pads, -1, (0, 0, 255), 3)
cv2.imshow("pads", image)
# cv2.imwrite("result.jpg", image)
cv2.waitKey(0)