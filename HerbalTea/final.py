#!/usr/bin/python
# -*- coding: utf-8 -*-

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script


import rospy
import cv2
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
import speech_recognition as sr
import os
import dialogflow
import faulthandler
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'gcloud_cred.json'

DIALOGFLOW_PROJECT_ID = 'herbaltea-mn9r'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'



class GoToPose:

    def __init__(self):
        self.goal_sent = False

        # What to do if shut down (e.g. Ctrl-C or failure)

        rospy.on_shutdown(self.shutdown)

        # Tell the action client that we want to spin a thread by default

        self.move_base = actionlib.SimpleActionClient('move_base',
                MoveBaseAction)
        rospy.loginfo('Wait for the action server to come up')

        # Allow up to 5 seconds for the action server to come up

        self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal

        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4'
                ]))

        # Start moving

        self.move_base.send_goal(goal)

        # Allow TurtleBot up to 60 seconds to complete task

        success = self.move_base.wait_for_result(rospy.Duration(60))

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()
            self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()

    rospy.loginfo('Stop')
    rospy.sleep(1)
    
cord = ([0,0,384,384],[240, 70, 125, 125],[45,75,55,95],[85,70,120,120],[290,180,65,110])
img = cv2.imread('house_map.png', 1)
cv2.imwrite("cache.png",img)
refPt=[]
i1=0
faulthandler.enable()
    

    
def click_event(event, x, y, flags, params):
    

    # checking for left mouse clicks 
    if (event == cv2.EVENT_LBUTTONDOWN) : 
        img = cv2.imread('cache.png', 1)

        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y)
        global refPt 
        rwfPt = [(x,y)]
		
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText(img, '.', (x,y), font, 1, (255, 0, 0), 2) 
        cv2.imshow('Submap', img)

        
        
def show_submap(i):
    # reading the image
    global j
    j=i
    img = cv2.imread('house_map.pgm', 1)
    img = img[cord[i][1]:cord[i][1]+cord[i][3], cord[i][0]:cord[i][0]+cord[i][2]]
    cv2.imwrite("cache.png",img)

    # displaying the image 
    cv2.imshow('Submap', img) 

    # setting mouse hadler for the image 
    # and calling the click_event() function 
    cv2.setMouseCallback('Submap', click_event) 

    cv2.waitKey(0) 
    cv2.destroyAllWindows()
    #refPt = [(refPt[0][0]+cord[i][0]-192,refPt[0][1]+cord[i][1]-192)]
    


def tell_me_coordinates_of(inten):
    if inten=='Kitchen':
        show_submap(1)
        send_pts = {'x': 4, 'y': 1}
    elif inten=='Room1':
        show_submap(4)
        send_pts = {'x': 6, 'y': -1}
    elif inten=='Room2':
        show_submap(2)
        send_pts = {'x': -6, 'y': 3}
    elif inten=='Dock':
        send_pts = {'x': -0.25, 'y': 1}
    elif inten=='Hall':
        show_submap(3)
        send_pts = {'x': -3, 'y': 1}
    else:
        show_submap(0)
        send_pts = {'x': 1, 'y': 1}
        
    
    return send_pts
    
def analyse(txt):
    text_to_be_analyzed = txt

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    #print("Query text:", response.query_result.query_text)
    inten =response.query_result.intent.display_name
    print("Detected intent:", inten)
    #print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    #print("Fulfillment text:", response.query_result.fulfillment_text)
    coordinate=tell_me_coordinates_of(inten)
    return coordinate



if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToPose()

        pos={'x': 0, 'y': 0}
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source)
            print("Time over, thanks")
        try:
            # using google speech recognition
            txt=r.recognize_google(audio_text);
            print("Text: "+txt)
            
            
        except:
             print("Sorry, I did not get that")

        #position = {'x': -0.22, 'y': 1}
        pos=analyse(txt)
        position = pos

        quaternion = {
            'r1': 0.000,
            'r2': 0.000,
            'r3': 0.000,
            'r4': 1.000,
            }

        rospy.loginfo('Go to (%s, %s) pose', position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo('Hooray, reached the desired pose')
        else:
            rospy.loginfo('The base failed to reach the desired pose')

        # Sleep to give the last log messages time to be sent

        rospy.sleep(1)
    except rospy.ROSInterruptException:

        rospy.loginfo('Ctrl-C caught. Quitting')


