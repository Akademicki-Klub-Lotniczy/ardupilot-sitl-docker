#!/usr/bin/python3

import argparse
import os
from subprocess import check_output

DEFAULT_LOCATION = 'Legnica'


# TODO: noninteractive, background mode
# Got it to run noninteractively with
# docker run -itd --net=host wnt3rmute/ardupilot-sitl:latest ./sim_vehicle.py -v ArduPlane -N


class SitlDockerHelper:
    def __init__(self, vehicle, location=DEFAULT_LOCATION, map_on=False, console_on=False, run_in_background=False):
        self.vehicle = vehicle
        self.location = location
        self.map_on = map_on
        self.console_on = console_on
        self.run_in_background = run_in_background

    def run(self):
        # Default arguments, always used
        docker_args = [
            'docker',
            'run',
            '-it',
            '--net=host',
            '--env=DISPLAY',
            '--volume',
            f'{os.environ["HOME"]}/.Xauthority:/home/akl/.Xauthority:rw',
        ]

        if self.run_in_background:
            docker_args.append('-d')  # -d: detach

        # Default arguments for the container, always used
        docker_args.extend([
            'wnt3rmute/ardupilot-sitl',
            './sim_vehicle.py',
            '-N',
        ])

        docker_args.extend([
            '-v',
            self.vehicle,
            '-L',
            self.location
        ])

        if not self.run_in_background:
            print("=== Replacing the current process with Ardupilot Terminal ===")
            os.execvp('docker', docker_args)

        else:
            self.container_id = check_output(docker_args).decode().replace('\n', '')

    def stop(self):
        os.system(f'docker stop {self.container_id}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SITL Runner')

    parser.add_argument(
        '-m', '--map', help='Show the map window', action='store_true')
    parser.add_argument('-c', '--console',
                        help='Show the console window', action='store_true')
    parser.add_argument(
        '-v', '--vehicle', help='Choose vehicle (ArduPlane or ArduCopter)', required=True)
    parser.add_argument('-l', '--location',
                        help=f"Select location ({DEFAULT_LOCATION} by default)", default=DEFAULT_LOCATION)
    cli_args = parser.parse_args()

    runner = SitlDockerHelper(cli_args.vehicle, cli_args.location, cli_args.map, cli_args.console)
    runner.run()


'''
if cli_args.map:
    docker_args.append('--map')

if cli_args.console:
    docker_args.append('--console')

if cli_args.vehicle:
    vehicle = cli_args.vehicle.strip()
    # print(vehicle)
    docker_args.append('-v')
    docker_args.append(vehicle)

docker_args.append('-L')
docker_args.append(cli_args.location)
'''
