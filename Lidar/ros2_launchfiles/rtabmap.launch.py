# Requirements:
#   A realsense D400 series
#   Install realsense2 ros2 package (refactor branch)
# Example:
#   $ ros2 run realsense_node realsense_node
#   $ ros2 launch rtabmap_ros realsense_d400.launch.py

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    parameters=[{
          'frame_id':'camera_link',
          'subscribe_depth':False,
          'approx_sync':True}]

    remappings=[
          ('rgb/image', '/camera/color/image_raw'),
          ('depth/image', '/camera/depth/image_rect_raw'),
	  ('rgb/camera_info', '/camera/color/camera_info'),
	  
	]
    
    remappings_odo=[
          ('rgb/image', '/camera/color/image_raw'),
          ('rgb/camera_info', '/camera/color/camera_info'),
          ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
	  
	  
	]

    
    rgbd_sync_parameters=[{
        'frame_id':'camera_link',
        'approx_sync':True,
        'queue_size':20,
	'compressed_rate':100,
	


    }]

	
    rtabmap_parameters=[{
        'frame_id':'camera_link',
        'subscribe_rgbd':True,
	'subscribe_rgb':False,
        'subscribe_scan':False,
        'subscribe_depth':False,
        'subscribe_scan_cloud':False,
        'approx_sync':True,
        'queue_size':20,
	'DetectionRate':10.0
	


    }]

    odom_parameters=[{

        'Vis/EstimationType':'0',
        'subscribe_rgbd':True,
	'subscribe_rgb':False,
        'approx_sync':True,
        'frame_id':'camera_link',
        'queue_size':20,
	
        'Vis/MaxDepth':'3.5',
        'Vis/EstimationType':'0',
        'Vis/CorGuessWinSize':'0',
        'Vis/MinInliers':'10',
        'Vis/InlierDistance':'0.02',
        'Vis/CorGuessWinSize':'0',
        'Vis/CorNNType':'3',
        'OdomF2M/BundleAdjustment':'0',
        'OdomF2M/MaxSize':'1000',
    }]


    return LaunchDescription([
        # Set env var to print messages to stdout immediately
        SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),

        # Nodes to launch
        Node(
            package='rtabmap_ros', node_executable='rgbd_odometry', output='screen',
            parameters=odom_parameters,
            ),

	
        Node(
            package='rtabmap_ros', node_executable='rtabmap', output='screen',
            parameters=rtabmap_parameters,
            arguments=['-d'],
	    ),
    ])
