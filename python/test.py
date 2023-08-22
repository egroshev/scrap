def ruleRampUp(slopeArr, xintArr, ymaxArr):
    """
    if line2 or line3 >= 300mV
        line2 >= line3 + 200mV
    if line2 or line3 < 300mV
        # no requirement.
    find x boundaries for applying rule

    Args:
        slopeArr ([float]): slope array in volts/sec for rails 1,2,3.
                            This ramp rate should always be a positive, this method accounts for that fact.
        xintArr ([float]): delay array in sec for rails 1,2,3
        ymaxArr ([float]): nominal or max expected voltage array in volts for rails 1,2,3
        yArr ([float]): 
    """

    def yUp(slope, xint, ymax, x):
        """
        This method gives you y value for a given x, or returns y boundaries.
        y = m(x-b) {0 <= y <= ymax}
        """
        if x <= xint:
            # boundary condition, cannot have negative y.
            return 0
        y = slope * (x - xint)
        if y >= ymax:
            # boundary condition, canot have higher than ymax
            return ymax
        return y

    def xUp(slope, xint, ymax, y):
        """
        This method gives the x value for a given y, or returns x boundaries.
        May be able to get away with x boundaries for all intents and purposes
        x = y/m + b {0 <= y <= ymax}
        """
        if y <= 0:
            # boundary condition, cannot have negative y.
            return xint
        if y >= ymax:
            # boundary condition, canot have higher than ymax
            return ymax/slope + xint
        return y/slope + xint

    # RULE
    # if line2 or line3 >= 300mV
    #     line2 >= line3 + 200mV
    # if line2 or line3 < 300mV
    #     # no requirement.
    # END RULE

    # find x boundaries for applying rule
    x2_low = xUp(slopeArr[2], xintArr[2], ymaxArr[2], y=0.3)
    x3_low = xUp(slopeArr[3], xintArr[3], ymaxArr[3], y=0.3)
    x2_high = xUp(slopeArr[2], xintArr[2], ymaxArr[2], y=ymaxArr[2])
    x3_high = xUp(slopeArr[3], xintArr[3], ymaxArr[3], y=ymaxArr[3])
    x_low_first = min(x2_low, x3_low) #use x boundary of whichever goes up to 0.3V soonest
    x_high_first = min(x2_high, x3_high) #use x boundary of whichever reaches their max voltage soonest.
    
    # Use the x boundaries to determine if we meet the rule conditions.
    y2_low = yUp(slopeArr[2], xintArr[2], ymaxArr[2], x=x_low_first)
    y3_low = yUp(slopeArr[3], xintArr[3], ymaxArr[3], x=x_low_first)
    if round(y2_low, 9) < round(y3_low + 0.2, 9): # floating point arithmetic is innacurate, so truncate innacuracy at 9th decimal.
        return False
    y2_high = yUp(slopeArr[2], xintArr[2], ymaxArr[2], x=x_high_first)
    y3_high = yUp(slopeArr[3], xintArr[3], ymaxArr[3], x=x_high_first)
    if round(y2_high, 9) < round(y3_high + 0.2, 9): # floating point arithmetic is innacurate, so truncate innacuracy at 9th deicimal.
        return False
    return True


def ruleRampDown(slopeArr, xintArr, ymaxArr):
    """
    if line2 or line3 >= 300mV
        line2 >= line3 + 200mV
    if line2 or line3 < 300mV
        # no requirement.
    find x boundaries for applying rule

    Args:
        slopeArr ([float]): slope array in volts/sec for rails 1,2,3. 
                            This ramp rate should always be a positive, this method accounts for that fact.
        xintArr ([float]): delay array in sec for rails 1,2,3
        ymaxArr ([float]): nominal or max expected voltage array in volts for rails 1,2,3
        yArr ([float]): 
    """

    def yDown(slope, xint, ymax, x):
        """
        This method gives you y value for a given x, or returns y boundaries.
        y = m(b-x) + ymax {0 <= y <= ymax}
        """
        if x <= xint:
            # boundary condition, canot have higher than ymax
            return ymax
        y = slope * (xint - x) + ymax
        if y <= 0:
            # boundary condition, cannot have negative y.
            return 0
        return y

    def xDown(slope, xint, ymax, y):
        """
        This method gives the x value for a given y, or returns x boundaries.
        May be able to get away with x boundaries for all intents and purposes
        x = (ymax-y)/m + b {0 <= y <= ymax}
        """
        if y >= ymax:
            return xint
        if y <= 0:
            return ymax/slope + xint
        return (ymax-y)/slope + xint

    # RULE
    # if line2 or line3 >= 300mV
    #     line2 >= line3 + 200mV
    # if line2 or line3 < 300mV
    #     # no requirement.
    # END RULE

    # find x boundaries for applying rule
    x2_high = xDown(slopeArr[2], xintArr[2], ymaxArr[2], y=ymaxArr[2])
    x3_high = xDown(slopeArr[3], xintArr[3], ymaxArr[3], y=ymaxArr[3])
    x2_low = xDown(slopeArr[2], xintArr[2], ymaxArr[2], y=0.3)
    x3_low = xDown(slopeArr[3], xintArr[3], ymaxArr[3], y=0.3)
    x_high_last = max(x2_high, x3_high) #use x boundary of whichever boundary is the last.
    x_low_last = max(x2_low, x3_low) #use x boundary of whichever declines to 0.3V last (last as per spec, but if following downramp image, it is first)
    
    # Use the x boundaries to determine if we meet the rule conditions.
    y2_high = yDown(slopeArr[2], xintArr[2], ymaxArr[2], x=x_high_last)
    y3_high = yDown(slopeArr[3], xintArr[3], ymaxArr[3], x=x_high_last)
    if round(y2_high, 9) < round(y3_high + 0.2, 9): # floating point arithmetic is innacurate, so truncate innacuracy at 9th deicimal.
        return False
    y2_low = yDown(slopeArr[2], xintArr[2], ymaxArr[2], x=x_low_last)
    y3_low = yDown(slopeArr[3], xintArr[3], ymaxArr[3], x=x_low_last)
    if round(y2_low, 9) < round(y3_low + 0.2, 9): # floating point arithmetic is innacurate, so truncate innacuracy at 9th decimal.
        return False
    return True

slopeArr = [None, 2500, 1200, 400]
xintArr = [None, 0, 0, 0.00000000]
ymaxArr = [None, 2.5, 1.2, 0.8]
print(ruleRampUp(slopeArr=slopeArr, xintArr=xintArr, ymaxArr=ymaxArr))

slopeArr = [None, 2500, 1200, 1300] # PWR2 descends at slower rate.
xintArr = [None, 0, 0.000034, 0.0002] # PWR2 starts descending first.
ymaxArr = [None, 2.5, 1.2, 0.8]
print(ruleRampDown(slopeArr=slopeArr, xintArr=xintArr, ymaxArr=ymaxArr)) 
# At PWR3 initial descent, PWR2 barely 200mV higher, but after both under 300mV, PWR2 is segnificantly larger since PWR3 descends at faster rate.


# # RAMP UP EQUATIONS WITH RAMP UP BOUNDARIES
# def yup(slope, xint, ymax, x):
#     """
#     This method gives you y value for a given x, or returns y boundaries.
#     y = m(x-b) {0 <= y <= ymax}
#     """
#     if x <= xint:
#         # boundary condition, cannot have negative y.
#         return 0
#     y = slope * (x - xint)
#     if y >= ymax:
#         # boundary condition, canot have higher than ymax
#         return ymax
#     return y

# def xup(slope, xint, ymax, y):
#     """
#     This method gives the x value for a given y, or returns x boundaries.
#     May be able to get away with x boundaries for all intents and purposes
#     x = y/m + b {0 <= y <= ymax}
#     """
#     if y <= 0:
#         # boundary condition, cannot have negative y.
#         return xint
#     if y >= ymax:
#         # boundary condition, canot have higher than ymax
#         return ymax/slope + xint
#     return y/slope + xint


# # RAMP DOWN EQUATIONS WITH RAMP DOWN BOUNDARIES
# def ydown(slope, xint, ymax, x):
#     """
#     This method gives you y value for a given x, or returns y boundaries.
#     y = m(b-x) + ymax {0 <= y <= ymax}
#     """
#     if x <= xint:
#         # boundary condition, canot have higher than ymax
#         return ymax
#     y = slope * (xint - x) + ymax
#     if y <= 0:
#         # boundary condition, cannot have negative y.
#         return 0
#     return y

# def xdown(slope, xint, ymax, y):
#     """
#     This method gives the x value for a given y, or returns x boundaries.
#     May be able to get away with x boundaries for all intents and purposes
#     x = (ymax-y)/m + b {0 <= y <= ymax}
#     """
#     if y >= ymax:
#         return xint
#     if y <= 0:
#         return ymax/slope + xint
#     return (ymax-y)/slope + xint


# #print (y(slopeArr[1], xintArr[1], ymaxArr[1], 0.001))
# print ("y")
# print (yup(2.6, 0, 2.6, x=2))
# print (yup(2.6, 0, 2.6, x=1))
# print (yup(2.6, 0, 2.6, x=0.5))
# print (yup(2.6, 0, 2.6, x=0))
# print (yup(2.6, 0, 2.6, x=-1))
# print ("x")
# print (xup(2.6, 0, 2.6, y=-1))
# print (xup(2.6, 0, 2.6, y=0))
# print (xup(2.6, 0, 2.6, y=0.52))
# print (xup(2.6, 0, 2.6, y=1.82))
# print (xup(2.6, 0, 2.6, y=2.6))
# print (xup(2.6, 0, 2.6, y=3))

# print ("y")
# print (ydown(2.6, 0, 2.6, x=2))
# print (ydown(2.6, 0, 2.6, x=1))
# print (ydown(2.6, 0, 2.6, x=0.5))
# print (ydown(2.6, 0, 2.6, x=0))
# print (ydown(2.6, 0, 2.6, x=-1))
# print ("x")
# print (xdown(2.6, 0, 2.6, y=-1))
# print (xdown(2.6, 0, 2.6, y=0))
# print (xdown(2.6, 0, 2.6, y=0.52))
# print (xdown(2.6, 0, 2.6, y=1.82))
# print (xdown(2.6, 0, 2.6, y=2.6))
# print (xdown(2.6, 0, 2.6, y=3))