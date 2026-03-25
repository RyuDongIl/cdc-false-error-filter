module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    input  wire ctrl_other,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_UART1_INTRDY;

    wire and_root;
    assign and_root = ACCEPT_UART1_INTRDY & ctrl_other;

    src_cell u_src (
        .clk(CK4CI_S0),
        .d(d_in),
        .en(and_root),
        .q(q_out)
    );

    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule

module src_cell(
    input  wire clk,
    input  wire d,
    input  wire en,
    output reg  q
);
    always @(posedge clk) begin
        if (en)
            q <= d;
    end
endmodule
