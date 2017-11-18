

"""Searches all templates to find the best match. Search will proceed from smallest
template size to largest template size and will terminate pre-maturely if
the match correlation decreases continuously with a size increase"""
def findScale(inputFrame, template):
    maxMatchVal = 0
    maxMatchLoc = (0, 0)
    maxIndex = currIndex
    for idx, template in enumerate(templates):       
        res = cv2.matchTemplate(frame, template, cv2.TM_CCORR_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal > maxMatchVal:
            maxMatchVal = maxVal
            maxMatchLoc = maxLoc
            maxIndex = idx
    return maxLoc, maxIndex

""" Searches above and below current index to see which template matches
the input frame better and returns the top left coordinate, the new best index
"""
def adjustScale(currentFrame, currIndex, templates):
    maxMatchVal = 0
    maxMatchLoc = (0, 0)
    maxIndex = currIndex
    for idx in range(currIndex-1, currIndex+2):
        if idx >=0 and idx < len(templates):        
            res = cv2.matchTemplate(frame, templates[currIndex], cv2.TM_CCORR_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if maxVal > maxMatchVal:
                maxMatchVal = maxVal
                maxMatchLoc = maxLoc
                maxIndex = idx
    return maxLoc, maxIndex