import RPi.GPIO as GPIO
from time import sleep

class A4988:
    def __init__(self, Pin_dir, Pin_step, Pin_enable):
        self.mPin_dir = Pin_dir
        self.mPin_step = Pin_step
        self.mPin_enable = Pin_enable

        self.SetWaitTime(0.001)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.mPin_dir, GPIO.OUT)
        GPIO.setup(self.mPin_step, GPIO.OUT)
        GPIO.setup(self.mPin_enable, GPIO.OUT)

        GPIO.output(self.mPin_enable, GPIO.LOW)

    def SetWaitTime(self, wait):
        self.mStep_wait = wait

    def Step_CW(self, step_count):
        GPIO.output(self.mPin_dir, 0)
        for i in range(step_count):
            GPIO.output(self.mPin_step, GPIO.HIGH)
            sleep(self.mStep_wait)
            GPIO.output(self.mPin_step, GPIO.LOW)
            sleep(self.mStep_wait)

    def Step_CCW(self, step_count):
        GPIO.output(self.mPin_dir, 1)
        for i in range(step_count):
            GPIO.output(self.mPin_step, GPIO.HIGH)
            sleep(self.mStep_wait)
            GPIO.output(self.mPin_step, GPIO.LOW)
            sleep(self.mStep_wait)

    # def Cleanup(self):
    #     GPIO.cleanup()