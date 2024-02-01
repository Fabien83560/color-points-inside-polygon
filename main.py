# ORTEGA Fabien - TP1

import xml.etree.ElementTree as ET
import time 

def orientation(firstPoint, secondPoint, thirdPoint):
    """
    Calculate the orientation of three points.
    """
    return (firstPoint[0] * secondPoint[1]) + (secondPoint[0] * thirdPoint[1]) + (thirdPoint[0] * firstPoint[1]) - (firstPoint[0] * thirdPoint[1]) - (secondPoint[0] * firstPoint[1]) - (thirdPoint[0] * secondPoint[1])

def intersect(firstSegment, secondSegment):
    """
    Check if two line segments intersect.
    """
    firstSegmentPointX, firstSegmentPointY = firstSegment
    secondSegmentPointX, secondSegmentPointY = secondSegment

    firstOrientation = orientation(firstSegmentPointX, secondSegmentPointX, secondSegmentPointY)
    secondOrientation = orientation(secondSegmentPointX, secondSegmentPointY, firstSegmentPointY)
    thirdOrientation = orientation(firstSegmentPointX, firstSegmentPointY, secondSegmentPointX)
    fourthOrientation = orientation(firstSegmentPointX, firstSegmentPointY, secondSegmentPointY)

    if ((firstOrientation == 0 and ((fourthOrientation > 0 and thirdOrientation < 0) or (fourthOrientation < 0 and thirdOrientation > 0))) or (firstSegment[0] == secondSegment[0])):
        return "yellow"
    
    return ((secondOrientation > 0 and firstOrientation < 0) or (secondOrientation < 0 and firstOrientation > 0)) and ((fourthOrientation > 0 and thirdOrientation < 0) or (fourthOrientation < 0 and thirdOrientation > 0))

def isInsidePolygon(actualX, actualY, polygon, max_x):
    """
    Check if a point is inside, outside, or on the border of a polygon.
    """
    intersectCount = 0
    firstSegment = [[actualX, actualY], [max_x, actualY + 1]]
    
    for i in range(len(polygon)):
        secondSegment = [polygon[i], polygon[(i + 1) % len(polygon)]]
        actualIntersect = intersect(firstSegment, secondSegment)
        
        if actualIntersect == "yellow":
            return "yellow"
        elif actualIntersect:
            intersectCount += 1
    
    if intersectCount % 2 == 1:
        return "green"
    else:
        return "red"

def printReport(inside, outside, border, finalTime):
    """
    Print the report containing statistics and execution time.
    """
    print("-----------------------------")
    print("Report")
    print("-----------------------------")
    print("Inside : ", inside)
    print("Outside : ", outside)
    print("Border : ", border)
    print("-----------------------------")
    print("Time : ", finalTime, "seconds")
    print("-----------------------------")

def transform_svg(inputFilename, outputFilename):
    """
    Transform SVG file based on polygon and point positions.
    """
    # Read the SVG file
    tree = ET.parse(inputFilename)
    root = tree.getroot()

    # Extract polygon vertices
    polygon = []
    for path in root.findall('.//{http://www.w3.org/2000/svg}polygon'):
        svgPoints = path.attrib['points'].split()

        for point in svgPoints:
            array = point.split(",")
            polygon.append([int(array[0]), int(array[1])])

    inside = 0
    outside = 0
    border = 0

    max_x = int(root.attrib.get('width', 0))

    # Process each point and color accordingly
    t1 = time.time()
    for point in root.findall('.//{http://www.w3.org/2000/svg}circle'):
        x = int(point.attrib['cx'])
        y = int(point.attrib['cy'])
        value = isInsidePolygon(x, y, polygon, max_x)
        
        if value == "green":
            point.attrib['fill'] = 'green'
            inside += 1
        elif value == "red":
            point.attrib['fill'] = 'red'
            outside += 1
        else:
            point.attrib['fill'] = 'yellow'
            border += 1
    
    finalTime = "{:.2f}".format(time.time() - t1)

    printReport(inside, outside, border, finalTime)
    
    # Save the modified SVG file
    tree.write(outputFilename)

inputFilename = "img/italy.svg"
outputFilename = "out/output.svg"
transform_svg(inputFilename, outputFilename)
