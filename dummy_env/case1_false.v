module top(
    input  wire clk_a,
    input  wire clk_b,
    input  wire d_in,
    output reg  q_out,
    output reg  q_dst
);

    // non-matching root signal
    wire OTHER_READY;

    wire and_out;
    wire ctrl_other;

    assign and_out   = OTHER_READY & ctrl_other;

    always @(posedge clk_a) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge clk_b) begin
        q_dst <= q_out;
    end
endmodule
