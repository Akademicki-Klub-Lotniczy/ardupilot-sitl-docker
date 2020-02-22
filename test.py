from sitl import SitlDockerHelper
from subprocess import check_output
from time import sleep


def test_container_lifecycle():
	# Check how many docker containers are running
	num_of_containers = int(check_output('docker ps | wc -l', shell=True))

	print('setting up the runnner')
	runner = SitlDockerHelper('ArduPlane', run_in_background=True)

	print('running the container')
	runner.run()
	sleep(10)

	new_num_of_containers = int(check_output('docker ps | wc -l', shell=True))

	# Check if the number of running containers has increased
	assert num_of_containers + 1 == new_num_of_containers

	print('stopping')
	runner.stop()

	# Check if the num of running containers is back to the start state
	assert int(check_output('docker ps | wc -l', shell=True)) == num_of_containers

