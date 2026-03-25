module ff_wrapper(
    input  wire clk,
    input  wire d,
    input  wire en,
    output wire q
);
    wire ff_q;

    ff_datapath u_ff(
        .clk(clk),
        .d(d),
        .en(en),
        .q(ff_q)
    );

    assign q = ff_q;
endmodule
