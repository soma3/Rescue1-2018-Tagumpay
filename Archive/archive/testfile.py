# importing things

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils # for things like resizing (?)
import time

camera = PiCamera()
camera.framerate = 10
camera.sensor_mode = 2
camera.resolution = (656, 452)
rawCapture = PiRGBArray(camera, size=(656, 452))



def extend (lines): #takes lines and returns extended ones
	extlines=[]
	for line in lines:
		x1 = line[0][0]
		y1 = line[0][1]
		x2 = line[0][2]
		y2 = line[0][3]
		leng = np.sqrt((y1-y2)**2+(x1-x2)**2)
		if x2-x1 != 0:
                    grad = np.arctan((y2-y1)/(x2-x1))
                    extlines.append([(x1-extLen*np.cos(grad)),(y1-extLen*np.sin(grad)),(x2+extLen*np.cos(grad)),(y2+extLen*np.sin(grad))])
                else:
                    extlines.append([(x1),(y1-extLen),(x2),(y2+extLen)])
                    
	return extlines
    
def intersect (l1,l2): #returns point of intersection of line segments and  if they're perpendicular
	int = True
	
	if l1[2]-l1[0] != 0:
            grad1 = np.arctan((l1[3]-l1[1])/(l1[2]-l1[0])) #gradient of line 1
            int1 = l1[1]-(l1[0]*(np.tan(grad1))) #y intercept of line 1
            if l2[2] - l2[0] != 0: #if both lines are nonvertical
                grad2 = np.arctan((l2[3]-l2[1])/(l2[2]-l2[0])) #gradient of line 2
                int2 = l2[1]-(l2[0]*(np.tan(grad2))) #y intercept of line 2
                if grad1 != grad2: #if not parallel
                    ptx = (int2 - int1)/((np.tan(grad1)) - (np.tan(grad2))) #x coord of intersection
                    pty = (np.tan(grad1))*ptx + int1 #y coord of intersection
                else:
                    int = False
                    return ([False])
            else: #if only line 2 is vertical
                grad2 = 3.14/2
                ptx = l2[0]
                pty = np.tan(grad1)*ptx + int1
        else:
            grad1 = 3.14/2
            if l2[2] - l2[0] != 0: #if only line 1 is vertical
                grad2 = np.arctan((l2[3]-l2[1])/(l2[2]-l2[0])) #gradient of line 2
                int2 = l2[1]-(l2[0]*(np.tan(grad2))) #y intercept of line 2
                ptx = l1[0]
                pty = np.tan(grad2)*ptx + int2
            else:
                int = False
                return ([False])
        if int is True:
            if l1[0]<=ptx<=l1[2] and l2[0]<=ptx<=l2[2]: #if the point of intersection lies within both line segments
                if grad1 < 0:
                    recgrad = grad1 + 3.14/2
                else:
                    recgrad = grad1 - 3.14/2
                if 1.2+recgrad>= grad2 >=recgrad- 1.2: #if the two lines are kinda perpendicular
                    return [True, ptx , pty]
                else: 
                    return [False, ptx , pty]
            else:
                return [False]


def cornerlist (lines): #takes lines and returns the coordinates of corners
	cornerlist = [] #creates array
	i = 0
	if lines != None: #if there are lines
		while i < len(lines) - 1: #runs through every combination of lines
			j = i + 1
			while j < len (lines) -1:
				out = intersect(lines[i],lines[j])
				if out[0] is True: #checks if they are intersecting and perpendicular
					cornerlist.append([out[1],out[2]]) #adds the coordinates of corners to the array
				j = j + 1
			i = i + 1
	return cornerlist

def proxCorners (corners, proxLen): #finds if there are areas w more than 1 corners next to each others and where they are
	#probably has a lot of redundant lines when it checks if a corner has already been included in a cluster
	i = 0
	proxCorners = [] #sets up array for clustered corners
	while i < len(corners)-1:
		j = i + 1
		while j < len(corners)-1: #runs through all combinations of corners
			dist = np.sqrt((corners[i][0]-corners[j][0])**2 + (corners[i][1]-corners[j][1])**2)
			print corners[i]
			print corners[j]
			print proxCorners
			if dist <= proxLen: #if the distance between 2 corners is less than a certain distance
				if any(corners[i] in x for x in proxCorners): 
					iposn = [(k, corners[i]) for k, el in enumerate(proxCorners) if corners[i] in el]
					if all(corners[j] not in x for x in proxCorners): # if the both corners are included, don't do anything
                                            proxCorners[iposn[0][0]].append(corners[j]) #add second corner to the cluster with the first one
                                        elif corners[j] not in proxCorners[iposn[0][0]]:
                                            jposn = [(k, corners[j]) for k, el in enumerate(proxCorners) if corners[j] in el]
                                            repeat = proxCorners[jposn[0][0]]
                                            proxCorners[iposn[0][0]].extend(repeat)
                                            proxCorners = np.delete(proxCorners, jposn[0][0],0)
				elif any(corners[j] in x for x in proxCorners): #if only the second corner is already included, 
					jposn = [(k, corners[j]) for k, el in enumerate(proxCorners) if corners[j] in el]					
					proxCorners[jposn[0][0]].append(corners[i]) #add the first corner to the cluster with the second one 
				else:
					proxCorners.append([corners[i],corners[j]]) #if both corners haven't been found, add it to a new cluster
                        else:
                            print [corners[j]]
                            print proxCorners
                            proxCorners.append([corners[i]])
                            proxCorners.append([corners[j]])
                            
                        j = j + 1
		i = i + 1
	cornerClusters = [] #sets up array for posn of clusters
	i = 0
	print 'mao'
	print proxCorners
	while i < len(proxCorners)-1:
		cluster = proxCorners[i]
		j = 0 
		xsum = 0
		ysum = 0
		while j < len(cluster)-1:
			xsum = xsum + cluster[j][0]
			ysum = ysum + cluster[j][1]
			j = j +1
		if len(cluster)>0: #why do i need this line???
                    xavg = xsum / len(cluster)
                    yavg = ysum / len(cluster)
                    cornerClusters.append([xavg, yavg, len(cluster)])

        return cornerClusters	

extLen = 15 #check what value to use!

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
        resized = imutils.resize(image, 500)
        crop = resized[0:300,300:499]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) # convert to grayscale
	blur = cv2.GaussianBlur(gray,(5,5),0) # remove noise
	thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize = 501, C = -10)
        canny = cv2.Canny(blur, 90, 70, apertureSize=3)
        line = cv2.HoughLinesP(canny, 1, 0.05, 15, minLineLength=30 , maxLineGap=20)
        '''for x1,y1,x2,y2 in line[0]:
            canny=cv2.line(blur, (x1,y1), (x2, y2), (0,0,255),22)
        '''
        extline = []
        cornerClust =[[]]
        ##print(len(line))
	
	if line is not None:
            extline = extend(line)
            corners = cornerlist(extline)
            cornerClust = proxCorners(corners, 5) #groups repeated corners together
            print len(cornerClust)
            if len(cornerClust) == 2: #consider using proxCorners again if there are random dots / 2 intersections in frame
                cv2.putText(blur, 'T JUNCTION', (0,0), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0))
            elif len(cornerClust) == 3:
                cv2.putText(blur, '???', (0,0), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0))
            elif len(cornerClust) > 3:
                cv2.putText(blur, 'INTERSECTION', (0,0), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0))
            else:
                cv2.putText(blur, 'nothing', (0,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0))
            
           
            i = 0
            while i <len(line)-1: 
                #cv2.line(blur,(int(line[i][0][0]),int(line[i][0][1])),(int(line[i][0][2]),int(line[i][0][3])),(0,255,0),2)
                i=i+1
            i = 0
            while i <len(extline)-1: 
                cv2.line(blur,(int(extline[i][0]),int(extline[i][1])),(int(extline[i][2]),int(extline[i][3])),(0,255,0),2)
                i=i+1
            i = 0
            while i<len(cornerClust)-1:
                #cv2.circle(blur, (int(cornerClust[i][0]),int(cornerClust[i][1])),4,(255,0,0),thickness=-1)
                i = i+1
            while i<len(corners)-1:
                cv2.circle(blur, (int(corners[i][0]),int(corners[i][1])),4,(255,0,0),thickness=-1)
                i = i+1
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	cv2.namedWindow("Frame")
	cv2.imshow("Frame",blur)
	cv2.imshow("Frame2",canny)
	print'frame'
    
	key = cv2.waitKey(10) & 0xFF
	
	if key == ord("q"):
                break
	