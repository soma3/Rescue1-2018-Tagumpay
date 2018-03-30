import numpy

def intersect (l1,l2): #returns point of intersection of line segments and  if they're perpendicular
	grad1 = (l1[3]-l1[1])/(l1[2]-l1[0]) #gradient of line 1
	grad2 = (l2[3]-l2[1])/(l2[2]-l2[0]) #gradient of line 2
	int1 = l1[1]-(l1[0]*grad1) #y intercept of line 1
	int2 = l2[1]-(l2[0]*grad2) #y intercept of line 2
	if grad1 != grad2: #if not parallel
		ptx = (int2 - int1)/(grad1 - grad2) #x coord of intersection
		pty = grad1*ptx + int1 #y coord of intersection
		if l1[0]<=ptx<=l1[2] and l2[0]<=ptx<=l2[2]: #if the point of intersection lies within both line segments
			recgrad = -1/grad1 
			if 0.85*grad2>=abs(recgrad)>=1.15*grad2: #if the two lines are kinda perpendicular
				return [True, ptx , pty]
			else: 
				return [False, ptx , pty]

def extend (lines): #takes lines and returns extended ones
	for line in lines:
		x1 = line[0]
		y1 = line[1]
		x2 = line[2]
		y2 = line[3]
		grad = (y2-y1)/(x2-x1) 
		leng = numpy.sqrt((y1-y2)**2+(x1-x2)**2)
		extlines.append([(x1-extLen),(y1-extLen*grad),(x2+extLen),(y2+extLen*grad)])
	return extlines

def cornerlist (lines): #takes lines and returns the coordinates of corners
	cornerlist = [] #creates array
	extended = extend(lines) #extends lines
	i = 0 
	if lines != None: #if there are lines
		while i < len(extended) - 1: #runs through every combination of lines
			j = i
			while j < len (extended) -1:
				out = intersect(lines[i],lines[j]) 
				if (out[1]): #checks if they are intersecting and perpendicular
					cornerlist.append([out[2],out[3]]) #adds the coordinates of corners to the array
				j = j + 1
			i = i + 1
	return cornerlist

def proxCorners (corners): #finds if there are areas w more than 1 corners next to each others and where they are
	#probably has a lot of redundant lines when it checks if a corner has already been included in a cluster
	i = 0
	proxCorners = [] #sets up array for clustered corners
	while i < len(corners)-1:
		j = i
		while j < len(corners)-1: #runs through all combinations of corners
			dist = numpy.sqrt((corner[i][0]-corner[j][0])**2 + (corner[i][1]-corner[j][1])**2)
			if dist <= proxLen: #if the distance between 2 corners is less than a certain distance
				if corners[i] in proxcorners: 
					iposn = proxcorners.index(corners[i])
					if corners[j] not in proxcorners: # if the both corners are included, don't do anything
                                            proxcorners[iposn].extend(corners[j]) #add second corner to the cluster with the first one
				elif corners[j] in proxcorners: #if only the second corner is already included, 
					jposn = proxcorners.index(corners[j])
					proxCorners[jposn].extend(corners[i]) #add the first corner to the cluster with the second one 
				else:
					proxCorners.append(corners[i],corners[j]) #if both corners haven't been found, add it to a new cluster
			j = j + 1
		i = i + 1
	cornerClusters = [] #sets up array for posn of clusters
	i = 0
	while i < len(proxCorners)-1:
		cluster = proxCorners[i]
		j = 0 
		xsum = 0
		ysum = 0
		while j < len(cluster)-1:
			xsum = xsum + cluster[j][0]
			ysum = ysum + cluster[j][1]
		xavg = xsum / len(cluster)
		yavg = ysum / len(cluster)
		cornerClusters.append(xavg, yavg, len(cluster))
        return cornerClusters

	
		

extLen = 0.1 #check what value to use!
proxLen = 20 #check what value to use!






'''plan for detecting intersections?
- extend all lines slightly (so make all hough line p outputs 5% longer or something)
- if intersect and perpendicular -> this is a corner
- find the coordinates of all corners
- if 2 corners fall within a x by x square - its a T junction
- if 4 corners fall within a x by x square - its an intersection! wew
'''