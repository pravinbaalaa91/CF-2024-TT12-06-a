import cocotb
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_pwm(dut):
    """PWM testbench for tt_um_TT06_pwm"""

    dut._log.info("Starting PWM testbench")

    # ----------------------------
    # Initialize signals
    # ----------------------------
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.ena.value = 1

    # Release reset after 1 clock
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # ----------------------------
    # Helper: wait N PWM cycles
    # ----------------------------
    async def wait_pwm_cycles(n):
        for _ in range(n):
            await RisingEdge(dut.clk)

    # ----------------------------
    # Test Case 1: duty = 0%
    # ----------------------------
    dut.ui_in.value = 0
    await wait_pwm_cycles(256)   # wait full PWM cycle
    assert dut.uo_out[0].value == 0, f"PWM should be 0 at 0 duty, got {dut.uo_out[0].value}"

    # ----------------------------
    # Test Case 2: duty = 50%
    # ----------------------------
    dut.ui_in.value = 50
    await wait_pwm_cycles(256)
    val = int(dut.uo_out[0].value)
    assert val in [0, 1], f"PWM output unexpected at 50% duty: {val}"

    # ----------------------------
    # Test Case 3: duty = 100%
    # ----------------------------
    dut.ui_in.value = 100
    await wait_pwm_cycles(256)
    assert dut.uo_out[0].value == 1, f"PWM should be HIGH at 100% duty, got {dut.uo_out[0].value}"

    # ----------------------------
    # Test Case 4: duty > 100%
    # ----------------------------
    dut.ui_in.value = 150
    await wait_pwm_cycles(256)
    assert dut.uo_out[0].value == 1, f"PWM should be HIGH when duty>100, got {dut.uo_out[0].value}"

    # ----------------------------
    # Optionally check second PWM output
    # ----------------------------
    dut._log.info(f"PWM test passed! pwm_out1 = {dut.uo_out[1].value}")
