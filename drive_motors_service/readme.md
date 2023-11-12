# Drive Motors Service

This folder specifies and holds test for a drive_motors service. What is a drive motors service? It sits on RabbitMQ and will accept commands for controlling drive motors.

Queue topics:

- drive.motors.*

## Drive motor control

- drive.motors.get_capabilities -> Ask drive motor handlers to emit their capabilities
- drive.motors.capabilities -> braodcast capabilities
    - "{motors: 2}" - the number of motors
- drive.motors.speed -> Body "(<-1.0 to 1.0>, .. motor n)" -> Set motor speed. Will stop after 1 second with no further speed messages
- drive.motors.stop -> Stop all motors
- drive.motors.forward : Body (0 < x> <= 1.0) -> Drive forward this speed
- drive.motors.backward : Body (0 < x> <= 1.0) -> Drive backward this speed
- drive.motors.left : 
