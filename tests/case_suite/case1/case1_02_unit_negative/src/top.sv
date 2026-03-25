module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    input  wire ctrl_other,
    output reg  q_out,
    output reg  q_dst
);

    wire OTHER_READY;
    wire and_out;

    assign and_out   = OTHER_READY & ctrl_other;

    always @(posedge CK4CI_S0) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule
