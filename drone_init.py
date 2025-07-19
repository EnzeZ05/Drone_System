from djitellopy import tello
tello.CONTROL_UDP_PORT = 8890

drone = tello.Tello()

def _launch():
    drone.connect()
    print(drone.get_battery())

def _takeoff():
    drone.takeoff()
    drone.streamon()

def _land():
    drone.land()