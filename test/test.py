# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start PWM test")

    # Clock 100 kHz
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # === Test 0% duty cycle ===
    dut.ui_in.value = 0  # dc = 0
    await ClockCycles(dut.clk, 300)  # wait a while
    assert dut.uo_out[0].value == 0, "PWM should stay LOW at 0% duty"

    # === Test 100% duty cycle ===
    dut.ui_in.value = 100  # dc = 100
    await ClockCycles(dut.clk, 300)
    assert dut.uo_out[0].value == 1, "PWM should stay HIGH at 100% duty"

    # === Test 50% duty cycle ===
    dut.ui_in.value = 50
    highs = 0
    lows = 0
    for _ in range(512):
        await ClockCycles(dut.clk, 1)
        if dut.uo_out[0].value == 1:
            highs += 1
        else:
            lows += 1
    duty_measured = highs / (highs + lows)
    dut._log.info(f"Measured duty cycle: {duty_measured:.2f}")
    assert 0.45 < duty_measured < 0.55, "PWM should be ~50% duty"
