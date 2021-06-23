#######################
Installation Raspberry
#######################

To install ROS and R-TabMAP run the custominstallscript.sh on the Raspberry Pi with a clean Ubuntu 18.04.

See Ros2_RTAB.odt for the neccessary locations of the slightly adapted ros2 launchfiles.


#######################
Installation Edge Cloud
#######################

To install ROS and R-TabMAP run the custominstallscript.sh on an Ubuntu 18.04. The used cpu cores of the make commands can be increased beforehand.

See Ros2_RTAB.odt for the neccessary locations of the slightly adapted ros2 launchfiles. Only the rtabmap.launch.py is needed


#######################
Configuration R-TabMAP
#######################

rtabmap is natively working at 1 frame per second. This needs to be adjusted to 30 fps. 

The rtabmap parameters can be accessed and executed as mentioned in the Ros2_RTAB.odt:

Parameters are saved here:
“.../rtabmap/corelib/include/rtabmap/core/Parameters.h”

After changing a parameter you have to remake the whole library. Therfore repeat the steps from Installation Step 3:
RTAB-Map library:


 $ cd rtabmap/build
 $ cmake ..
 $ make -j4
 $ sudo make install
 $ sudo ldconfig
 
#######################
Running ROS
#######################

When running ROS each bash needs to have this executed: 

 $ cd ~/ros2_ws
 $ . install/setup.bash


The Camera node can be started by executing this on the Raspberry:

 $ ros2 launch realsense2_camera rs_launch.py


The rgbd_sync node can be started by executing this on the Raspberry:

 $ ros2 launch rtabmap_ros rgbd_sync.launch.py


The rtabmap node can be started by executing this on the Raspberry or the Edge Cloud:

 $ ros2 launch rtabmap_ros rtabmap.launch.py


One can end nodes by pressing ctrl+C. 

The rtabmap node will save a rtabmap.db under ~/.ros/rtabmap.db
This database will be used during further runs. If this is not wanted, one has to delete it or move it to another location.

 $ rm ~/.ros/rtabmap.db

To review the databases one can use the rtabmap-databaseViewer:

 $ rtabmap-databaseViewer








 
 
