# import motors
# import IDA_star
# import Two_hase_Algorithm
import random

def Create_scramble(scramble_length):
    move_names = "U U' U2 D D' D2 L L' L2 R R' R2 F F' F2 B B' B2 P"
    random_scramble = []
    for i in range(scramble_length):
        random_scramble += random.choice(move_names)
    print('random_scramble = ', random_scramble)
    return random_scramble

if __name__ == '__main__':
    scramble_length = 20
    scramble = Create_scramble(scramble_length)

    # motor = motors.Motor()
    # motor.Solve(scramble)