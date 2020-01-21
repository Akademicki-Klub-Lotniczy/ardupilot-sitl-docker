# What's this?
[Ardupilot](http://ardupilot.org/) - open-source autopilot for unmanned vehicles (drones, planes, boats, you tell me)

[SITL](http://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html) - software in the loop - a simulator for ardupilot


**This docker image is configured for *ArduCopter* and *ArduPlane*.**


GUI works through sharing the `.Xauthority` file

# Usage

Just use docker-compose from [here](https://github.com/Wint3rmute/ardupilot-sitl-docker/blob/master/docker-compose.yml)


Or if you HAVE to use just docker, here's your long boi:

`docker run -it --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/home/akl/.Xauthority:rw" wnt3rmute/ardupilot-sitl ./sim_vehicle.py -L Ballarat --console --map -v ArduCopter -N`