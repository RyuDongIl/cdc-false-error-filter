module layer2_seed(
    input  wire clk,
    input  wire d,
    input  wire en,
    output wire q
);
    wire enable_b;
    assign enable_b = en & 1'b1;

    ff_wrapper u_ffw (
        .clk(clk),
        .d(d),
        .en(enable_b),
        .q(q)
    );
endmodule
