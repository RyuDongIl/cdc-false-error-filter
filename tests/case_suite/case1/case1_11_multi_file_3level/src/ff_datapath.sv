module ff_datapath(
    input  wire clk,
    input  wire d,
    input  wire en,
    output reg  q
);
    always @(posedge clk) begin
        if (en)
            q <= d;
    end
endmodule
