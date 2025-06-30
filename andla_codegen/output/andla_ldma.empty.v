`include "andla.vh"

module andla_ldma (

clk
,rst_n
// autogen_exceptport_start
,rf_ldma_except_trigger
// autogen_exceptport_stop

// autogen_port_start
, rf_ldma_sfence
, rf_ldma_direction
, rf_ldma_exram_addr
, rf_ldma_shram_addr
, rf_ldma_exram_c
, rf_ldma_exram_w
, rf_ldma_exram_h
, rf_ldma_exram_n
, rf_ldma_exram_stride_w_size
, rf_ldma_exram_stride_h_size
, rf_ldma_exram_stride_n_size
, rf_ldma_shram_c
, rf_ldma_shram_w
, rf_ldma_shram_h
, rf_ldma_shram_n
, rf_ldma_shram_pad_right
, rf_ldma_shram_pad_left
, rf_ldma_shram_pad_up
, rf_ldma_shram_pad_down
, rf_ldma_const_value
, rf_ldma_ch_num
, rf_ldma_ldma_decomp_padding_by_pass
, rf_ldma_ram_padding_value
, rf_ldma_pad_c_front
, rf_ldma_pad_c_back
, rf_ldma_ldma_chsum_sel
, rf_ldma_ldma_chsum_data
, rf_ldma_shram_stride_w_size
, rf_ldma_shram_stride_h_size
, rf_ldma_shram_stride_n_size
// autogen_port_stop
);

// autogen_bitwidth_start
localparam LDMA_SFENCE_BITWIDTH                       =  `LDMA_SFENCE_BITWIDTH;
localparam LDMA_DIRECTION_BITWIDTH                    =  `LDMA_DIRECTION_BITWIDTH;
localparam LDMA_EXRAM_ADDR_LSB_BITWIDTH               =  `LDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam LDMA_EXRAM_ADDR_MSB_BITWIDTH               =  `LDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam LDMA_EXRAM_ADDR_BITWIDTH                   =  `LDMA_EXRAM_ADDR_BITWIDTH;
localparam LDMA_SHRAM_ADDR_BITWIDTH                   =  `LDMA_SHRAM_ADDR_BITWIDTH;
localparam LDMA_EXRAM_C_BITWIDTH                      =  `LDMA_EXRAM_C_BITWIDTH;
localparam LDMA_EXRAM_W_BITWIDTH                      =  `LDMA_EXRAM_W_BITWIDTH;
localparam LDMA_EXRAM_H_BITWIDTH                      =  `LDMA_EXRAM_H_BITWIDTH;
localparam LDMA_EXRAM_N_BITWIDTH                      =  `LDMA_EXRAM_N_BITWIDTH;
localparam LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH          =  `LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH          =  `LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH;
localparam LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH          =  `LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH;
localparam LDMA_SHRAM_C_BITWIDTH                      =  `LDMA_SHRAM_C_BITWIDTH;
localparam LDMA_SHRAM_W_BITWIDTH                      =  `LDMA_SHRAM_W_BITWIDTH;
localparam LDMA_SHRAM_H_BITWIDTH                      =  `LDMA_SHRAM_H_BITWIDTH;
localparam LDMA_SHRAM_N_BITWIDTH                      =  `LDMA_SHRAM_N_BITWIDTH;
localparam LDMA_SHRAM_PAD_RIGHT_BITWIDTH              =  `LDMA_SHRAM_PAD_RIGHT_BITWIDTH;
localparam LDMA_SHRAM_PAD_LEFT_BITWIDTH               =  `LDMA_SHRAM_PAD_LEFT_BITWIDTH;
localparam LDMA_SHRAM_PAD_UP_BITWIDTH                 =  `LDMA_SHRAM_PAD_UP_BITWIDTH;
localparam LDMA_SHRAM_PAD_DOWN_BITWIDTH               =  `LDMA_SHRAM_PAD_DOWN_BITWIDTH;
localparam LDMA_CONST_VALUE_BITWIDTH                  =  `LDMA_CONST_VALUE_BITWIDTH;
localparam LDMA_CH_NUM_BITWIDTH                       =  `LDMA_CH_NUM_BITWIDTH;
localparam LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH  =  `LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH;
localparam LDMA_RAM_PADDING_VALUE_BITWIDTH            =  `LDMA_RAM_PADDING_VALUE_BITWIDTH;
localparam LDMA_PAD_C_FRONT_BITWIDTH                  =  `LDMA_PAD_C_FRONT_BITWIDTH;
localparam LDMA_PAD_C_BACK_BITWIDTH                   =  `LDMA_PAD_C_BACK_BITWIDTH;
localparam LDMA_LDMA_CHSUM_SEL_BITWIDTH               =  `LDMA_LDMA_CHSUM_SEL_BITWIDTH;
localparam LDMA_LDMA_CHSUM_DATA_BITWIDTH              =  `LDMA_LDMA_CHSUM_DATA_BITWIDTH;
localparam LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH          =  `LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH          =  `LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH;
localparam LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH          =  `LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH;
// autogen_bitwidth_stop

input                                                  clk;
input                                                  rst_n;

// autogen_io_start
input 	 [1-1:0] rf_ldma_sfence;
input 	 [LDMA_DIRECTION_BITWIDTH-1:0] rf_ldma_direction;
input 	 [LDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_ldma_exram_addr;
input 	 [LDMA_SHRAM_ADDR_BITWIDTH-1:0] rf_ldma_shram_addr;
input 	 [LDMA_EXRAM_C_BITWIDTH-1:0] rf_ldma_exram_c;
input 	 [LDMA_EXRAM_W_BITWIDTH-1:0] rf_ldma_exram_w;
input 	 [LDMA_EXRAM_H_BITWIDTH-1:0] rf_ldma_exram_h;
input 	 [LDMA_EXRAM_N_BITWIDTH-1:0] rf_ldma_exram_n;
input 	 [LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma_exram_stride_w_size;
input 	 [LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_ldma_exram_stride_h_size;
input 	 [LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_ldma_exram_stride_n_size;
input 	 [LDMA_SHRAM_C_BITWIDTH-1:0] rf_ldma_shram_c;
input 	 [LDMA_SHRAM_W_BITWIDTH-1:0] rf_ldma_shram_w;
input 	 [LDMA_SHRAM_H_BITWIDTH-1:0] rf_ldma_shram_h;
input 	 [LDMA_SHRAM_N_BITWIDTH-1:0] rf_ldma_shram_n;
input 	 [LDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0] rf_ldma_shram_pad_right;
input 	 [LDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0] rf_ldma_shram_pad_left;
input 	 [LDMA_SHRAM_PAD_UP_BITWIDTH-1:0] rf_ldma_shram_pad_up;
input 	 [LDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0] rf_ldma_shram_pad_down;
input 	 [LDMA_CONST_VALUE_BITWIDTH-1:0] rf_ldma_const_value;
input 	 [LDMA_CH_NUM_BITWIDTH-1:0] rf_ldma_ch_num;
input 	 [LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH-1:0] rf_ldma_ldma_decomp_padding_by_pass;
input 	 [LDMA_RAM_PADDING_VALUE_BITWIDTH-1:0] rf_ldma_ram_padding_value;
input 	 [LDMA_PAD_C_FRONT_BITWIDTH-1:0] rf_ldma_pad_c_front;
input 	 [LDMA_PAD_C_BACK_BITWIDTH-1:0] rf_ldma_pad_c_back;
input 	 [LDMA_LDMA_CHSUM_SEL_BITWIDTH-1:0] rf_ldma_ldma_chsum_sel;
output	 [LDMA_LDMA_CHSUM_DATA_BITWIDTH-1:0] rf_ldma_ldma_chsum_data;
input 	 [LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma_shram_stride_w_size;
input 	 [LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_ldma_shram_stride_h_size;
input 	 [LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_ldma_shram_stride_n_size;
// autogen_io_stop

// autogen_exceptio_start
output                 rf_ldma_except_trigger;
// autogen_exceptio_stop

endmodule
