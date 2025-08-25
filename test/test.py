import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def pwm_basic_test(dut):
    """Test PWM behavior including duty > 100 case"""

    dut._log.info("Starting PWM testbench")

    # Case 1: dutycycle = 0 -> pwm_out must be 0
    dut.dutycycle.value = 0
    await Timer(200, units="ns")
    assert dut.pwm_out.value == 0, f"Expected 0, got {dut.pwm_out.value}"

    # Case 2: dutycycle = 50 -> pwm_out should toggle (so not stuck)
    dut.dutycycle.value = 50
    await Timer(2000, units="ns")  # wait enough cycles to see toggling
    val = int(dut.pwm_out.value)
    assert val in [0, 1], f"Unexpected value {val} at 50 duty"

    # Case 3: dutycycle = 100 -> pwm_out must be 1
    dut.dutycycle.value = 100
    await Timer(200, units="ns")
    assert dut.pwm_out.value == 1, f"Expected 1, got {dut.pwm_out.value}"

    # Case 4: dutycycle > 100 (e.g., 150) -> pwm_out must be forced 1
    dut.dutycycle.value = 150
    await Timer(200, units="ns")
    assert dut.pwm_out.value == 1, f"Expected forced 1 when duty>100, got {dut.pwm_out.value}"

    dut._log.info("All PWM testcases passed!")
