#!/usr/bin/python3

import argparse
import os

DEFAULT_LOCATION = 'Legnica'

parser = argparse.ArgumentParser(description='SITL Runner')

parser.add_argument('-m', '--map', help='Show the map window', action='store_true')
parser.add_argument('-c', '--console', help='Show the console window', action='store_true')
parser.add_argument('-v', '--vehicle', help='Choose vehicle (ArduPlane or ArduCopter)', required=True )
parser.add_argument('-l', '--location', help=f"Select location ({DEFAULT_LOCATION} by default)", default=DEFAULT_LOCATION)
cli_args = parser.parse_args()

# TODO: noninteractive, background mode
# Got it to run noninteractively with
# docker run -itd --net=host wnt3rmute/ardupilot-sitl:latest ./sim_vehicle.py -v ArduPlane -N

docker_args = ['docker',
        'run',
        '-it',
        '--net=host',
        '--env=DISPLAY',
        '--volume',
        f'{os.environ["HOME"]}/.Xauthority:/home/akl/.Xauthority:rw',
        'wnt3rmute/ardupilot-sitl',
        './sim_vehicle.py',
        '-N',
]

if cli_args.map:
    docker_args.append('--map')

if cli_args.console:
    docker_args.append('--console')

if cli_args.vehicle:
    vehicle = cli_args.vehicle.strip()
    #print(vehicle)
    docker_args.append('-v')
    docker_args.append(vehicle)

docker_args.append('-L')
docker_args.append(cli_args.location)


for arg in docker_args:
    print(arg, end=' ')

print()

os.execvp('docker', docker_args)
