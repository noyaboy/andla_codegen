`include "andla.vh"

module andla_cdma (

clk
,rst_n
// autogen_exceptport_start
,rf_cdma_except_trigger
// autogen_exceptport_stop

// autogen_port_start
, rf_cdma_sfence
, rf_cdma_direction
, rf_cdma_exram_addr
, rf_cdma_exram_c
, rf_cdma_exram_w
, rf_cdma_exram_stride_w
// autogen_port_stop
);

// autogen_bitwidth_start
localparam CDMA_SFENCE_BITWIDTH                       =  `CDMA_SFENCE_BITWIDTH;
localparam CDMA_DIRECTION_BITWIDTH                    =  `CDMA_DIRECTION_BITWIDTH;
localparam CDMA_EXRAM_ADDR_LSB_BITWIDTH               =  `CDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam CDMA_EXRAM_ADDR_MSB_BITWIDTH               =  `CDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam CDMA_EXRAM_ADDR_BITWIDTH                   =  `CDMA_EXRAM_ADDR_BITWIDTH;
localparam CDMA_EXRAM_C_BITWIDTH                      =  `CDMA_EXRAM_C_BITWIDTH;
localparam CDMA_EXRAM_W_BITWIDTH                      =  `CDMA_EXRAM_W_BITWIDTH;
localparam CDMA_EXRAM_STRIDE_W_BITWIDTH               =  `CDMA_EXRAM_STRIDE_W_BITWIDTH;
// autogen_bitwidth_stop

input                                                  clk;
input                                                  rst_n;

// autogen_io_start
input 	 [1-1:0] rf_cdma_sfence;
input 	 [CDMA_DIRECTION_BITWIDTH-1:0] rf_cdma_direction;
input 	 [CDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_cdma_exram_addr;
input 	 [CDMA_EXRAM_C_BITWIDTH-1:0] rf_cdma_exram_c;
input 	 [CDMA_EXRAM_W_BITWIDTH-1:0] rf_cdma_exram_w;
input 	 [CDMA_EXRAM_STRIDE_W_BITWIDTH-1:0] rf_cdma_exram_stride_w;
// autogen_io_stop

// autogen_exceptio_start
output                 rf_cdma_except_trigger;
// autogen_exceptio_stop

endmodule
