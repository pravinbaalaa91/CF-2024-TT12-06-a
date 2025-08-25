`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a VCD file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [6:0] dc;
  wire pwm_out;
  wire pwm_out1;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate your design
  pwm user_project (

      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .clk    (clk),
      .reset  (rst_n),   // mapped reset
      .dc     (dc),
      .pwm_out(pwm_out),
      .pwm_out1(pwm_out1)
  );

  // Clock generation
  always #1953 clk = ~clk;

  // Stimulus
  initial begin
    clk   = 0;
    rst_n = 0;
    ena   = 1;  // TT expects ena high when active
    dc    = 0;

    #1000 rst_n = 1;

    #10000000 dc = 7'd25;
    #10000000 dc = 7'd50;
    #10000000 dc = 7'd75;
    #10000000 dc = 7'd100;

    #10000000 $finish;
  end

  // Monitor
  initial begin
    $monitor("Time = %t | DC = %d%% | PWM_OUT = %b", $time, dc, pwm_out);
  end

endmodule
