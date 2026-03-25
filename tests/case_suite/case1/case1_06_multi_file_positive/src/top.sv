module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    input  wire ctrl_other,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_UART4_INTRDY;
    wire and_root;
    assign and_root = ACCEPT_UART4_INTRDY & ctrl_other;

    src_block u_src(
        .clk(CK4CI_S0),
        .d(d_in),
        .en(and_root),
        .q(q_out)
    );

    dst_block u_dst(
        .clk(MC_CK_S0),
        .d(q_out),
        .q(q_dst)
    );
endmodule
