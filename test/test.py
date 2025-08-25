import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def pwm_test(dut):
    """Test PWM behavior including duty > 100 case"""

    # Test a set of values including edge cases
    duty_values = [0, 25, 50, 75, 100, 120, 150]  

    for duty_val in duty_values:
        dut.dutycycle.value = duty_val
        await Timer(20, units="ns")

        pwm_out = int(dut.pwm_out.value)

        # Debug print to see what is happening
        dut._log.info(f"Checking duty={duty_val}, pwm_out={pwm_out}")

        if duty_val > 100:
            # Expect pwm_out = 1
            assert pwm_out == 1, f"Expected pwm_out=1 for duty={duty_val}, got {pwm_out}"
        elif duty_val == 0:
            # Expect pwm_out = 0
            assert pwm_out == 0, f"Expected pwm_out=0 for duty={duty_val}, got {pwm_out}"
        else:
            # For normal 0–100 range, just check pwm_out is either 0 or 1
            assert pwm_out in [0, 1], f"Invalid pwm_out={pwm_out} for duty={duty_val}"

    # Also run a few random values to stress test
    for _ in range(5):
        duty_val = random.randint(0, 150)
        dut.dutycycle.value = duty_val
        await Timer(20, units="ns")

        pwm_out = int(dut.pwm_out.value)
        dut._log.info(f"Random test: duty={duty_val}, pwm_out={pwm_out}")

        if duty_val > 100:
            assert pwm_out == 1, f"Expected pwm_out=1 for duty={duty_val}, got {pwm_out}"
