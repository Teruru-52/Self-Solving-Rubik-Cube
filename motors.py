import a4988
import RPi.GPIO as GPIO

class Motor:
    def __init__(self):
        self.motor_U = a4988.A4988(Pin_dir=0, Pin_step=5)
        self.motor_D = a4988.A4988(Pin_dir=6, Pin_step=13)
        self.motor_L = a4988.A4988(Pin_dir=26, Pin_step=19)
        self.motor_R = a4988.A4988(Pin_dir=17, Pin_step=27)
        self.motor_F = a4988.A4988(Pin_dir=22, Pin_step=10)
        self.motor_B = a4988.A4988(Pin_dir=9, Pin_step=11)

    def Solve(self, scramble):
        for move_name in scramble.split(" "):
            if move_name == "U":
                self.motor_U.Step_CW(50)
            elif move_name == "U'":
                self.motor_U.Step_CCW(50)
            elif move_name == "U2":
                self.motor_U.Step_CW(100)

            elif move_name == "D":
                self.motor_D.Step_CW(50)
            elif move_name == "D'":
                self.motor_D.Step_CCW(50)
            elif move_name == "D2":
                self.motor_D.Step_CW(100)

            elif move_name == "L":
                self.motor_L.Step_CW(50)
            elif move_name == "L'":
                self.motor_L.Step_CCW(50)
            elif move_name == "L2":
                self.motor_L.Step_CW(100)

            elif move_name == "R":
                self.motor_R.Step_CW(50)
            elif move_name == "R'":
                self.motor_R.Step_CCW(50)
            elif move_name == "R2":
                self.motor_R.Step_CW(100)

            elif move_name == "F":
                self.motor_F.Step_CW(50)
            elif move_name == "F'":
                self.motor_F.Step_CCW(50)
            elif move_name == "F2":
                self.motor_F.Step_CW(100)

            elif move_name == "B":
                self.motor_B.Step_CW(50)
            elif move_name == "B'":
                self.motor_B.Step_CCW(50)
            elif move_name == "B2":
                self.motor_B.Step_CW(100)

            else:
                print("no move_name")

    def Cleanup(self):
        GPIO.cleanup()