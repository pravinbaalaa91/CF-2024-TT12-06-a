# ===============================
# Makefile for RTL & GLS (Verilog testbench)
# ===============================

# Simulator
SIM ?= icarus

# Source directory
SRC_DIR = $(PWD)/../src

# RTL sources
PROJECT_SOURCES = $(SRC_DIR)/tt_um_TT06_pwm.v $(SRC_DIR)/pwm.v

# Testbench
TB = $(PWD)/tb.v

# Gate-level netlist
GL_NETLIST = $(PWD)/gate_level_netlist.v

# Output file
OUT = sim.out

# Sky130 PDK paths
PDK = $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog
GL_LIBS = $(PDK)/primitives.v $(PDK)/sky130_fd_sc_hd.v

# GLS compile defines
GL_DEFINES = -DGL_TEST -DFUNCTIONAL -DUSE_POWER_PINS -DSIM -DUNIT_DELAY=\#1

# ===============================
# Targets
# ===============================

# Default: RTL simulation
all: rtl

# RTL simulation
rtl:
	@echo "Running RTL simulation..."
	iverilog -o $(OUT) $(PROJECT_SOURCES) $(TB)
	vvp $(OUT)

# Gate-level simulation
gl:
	@echo "Running Gate-Level simulation..."
	iverilog -o $(OUT) $(GL_DEFINES) $(GL_LIBS) $(GL_NETLIST) $(TB)
	vvp $(OUT)

# Clean
clean:
	rm -f $(OUT) tb.vcd

.PHONY: all rtl gl clean
