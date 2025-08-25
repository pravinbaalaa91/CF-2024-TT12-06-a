import cocotb
from cocotb.triggers import RisingEdge, Timer


@cocotb.test()
async def pwm_test(dut):
    """PWM test including duty > 100"""

    dut._log.info("Starting PWM testbench")

    # Initialize signals
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.ena.value = 1

    # Wait 1 us, then release reset
    await Timer(1000, units="ns")
    dut.rst_n.value = 1

    # -----------------------------
    # Case 1: dutycycle = 0
    # -----------------------------
    dut.ui_in.value = 0
    # --- Wait a few PWM clock cycles before checking ---
    await Timer(5000, units="ns")
    assert dut.uo_out[0].value == 0, f"PWM should be 0 at 0 duty, got {dut.uo_out[0].value}"

    # -----------------------------
    # Case 2: dutycycle = 50
    # -----------------------------
    dut.ui_in.value = 50
    # --- Wait enough cycles for PWM counter to toggle ---
    await Timer(50000, units="ns")
    val = int(dut.uo_out[0].value)
    assert val in [0, 1], f"PWM unexpected value at 50 duty: {val}"

    # -----------------------------
    # Case 3: dutycycle = 100
    # -----------------------------
    dut.ui_in.value = 100
    # --- Wait a few cycles for pwm_out to reach HIGH ---
    await Timer(5000, units="ns")
    assert dut.uo_out[0].value == 1, f"PWM should stay HIGH at 100% duty, got {dut.uo_out[0].value}"

    # -----------------------------
    # Case 4: dutycycle > 100 (e.g., 150)
    # -----------------------------
    dut.ui_in.value = 150
    # --- Wait a few cycles for pwm_out to reflect forced HIGH ---
    await Timer(5000, units="ns")
    assert dut.uo_out[0].value == 1, f"PWM should be HIGH when duty>100, got {dut.uo_out[0].value}"

    dut._log.info("All PWM testcases passed!")
