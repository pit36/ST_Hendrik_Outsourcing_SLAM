sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential automake libtool
sudo apt install -y curl gnupg2 lsb-release
sudo apt install -y libfreetype6-dev libfreeimage-dev libzzip-dev libxrandr-dev libxaw7-dev freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev
sudo apt install -y libpcl-dev
sudo apt install -y cmake
hash -r


####
ROS_DISTRO=eloquent
sudo apt update && sudo apt install -y curl gnupg2 lsb-release
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
sudo apt update
sudo apt install -y ros-$ROS_DISTRO-ros-base

#Environment setup
echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-colcon-common-extensions


locale  # check for UTF-8
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale  # verify settings

sudo apt update && sudo apt install -y \
  build-essential \
  git \
  python3-pip \
  python-rosdep \
  python3-vcstool \
  wget


# install some pip packages needed for testing
python3 -m pip install -U \
  argcomplete \
  flake8 \
  flake8-blind-except \
  flake8-builtins \
  flake8-class-newline \
  flake8-comprehensions \
  flake8-deprecated \
  flake8-docstrings \
  flake8-import-order \
  flake8-quotes \
  pytest-repeat \
  pytest-rerunfailures \
  pytest \
  pytest-cov \
  pytest-runner \
  setuptools

# install Fast-RTPS dependencies
sudo apt install -y \
  libasio-dev \
  libtinyxml2-dev
# install Cyclone DDS dependencies
sudo apt install -y \
  libcunit1-dev

sudo apt autoremove -y


### Librealsense install

sudo apt update
sudo apt dist-upgrade 
sudo apt install -y automake libtool vim cmake libusb-1.0-0-dev libx11-dev xorg-dev libglu1-mesa-dev
sudo apt install -y libtbb-dev libxinerama-dev 
sudo apt install -y libxcursor-dev 

sudo ldconfig



cd ~
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/ 


sudo su
udevadm control --reload-rules && udevadm trigger
exit

echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> ~/.bashrc

source ~/.bashrc



cd ~
git clone --depth=1 -b v3.10.0 https://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j1
sudo make install
cd python
export LD_LIBRARY_PATH=../src/.libs
python3 setup.py build --cpp_implementation 
python3 setup.py test --cpp_implementation
sudo python3 setup.py install --cpp_implementation
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3
sudo ldconfig
protoc --version


cd ~/librealsense
mkdir  build  
cd build
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release -DFORCE_LIBUVC=true
make -j1
sudo make install


cd ~/librealsense/build
cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)
make -j1
sudo make install

echo "export PYTHONPATH=$PYTHONPATH:/usr/local/lib" >> ~/.bashrc

source ~/.bashrc

sudo apt install -y python-opengl
sudo -H pip3 install pyopengl
sudo -H pip3 install pyopengl_accelerate==3.1.3rc1


### ROS <-> librealsense     

mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src/
git clone https://github.com/IntelRealSense/realsense-ros.git -b eloquent
cd ~/ros2_ws
sudo apt install -y python-rosdep
sudo rosdep init
rosdep update --include-eol-distros
rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
colcon build
. install/local_setup.bash


#### ROS2 Repositories

wget https://raw.githubusercontent.com/ros2/ros2/eloquent/ros2.repos
vcs import src < ros2.repos
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update --include-eol-distros
rosdep install --from-paths src --ignore-src --rosdistro eloquent -y --skip-keys "console_bridge fastcdr fastrtps libopensplice67 libopensplice69 rti-connext-dds-5.3.1 urdfdom_headers"
colcon build --symlink-install

## Source script. wichtig in jedem neuen Terminal.
. ~/ros2_ws/install/setup.bash

## rtabmap installieren
cd ~
git clone https://github.com/introlab/rtabmap.git rtabmap
cd rtabmap/build
cmake ..
make -j1
sudo make install
sudo ldconfig


### holen von mehr repos
cd ~/ros2_ws
git clone --branch ros2 https://github.com/introlab/rtabmap_ros.git src/rtabmap_ros
cd ~/ros2_ws/src 
git clone --branch eloquent-devel https://github.com/ros-perception/perception_pcl.git
git clone --branch ros2 https://github.com/ros-perception/pcl_msgs.git
git clone --branch eloquent https://github.com/ros-perception/vision_opencv.git

# Sequence of packages to be installed is important --> first rviz_default_plugin --> second rtabmaps_ros --> third all packages
cd ~/ros2_ws
MAKEFLAGS="-j2 -l2" colcon build --packages-up-to rviz_common --symlink-install
. ~/ros2_ws/install/setup.bash
MAKEFLAGS="-j2 -l2" colcon build --packages-up-to rviz_default_plugins --symlink-install
. ~/ros2_ws/install/setup.bash
MAKEFLAGS="-j2 -l2" colcon build --packages-up-to rtabmap_ros --symlink-install
. ~/ros2_ws/install/setup.bash
MAKEFLAGS="-j2 -l2" colcon build --symlink-install
. ~/ros2_ws/install/setup.bash









