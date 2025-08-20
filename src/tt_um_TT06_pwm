
`default_nettype none
module tt_um_TT06_pwm (
    input  wire clk,
    input  wire rst_n,
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire ena
);

    // Active-low reset → convert to active-high
    wire reset = ~rst_n;

    // Duty cycle from ui_in[6:0]
    wire [6:0] dc = ui_in[6:0];
    reg pwm_out;
    reg pwm_out1;

    // Internal PWM module
    pwm pwm_inst (
        .clk(clk),
        .reset(reset),
        .dc(dc),
        .pwm_out(pwm_out),
        .pwm_out1(pwm_out1)
    );

    // Map outputs
    assign uo_out[0] = pwm_out;
    assign uo_out[1] = pwm_out1;
    assign uo_out[7:2] = 0;

    // Not using bidirectional IOs
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;
    wire _unused = &{ui_in[7], uio_in[7:0], ena};

endmodule


module pwm (
    input clk,
    input reset,
    input wire [6:0] dc,
    output reg pwm_out,
    output reg pwm_out1
);
    reg [7:0] count;
    wire [7:0] threshold;

    assign threshold = (dc * 255) / 100;

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            count <= 8'd0;
            pwm_out <= 0;
            pwm_out1 <= 0;
        end else begin
            count <= count + 1;

            if (threshold == 0) begin
                pwm_out <= 0;
            end else if (dc >= 7'd100) begin
                pwm_out <= 1;
            end else if (count <= threshold) begin
                pwm_out <= 1;
            end else begin
                pwm_out <= 0;
            end

            pwm_out1 <= pwm_out;
        end
    end
endmodule
