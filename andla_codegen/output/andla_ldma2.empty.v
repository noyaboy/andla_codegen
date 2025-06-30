`include "andla.vh"

module andla_ldma2 (

clk
,rst_n
// autogen_exceptport_start
// autogen_exceptport_stop

// autogen_port_start
, rf_ldma2_mode_ctrl
, rf_ldma2_roll_ic_iw_w_pad_size
, rf_ldma2_roll_ic_kw_size
, rf_ldma2_roll_kr_stride_w_size
, rf_ldma2_roll_pad_w_left_w_ic_size
, rf_ldma2_roll_pad_w_right_w_ic_size
, rf_ldma2_roll_pad_h_size
// autogen_port_stop
);

// autogen_bitwidth_start
localparam LDMA2_MODE_CTRL_BITWIDTH                   =  `LDMA2_MODE_CTRL_BITWIDTH;
localparam LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH       =  `LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH;
localparam LDMA2_ROLL_IC_KW_SIZE_BITWIDTH             =  `LDMA2_ROLL_IC_KW_SIZE_BITWIDTH;
localparam LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH       =  `LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH   =  `LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH  =  `LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_H_SIZE_BITWIDTH             =  `LDMA2_ROLL_PAD_H_SIZE_BITWIDTH;
// autogen_bitwidth_stop

input                                                  clk;
input                                                  rst_n;

// autogen_io_start
input 	 [LDMA2_MODE_CTRL_BITWIDTH-1:0] rf_ldma2_mode_ctrl;
input 	 [LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1:0] rf_ldma2_roll_ic_iw_w_pad_size;
input 	 [LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1:0] rf_ldma2_roll_ic_kw_size;
input 	 [LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma2_roll_kr_stride_w_size;
input 	 [LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_w_left_w_ic_size;
input 	 [LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_w_right_w_ic_size;
input 	 [LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_h_size;
// autogen_io_stop

// autogen_exceptio_start
// autogen_exceptio_stop

endmodule
