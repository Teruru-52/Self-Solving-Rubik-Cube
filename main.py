# import motors
import IDA_star
# import Two_hase_Algorithm
import random

def Set_random_scramble(random_count):
    move_names = "U U' U2 D D' D2 L L' L2 R R' R2 F F' F2 B B' B2"
    random_scramble = []
    for i in range(random_count):
        random_scramble += random.choice(move_names)
    print('random_scramble = ', random_scramble)
    return random_scramble

if __name__ == '__main__':
    random_count = 20
    random_scramble = Set_random_scramble(random_count)

    # motor = motors.Motor()