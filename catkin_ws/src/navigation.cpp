#include &lt;ros/ros.h&gt;
#include &lt;move_base_msgs/MoveBaseAction.h&gt;
#include &lt;actionlib/client/simple_action_client.h&gt;
typedef actionlib::SimpleActionClient&lt;move_base_msgs::MoveBaseAction&gt;
MoveBaseClient;
int main(int argc, char** argv){
	ros::init(argc, argv, &quot;simple_navigation_goals&quot;);
	
	//tell the action client that we want to spin a thread by default
	MoveBaseClient ac(&quot;move_base&quot;, true);
	
	//wait for the action server to come up
	while(!ac.waitForServer(ros::Duration(5.0))){
		ROS_INFO(&quot;Waiting for the move_base action server to come up&quot;);
	}
	
	move_base_msgs::MoveBaseGoal goal;
	
	//we&#39;ll send a goal to the robot to move 1 meter forward
	goal.target_pose.header.frame_id = &quot;base_link&quot;;
	goal.target_pose.header.stamp = ros::Time::now();
	
	goal.target_pose.pose.position.x = 1.0;
	goal.target_pose.pose.orientation.w = 1.0;

	ROS_INFO(&quot;Sending goal&quot;);
	ac.sendGoal(goal);
	ac.waitForResult();
	if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
		ROS_INFO(&quot;Hooray, the base moved 1 meter forward&quot;);
	else
		ROS_INFO(&quot;The base failed to move forward 1 meter for some reason&quot;);
	return 0;
}
