module system_top_11(
    input  wire CK4CI_S11,
    input  wire MC_CK_S11,
    input  wire d_in,
    input  wire control_hint,
    output wire q_out,
    output reg  q_dst
);

    wire and_layer;
    wire source_q;

    // Source-enable root
    wire ACCEPT_UART11_INTRDY;
    assign and_layer = ACCEPT_UART11_INTRDY & control_hint;

    layer2_seed u_seed (
        .clk(CK4CI_S11),
        .d(d_in),
        .en(and_layer),
        .q(source_q)
    );

    assign q_out = source_q;

    always @(posedge MC_CK_S11) begin
        q_dst <= q_out;
    end
endmodule
