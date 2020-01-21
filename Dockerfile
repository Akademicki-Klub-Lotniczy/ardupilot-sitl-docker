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

RUN mkdir /home/akl/compiler
WORKDIR /home/akl/compiler

# Pull installation instruction for the compiler supported by ardupilot
RUN wget https://gist.githubusercontent.com/Wint3rmute/03dd31bd3fb8cea2ac6c3535331e1876/raw/b40142af3fb61c6e7d8f4564eb245d36e9332748/PKGBUILD 

# Install the compiler package (must not be run as root)
RUN makepkg -sri --noconfirm


# Pull ardupilot
WORKDIR /home/akl
RUN git clone https://github.com/ArduPilot/ardupilot.git
# From now on, following the official guide: https://github.com/ArduPilot/ardupilot/blob/master/BUILD.md
WORKDIR /home/akl/ardupilot
RUN git submodule update --init --recursive

# OKAY SO SINCE ARCH USES PYTHON3 AS DEFAULT, WAF WONT RUN CORRECTLY
# SINCE ITS MEANT FOR PYTHON2i
# Thats why I echo the shebang for python2 into the top of the waf <3
# RUN cp waf wafbackup
# RUN echo "#!/usr/bin/env python2" > waf
# RUN cat wafbackup >> waf

RUN ./waf configure
RUN ./waf copter
RUN ./waf plane

WORKDIR /home/akl/ardupilot/Tools/autotest

# Same thing as Waf
# RUN cp sim_vehicle.py sim_vehicle_backup.py
# RUN echo "#!/usr/bin/env python2" > sim_vehicle.py 
# RUN cat sim_vehicle_backup.py >> sim_vehicle.py

# Image size before cleaning up:
# wnt3rmute/ardupilot-sitl   latest              7e392bf31577        45 hours ago        3.95GB


####################
#   Cleaning up    #
####################

# Switch to root for doing administration stuff
USER root

# Clear the pacman cache
# RUN pacman -Sc --noconfirm

# Clear the compiler dir
RUN rm -rf /home/akl/compiler

# Uninstall the compiler package
RUN pacman -Rscn gcc-arm-none-eabi-bin-6-2017-q2 --noconfirm

# Image size after cleaning up:
# wnt3rmute/ardupilot-sitl   latest              52df6f37fd04        2 minutes ago       3.89GB
# A smaller difference than i was expecting... TODO: clear more stuff

# Switch back to akl
USER akl