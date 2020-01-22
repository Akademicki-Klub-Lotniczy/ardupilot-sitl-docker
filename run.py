import argparse
import os

parser = argparse.ArgumentParser(description='SITL Runner')

parser.add_argument('--map', help='Show the map window', action='store_true')
parser.add_argument('--console', help='Show the console window', action='store_true')
parser.add_argument('-v', help='Choose vehicle' )

cli_args = parser.parse_args()

# `os.execvp` ignores the first arg, so there's a dummy
docker_args = ['docker',
        'run',
        '-it',
        '--net=host',
        '--env=DISPLAY',
        '--volume',
        '/home/wint3rmute/.Xauthority:/home/akl/.Xauthority:rw',
        'wnt3rmute/ardupilot-sitl',
        './sim_vehicle.py',
        #'--console',
        #'--map',
        #'-v',
        #'ArduCopter',
        '-N',
]

if cli_args.map:
    docker_args.append('--map')

if cli_args.console:
    docker_args.append('--console')

if not cli_args.v:
    print('no vehicle set!')
    exit()
else:
    vehicle = cli_args.v.strip()
    print(vehicle)
    docker_args.append('-v')
    docker_args.append(f'{vehicle}')



for arg in docker_args:
    print(arg, end=' ')

print()

os.execvp('docker', docker_args)
