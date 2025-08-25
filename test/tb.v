`default_nettype none
`timescale 1ns / 1ps

module tb ();

  // Testbench signals
  reg clk;
  reg rst_n;
  reg ena;
  reg  [7:0] ui_in;
  reg  [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // DUT instantiation
  tt_um_TT06_pwm dut (
      .clk    (clk),
      .rst_n  (rst_n),
      .ena    (ena),
      .ui_in  (ui_in),
      .uo_out (uo_out),
      .uio_in (uio_in),
      .uio_out(uio_out),
      .uio_oe (uio_oe)
`ifdef GL_TEST
      ,.VPWR(VPWR),
      .VGND(VGND)
`endif
  );

  // Clock generation (approx 256 kHz like TT default sim)
  always #1953 clk = ~clk;

  // Stimulus
  initial begin
    // Initialize signals
    clk    = 0;
    rst_n  = 0;
    ena    = 1;    // TT requires ena high
    ui_in  = 0;
    uio_in = 0;

    // Release reset
    #1000 rst_n = 1;

    // Apply different duty cycles
    #10000000 ui_in = 8'd25;   // ~20% duty
    #10000000 ui_in = 8'd50;   // ~40% duty
    #10000000 ui_in = 8'd75;   // ~60% duty
    #10000000 ui_in = 8'd100;  // ~80% duty

    #10000000 $finish;
  end

  // VCD dump for waveform analysis
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
  end

  // Monitor for quick check
  initial begin
    $monitor("Time=%t | ui_in=%d | PWM_OUT0=%b | PWM_OUT1=%b",
              $time, ui_in, uo_out[0], uo_out[1]);
  end

endmodule
