module top(
    input  wire CK4CI_S0,
    input  wire MC_CK_S0,
    input  wire d_in,
    input  wire p1,
    input  wire p2,
    input  wire p3,
    input  wire p4,
    input  wire p5,
    output reg  q_out,
    output reg  q_dst
);
    wire ACCEPT_DPT5_INTRDY;
    (* keep *) wire n1;
    (* keep *) wire n2;
    (* keep *) wire n3;
    (* keep *) wire n4;
    (* keep *) wire n5;
    wire and_out;

    // 5-hop chain so this should only be caught within default depth=5
    assign n1 = ACCEPT_DPT5_INTRDY & p1;
    assign n2 = n1 & p2;
    assign n3 = n2 & p3;
    assign n4 = n3 & p4;
    assign n5 = n4 & p5;
    assign and_out = n5;

    always @(posedge CK4CI_S0) begin
        if (and_out)
            q_out <= d_in;
    end

    always @(posedge MC_CK_S0) begin
        q_dst <= q_out;
    end
endmodule
