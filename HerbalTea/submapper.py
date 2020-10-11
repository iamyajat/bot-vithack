# importing the module 
import cv2
import faulthandler

faulthandler.enable()
# function to display the coordinates of 
# of the points clicked on the image 
cord = ([0,0,384,384],[240, 70, 125, 125],[45,75,55,95],[85,70,120,120],[290,180,65,110])
raw_img = cv2.imread('house_map.png', 1)
#cv2.imwrite("cache.png",img)
def click_event(event, x, y, flags, params): 

	# checking for left mouse clicks 
	if event == cv2.EVENT_LBUTTONDOWN: 

		#img = cv2.imread('cache.png', 1)
		img = raw_img[cord[i][1]:cord[i][1]+cord[i][3], cord[i][0]:cord[i][0]+cord[i][2]]

		# displaying the coordinates 
		# on the Shell 
		print(x, ' ', y) 
		global refPt
		refPt=[(x,y)]

		# displaying the coordinates 
		# on the image window 
		font = cv2.FONT_HERSHEY_SIMPLEX 
		cv2.putText(img, '.', (x,y), font,1, (255, 0, 0), 2) 
		cv2.imshow('image', img) 


# driver function 
#if __name__=="__main__": 
def submap_maker():
	# reading the image
	global i
	raw_img = cv2.imread('house_map.png', 1)
	i = int(input())
	print(i)
	img = raw_img[cord[i][1]:cord[i][1]+cord[i][3], cord[i][0]:cord[i][0]+cord[i][2]]
	#cv2.imwrite("cache.png",img)

	# displaying the image 
	cv2.imshow('image', img) 
	print(img.shape)

	# setting mouse hadler for the image 
	# and calling the click_event() function 
	cv2.setMouseCallback('image', click_event)
	
	cv2.waitKey(0) 
	cv2.destroyAllWindows() 
	
	
submap_maker()
print(refPt)

refPt = [(refPt[0][0]+cord[i][0]-192,refPt[0][1]+cord[i][1]-192)]

print(refPt)



