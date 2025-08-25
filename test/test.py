import cocotb
from cocotb.triggers import RisingEdge, Timer
import random


@cocotb.test()
async def test_project(dut):
    """PWM Testbench"""

    cocotb.log.info("Start PWM test")

    # Reset sequence
    dut.rst_n.value = 0
    dut.clk.value = 0
    await Timer(10, units="ns")
    dut.rst_n.value = 1
    await Timer(10, units="ns")

    # Clock generator
    async def clock_gen():
        while True:
            dut.clk.value = 0
            await Timer(5, units="ns")
            dut.clk.value = 1
            await Timer(5, units="ns")

    cocotb.start_soon(clock_gen())

    # ---- Test 0% duty ----
    dut.ui_in.value = 0b0000000  # dc = 0
    await Timer(2000, units="ns")
    assert dut.uo_out[0].value == 0, "PWM should stay LOW at 0% duty"

    # ---- Test 100% duty ----
    dut.ui_in.value = 0b1100100  # 100 in decimal, dc = 100
    await Timer(2000, units="ns")
    assert dut.uo_out[0].value == 1, "PWM should stay HIGH at 100% duty"

    # ---- Test 50% duty ----
    dut.ui_in.value = 50  # 50% duty
    high_count = 0
    total_cycles = 200

    for _ in range(total_cycles):
        await RisingEdge(dut.clk)
        if dut.uo_out[0].value == 1:
            high_count += 1

    duty_measured = (high_count / total_cycles) * 100
    assert 40 <= duty_measured <= 60, f"Expected ~50% duty, got {duty_measured:.2f}%"

    # ---- Randomized test for robustness ----
    for _ in range(5):
        dc = random.randint(1, 99)
        dut.ui_in.value = dc
        high_count = 0
        total_cycles = 300
        for _ in range(total_cycles):
            await RisingEdge(dut.clk)
            if dut.uo_out[0].value == 1:
                high_count += 1
        duty_measured = (high_count / total_cycles) * 100
        expected = dc
        assert abs(duty_measured - expected) < 15, f"Duty mismatch: expected ~{expected}%, got {duty_measured:.2f}%"

    cocotb.log.info("PWM test completed successfully")
