module top(
    input  wire CK4CI_S0,
    input  wire WRONG_DST,
    input  wire d_in,
    input  wire ctrl_other,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_UART3_INTRDY;
    wire and_out;
    assign and_out = ACCEPT_UART3_INTRDY & ctrl_other;
    always @(posedge CK4CI_S0) begin
        if (and_out)
            q_out <= d_in;
    end
    always @(posedge WRONG_DST) begin
        q_dst <= q_out;
    end
endmodule
