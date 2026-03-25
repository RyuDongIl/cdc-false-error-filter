module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    output reg  q_out,
    output reg  q_dst
);

    // root signal that should classify as false path when traced backward
    wire ACCEPT_UART0_INTRDY;

    // logic chain into source FF enable
    wire and_out;
    wire ctrl_other;

    assign and_out   = ACCEPT_UART0_INTRDY & ctrl_other;

    always @(posedge CK4CI_S0) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule
