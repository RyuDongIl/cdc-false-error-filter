module top(
    input  wire clk_a,
    input  wire clk_b,
    input  wire d_in,
    output reg  q_out,
    output reg  q_dst
);

    // root signal that should classify as false path when traced backward
    wire ACCEPT_UART0_INTRDY;

    // logic chain into source FF enable
    wire and_out;
    wire ctrl_other;

    assign and_out   = ACCEPT_UART0_INTRDY & ctrl_other;

    always @(posedge clk_a) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge clk_b) begin
        q_dst <= q_out;
    end
endmodule
