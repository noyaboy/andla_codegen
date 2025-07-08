`include "andla.vh"

module andla_sdma (

clk
,rst_n
// autogen_exceptport_start
,rf_sdma_except_trigger
// autogen_exceptport_stop

// autogen_port_start
, rf_sdma_sfence
, rf_sdma_direction
, rf_sdma_exram_addr
, rf_sdma_shram_addr
, rf_sdma_exram_c
, rf_sdma_exram_w
, rf_sdma_exram_h
, rf_sdma_exram_n
, rf_sdma_exram_stride_w_size
, rf_sdma_exram_stride_h_size
, rf_sdma_exram_stride_n_size
, rf_sdma_shram_c
, rf_sdma_shram_w
, rf_sdma_shram_h
, rf_sdma_shram_n
, rf_sdma_shram_pad_right
, rf_sdma_shram_pad_left
, rf_sdma_shram_pad_up
, rf_sdma_shram_pad_down
, rf_sdma_const_value
, rf_sdma_ch_num
, rf_sdma_sdma_depadding_by_pass
, rf_sdma_preserved0
, rf_sdma_preserved1
, rf_sdma_preserved2
, rf_sdma_sdma_chsum_sel
, rf_sdma_sdma_chsum_data
, rf_sdma_shram_stride_w_size
, rf_sdma_shram_stride_h_size
, rf_sdma_shram_stride_n_size
// autogen_port_stop
);

// autogen_bitwidth_start
localparam SDMA_SFENCE_BITWIDTH                 = `SDMA_SFENCE_BITWIDTH;
localparam SDMA_DIRECTION_BITWIDTH              = `SDMA_DIRECTION_BITWIDTH;
localparam SDMA_EXRAM_ADDR_LSB_BITWIDTH         = `SDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam SDMA_EXRAM_ADDR_MSB_BITWIDTH         = `SDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam SDMA_EXRAM_ADDR_BITWIDTH             = `SDMA_EXRAM_ADDR_BITWIDTH;
localparam SDMA_SHRAM_ADDR_BITWIDTH             = `SDMA_SHRAM_ADDR_BITWIDTH;
localparam SDMA_EXRAM_C_BITWIDTH                = `SDMA_EXRAM_C_BITWIDTH;
localparam SDMA_EXRAM_W_BITWIDTH                = `SDMA_EXRAM_W_BITWIDTH;
localparam SDMA_EXRAM_H_BITWIDTH                = `SDMA_EXRAM_H_BITWIDTH;
localparam SDMA_EXRAM_N_BITWIDTH                = `SDMA_EXRAM_N_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH    = `SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH    = `SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH    = `SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH;
localparam SDMA_SHRAM_C_BITWIDTH                = `SDMA_SHRAM_C_BITWIDTH;
localparam SDMA_SHRAM_W_BITWIDTH                = `SDMA_SHRAM_W_BITWIDTH;
localparam SDMA_SHRAM_H_BITWIDTH                = `SDMA_SHRAM_H_BITWIDTH;
localparam SDMA_SHRAM_N_BITWIDTH                = `SDMA_SHRAM_N_BITWIDTH;
localparam SDMA_SHRAM_PAD_RIGHT_BITWIDTH        = `SDMA_SHRAM_PAD_RIGHT_BITWIDTH;
localparam SDMA_SHRAM_PAD_LEFT_BITWIDTH         = `SDMA_SHRAM_PAD_LEFT_BITWIDTH;
localparam SDMA_SHRAM_PAD_UP_BITWIDTH           = `SDMA_SHRAM_PAD_UP_BITWIDTH;
localparam SDMA_SHRAM_PAD_DOWN_BITWIDTH         = `SDMA_SHRAM_PAD_DOWN_BITWIDTH;
localparam SDMA_CONST_VALUE_BITWIDTH            = `SDMA_CONST_VALUE_BITWIDTH;
localparam SDMA_CH_NUM_BITWIDTH                 = `SDMA_CH_NUM_BITWIDTH;
localparam SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH = `SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH;
localparam SDMA_PRESERVED0_BITWIDTH             = `SDMA_PRESERVED0_BITWIDTH;
localparam SDMA_PRESERVED1_BITWIDTH             = `SDMA_PRESERVED1_BITWIDTH;
localparam SDMA_PRESERVED2_BITWIDTH             = `SDMA_PRESERVED2_BITWIDTH;
localparam SDMA_SDMA_CHSUM_SEL_BITWIDTH         = `SDMA_SDMA_CHSUM_SEL_BITWIDTH;
localparam SDMA_SDMA_CHSUM_DATA_BITWIDTH        = `SDMA_SDMA_CHSUM_DATA_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH    = `SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH    = `SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH    = `SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH;
// autogen_bitwidth_stop

input                                                  clk;
input                                                  rst_n;

// autogen_io_start
input 	 [1-1:0] rf_sdma_sfence;
input 	 [SDMA_DIRECTION_BITWIDTH-1:0] rf_sdma_direction;
input 	 [SDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_sdma_exram_addr;
input 	 [SDMA_SHRAM_ADDR_BITWIDTH-1:0] rf_sdma_shram_addr;
input 	 [SDMA_EXRAM_C_BITWIDTH-1:0] rf_sdma_exram_c;
input 	 [SDMA_EXRAM_W_BITWIDTH-1:0] rf_sdma_exram_w;
input 	 [SDMA_EXRAM_H_BITWIDTH-1:0] rf_sdma_exram_h;
input 	 [SDMA_EXRAM_N_BITWIDTH-1:0] rf_sdma_exram_n;
input 	 [SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_sdma_exram_stride_w_size;
input 	 [SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_sdma_exram_stride_h_size;
input 	 [SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_sdma_exram_stride_n_size;
input 	 [SDMA_SHRAM_C_BITWIDTH-1:0] rf_sdma_shram_c;
input 	 [SDMA_SHRAM_W_BITWIDTH-1:0] rf_sdma_shram_w;
input 	 [SDMA_SHRAM_H_BITWIDTH-1:0] rf_sdma_shram_h;
input 	 [SDMA_SHRAM_N_BITWIDTH-1:0] rf_sdma_shram_n;
input 	 [SDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0] rf_sdma_shram_pad_right;
input 	 [SDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0] rf_sdma_shram_pad_left;
input 	 [SDMA_SHRAM_PAD_UP_BITWIDTH-1:0] rf_sdma_shram_pad_up;
input 	 [SDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0] rf_sdma_shram_pad_down;
input 	 [SDMA_CONST_VALUE_BITWIDTH-1:0] rf_sdma_const_value;
input 	 [SDMA_CH_NUM_BITWIDTH-1:0] rf_sdma_ch_num;
input 	 [SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH-1:0] rf_sdma_sdma_depadding_by_pass;
input 	 [SDMA_PRESERVED0_BITWIDTH-1:0] rf_sdma_preserved0;
input 	 [SDMA_PRESERVED1_BITWIDTH-1:0] rf_sdma_preserved1;
input 	 [SDMA_PRESERVED2_BITWIDTH-1:0] rf_sdma_preserved2;
input 	 [SDMA_SDMA_CHSUM_SEL_BITWIDTH-1:0] rf_sdma_sdma_chsum_sel;
output	 [SDMA_SDMA_CHSUM_DATA_BITWIDTH-1:0] rf_sdma_sdma_chsum_data;
input 	 [SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_sdma_shram_stride_w_size;
input 	 [SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_sdma_shram_stride_h_size;
input 	 [SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_sdma_shram_stride_n_size;
// autogen_io_stop

// autogen_exceptio_start
output                 rf_sdma_except_trigger;
// autogen_exceptio_stop

endmodule
