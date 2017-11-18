import cv2

"""Searches all templates to find the best match. Search will proceed from smallest
template size to largest template size and will terminate pre-maturely if
the match correlation decreases continuously with a size increase"""
def findScale(inputFrame, templates):
    maxMatchVal = -1
    maxIndex = 0  #Index of best match

    for idx, (template, templateMaxVal) in enumerate(templates):
        res = cv2.matchTemplate(inputFrame, template, cv2.TM_SQDIFF)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        maxVal /= templateMaxVal #Compare against the maximum correlation value
        if maxVal > maxMatchVal:
            maxMatchVal = maxVal
            maxIndex = idx
    return maxIndex

""" Searches above and below current index to see which template matches
the input frame better and returns the top left coordinate, the new best index
"""
def adjustScale(currentFrame, currIndex, templates):
    maxMatchVal = 0
    maxMatchLoc = (0, 0)
    maxIndex = currIndex
    for idx in range(currIndex-1, currIndex+2):
        if 0 <= idx < len(templates):
            res = cv2.matchTemplate(currentFrame, templates[idx][0], cv2.TM_SQDIFF)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            maxVal /= templates[idx][1] #Normalize against best match
            if maxVal > maxMatchVal:
                maxMatchVal = maxVal
                maxMatchLoc = maxLoc
                maxIndex = idx
    return  maxMatchLoc, maxIndex