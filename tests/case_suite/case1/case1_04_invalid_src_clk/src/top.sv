module top(
    input  wire WRONG_CLK,
    input  wire MC_CK_S0,
    input  wire d_in,
    input  wire ctrl_other,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_UART2_INTRDY;
    wire and_out;
    assign and_out = ACCEPT_UART2_INTRDY & ctrl_other;
    always @(posedge WRONG_CLK) begin
        if (and_out)
            q_out <= d_in;
    end
    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule
