import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import random


@cocotb.test()
async def pwm_basic_test(dut):
    """Basic sanity test for PWM module with special >100 duty rule"""
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())  # 100 MHz clock

    # Reset
    dut.rst.value = 1
    await Timer(20, units="ns")
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Apply some fixed duty cycle values
    for duty in [0, 50, 100, 120, 200]:
        dut.duty.value = duty
        await Timer(500, units="ns")

        if duty > 100:
            # Expect always HIGH
            for _ in range(50):
                await RisingEdge(dut.clk)
                assert dut.pwm_out.value == 1, f"Expected PWM=1 for duty>{duty}, but got {dut.pwm_out.value}"
        else:
            cocotb.log.info(f"[BASIC TEST] Duty={duty}, PWM Out={int(dut.pwm_out.value)}")


@cocotb.test()
async def pwm_random_test(dut):
    """Randomized test for PWM module including >100 duty special rule"""
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())  # 100 MHz clock

    # Reset
    dut.rst.value = 1
    await Timer(20, units="ns")
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    for i in range(10):  # 10 random cases per run
        duty = random.randint(0, 255)
        dut.duty.value = duty
        await Timer(1000, units="ns")

        if duty > 100:
            # Must stay HIGH always
            for _ in range(50):
                await RisingEdge(dut.clk)
                assert dut.pwm_out.value == 1, f"Expected always HIGH for duty={duty}, but got {dut.pwm_out.value}"
            cocotb.log.info(f"[RANDOM TEST] Duty={duty}, Output always HIGH as expected")
        else:
            # Normal PWM behavior → check duty ratio
            high_count = 0
            total_cycles = 128
            for _ in range(total_cycles):
                await RisingEdge(dut.clk)
                if dut.pwm_out.value.integer == 1:
                    high_count += 1

            expected_high = duty
            error = abs(high_count - expected_high)
            cocotb.log.info(f"[RANDOM TEST] Duty={duty}, HighCount={high_count}, Expected≈{expected_high}")
            assert error <= 2, f"PWM mismatch: duty={duty}, got high_count={high_count}, expected≈{expected_high}"
