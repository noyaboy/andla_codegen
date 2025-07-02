`include "andla.vh"

module andla_empty (

clk
,rst_n
// autogen_exceptport_start
,rf_cdma_except_trigger
,rf_fme0_except_trigger
,rf_ldma_except_trigger
,rf_sdma_except_trigger
// autogen_exceptport_stop

// autogen_port_start
, rf_csr_exram_based_addr_0
, rf_csr_exram_based_addr_1
, rf_csr_exram_based_addr_2
, rf_csr_exram_based_addr_3
, rf_csr_exram_based_addr_4
, rf_csr_exram_based_addr_5
, rf_csr_exram_based_addr_6
, rf_csr_exram_based_addr_7
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
, rf_fme0_sfence
, rf_fme0_mode
, rf_fme0_im_dilated_rate
, rf_fme0_im_pad
, rf_fme0_im_iw
, rf_fme0_im_ih
, rf_fme0_im_ic
, rf_fme0_im_stride
, rf_fme0_im_kernel
, rf_fme0_mode_ex
, rf_fme0_em_iw
, rf_fme0_em_ih
, rf_fme0_em_ic
, rf_fme0_om_ow
, rf_fme0_om_oh
, rf_fme0_om_oc
, rf_fme0_im_addr_init
, rf_fme0_kr_addr_init
, rf_fme0_bs_addr_init
, rf_fme0_pl_addr_init
, rf_fme0_em_addr_init
, rf_fme0_om_addr_init
, rf_fme0_em_alignment_iciw
, rf_fme0_om_alignment_ocow
, rf_fme0_alignment_kckwkh
, rf_fme0_alignment_kckw
, rf_fme0_sc_addr_init
, rf_fme0_sh_addr_init
, rf_fme0_im_kc
, rf_ldma2_mode_ctrl
, rf_ldma2_roll_ic_iw_w_pad_size
, rf_ldma2_roll_ic_kw_size
, rf_ldma2_roll_kr_stride_w_size
, rf_ldma2_roll_pad_w_left_w_ic_size
, rf_ldma2_roll_pad_w_right_w_ic_size
, rf_ldma2_roll_pad_h_size
, rf_cdma_sfence
, rf_cdma_direction
, rf_cdma_exram_addr
, rf_cdma_exram_c
, rf_cdma_exram_w
, rf_cdma_exram_stride_w
// autogen_port_stop
);

// autogen_bitwidth_start
localparam CSR_ID_BITWIDTH                            =  `CSR_ID_BITWIDTH;
localparam CSR_REVISION_BITWIDTH                      =  `CSR_REVISION_BITWIDTH;
localparam CSR_STATUS_BITWIDTH                        =  `CSR_STATUS_BITWIDTH;
localparam CSR_CONTROL_BITWIDTH                       =  `CSR_CONTROL_BITWIDTH;
localparam CSR_CREDIT_BITWIDTH                        =  22;
localparam CSR_COUNTER_LSB_BITWIDTH                   =  `CSR_COUNTER_LSB_BITWIDTH;
localparam CSR_COUNTER_MSB_BITWIDTH                   =  `CSR_COUNTER_MSB_BITWIDTH;
localparam CSR_COUNTER_BITWIDTH                       =  `CSR_COUNTER_BITWIDTH;
localparam CSR_COUNTER_MASK_BITWIDTH                  =  `CSR_COUNTER_MASK_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_0_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_0_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_1_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_1_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_2_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_2_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_3_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_3_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_4_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_4_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_5_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_5_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_6_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_6_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH        =  `CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_7_BITWIDTH            =  `CSR_EXRAM_BASED_ADDR_7_BITWIDTH;
localparam CSR_NOP_BITWIDTH                           =  `CSR_NOP_BITWIDTH;
localparam SDMA_SFENCE_BITWIDTH                       =  `SDMA_SFENCE_BITWIDTH;
localparam SDMA_DIRECTION_BITWIDTH                    =  `SDMA_DIRECTION_BITWIDTH;
localparam SDMA_EXRAM_ADDR_LSB_BITWIDTH               =  `SDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam SDMA_EXRAM_ADDR_MSB_BITWIDTH               =  `SDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam SDMA_EXRAM_ADDR_BITWIDTH                   =  `SDMA_EXRAM_ADDR_BITWIDTH;
localparam SDMA_SHRAM_ADDR_BITWIDTH                   =  `SDMA_SHRAM_ADDR_BITWIDTH;
localparam SDMA_EXRAM_C_BITWIDTH                      =  `SDMA_EXRAM_C_BITWIDTH;
localparam SDMA_EXRAM_W_BITWIDTH                      =  `SDMA_EXRAM_W_BITWIDTH;
localparam SDMA_EXRAM_H_BITWIDTH                      =  `SDMA_EXRAM_H_BITWIDTH;
localparam SDMA_EXRAM_N_BITWIDTH                      =  `SDMA_EXRAM_N_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH          =  `SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH          =  `SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH          =  `SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH;
localparam SDMA_SHRAM_C_BITWIDTH                      =  `SDMA_SHRAM_C_BITWIDTH;
localparam SDMA_SHRAM_W_BITWIDTH                      =  `SDMA_SHRAM_W_BITWIDTH;
localparam SDMA_SHRAM_H_BITWIDTH                      =  `SDMA_SHRAM_H_BITWIDTH;
localparam SDMA_SHRAM_N_BITWIDTH                      =  `SDMA_SHRAM_N_BITWIDTH;
localparam SDMA_SHRAM_PAD_RIGHT_BITWIDTH              =  `SDMA_SHRAM_PAD_RIGHT_BITWIDTH;
localparam SDMA_SHRAM_PAD_LEFT_BITWIDTH               =  `SDMA_SHRAM_PAD_LEFT_BITWIDTH;
localparam SDMA_SHRAM_PAD_UP_BITWIDTH                 =  `SDMA_SHRAM_PAD_UP_BITWIDTH;
localparam SDMA_SHRAM_PAD_DOWN_BITWIDTH               =  `SDMA_SHRAM_PAD_DOWN_BITWIDTH;
localparam SDMA_CONST_VALUE_BITWIDTH                  =  `SDMA_CONST_VALUE_BITWIDTH;
localparam SDMA_CH_NUM_BITWIDTH                       =  `SDMA_CH_NUM_BITWIDTH;
localparam SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH       =  `SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH;
localparam SDMA_PRESERVED0_BITWIDTH                   =  `SDMA_PRESERVED0_BITWIDTH;
localparam SDMA_PRESERVED1_BITWIDTH                   =  `SDMA_PRESERVED1_BITWIDTH;
localparam SDMA_PRESERVED2_BITWIDTH                   =  `SDMA_PRESERVED2_BITWIDTH;
localparam SDMA_SDMA_CHSUM_SEL_BITWIDTH               =  `SDMA_SDMA_CHSUM_SEL_BITWIDTH;
localparam SDMA_SDMA_CHSUM_DATA_BITWIDTH              =  `SDMA_SDMA_CHSUM_DATA_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH          =  `SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH          =  `SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH          =  `SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH;
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
localparam FME0_SFENCE_BITWIDTH                       =  `FME0_SFENCE_BITWIDTH;
localparam FME0_MODE_BITWIDTH                         =  `FME0_MODE_BITWIDTH;
localparam FME0_IM_DILATED_RATE_BITWIDTH              =  `FME0_IM_DILATED_RATE_BITWIDTH;
localparam FME0_IM_PAD_BITWIDTH                       =  `FME0_IM_PAD_BITWIDTH;
localparam FME0_IM_IW_BITWIDTH                        =  `FME0_IM_IW_BITWIDTH;
localparam FME0_IM_IH_BITWIDTH                        =  `FME0_IM_IH_BITWIDTH;
localparam FME0_IM_IC_BITWIDTH                        =  `FME0_IM_IC_BITWIDTH;
localparam FME0_IM_STRIDE_BITWIDTH                    =  `FME0_IM_STRIDE_BITWIDTH;
localparam FME0_IM_KERNEL_BITWIDTH                    =  `FME0_IM_KERNEL_BITWIDTH;
localparam FME0_MODE_EX_BITWIDTH                      =  `FME0_MODE_EX_BITWIDTH;
localparam FME0_EM_IW_BITWIDTH                        =  `FME0_EM_IW_BITWIDTH;
localparam FME0_EM_IH_BITWIDTH                        =  `FME0_EM_IH_BITWIDTH;
localparam FME0_EM_IC_BITWIDTH                        =  `FME0_EM_IC_BITWIDTH;
localparam FME0_OM_OW_BITWIDTH                        =  `FME0_OM_OW_BITWIDTH;
localparam FME0_OM_OH_BITWIDTH                        =  `FME0_OM_OH_BITWIDTH;
localparam FME0_OM_OC_BITWIDTH                        =  `FME0_OM_OC_BITWIDTH;
localparam FME0_IM_ADDR_INIT_BITWIDTH                 =  `FME0_IM_ADDR_INIT_BITWIDTH;
localparam FME0_KR_ADDR_INIT_BITWIDTH                 =  `FME0_KR_ADDR_INIT_BITWIDTH;
localparam FME0_BS_ADDR_INIT_BITWIDTH                 =  `FME0_BS_ADDR_INIT_BITWIDTH;
localparam FME0_PL_ADDR_INIT_BITWIDTH                 =  `FME0_PL_ADDR_INIT_BITWIDTH;
localparam FME0_EM_ADDR_INIT_BITWIDTH                 =  `FME0_EM_ADDR_INIT_BITWIDTH;
localparam FME0_OM_ADDR_INIT_BITWIDTH                 =  `FME0_OM_ADDR_INIT_BITWIDTH;
localparam FME0_EM_ALIGNMENT_ICIW_BITWIDTH            =  `FME0_EM_ALIGNMENT_ICIW_BITWIDTH;
localparam FME0_OM_ALIGNMENT_OCOW_BITWIDTH            =  `FME0_OM_ALIGNMENT_OCOW_BITWIDTH;
localparam FME0_ALIGNMENT_KCKWKH_BITWIDTH             =  `FME0_ALIGNMENT_KCKWKH_BITWIDTH;
localparam FME0_ALIGNMENT_KCKW_BITWIDTH               =  `FME0_ALIGNMENT_KCKW_BITWIDTH;
localparam FME0_SC_ADDR_INIT_BITWIDTH                 =  `FME0_SC_ADDR_INIT_BITWIDTH;
localparam FME0_SH_ADDR_INIT_BITWIDTH                 =  `FME0_SH_ADDR_INIT_BITWIDTH;
localparam FME0_IM_KC_BITWIDTH                        =  `FME0_IM_KC_BITWIDTH;
localparam LDMA2_MODE_CTRL_BITWIDTH                   =  `LDMA2_MODE_CTRL_BITWIDTH;
localparam LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH       =  `LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH;
localparam LDMA2_ROLL_IC_KW_SIZE_BITWIDTH             =  `LDMA2_ROLL_IC_KW_SIZE_BITWIDTH;
localparam LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH       =  `LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH   =  `LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH  =  `LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_H_SIZE_BITWIDTH             =  `LDMA2_ROLL_PAD_H_SIZE_BITWIDTH;
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
input 	 [CSR_EXRAM_BASED_ADDR_0_BITWIDTH-1:0] rf_csr_exram_based_addr_0;
input 	 [CSR_EXRAM_BASED_ADDR_1_BITWIDTH-1:0] rf_csr_exram_based_addr_1;
input 	 [CSR_EXRAM_BASED_ADDR_2_BITWIDTH-1:0] rf_csr_exram_based_addr_2;
input 	 [CSR_EXRAM_BASED_ADDR_3_BITWIDTH-1:0] rf_csr_exram_based_addr_3;
input 	 [CSR_EXRAM_BASED_ADDR_4_BITWIDTH-1:0] rf_csr_exram_based_addr_4;
input 	 [CSR_EXRAM_BASED_ADDR_5_BITWIDTH-1:0] rf_csr_exram_based_addr_5;
input 	 [CSR_EXRAM_BASED_ADDR_6_BITWIDTH-1:0] rf_csr_exram_based_addr_6;
input 	 [CSR_EXRAM_BASED_ADDR_7_BITWIDTH-1:0] rf_csr_exram_based_addr_7;
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
input 	 [1-1:0] rf_fme0_sfence;
input 	 [FME0_MODE_BITWIDTH-1:0] rf_fme0_mode;
input 	 [FME0_IM_DILATED_RATE_BITWIDTH-1:0] rf_fme0_im_dilated_rate;
input 	 [FME0_IM_PAD_BITWIDTH-1:0] rf_fme0_im_pad;
input 	 [FME0_IM_IW_BITWIDTH-1:0] rf_fme0_im_iw;
input 	 [FME0_IM_IH_BITWIDTH-1:0] rf_fme0_im_ih;
input 	 [FME0_IM_IC_BITWIDTH-1:0] rf_fme0_im_ic;
input 	 [FME0_IM_STRIDE_BITWIDTH-1:0] rf_fme0_im_stride;
input 	 [FME0_IM_KERNEL_BITWIDTH-1:0] rf_fme0_im_kernel;
input 	 [FME0_MODE_EX_BITWIDTH-1:0] rf_fme0_mode_ex;
input 	 [FME0_EM_IW_BITWIDTH-1:0] rf_fme0_em_iw;
input 	 [FME0_EM_IH_BITWIDTH-1:0] rf_fme0_em_ih;
input 	 [FME0_EM_IC_BITWIDTH-1:0] rf_fme0_em_ic;
input 	 [FME0_OM_OW_BITWIDTH-1:0] rf_fme0_om_ow;
input 	 [FME0_OM_OH_BITWIDTH-1:0] rf_fme0_om_oh;
input 	 [FME0_OM_OC_BITWIDTH-1:0] rf_fme0_om_oc;
input 	 [FME0_IM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_im_addr_init;
input 	 [FME0_KR_ADDR_INIT_BITWIDTH-1:0] rf_fme0_kr_addr_init;
input 	 [FME0_BS_ADDR_INIT_BITWIDTH-1:0] rf_fme0_bs_addr_init;
input 	 [FME0_PL_ADDR_INIT_BITWIDTH-1:0] rf_fme0_pl_addr_init;
input 	 [FME0_EM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_em_addr_init;
input 	 [FME0_OM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_om_addr_init;
input 	 [FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1:0] rf_fme0_em_alignment_iciw;
input 	 [FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1:0] rf_fme0_om_alignment_ocow;
input 	 [FME0_ALIGNMENT_KCKWKH_BITWIDTH-1:0] rf_fme0_alignment_kckwkh;
input 	 [FME0_ALIGNMENT_KCKW_BITWIDTH-1:0] rf_fme0_alignment_kckw;
input 	 [FME0_SC_ADDR_INIT_BITWIDTH-1:0] rf_fme0_sc_addr_init;
input 	 [FME0_SH_ADDR_INIT_BITWIDTH-1:0] rf_fme0_sh_addr_init;
input 	 [FME0_IM_KC_BITWIDTH-1:0] rf_fme0_im_kc;
input 	 [LDMA2_MODE_CTRL_BITWIDTH-1:0] rf_ldma2_mode_ctrl;
input 	 [LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1:0] rf_ldma2_roll_ic_iw_w_pad_size;
input 	 [LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1:0] rf_ldma2_roll_ic_kw_size;
input 	 [LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma2_roll_kr_stride_w_size;
input 	 [LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_w_left_w_ic_size;
input 	 [LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_w_right_w_ic_size;
input 	 [LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_h_size;
input 	 [1-1:0] rf_cdma_sfence;
input 	 [CDMA_DIRECTION_BITWIDTH-1:0] rf_cdma_direction;
input 	 [CDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_cdma_exram_addr;
input 	 [CDMA_EXRAM_C_BITWIDTH-1:0] rf_cdma_exram_c;
input 	 [CDMA_EXRAM_W_BITWIDTH-1:0] rf_cdma_exram_w;
input 	 [CDMA_EXRAM_STRIDE_W_BITWIDTH-1:0] rf_cdma_exram_stride_w;
// autogen_io_stop

// autogen_exceptio_start
output                 rf_cdma_except_trigger;
output                 rf_fme0_except_trigger;
output                 rf_ldma_except_trigger;
output                 rf_sdma_except_trigger;
// autogen_exceptio_stop

endmodule
