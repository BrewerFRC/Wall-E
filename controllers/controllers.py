import arduino_controller, maestro_controller, head as h, arms as a, drivetrain as dt

arduino = arduino_controller.Arduino()
maestro = maestro_controller.Controller()

drivetrain = dt.DriveTrain(servo,CH_RIGHT_MOTOR,CH_LEFT_MOTOR)
head = h.Head(servo)
arms = a.Arms()
