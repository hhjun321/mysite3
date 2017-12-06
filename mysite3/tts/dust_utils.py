from math import sin, cos, sqrt, atan2, radians
# approximate radius of earth in km
def getDistance(x1,y1,x2,y2):

    R = 6373.0

    lat1 = radians(float(x1) )
    lon1 = radians(float(y1))
    lat2 = radians( float(x2))
    lon2 = radians(float(y2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    #print("Result:", distance)

    return distance


#urlopen('http://172.30.1.58/led?led='+txt)
