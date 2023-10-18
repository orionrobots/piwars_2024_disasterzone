import gpiozero


# motor pins
# M1 - dir/phase is "dirb", and pwm is "pwmb"
# M2 - dir/phase is "dira", and pwm is "pwma"

# dira -> 23
# pwma -> 18
# dirb -> 24
# pwmb -> 19

class Robot(gpiozero.PhaseEnableRobot):
    def __init__(self):
        m1_dir = 24
        m1_pwm = 19
        m2_dir = 23
        m2_pwm = 18
        super().__init__(left=(m1_dir, m1_pwm), right=(m2_dir, m2_pwm))
