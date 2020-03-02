FROM archlinux/base

# Let's get the basic stuff out of the way
RUN pacman -Syu base-devel --noconfirm

# Python2
RUN pacman -S git python python-pip python-setuptools --noconfirm

# For ardupilot communication using TCP
RUN pip install wheel
RUN pip install pymavlink mavproxy

# Not needed to compile, but required for the map and GUI to work
RUN sudo pacman -S gcc procps-ng xterm wget tk python-wxpython --noconfirm
RUN sudo pacman -S python-numpy --noconfirm
RUN sudo pip install opencv-python 

# Create a user
RUN useradd -m akl

# Give passwordless sudo access
RUN echo "akl ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# From this point, the container runs as the `akl` user is logged in
USER akl


# Pull ardupilot
WORKDIR /home/akl
RUN git clone --single-branch --branch plane4.0 https://github.com/ArduPilot/ardupilot.git 
# From now on, following the official guide: https://github.com/ArduPilot/ardupilot/blob/master/BUILD.md
WORKDIR /home/akl/ardupilot
RUN git submodule update --init --recursive


RUN ./waf configure
RUN ./waf copter
RUN ./waf plane

FROM archlinux/base


# Python, required to compile
RUN pacman -Syu git python python-pip python-setuptools --noconfirm

# Not needed to compile, but required for the map and GUI to work
RUN pacman -S gcc procps-ng xterm wget tk python-wxpython python-numpy which --noconfirm
RUN pip install opencv-python 


# For ardupilot communication using TCP
# wheel needs to be installed before pymavlink
RUN pip install wheel 
RUN pip install pymavlink mavproxy


RUN useradd -m akl
RUN mkdir /home/akl/ardupilot

COPY --from=0 /home/akl/ardupilot /home/akl/ardupilot

USER akl
WORKDIR /home/akl/ardupilot/Tools/autotest

# Custom AKL missions
COPY test_mission.txt .

# Custom AKL locations
RUN echo "Legnica=51.18268,16.17713,113,80" >> locations.txt

# Optional params for arm checks disabling (for faster arming in tests)
RUN echo "ARMING_CHECK 0" >> no_pre_arm_checks.parm
