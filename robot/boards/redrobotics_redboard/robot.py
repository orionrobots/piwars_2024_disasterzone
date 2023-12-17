import gpiozero


# motor pins
# M1 - dir/phase is "dirb", and pwm is "pwmb"
# M2 - dir/phase is "dira", and pwm is "pwma"

# dira -> 23
# pwma -> 18
# dirb -> 24
# pwmb -> 25

class Robot(gpiozero.Robot):
    def __init__(self):
        m1_dir = 24
        m1_pwm = 25
        m2_dir = 23
        m2_pwm = 18
        super().__init__(left=(m1_pwm, m1_dir), right=(m2_pwm, m2_dir))
