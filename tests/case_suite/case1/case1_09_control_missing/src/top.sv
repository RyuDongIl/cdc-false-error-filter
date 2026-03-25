module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    output reg  q_out,
    output reg  q_dst
);
    // no enable input on source FF
    always @(posedge CK4CI_S0) begin
        q_out <= d_in;
    end

    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule
