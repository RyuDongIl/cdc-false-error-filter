module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    input  wire sel,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_MUX_INTRDY;
    wire alt_signal;
    wire mux_en;
    wire and_out;

    assign alt_signal = 1'b0;
    assign mux_en = sel ? ACCEPT_MUX_INTRDY : alt_signal;
    assign and_out = mux_en & 1'b1;

    always @(posedge CK4CI_S0) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule
