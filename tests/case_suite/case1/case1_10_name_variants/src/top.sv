module top(
    input  wire ck4ci_lane0,
    input  wire mc_ck_lane0,
    input  wire d_in,
    input  wire ctrl_other,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_UART10_INTRDY;
    wire and_out;

    assign and_out = ACCEPT_UART10_INTRDY & ctrl_other;

    always @(posedge ck4ci_lane0) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge mc_ck_lane0) begin
        q_dst <= q_out;
    end
endmodule
