module pwm (
    input  wire       clk,
    input  wire       reset,
    input  wire [6:0] dc,        // duty cycle: 0–100
    output reg        pwm_out,
    output reg        pwm_out1
);

    reg [7:0] count;
    reg [7:0] threshold;

    // Clamp duty cycle and compute threshold
    always @(*) begin
        if (dc >= 7'd100)
            threshold = 8'd255;                 // 100% duty cycle
        else
            threshold = (dc * 8'd255) / 7'd100; // Scale dc to 0–255
    end

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            count   <= 8'd0;
            pwm_out <= 1'b0;
            pwm_out1 <= 1'b0;
        end else begin
            count <= count + 1;

            if (dc == 0) begin
                pwm_out <= 1'b0;   // 0% duty
            end else if (dc >= 100) begin
                pwm_out <= 1'b1;   // 100% duty
            end else if (count < threshold) begin
                pwm_out <= 1'b1;   // Normal PWM
            end else begin
                pwm_out <= 1'b0;
            end

            pwm_out1 <= pwm_out;   // duplicate output
        end
    end

endmodule
