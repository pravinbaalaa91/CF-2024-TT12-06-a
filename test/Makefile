# ================================================================
# Makefile for cocotb testbench
# See: https://docs.cocotb.org/en/stable/quickstart.html
# ================================================================

# ------------------------
# Defaults
# ------------------------
SIM             ?= icarus
TOPLEVEL_LANG   ?= verilog

# Source directory
SRC_DIR         = $(PWD)/../src

# Project source files
PROJECT_SOURCES = pwm.v tt_um_TT06_pwm.v


# ------------------------
# RTL vs Gate-Level build
# ------------------------
ifneq ($(GATES), yes)     # RTL simulation
    SIM_BUILD        = sim_build/rtl
    VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else                      # Gate-level simulation
    SIM_BUILD        = sim_build/gl

    COMPILE_ARGS    += -DGL_TEST
    COMPILE_ARGS    += -DFUNCTIONAL
    COMPILE_ARGS    += -DUSE_POWER_PINS
    COMPILE_ARGS    += -DSIM
    COMPILE_ARGS    += -DUNIT_DELAY=\#1

    VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
    VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

    # This gets copied in by the GDS action workflow
    VERILOG_SOURCES += $(PWD)/gate_level_netlist.v
endif

# ------------------------
# Common Configuration
# ------------------------
# Allow sharing config between design and testbench via include
COMPILE_ARGS    += -I$(SRC_DIR)

# Include testbench source
VERILOG_SOURCES += $(PWD)/tb.v

# ------------------------
# cocotb setup
# ------------------------
# TOPLEVEL is the HDL module to be instantiated (tb is your testbench)
TOPLEVEL        = tb

# MODULE is the Python file (test.py → MODULE = test)
MODULE          = test

# Include cocotb's make rules to take care of simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
