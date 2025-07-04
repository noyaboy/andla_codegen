`include "andla.vh"

module andla_regfile(

//{{{ module
clk
,rst_n
,issue_rf_riurwaddr
,issue_rf_riuwe
,issue_rf_riuwdata
,issue_rf_riuwstatus
,issue_rf_riurdata
,ip_rf_status_clr
,rf_block_intr
,fetch_buffer_free_entry
,sqr_credit

// autogen_exceptport_start
,rf_cdma_except_trigger
,rf_fme0_except_trigger
,rf_ldma_except_trigger
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
//}}}

//{{{ parameters
// autogen_bitwidth_start
localparam CSR_ID_BITWIDTH                           = `CSR_ID_BITWIDTH;
localparam CSR_REVISION_BITWIDTH                     = `CSR_REVISION_BITWIDTH;
localparam CSR_STATUS_BITWIDTH                       = `CSR_STATUS_BITWIDTH;
localparam CSR_CONTROL_BITWIDTH                      = `CSR_CONTROL_BITWIDTH;
localparam CSR_CREDIT_BITWIDTH                       = 22;
localparam CSR_COUNTER_LSB_BITWIDTH                  = `CSR_COUNTER_LSB_BITWIDTH;
localparam CSR_COUNTER_MSB_BITWIDTH                  = `CSR_COUNTER_MSB_BITWIDTH;
localparam CSR_COUNTER_BITWIDTH                      = `CSR_COUNTER_BITWIDTH;
localparam CSR_COUNTER_MASK_BITWIDTH                 = `CSR_COUNTER_MASK_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_0_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_0_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_1_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_1_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_2_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_2_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_3_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_3_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_4_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_4_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_5_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_5_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_6_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_6_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH       = `CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH;
localparam CSR_EXRAM_BASED_ADDR_7_BITWIDTH           = `CSR_EXRAM_BASED_ADDR_7_BITWIDTH;
localparam CSR_NOP_BITWIDTH                          = `CSR_NOP_BITWIDTH;
localparam SDMA_SFENCE_BITWIDTH                      = `SDMA_SFENCE_BITWIDTH;
localparam SDMA_DIRECTION_BITWIDTH                   = `SDMA_DIRECTION_BITWIDTH;
localparam SDMA_EXRAM_ADDR_LSB_BITWIDTH              = `SDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam SDMA_EXRAM_ADDR_MSB_BITWIDTH              = `SDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam SDMA_EXRAM_ADDR_BITWIDTH                  = `SDMA_EXRAM_ADDR_BITWIDTH;
localparam SDMA_SHRAM_ADDR_BITWIDTH                  = `SDMA_SHRAM_ADDR_BITWIDTH;
localparam SDMA_EXRAM_C_BITWIDTH                     = `SDMA_EXRAM_C_BITWIDTH;
localparam SDMA_EXRAM_W_BITWIDTH                     = `SDMA_EXRAM_W_BITWIDTH;
localparam SDMA_EXRAM_H_BITWIDTH                     = `SDMA_EXRAM_H_BITWIDTH;
localparam SDMA_EXRAM_N_BITWIDTH                     = `SDMA_EXRAM_N_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH         = `SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH         = `SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH;
localparam SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH         = `SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH;
localparam SDMA_SHRAM_C_BITWIDTH                     = `SDMA_SHRAM_C_BITWIDTH;
localparam SDMA_SHRAM_W_BITWIDTH                     = `SDMA_SHRAM_W_BITWIDTH;
localparam SDMA_SHRAM_H_BITWIDTH                     = `SDMA_SHRAM_H_BITWIDTH;
localparam SDMA_SHRAM_N_BITWIDTH                     = `SDMA_SHRAM_N_BITWIDTH;
localparam SDMA_SHRAM_PAD_RIGHT_BITWIDTH             = `SDMA_SHRAM_PAD_RIGHT_BITWIDTH;
localparam SDMA_SHRAM_PAD_LEFT_BITWIDTH              = `SDMA_SHRAM_PAD_LEFT_BITWIDTH;
localparam SDMA_SHRAM_PAD_UP_BITWIDTH                = `SDMA_SHRAM_PAD_UP_BITWIDTH;
localparam SDMA_SHRAM_PAD_DOWN_BITWIDTH              = `SDMA_SHRAM_PAD_DOWN_BITWIDTH;
localparam SDMA_CONST_VALUE_BITWIDTH                 = `SDMA_CONST_VALUE_BITWIDTH;
localparam SDMA_CH_NUM_BITWIDTH                      = `SDMA_CH_NUM_BITWIDTH;
localparam SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH      = `SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH;
localparam SDMA_PRESERVED0_BITWIDTH                  = `SDMA_PRESERVED0_BITWIDTH;
localparam SDMA_PRESERVED1_BITWIDTH                  = `SDMA_PRESERVED1_BITWIDTH;
localparam SDMA_PRESERVED2_BITWIDTH                  = `SDMA_PRESERVED2_BITWIDTH;
localparam SDMA_SDMA_CHSUM_SEL_BITWIDTH              = `SDMA_SDMA_CHSUM_SEL_BITWIDTH;
localparam SDMA_SDMA_CHSUM_DATA_BITWIDTH             = `SDMA_SDMA_CHSUM_DATA_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH         = `SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH         = `SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH;
localparam SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH         = `SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH;
localparam LDMA_SFENCE_BITWIDTH                      = `LDMA_SFENCE_BITWIDTH;
localparam LDMA_DIRECTION_BITWIDTH                   = `LDMA_DIRECTION_BITWIDTH;
localparam LDMA_EXRAM_ADDR_LSB_BITWIDTH              = `LDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam LDMA_EXRAM_ADDR_MSB_BITWIDTH              = `LDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam LDMA_EXRAM_ADDR_BITWIDTH                  = `LDMA_EXRAM_ADDR_BITWIDTH;
localparam LDMA_SHRAM_ADDR_BITWIDTH                  = `LDMA_SHRAM_ADDR_BITWIDTH;
localparam LDMA_EXRAM_C_BITWIDTH                     = `LDMA_EXRAM_C_BITWIDTH;
localparam LDMA_EXRAM_W_BITWIDTH                     = `LDMA_EXRAM_W_BITWIDTH;
localparam LDMA_EXRAM_H_BITWIDTH                     = `LDMA_EXRAM_H_BITWIDTH;
localparam LDMA_EXRAM_N_BITWIDTH                     = `LDMA_EXRAM_N_BITWIDTH;
localparam LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH         = `LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH         = `LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH;
localparam LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH         = `LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH;
localparam LDMA_SHRAM_C_BITWIDTH                     = `LDMA_SHRAM_C_BITWIDTH;
localparam LDMA_SHRAM_W_BITWIDTH                     = `LDMA_SHRAM_W_BITWIDTH;
localparam LDMA_SHRAM_H_BITWIDTH                     = `LDMA_SHRAM_H_BITWIDTH;
localparam LDMA_SHRAM_N_BITWIDTH                     = `LDMA_SHRAM_N_BITWIDTH;
localparam LDMA_SHRAM_PAD_RIGHT_BITWIDTH             = `LDMA_SHRAM_PAD_RIGHT_BITWIDTH;
localparam LDMA_SHRAM_PAD_LEFT_BITWIDTH              = `LDMA_SHRAM_PAD_LEFT_BITWIDTH;
localparam LDMA_SHRAM_PAD_UP_BITWIDTH                = `LDMA_SHRAM_PAD_UP_BITWIDTH;
localparam LDMA_SHRAM_PAD_DOWN_BITWIDTH              = `LDMA_SHRAM_PAD_DOWN_BITWIDTH;
localparam LDMA_CONST_VALUE_BITWIDTH                 = `LDMA_CONST_VALUE_BITWIDTH;
localparam LDMA_CH_NUM_BITWIDTH                      = `LDMA_CH_NUM_BITWIDTH;
localparam LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH = `LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH;
localparam LDMA_RAM_PADDING_VALUE_BITWIDTH           = `LDMA_RAM_PADDING_VALUE_BITWIDTH;
localparam LDMA_PAD_C_FRONT_BITWIDTH                 = `LDMA_PAD_C_FRONT_BITWIDTH;
localparam LDMA_PAD_C_BACK_BITWIDTH                  = `LDMA_PAD_C_BACK_BITWIDTH;
localparam LDMA_LDMA_CHSUM_SEL_BITWIDTH              = `LDMA_LDMA_CHSUM_SEL_BITWIDTH;
localparam LDMA_LDMA_CHSUM_DATA_BITWIDTH             = `LDMA_LDMA_CHSUM_DATA_BITWIDTH;
localparam LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH         = `LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH         = `LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH;
localparam LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH         = `LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH;
localparam FME0_SFENCE_BITWIDTH                      = `FME0_SFENCE_BITWIDTH;
localparam FME0_MODE_BITWIDTH                        = `FME0_MODE_BITWIDTH;
localparam FME0_IM_DILATED_RATE_BITWIDTH             = `FME0_IM_DILATED_RATE_BITWIDTH;
localparam FME0_IM_PAD_BITWIDTH                      = `FME0_IM_PAD_BITWIDTH;
localparam FME0_IM_IW_BITWIDTH                       = `FME0_IM_IW_BITWIDTH;
localparam FME0_IM_IH_BITWIDTH                       = `FME0_IM_IH_BITWIDTH;
localparam FME0_IM_IC_BITWIDTH                       = `FME0_IM_IC_BITWIDTH;
localparam FME0_IM_STRIDE_BITWIDTH                   = `FME0_IM_STRIDE_BITWIDTH;
localparam FME0_IM_KERNEL_BITWIDTH                   = `FME0_IM_KERNEL_BITWIDTH;
localparam FME0_MODE_EX_BITWIDTH                     = `FME0_MODE_EX_BITWIDTH;
localparam FME0_EM_IW_BITWIDTH                       = `FME0_EM_IW_BITWIDTH;
localparam FME0_EM_IH_BITWIDTH                       = `FME0_EM_IH_BITWIDTH;
localparam FME0_EM_IC_BITWIDTH                       = `FME0_EM_IC_BITWIDTH;
localparam FME0_OM_OW_BITWIDTH                       = `FME0_OM_OW_BITWIDTH;
localparam FME0_OM_OH_BITWIDTH                       = `FME0_OM_OH_BITWIDTH;
localparam FME0_OM_OC_BITWIDTH                       = `FME0_OM_OC_BITWIDTH;
localparam FME0_IM_ADDR_INIT_BITWIDTH                = `FME0_IM_ADDR_INIT_BITWIDTH;
localparam FME0_KR_ADDR_INIT_BITWIDTH                = `FME0_KR_ADDR_INIT_BITWIDTH;
localparam FME0_BS_ADDR_INIT_BITWIDTH                = `FME0_BS_ADDR_INIT_BITWIDTH;
localparam FME0_PL_ADDR_INIT_BITWIDTH                = `FME0_PL_ADDR_INIT_BITWIDTH;
localparam FME0_EM_ADDR_INIT_BITWIDTH                = `FME0_EM_ADDR_INIT_BITWIDTH;
localparam FME0_OM_ADDR_INIT_BITWIDTH                = `FME0_OM_ADDR_INIT_BITWIDTH;
localparam FME0_EM_ALIGNMENT_ICIW_BITWIDTH           = `FME0_EM_ALIGNMENT_ICIW_BITWIDTH;
localparam FME0_OM_ALIGNMENT_OCOW_BITWIDTH           = `FME0_OM_ALIGNMENT_OCOW_BITWIDTH;
localparam FME0_ALIGNMENT_KCKWKH_BITWIDTH            = `FME0_ALIGNMENT_KCKWKH_BITWIDTH;
localparam FME0_ALIGNMENT_KCKW_BITWIDTH              = `FME0_ALIGNMENT_KCKW_BITWIDTH;
localparam FME0_SC_ADDR_INIT_BITWIDTH                = `FME0_SC_ADDR_INIT_BITWIDTH;
localparam FME0_SH_ADDR_INIT_BITWIDTH                = `FME0_SH_ADDR_INIT_BITWIDTH;
localparam FME0_IM_KC_BITWIDTH                       = `FME0_IM_KC_BITWIDTH;
localparam LDMA2_MODE_CTRL_BITWIDTH                  = `LDMA2_MODE_CTRL_BITWIDTH;
localparam LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH      = `LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH;
localparam LDMA2_ROLL_IC_KW_SIZE_BITWIDTH            = `LDMA2_ROLL_IC_KW_SIZE_BITWIDTH;
localparam LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH      = `LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH  = `LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH = `LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH;
localparam LDMA2_ROLL_PAD_H_SIZE_BITWIDTH            = `LDMA2_ROLL_PAD_H_SIZE_BITWIDTH;
localparam CDMA_SFENCE_BITWIDTH                      = `CDMA_SFENCE_BITWIDTH;
localparam CDMA_DIRECTION_BITWIDTH                   = `CDMA_DIRECTION_BITWIDTH;
localparam CDMA_EXRAM_ADDR_LSB_BITWIDTH              = `CDMA_EXRAM_ADDR_LSB_BITWIDTH;
localparam CDMA_EXRAM_ADDR_MSB_BITWIDTH              = `CDMA_EXRAM_ADDR_MSB_BITWIDTH;
localparam CDMA_EXRAM_ADDR_BITWIDTH                  = `CDMA_EXRAM_ADDR_BITWIDTH;
localparam CDMA_EXRAM_C_BITWIDTH                     = `CDMA_EXRAM_C_BITWIDTH;
localparam CDMA_EXRAM_W_BITWIDTH                     = `CDMA_EXRAM_W_BITWIDTH;
localparam CDMA_EXRAM_STRIDE_W_BITWIDTH              = `CDMA_EXRAM_STRIDE_W_BITWIDTH;
// autogen_bitwidth_stop

// autogen_baseaddrselbitwidth_start
localparam SDMA_BASE_ADDR_SELECT_BITWIDTH = 3;
localparam LDMA_BASE_ADDR_SELECT_BITWIDTH = 3;
localparam CDMA_BASE_ADDR_SELECT_BITWIDTH = 3;
// autogen_baseaddrselbitwidth_stop

// autogen_ipnum_start
localparam ITEM_ID_NUM = `ITEM_ID_NUM;
// autogen_ipnum_stop

localparam ID_DATA                                   = `ANDLA_CSR_ID;
localparam REVISION_DATA                             = `ANDLA_CSR_REVISION;
parameter  RF_ADDR_BITWIDTH                          = `ANDLA_RF_ADDR_BITWIDTH;         
parameter  RF_WDATA_BITWIDTH                         = `ANDLA_RF_WDATA_BITWIDTH;        
parameter  RF_RDATA_BITWIDTH                         = `ANDLA_RF_RDATA_BITWIDTH;       
parameter  ITEM_ID_BITWIDTH                          = `ANDLA_RF_ID_BITWIDTH;           
parameter  INDEX_BITWIDTH                            = `ANDLA_RF_INDEX_BITWIDTH;        
parameter  ADDR_BITWIDTH                             = `ANDLA_IBMC_ADDR_BITWIDTH;       
parameter  AXI_ADDR_WIDTH                            = `ANDLA_AXI_ADDR_WIDTH;           
parameter  DDMA_C_SIZE_BITWIDTH                      = `ANDLA_RF_DDMA_C_SIZE_BITWIDTH;  
parameter  DDMA_W_SIZE_BITWIDTH                      = `ANDLA_RF_DDMA_W_SIZE_BITWIDTH;  
parameter  DDMA_H_SIZE_BITWIDTH                      = `ANDLA_RF_DDMA_H_SIZE_BITWIDTH;  
parameter  DDMA_N_SIZE_BITWIDTH                      = `ANDLA_RF_DDMA_N_SIZE_BITWIDTH;  
parameter  DDMA_PAD_BITWIDTH                         = `ANDLA_RF_DDMA_PAD_BITWIDTH;     
parameter  DDMA_STRIDE_BITWIDTH                      = `ANDLA_RF_DDMA_STRIDE_BITWIDTH;  
parameter  CHANNEL_SIZE_BITWIDTH                     = `ANDLA_DLA_CHANNEL_SIZE_BITWIDTH;
parameter  IMAGE_SIZE_BITWIDTH                       = `ANDLA_DLA_IMAGE_SIZE_BITWIDTH;  
parameter  KERNEL_SIZE_BITWIDTH                      = `ANDLA_DLA_KERNEL_SIZE_BITWIDTH; 
parameter  STATUS_REG_WIDTH                          = `ANDLA_RF_STATUS_BITWIDTH;       
parameter  CONTROL_BITWIDTH                          = `ANDLA_RF_CONTROL_BITWIDTH;      
localparam AXIADDR_LSB_WIDTH                         = `ANDLA_RF_WDATA_BITWIDTH;                           
localparam AXIADDR_MSB_WIDTH                         = `ANDLA_RF_RDATA_BITWIDTH - `ANDLA_RF_WDATA_BITWIDTH;
localparam C_SIZE_ZERO_EXTEND                        = DDMA_C_SIZE_BITWIDTH - RF_WDATA_BITWIDTH;         
localparam STRIDE_ZERO_EXTEND                        = DDMA_STRIDE_BITWIDTH - RF_WDATA_BITWIDTH;         
parameter  CDMA_DATA_BUF_DEPTH                       = `ANDLA_FETCH_FIFO_DEPTH;
localparam CDMA_DATA_BUF_WIDTH                       = $clog2(CDMA_DATA_BUF_DEPTH) + 1;
parameter  BIU_DATA_WIDTH		                     = 64;
parameter  CDMA_CMD_WIDTH		                     = 32;
parameter  FETCH_SRAM_EN                             = 1;
localparam CREDIT_INIT_VALUE                         = FETCH_SRAM_EN ? ( (CDMA_DATA_BUF_DEPTH+4) * BIU_DATA_WIDTH / CDMA_CMD_WIDTH): (  CDMA_DATA_BUF_DEPTH * BIU_DATA_WIDTH / CDMA_CMD_WIDTH);
localparam CREDIT_BITWIDTH                           = $clog2(CREDIT_INIT_VALUE+1);

//{{{ input/output
input                                                  clk;
input                                                  rst_n;
//From disp TBD joe naming rule
input  [RF_ADDR_BITWIDTH-                         1:0] issue_rf_riurwaddr;
input                                                  issue_rf_riuwe;
input  [RF_WDATA_BITWIDTH-                        1:0] issue_rf_riuwdata;
output                                                 issue_rf_riuwstatus;
output [RF_RDATA_BITWIDTH-                        1:0] issue_rf_riurdata;
// scoreboard interface
input  [ITEM_ID_NUM-                                   1:0] ip_rf_status_clr;
// Interrupt
output                                                 rf_block_intr;

// autogen_io_start
wire  	 [CSR_EXRAM_BASED_ADDR_0_BITWIDTH-1:0] csr_exram_based_addr_0;
wire  	 [CSR_EXRAM_BASED_ADDR_1_BITWIDTH-1:0] csr_exram_based_addr_1;
wire  	 [CSR_EXRAM_BASED_ADDR_2_BITWIDTH-1:0] csr_exram_based_addr_2;
wire  	 [CSR_EXRAM_BASED_ADDR_3_BITWIDTH-1:0] csr_exram_based_addr_3;
wire  	 [CSR_EXRAM_BASED_ADDR_4_BITWIDTH-1:0] csr_exram_based_addr_4;
wire  	 [CSR_EXRAM_BASED_ADDR_5_BITWIDTH-1:0] csr_exram_based_addr_5;
wire  	 [CSR_EXRAM_BASED_ADDR_6_BITWIDTH-1:0] csr_exram_based_addr_6;
wire  	 [CSR_EXRAM_BASED_ADDR_7_BITWIDTH-1:0] csr_exram_based_addr_7;
output	 [1-1:0] rf_sdma_sfence;
output	 [SDMA_DIRECTION_BITWIDTH-1:0] rf_sdma_direction;
output	 [SDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_sdma_exram_addr;
output	 [SDMA_SHRAM_ADDR_BITWIDTH-1:0] rf_sdma_shram_addr;
output	 [SDMA_EXRAM_C_BITWIDTH-1:0] rf_sdma_exram_c;
output	 [SDMA_EXRAM_W_BITWIDTH-1:0] rf_sdma_exram_w;
output	 [SDMA_EXRAM_H_BITWIDTH-1:0] rf_sdma_exram_h;
output	 [SDMA_EXRAM_N_BITWIDTH-1:0] rf_sdma_exram_n;
output	 [SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_sdma_exram_stride_w_size;
output	 [SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_sdma_exram_stride_h_size;
output	 [SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_sdma_exram_stride_n_size;
output	 [SDMA_SHRAM_C_BITWIDTH-1:0] rf_sdma_shram_c;
output	 [SDMA_SHRAM_W_BITWIDTH-1:0] rf_sdma_shram_w;
output	 [SDMA_SHRAM_H_BITWIDTH-1:0] rf_sdma_shram_h;
output	 [SDMA_SHRAM_N_BITWIDTH-1:0] rf_sdma_shram_n;
output	 [SDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0] rf_sdma_shram_pad_right;
output	 [SDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0] rf_sdma_shram_pad_left;
output	 [SDMA_SHRAM_PAD_UP_BITWIDTH-1:0] rf_sdma_shram_pad_up;
output	 [SDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0] rf_sdma_shram_pad_down;
output	 [SDMA_CONST_VALUE_BITWIDTH-1:0] rf_sdma_const_value;
output	 [SDMA_CH_NUM_BITWIDTH-1:0] rf_sdma_ch_num;
output	 [SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH-1:0] rf_sdma_sdma_depadding_by_pass;
output	 [SDMA_PRESERVED0_BITWIDTH-1:0] rf_sdma_preserved0;
output	 [SDMA_PRESERVED1_BITWIDTH-1:0] rf_sdma_preserved1;
output	 [SDMA_PRESERVED2_BITWIDTH-1:0] rf_sdma_preserved2;
output	 [SDMA_SDMA_CHSUM_SEL_BITWIDTH-1:0] rf_sdma_sdma_chsum_sel;
input 	 [SDMA_SDMA_CHSUM_DATA_BITWIDTH-1:0] rf_sdma_sdma_chsum_data;
output	 [SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_sdma_shram_stride_w_size;
output	 [SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_sdma_shram_stride_h_size;
output	 [SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_sdma_shram_stride_n_size;
output	 [1-1:0] rf_ldma_sfence;
output	 [LDMA_DIRECTION_BITWIDTH-1:0] rf_ldma_direction;
output	 [LDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_ldma_exram_addr;
output	 [LDMA_SHRAM_ADDR_BITWIDTH-1:0] rf_ldma_shram_addr;
output	 [LDMA_EXRAM_C_BITWIDTH-1:0] rf_ldma_exram_c;
output	 [LDMA_EXRAM_W_BITWIDTH-1:0] rf_ldma_exram_w;
output	 [LDMA_EXRAM_H_BITWIDTH-1:0] rf_ldma_exram_h;
output	 [LDMA_EXRAM_N_BITWIDTH-1:0] rf_ldma_exram_n;
output	 [LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma_exram_stride_w_size;
output	 [LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_ldma_exram_stride_h_size;
output	 [LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_ldma_exram_stride_n_size;
output	 [LDMA_SHRAM_C_BITWIDTH-1:0] rf_ldma_shram_c;
output	 [LDMA_SHRAM_W_BITWIDTH-1:0] rf_ldma_shram_w;
output	 [LDMA_SHRAM_H_BITWIDTH-1:0] rf_ldma_shram_h;
output	 [LDMA_SHRAM_N_BITWIDTH-1:0] rf_ldma_shram_n;
output	 [LDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0] rf_ldma_shram_pad_right;
output	 [LDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0] rf_ldma_shram_pad_left;
output	 [LDMA_SHRAM_PAD_UP_BITWIDTH-1:0] rf_ldma_shram_pad_up;
output	 [LDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0] rf_ldma_shram_pad_down;
output	 [LDMA_CONST_VALUE_BITWIDTH-1:0] rf_ldma_const_value;
output	 [LDMA_CH_NUM_BITWIDTH-1:0] rf_ldma_ch_num;
output	 [LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH-1:0] rf_ldma_ldma_decomp_padding_by_pass;
output	 [LDMA_RAM_PADDING_VALUE_BITWIDTH-1:0] rf_ldma_ram_padding_value;
output	 [LDMA_PAD_C_FRONT_BITWIDTH-1:0] rf_ldma_pad_c_front;
output	 [LDMA_PAD_C_BACK_BITWIDTH-1:0] rf_ldma_pad_c_back;
output	 [LDMA_LDMA_CHSUM_SEL_BITWIDTH-1:0] rf_ldma_ldma_chsum_sel;
input 	 [LDMA_LDMA_CHSUM_DATA_BITWIDTH-1:0] rf_ldma_ldma_chsum_data;
output	 [LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma_shram_stride_w_size;
output	 [LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0] rf_ldma_shram_stride_h_size;
output	 [LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0] rf_ldma_shram_stride_n_size;
output	 [1-1:0] rf_fme0_sfence;
output	 [FME0_MODE_BITWIDTH-1:0] rf_fme0_mode;
output	 [FME0_IM_DILATED_RATE_BITWIDTH-1:0] rf_fme0_im_dilated_rate;
output	 [FME0_IM_PAD_BITWIDTH-1:0] rf_fme0_im_pad;
output	 [FME0_IM_IW_BITWIDTH-1:0] rf_fme0_im_iw;
output	 [FME0_IM_IH_BITWIDTH-1:0] rf_fme0_im_ih;
output	 [FME0_IM_IC_BITWIDTH-1:0] rf_fme0_im_ic;
output	 [FME0_IM_STRIDE_BITWIDTH-1:0] rf_fme0_im_stride;
output	 [FME0_IM_KERNEL_BITWIDTH-1:0] rf_fme0_im_kernel;
output	 [FME0_MODE_EX_BITWIDTH-1:0] rf_fme0_mode_ex;
output	 [FME0_EM_IW_BITWIDTH-1:0] rf_fme0_em_iw;
output	 [FME0_EM_IH_BITWIDTH-1:0] rf_fme0_em_ih;
output	 [FME0_EM_IC_BITWIDTH-1:0] rf_fme0_em_ic;
output	 [FME0_OM_OW_BITWIDTH-1:0] rf_fme0_om_ow;
output	 [FME0_OM_OH_BITWIDTH-1:0] rf_fme0_om_oh;
output	 [FME0_OM_OC_BITWIDTH-1:0] rf_fme0_om_oc;
output	 [FME0_IM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_im_addr_init;
output	 [FME0_KR_ADDR_INIT_BITWIDTH-1:0] rf_fme0_kr_addr_init;
output	 [FME0_BS_ADDR_INIT_BITWIDTH-1:0] rf_fme0_bs_addr_init;
output	 [FME0_PL_ADDR_INIT_BITWIDTH-1:0] rf_fme0_pl_addr_init;
output	 [FME0_EM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_em_addr_init;
output	 [FME0_OM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_om_addr_init;
output	 [FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1:0] rf_fme0_em_alignment_iciw;
output	 [FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1:0] rf_fme0_om_alignment_ocow;
output	 [FME0_ALIGNMENT_KCKWKH_BITWIDTH-1:0] rf_fme0_alignment_kckwkh;
output	 [FME0_ALIGNMENT_KCKW_BITWIDTH-1:0] rf_fme0_alignment_kckw;
output	 [FME0_SC_ADDR_INIT_BITWIDTH-1:0] rf_fme0_sc_addr_init;
output	 [FME0_SH_ADDR_INIT_BITWIDTH-1:0] rf_fme0_sh_addr_init;
output	 [FME0_IM_KC_BITWIDTH-1:0] rf_fme0_im_kc;
output	 [LDMA2_MODE_CTRL_BITWIDTH-1:0] rf_ldma2_mode_ctrl;
output	 [LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1:0] rf_ldma2_roll_ic_iw_w_pad_size;
output	 [LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1:0] rf_ldma2_roll_ic_kw_size;
output	 [LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1:0] rf_ldma2_roll_kr_stride_w_size;
output	 [LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_w_left_w_ic_size;
output	 [LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_w_right_w_ic_size;
output	 [LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1:0] rf_ldma2_roll_pad_h_size;
output	 [1-1:0] rf_cdma_sfence;
output	 [CDMA_DIRECTION_BITWIDTH-1:0] rf_cdma_direction;
output	 [CDMA_EXRAM_ADDR_BITWIDTH-1:0] rf_cdma_exram_addr;
output	 [CDMA_EXRAM_C_BITWIDTH-1:0] rf_cdma_exram_c;
output	 [CDMA_EXRAM_W_BITWIDTH-1:0] rf_cdma_exram_w;
output	 [CDMA_EXRAM_STRIDE_W_BITWIDTH-1:0] rf_cdma_exram_stride_w;
// autogen_io_stop

input  [CDMA_DATA_BUF_WIDTH-                      1:0] fetch_buffer_free_entry; 
input  [CSR_CREDIT_BITWIDTH-                          1:0] sqr_credit;

// autogen_exceptio_start
input                 rf_cdma_except_trigger;
input                 rf_fme0_except_trigger;
input                 rf_ldma_except_trigger;
input                 rf_sdma_except_trigger;
// autogen_exceptio_stop
//}}}

//{{{ regs
// autogen_reg_start
reg	[CSR_STATUS_BITWIDTH-1:0]                      	csr_status_reg;
reg	[CSR_CONTROL_BITWIDTH-1:0]                     	csr_control_reg;
reg	[CSR_COUNTER_LSB_BITWIDTH-1:0]                 	csr_counter_lsb_reg;
reg	[CSR_COUNTER_MSB_BITWIDTH-1:0]                 	csr_counter_msb_reg;
reg	[CSR_COUNTER_MASK_BITWIDTH-1:0]                	csr_counter_mask_reg;
reg	[CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_0_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_0_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_1_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_1_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_2_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_2_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_3_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_3_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_4_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_4_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_5_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_5_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_6_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_6_msb_reg;
reg	[CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH-1:0]      	csr_exram_based_addr_7_lsb_reg;
reg	[CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH-1:0]      	csr_exram_based_addr_7_msb_reg;
reg	[SDMA_SFENCE_BITWIDTH-1:0]                     	sdma_sfence_reg;
reg	[SDMA_DIRECTION_BITWIDTH-1:0]                  	sdma_direction_reg;
reg	[SDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0]             	sdma_exram_addr_lsb_reg;
reg	[SDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0]             	sdma_exram_addr_msb_reg;
reg	[SDMA_SHRAM_ADDR_BITWIDTH-1:0]                 	sdma_shram_addr_reg;
reg	[SDMA_EXRAM_C_BITWIDTH-1:0]                    	sdma_exram_c_reg;
reg	[SDMA_EXRAM_W_BITWIDTH-1:0]                    	sdma_exram_w_reg;
reg	[SDMA_EXRAM_H_BITWIDTH-1:0]                    	sdma_exram_h_reg;
reg	[SDMA_EXRAM_N_BITWIDTH-1:0]                    	sdma_exram_n_reg;
reg	[SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0]        	sdma_exram_stride_w_size_reg;
reg	[SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0]        	sdma_exram_stride_h_size_reg;
reg	[SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0]        	sdma_exram_stride_n_size_reg;
reg	[SDMA_SHRAM_C_BITWIDTH-1:0]                    	sdma_shram_c_reg;
reg	[SDMA_SHRAM_W_BITWIDTH-1:0]                    	sdma_shram_w_reg;
reg	[SDMA_SHRAM_H_BITWIDTH-1:0]                    	sdma_shram_h_reg;
reg	[SDMA_SHRAM_N_BITWIDTH-1:0]                    	sdma_shram_n_reg;
reg	[SDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0]            	sdma_shram_pad_right_reg;
reg	[SDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0]             	sdma_shram_pad_left_reg;
reg	[SDMA_SHRAM_PAD_UP_BITWIDTH-1:0]               	sdma_shram_pad_up_reg;
reg	[SDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0]             	sdma_shram_pad_down_reg;
reg	[SDMA_CONST_VALUE_BITWIDTH-1:0]                	sdma_const_value_reg;
reg	[SDMA_CH_NUM_BITWIDTH-1:0]                     	sdma_ch_num_reg;
reg	[SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH-1:0]     	sdma_sdma_depadding_by_pass_reg;
reg	[SDMA_PRESERVED0_BITWIDTH-1:0]                 	sdma_preserved0_reg;
reg	[SDMA_PRESERVED1_BITWIDTH-1:0]                 	sdma_preserved1_reg;
reg	[SDMA_PRESERVED2_BITWIDTH-1:0]                 	sdma_preserved2_reg;
reg	[SDMA_SDMA_CHSUM_SEL_BITWIDTH-1:0]             	sdma_sdma_chsum_sel_reg;
reg	[SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0]        	sdma_shram_stride_w_size_reg;
reg	[SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0]        	sdma_shram_stride_h_size_reg;
reg	[SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0]        	sdma_shram_stride_n_size_reg;
reg	[LDMA_SFENCE_BITWIDTH-1:0]                     	ldma_sfence_reg;
reg	[LDMA_DIRECTION_BITWIDTH-1:0]                  	ldma_direction_reg;
reg	[LDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0]             	ldma_exram_addr_lsb_reg;
reg	[LDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0]             	ldma_exram_addr_msb_reg;
reg	[LDMA_SHRAM_ADDR_BITWIDTH-1:0]                 	ldma_shram_addr_reg;
reg	[LDMA_EXRAM_C_BITWIDTH-1:0]                    	ldma_exram_c_reg;
reg	[LDMA_EXRAM_W_BITWIDTH-1:0]                    	ldma_exram_w_reg;
reg	[LDMA_EXRAM_H_BITWIDTH-1:0]                    	ldma_exram_h_reg;
reg	[LDMA_EXRAM_N_BITWIDTH-1:0]                    	ldma_exram_n_reg;
reg	[LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0]        	ldma_exram_stride_w_size_reg;
reg	[LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0]        	ldma_exram_stride_h_size_reg;
reg	[LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0]        	ldma_exram_stride_n_size_reg;
reg	[LDMA_SHRAM_C_BITWIDTH-1:0]                    	ldma_shram_c_reg;
reg	[LDMA_SHRAM_W_BITWIDTH-1:0]                    	ldma_shram_w_reg;
reg	[LDMA_SHRAM_H_BITWIDTH-1:0]                    	ldma_shram_h_reg;
reg	[LDMA_SHRAM_N_BITWIDTH-1:0]                    	ldma_shram_n_reg;
reg	[LDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0]            	ldma_shram_pad_right_reg;
reg	[LDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0]             	ldma_shram_pad_left_reg;
reg	[LDMA_SHRAM_PAD_UP_BITWIDTH-1:0]               	ldma_shram_pad_up_reg;
reg	[LDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0]             	ldma_shram_pad_down_reg;
reg	[LDMA_CONST_VALUE_BITWIDTH-1:0]                	ldma_const_value_reg;
reg	[LDMA_CH_NUM_BITWIDTH-1:0]                     	ldma_ch_num_reg;
reg	[LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH-1:0]	ldma_ldma_decomp_padding_by_pass_reg;
reg	[LDMA_RAM_PADDING_VALUE_BITWIDTH-1:0]          	ldma_ram_padding_value_reg;
reg	[LDMA_PAD_C_FRONT_BITWIDTH-1:0]                	ldma_pad_c_front_reg;
reg	[LDMA_PAD_C_BACK_BITWIDTH-1:0]                 	ldma_pad_c_back_reg;
reg	[LDMA_LDMA_CHSUM_SEL_BITWIDTH-1:0]             	ldma_ldma_chsum_sel_reg;
reg	[LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0]        	ldma_shram_stride_w_size_reg;
reg	[LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0]        	ldma_shram_stride_h_size_reg;
reg	[LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0]        	ldma_shram_stride_n_size_reg;
reg	[FME0_SFENCE_BITWIDTH-1:0]                     	fme0_sfence_reg;
reg	[FME0_MODE_BITWIDTH-1:0]                       	fme0_mode_reg;
reg	[FME0_IM_DILATED_RATE_BITWIDTH-1:0]            	fme0_im_dilated_rate_reg;
reg	[FME0_IM_PAD_BITWIDTH-1:0]                     	fme0_im_pad_reg;
reg	[FME0_IM_IW_BITWIDTH-1:0]                      	fme0_im_iw_reg;
reg	[FME0_IM_IH_BITWIDTH-1:0]                      	fme0_im_ih_reg;
reg	[FME0_IM_IC_BITWIDTH-1:0]                      	fme0_im_ic_reg;
reg	[FME0_IM_STRIDE_BITWIDTH-1:0]                  	fme0_im_stride_reg;
reg	[FME0_IM_KERNEL_BITWIDTH-1:0]                  	fme0_im_kernel_reg;
reg	[FME0_MODE_EX_BITWIDTH-1:0]                    	fme0_mode_ex_reg;
reg	[FME0_EM_IW_BITWIDTH-1:0]                      	fme0_em_iw_reg;
reg	[FME0_EM_IH_BITWIDTH-1:0]                      	fme0_em_ih_reg;
reg	[FME0_EM_IC_BITWIDTH-1:0]                      	fme0_em_ic_reg;
reg	[FME0_OM_OW_BITWIDTH-1:0]                      	fme0_om_ow_reg;
reg	[FME0_OM_OH_BITWIDTH-1:0]                      	fme0_om_oh_reg;
reg	[FME0_OM_OC_BITWIDTH-1:0]                      	fme0_om_oc_reg;
reg	[FME0_IM_ADDR_INIT_BITWIDTH-1:0]               	fme0_im_addr_init_reg;
reg	[FME0_KR_ADDR_INIT_BITWIDTH-1:0]               	fme0_kr_addr_init_reg;
reg	[FME0_BS_ADDR_INIT_BITWIDTH-1:0]               	fme0_bs_addr_init_reg;
reg	[FME0_PL_ADDR_INIT_BITWIDTH-1:0]               	fme0_pl_addr_init_reg;
reg	[FME0_EM_ADDR_INIT_BITWIDTH-1:0]               	fme0_em_addr_init_reg;
reg	[FME0_OM_ADDR_INIT_BITWIDTH-1:0]               	fme0_om_addr_init_reg;
reg	[FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1:0]          	fme0_em_alignment_iciw_reg;
reg	[FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1:0]          	fme0_om_alignment_ocow_reg;
reg	[FME0_ALIGNMENT_KCKWKH_BITWIDTH-1:0]           	fme0_alignment_kckwkh_reg;
reg	[FME0_ALIGNMENT_KCKW_BITWIDTH-1:0]             	fme0_alignment_kckw_reg;
reg	[FME0_SC_ADDR_INIT_BITWIDTH-1:0]               	fme0_sc_addr_init_reg;
reg	[FME0_SH_ADDR_INIT_BITWIDTH-1:0]               	fme0_sh_addr_init_reg;
reg	[FME0_IM_KC_BITWIDTH-1:0]                      	fme0_im_kc_reg;
reg	[LDMA2_MODE_CTRL_BITWIDTH-1:0]                 	ldma2_mode_ctrl_reg;
reg	[LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1:0]     	ldma2_roll_ic_iw_w_pad_size_reg;
reg	[LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1:0]           	ldma2_roll_ic_kw_size_reg;
reg	[LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1:0]     	ldma2_roll_kr_stride_w_size_reg;
reg	[LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1:0] 	ldma2_roll_pad_w_left_w_ic_size_reg;
reg	[LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1:0]	ldma2_roll_pad_w_right_w_ic_size_reg;
reg	[LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1:0]           	ldma2_roll_pad_h_size_reg;
reg	[CDMA_SFENCE_BITWIDTH-1:0]                     	cdma_sfence_reg;
reg	[CDMA_DIRECTION_BITWIDTH-1:0]                  	cdma_direction_reg;
reg	[CDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0]             	cdma_exram_addr_lsb_reg;
reg	[CDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0]             	cdma_exram_addr_msb_reg;
reg	[CDMA_EXRAM_C_BITWIDTH-1:0]                    	cdma_exram_c_reg;
reg	[CDMA_EXRAM_W_BITWIDTH-1:0]                    	cdma_exram_w_reg;
reg	[CDMA_EXRAM_STRIDE_W_BITWIDTH-1:0]             	cdma_exram_stride_w_reg;
// autogen_reg_stop

//}}}

//{{{ wires
// autogen_wire_nx_start
wire	[CSR_STATUS_BITWIDTH-1:0]                         csr_status_nx;
wire	[CSR_CONTROL_BITWIDTH-1:0]                        csr_control_nx;
wire	[CSR_COUNTER_LSB_BITWIDTH-1:0]                    csr_counter_lsb_nx;
wire	[CSR_COUNTER_MSB_BITWIDTH-1:0]                    csr_counter_msb_nx;
wire	[CSR_COUNTER_MASK_BITWIDTH-1:0]                   csr_counter_mask_nx;
wire	[CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH-1:0]         csr_exram_based_addr_0_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH-1:0]         csr_exram_based_addr_0_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH-1:0]         csr_exram_based_addr_1_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH-1:0]         csr_exram_based_addr_1_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH-1:0]         csr_exram_based_addr_2_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH-1:0]         csr_exram_based_addr_2_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH-1:0]         csr_exram_based_addr_3_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH-1:0]         csr_exram_based_addr_3_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH-1:0]         csr_exram_based_addr_4_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH-1:0]         csr_exram_based_addr_4_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH-1:0]         csr_exram_based_addr_5_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH-1:0]         csr_exram_based_addr_5_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH-1:0]         csr_exram_based_addr_6_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH-1:0]         csr_exram_based_addr_6_msb_nx;
wire	[CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH-1:0]         csr_exram_based_addr_7_lsb_nx;
wire	[CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH-1:0]         csr_exram_based_addr_7_msb_nx;
wire	[SDMA_SFENCE_BITWIDTH-1:0]                        sdma_sfence_nx;
wire	[SDMA_DIRECTION_BITWIDTH-1:0]                     sdma_direction_nx;
wire	[SDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0]                sdma_exram_addr_lsb_nx;
wire	[SDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0]                sdma_exram_addr_msb_nx;
wire	[SDMA_SHRAM_ADDR_BITWIDTH-1:0]                    sdma_shram_addr_nx;
wire	[SDMA_EXRAM_C_BITWIDTH-1:0]                       sdma_exram_c_nx;
wire	[SDMA_EXRAM_W_BITWIDTH-1:0]                       sdma_exram_w_nx;
wire	[SDMA_EXRAM_H_BITWIDTH-1:0]                       sdma_exram_h_nx;
wire	[SDMA_EXRAM_N_BITWIDTH-1:0]                       sdma_exram_n_nx;
wire	[SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0]           sdma_exram_stride_w_size_nx;
wire	[SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0]           sdma_exram_stride_h_size_nx;
wire	[SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0]           sdma_exram_stride_n_size_nx;
wire	[SDMA_SHRAM_C_BITWIDTH-1:0]                       sdma_shram_c_nx;
wire	[SDMA_SHRAM_W_BITWIDTH-1:0]                       sdma_shram_w_nx;
wire	[SDMA_SHRAM_H_BITWIDTH-1:0]                       sdma_shram_h_nx;
wire	[SDMA_SHRAM_N_BITWIDTH-1:0]                       sdma_shram_n_nx;
wire	[SDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0]               sdma_shram_pad_right_nx;
wire	[SDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0]                sdma_shram_pad_left_nx;
wire	[SDMA_SHRAM_PAD_UP_BITWIDTH-1:0]                  sdma_shram_pad_up_nx;
wire	[SDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0]                sdma_shram_pad_down_nx;
wire	[SDMA_CONST_VALUE_BITWIDTH-1:0]                   sdma_const_value_nx;
wire	[SDMA_CH_NUM_BITWIDTH-1:0]                        sdma_ch_num_nx;
wire	[SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH-1:0]        sdma_sdma_depadding_by_pass_nx;
wire	[SDMA_PRESERVED0_BITWIDTH-1:0]                    sdma_preserved0_nx;
wire	[SDMA_PRESERVED1_BITWIDTH-1:0]                    sdma_preserved1_nx;
wire	[SDMA_PRESERVED2_BITWIDTH-1:0]                    sdma_preserved2_nx;
wire	[SDMA_SDMA_CHSUM_SEL_BITWIDTH-1:0]                sdma_sdma_chsum_sel_nx;
wire	[SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0]           sdma_shram_stride_w_size_nx;
wire	[SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0]           sdma_shram_stride_h_size_nx;
wire	[SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0]           sdma_shram_stride_n_size_nx;
wire	[LDMA_SFENCE_BITWIDTH-1:0]                        ldma_sfence_nx;
wire	[LDMA_DIRECTION_BITWIDTH-1:0]                     ldma_direction_nx;
wire	[LDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0]                ldma_exram_addr_lsb_nx;
wire	[LDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0]                ldma_exram_addr_msb_nx;
wire	[LDMA_SHRAM_ADDR_BITWIDTH-1:0]                    ldma_shram_addr_nx;
wire	[LDMA_EXRAM_C_BITWIDTH-1:0]                       ldma_exram_c_nx;
wire	[LDMA_EXRAM_W_BITWIDTH-1:0]                       ldma_exram_w_nx;
wire	[LDMA_EXRAM_H_BITWIDTH-1:0]                       ldma_exram_h_nx;
wire	[LDMA_EXRAM_N_BITWIDTH-1:0]                       ldma_exram_n_nx;
wire	[LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0]           ldma_exram_stride_w_size_nx;
wire	[LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0]           ldma_exram_stride_h_size_nx;
wire	[LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0]           ldma_exram_stride_n_size_nx;
wire	[LDMA_SHRAM_C_BITWIDTH-1:0]                       ldma_shram_c_nx;
wire	[LDMA_SHRAM_W_BITWIDTH-1:0]                       ldma_shram_w_nx;
wire	[LDMA_SHRAM_H_BITWIDTH-1:0]                       ldma_shram_h_nx;
wire	[LDMA_SHRAM_N_BITWIDTH-1:0]                       ldma_shram_n_nx;
wire	[LDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0]               ldma_shram_pad_right_nx;
wire	[LDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0]                ldma_shram_pad_left_nx;
wire	[LDMA_SHRAM_PAD_UP_BITWIDTH-1:0]                  ldma_shram_pad_up_nx;
wire	[LDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0]                ldma_shram_pad_down_nx;
wire	[LDMA_CONST_VALUE_BITWIDTH-1:0]                   ldma_const_value_nx;
wire	[LDMA_CH_NUM_BITWIDTH-1:0]                        ldma_ch_num_nx;
wire	[LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH-1:0]   ldma_ldma_decomp_padding_by_pass_nx;
wire	[LDMA_RAM_PADDING_VALUE_BITWIDTH-1:0]             ldma_ram_padding_value_nx;
wire	[LDMA_PAD_C_FRONT_BITWIDTH-1:0]                   ldma_pad_c_front_nx;
wire	[LDMA_PAD_C_BACK_BITWIDTH-1:0]                    ldma_pad_c_back_nx;
wire	[LDMA_LDMA_CHSUM_SEL_BITWIDTH-1:0]                ldma_ldma_chsum_sel_nx;
wire	[LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0]           ldma_shram_stride_w_size_nx;
wire	[LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0]           ldma_shram_stride_h_size_nx;
wire	[LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0]           ldma_shram_stride_n_size_nx;
wire	[FME0_SFENCE_BITWIDTH-1:0]                        fme0_sfence_nx;
wire	[FME0_MODE_BITWIDTH-1:0]                          fme0_mode_nx;
wire	[FME0_IM_DILATED_RATE_BITWIDTH-1:0]               fme0_im_dilated_rate_nx;
wire	[FME0_IM_PAD_BITWIDTH-1:0]                        fme0_im_pad_nx;
wire	[FME0_IM_IW_BITWIDTH-1:0]                         fme0_im_iw_nx;
wire	[FME0_IM_IH_BITWIDTH-1:0]                         fme0_im_ih_nx;
wire	[FME0_IM_IC_BITWIDTH-1:0]                         fme0_im_ic_nx;
wire	[FME0_IM_STRIDE_BITWIDTH-1:0]                     fme0_im_stride_nx;
wire	[FME0_IM_KERNEL_BITWIDTH-1:0]                     fme0_im_kernel_nx;
wire	[FME0_MODE_EX_BITWIDTH-1:0]                       fme0_mode_ex_nx;
wire	[FME0_EM_IW_BITWIDTH-1:0]                         fme0_em_iw_nx;
wire	[FME0_EM_IH_BITWIDTH-1:0]                         fme0_em_ih_nx;
wire	[FME0_EM_IC_BITWIDTH-1:0]                         fme0_em_ic_nx;
wire	[FME0_OM_OW_BITWIDTH-1:0]                         fme0_om_ow_nx;
wire	[FME0_OM_OH_BITWIDTH-1:0]                         fme0_om_oh_nx;
wire	[FME0_OM_OC_BITWIDTH-1:0]                         fme0_om_oc_nx;
wire	[FME0_IM_ADDR_INIT_BITWIDTH-1:0]                  fme0_im_addr_init_nx;
wire	[FME0_KR_ADDR_INIT_BITWIDTH-1:0]                  fme0_kr_addr_init_nx;
wire	[FME0_BS_ADDR_INIT_BITWIDTH-1:0]                  fme0_bs_addr_init_nx;
wire	[FME0_PL_ADDR_INIT_BITWIDTH-1:0]                  fme0_pl_addr_init_nx;
wire	[FME0_EM_ADDR_INIT_BITWIDTH-1:0]                  fme0_em_addr_init_nx;
wire	[FME0_OM_ADDR_INIT_BITWIDTH-1:0]                  fme0_om_addr_init_nx;
wire	[FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1:0]             fme0_em_alignment_iciw_nx;
wire	[FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1:0]             fme0_om_alignment_ocow_nx;
wire	[FME0_ALIGNMENT_KCKWKH_BITWIDTH-1:0]              fme0_alignment_kckwkh_nx;
wire	[FME0_ALIGNMENT_KCKW_BITWIDTH-1:0]                fme0_alignment_kckw_nx;
wire	[FME0_SC_ADDR_INIT_BITWIDTH-1:0]                  fme0_sc_addr_init_nx;
wire	[FME0_SH_ADDR_INIT_BITWIDTH-1:0]                  fme0_sh_addr_init_nx;
wire	[FME0_IM_KC_BITWIDTH-1:0]                         fme0_im_kc_nx;
wire	[LDMA2_MODE_CTRL_BITWIDTH-1:0]                    ldma2_mode_ctrl_nx;
wire	[LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1:0]        ldma2_roll_ic_iw_w_pad_size_nx;
wire	[LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1:0]              ldma2_roll_ic_kw_size_nx;
wire	[LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1:0]        ldma2_roll_kr_stride_w_size_nx;
wire	[LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1:0]    ldma2_roll_pad_w_left_w_ic_size_nx;
wire	[LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1:0]   ldma2_roll_pad_w_right_w_ic_size_nx;
wire	[LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1:0]              ldma2_roll_pad_h_size_nx;
wire	[CDMA_SFENCE_BITWIDTH-1:0]                        cdma_sfence_nx;
wire	[CDMA_DIRECTION_BITWIDTH-1:0]                     cdma_direction_nx;
wire	[CDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0]                cdma_exram_addr_lsb_nx;
wire	[CDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0]                cdma_exram_addr_msb_nx;
wire	[CDMA_EXRAM_C_BITWIDTH-1:0]                       cdma_exram_c_nx;
wire	[CDMA_EXRAM_W_BITWIDTH-1:0]                       cdma_exram_w_nx;
wire	[CDMA_EXRAM_STRIDE_W_BITWIDTH-1:0]                cdma_exram_stride_w_nx;
// autogen_wire_nx_stop

wire   [ITEM_ID_NUM- 1:0]              scoreboard;
wire   wr_taken;

// autogen_wire_en_start
wire   csr_status_en;
wire   csr_control_en;
wire   csr_counter_lsb_en;
wire   csr_counter_msb_en;
wire   csr_counter_mask_en;
wire   csr_exram_based_addr_0_lsb_en;
wire   csr_exram_based_addr_0_msb_en;
wire   csr_exram_based_addr_1_lsb_en;
wire   csr_exram_based_addr_1_msb_en;
wire   csr_exram_based_addr_2_lsb_en;
wire   csr_exram_based_addr_2_msb_en;
wire   csr_exram_based_addr_3_lsb_en;
wire   csr_exram_based_addr_3_msb_en;
wire   csr_exram_based_addr_4_lsb_en;
wire   csr_exram_based_addr_4_msb_en;
wire   csr_exram_based_addr_5_lsb_en;
wire   csr_exram_based_addr_5_msb_en;
wire   csr_exram_based_addr_6_lsb_en;
wire   csr_exram_based_addr_6_msb_en;
wire   csr_exram_based_addr_7_lsb_en;
wire   csr_exram_based_addr_7_msb_en;
wire   sdma_sfence_en;
wire   sdma_direction_en;
wire   sdma_exram_addr_lsb_en;
wire   sdma_exram_addr_msb_en;
wire   sdma_shram_addr_en;
wire   sdma_exram_c_en;
wire   sdma_exram_w_en;
wire   sdma_exram_h_en;
wire   sdma_exram_n_en;
wire   sdma_exram_stride_w_size_en;
wire   sdma_exram_stride_h_size_en;
wire   sdma_exram_stride_n_size_en;
wire   sdma_shram_c_en;
wire   sdma_shram_w_en;
wire   sdma_shram_h_en;
wire   sdma_shram_n_en;
wire   sdma_shram_pad_right_en;
wire   sdma_shram_pad_left_en;
wire   sdma_shram_pad_up_en;
wire   sdma_shram_pad_down_en;
wire   sdma_const_value_en;
wire   sdma_ch_num_en;
wire   sdma_sdma_depadding_by_pass_en;
wire   sdma_preserved0_en;
wire   sdma_preserved1_en;
wire   sdma_preserved2_en;
wire   sdma_sdma_chsum_sel_en;
wire   sdma_shram_stride_w_size_en;
wire   sdma_shram_stride_h_size_en;
wire   sdma_shram_stride_n_size_en;
wire   ldma_sfence_en;
wire   ldma_direction_en;
wire   ldma_exram_addr_lsb_en;
wire   ldma_exram_addr_msb_en;
wire   ldma_shram_addr_en;
wire   ldma_exram_c_en;
wire   ldma_exram_w_en;
wire   ldma_exram_h_en;
wire   ldma_exram_n_en;
wire   ldma_exram_stride_w_size_en;
wire   ldma_exram_stride_h_size_en;
wire   ldma_exram_stride_n_size_en;
wire   ldma_shram_c_en;
wire   ldma_shram_w_en;
wire   ldma_shram_h_en;
wire   ldma_shram_n_en;
wire   ldma_shram_pad_right_en;
wire   ldma_shram_pad_left_en;
wire   ldma_shram_pad_up_en;
wire   ldma_shram_pad_down_en;
wire   ldma_const_value_en;
wire   ldma_ch_num_en;
wire   ldma_ldma_decomp_padding_by_pass_en;
wire   ldma_ram_padding_value_en;
wire   ldma_pad_c_front_en;
wire   ldma_pad_c_back_en;
wire   ldma_ldma_chsum_sel_en;
wire   ldma_shram_stride_w_size_en;
wire   ldma_shram_stride_h_size_en;
wire   ldma_shram_stride_n_size_en;
wire   fme0_sfence_en;
wire   fme0_mode_en;
wire   fme0_im_dilated_rate_en;
wire   fme0_im_pad_en;
wire   fme0_im_iw_en;
wire   fme0_im_ih_en;
wire   fme0_im_ic_en;
wire   fme0_im_stride_en;
wire   fme0_im_kernel_en;
wire   fme0_mode_ex_en;
wire   fme0_em_iw_en;
wire   fme0_em_ih_en;
wire   fme0_em_ic_en;
wire   fme0_om_ow_en;
wire   fme0_om_oh_en;
wire   fme0_om_oc_en;
wire   fme0_im_addr_init_en;
wire   fme0_kr_addr_init_en;
wire   fme0_bs_addr_init_en;
wire   fme0_pl_addr_init_en;
wire   fme0_em_addr_init_en;
wire   fme0_om_addr_init_en;
wire   fme0_em_alignment_iciw_en;
wire   fme0_om_alignment_ocow_en;
wire   fme0_alignment_kckwkh_en;
wire   fme0_alignment_kckw_en;
wire   fme0_sc_addr_init_en;
wire   fme0_sh_addr_init_en;
wire   fme0_im_kc_en;
wire   ldma2_mode_ctrl_en;
wire   ldma2_roll_ic_iw_w_pad_size_en;
wire   ldma2_roll_ic_kw_size_en;
wire   ldma2_roll_kr_stride_w_size_en;
wire   ldma2_roll_pad_w_left_w_ic_size_en;
wire   ldma2_roll_pad_w_right_w_ic_size_en;
wire   ldma2_roll_pad_h_size_en;
wire   cdma_sfence_en;
wire   cdma_direction_en;
wire   cdma_exram_addr_lsb_en;
wire   cdma_exram_addr_msb_en;
wire   cdma_exram_c_en;
wire   cdma_exram_w_en;
wire   cdma_exram_stride_w_en;
// autogen_wire_en_stop

//}}}

//{{{ FF register
// autogen_seq_start
always @(posedge clk or negedge rst_n) begin
    if(~rst_n) begin
		csr_status_reg                                            <= { {(CSR_STATUS_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_control_reg                                           <= { {(CSR_CONTROL_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_counter_lsb_reg                                       <= { {(CSR_COUNTER_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_counter_msb_reg                                       <= { {(CSR_COUNTER_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_counter_mask_reg                                      <= { {(CSR_COUNTER_MASK_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_0_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_0_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_1_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_1_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_2_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_2_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_3_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_3_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_4_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_4_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_5_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_5_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_6_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_6_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_7_lsb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		csr_exram_based_addr_7_msb_reg                            <= { {(CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_sfence_reg                                           <= { {(SDMA_SFENCE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_direction_reg                                        <= { {(SDMA_DIRECTION_BITWIDTH-1){1'd0}}, 1'b1 };
		sdma_exram_addr_lsb_reg                                   <= { {(SDMA_EXRAM_ADDR_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_addr_msb_reg                                   <= { {(SDMA_EXRAM_ADDR_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_addr_reg                                       <= { {(SDMA_SHRAM_ADDR_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_c_reg                                          <= { {(SDMA_EXRAM_C_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_w_reg                                          <= { {(SDMA_EXRAM_W_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_h_reg                                          <= { {(SDMA_EXRAM_H_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_n_reg                                          <= { {(SDMA_EXRAM_N_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_stride_w_size_reg                              <= { {(SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_stride_h_size_reg                              <= { {(SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_exram_stride_n_size_reg                              <= { {(SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_c_reg                                          <= { {(SDMA_SHRAM_C_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_w_reg                                          <= { {(SDMA_SHRAM_W_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_h_reg                                          <= { {(SDMA_SHRAM_H_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_n_reg                                          <= { {(SDMA_SHRAM_N_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_pad_right_reg                                  <= { {(SDMA_SHRAM_PAD_RIGHT_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_pad_left_reg                                   <= { {(SDMA_SHRAM_PAD_LEFT_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_pad_up_reg                                     <= { {(SDMA_SHRAM_PAD_UP_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_pad_down_reg                                   <= { {(SDMA_SHRAM_PAD_DOWN_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_const_value_reg                                      <= { {(SDMA_CONST_VALUE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_ch_num_reg                                           <= { {(SDMA_CH_NUM_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_sdma_depadding_by_pass_reg                           <= { {(SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH-1){1'd0}}, 1'b1 };
		sdma_preserved0_reg                                       <= { {(SDMA_PRESERVED0_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_preserved1_reg                                       <= { {(SDMA_PRESERVED1_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_preserved2_reg                                       <= { {(SDMA_PRESERVED2_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_sdma_chsum_sel_reg                                   <= { {(SDMA_SDMA_CHSUM_SEL_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_stride_w_size_reg                              <= { {(SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_stride_h_size_reg                              <= { {(SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		sdma_shram_stride_n_size_reg                              <= { {(SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_sfence_reg                                           <= { {(LDMA_SFENCE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_direction_reg                                        <= { {(LDMA_DIRECTION_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_addr_lsb_reg                                   <= { {(LDMA_EXRAM_ADDR_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_addr_msb_reg                                   <= { {(LDMA_EXRAM_ADDR_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_addr_reg                                       <= { {(LDMA_SHRAM_ADDR_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_c_reg                                          <= { {(LDMA_EXRAM_C_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_w_reg                                          <= { {(LDMA_EXRAM_W_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_h_reg                                          <= { {(LDMA_EXRAM_H_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_n_reg                                          <= { {(LDMA_EXRAM_N_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_stride_w_size_reg                              <= { {(LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_stride_h_size_reg                              <= { {(LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_exram_stride_n_size_reg                              <= { {(LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_c_reg                                          <= { {(LDMA_SHRAM_C_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_w_reg                                          <= { {(LDMA_SHRAM_W_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_h_reg                                          <= { {(LDMA_SHRAM_H_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_n_reg                                          <= { {(LDMA_SHRAM_N_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_pad_right_reg                                  <= { {(LDMA_SHRAM_PAD_RIGHT_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_pad_left_reg                                   <= { {(LDMA_SHRAM_PAD_LEFT_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_pad_up_reg                                     <= { {(LDMA_SHRAM_PAD_UP_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_pad_down_reg                                   <= { {(LDMA_SHRAM_PAD_DOWN_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_const_value_reg                                      <= { {(LDMA_CONST_VALUE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_ch_num_reg                                           <= { {(LDMA_CH_NUM_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_ldma_decomp_padding_by_pass_reg                      <= { {(LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH-1){1'd0}}, 1'b1 };
		ldma_ram_padding_value_reg                                <= { {(LDMA_RAM_PADDING_VALUE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_pad_c_front_reg                                      <= { {(LDMA_PAD_C_FRONT_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_pad_c_back_reg                                       <= { {(LDMA_PAD_C_BACK_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_ldma_chsum_sel_reg                                   <= { {(LDMA_LDMA_CHSUM_SEL_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_stride_w_size_reg                              <= { {(LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_stride_h_size_reg                              <= { {(LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma_shram_stride_n_size_reg                              <= { {(LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_sfence_reg                                           <= { {(FME0_SFENCE_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_mode_reg                                             <= { {(FME0_MODE_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_dilated_rate_reg                                  <= { {(FME0_IM_DILATED_RATE_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_pad_reg                                           <= { {(FME0_IM_PAD_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_iw_reg                                            <= { {(FME0_IM_IW_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_ih_reg                                            <= { {(FME0_IM_IH_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_ic_reg                                            <= { {(FME0_IM_IC_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_stride_reg                                        <= { {(FME0_IM_STRIDE_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_kernel_reg                                        <= { {(FME0_IM_KERNEL_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_mode_ex_reg                                          <= { {(FME0_MODE_EX_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_em_iw_reg                                            <= { {(FME0_EM_IW_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_em_ih_reg                                            <= { {(FME0_EM_IH_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_em_ic_reg                                            <= { {(FME0_EM_IC_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_om_ow_reg                                            <= { {(FME0_OM_OW_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_om_oh_reg                                            <= { {(FME0_OM_OH_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_om_oc_reg                                            <= { {(FME0_OM_OC_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_addr_init_reg                                     <= { {(FME0_IM_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_kr_addr_init_reg                                     <= { {(FME0_KR_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_bs_addr_init_reg                                     <= { {(FME0_BS_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_pl_addr_init_reg                                     <= { {(FME0_PL_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_em_addr_init_reg                                     <= { {(FME0_EM_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_om_addr_init_reg                                     <= { {(FME0_OM_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_em_alignment_iciw_reg                                <= { {(FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_om_alignment_ocow_reg                                <= { {(FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_alignment_kckwkh_reg                                 <= { {(FME0_ALIGNMENT_KCKWKH_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_alignment_kckw_reg                                   <= { {(FME0_ALIGNMENT_KCKW_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_sc_addr_init_reg                                     <= { {(FME0_SC_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_sh_addr_init_reg                                     <= { {(FME0_SH_ADDR_INIT_BITWIDTH-1){1'd0}}, 1'b0 };
		fme0_im_kc_reg                                            <= { {(FME0_IM_KC_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_mode_ctrl_reg                                       <= { {(LDMA2_MODE_CTRL_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_roll_ic_iw_w_pad_size_reg                           <= { {(LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_roll_ic_kw_size_reg                                 <= { {(LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_roll_kr_stride_w_size_reg                           <= { {(LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_roll_pad_w_left_w_ic_size_reg                       <= { {(LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_roll_pad_w_right_w_ic_size_reg                      <= { {(LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		ldma2_roll_pad_h_size_reg                                 <= { {(LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1){1'd0}}, 1'b0 };
		cdma_sfence_reg                                           <= { {(CDMA_SFENCE_BITWIDTH-1){1'd0}}, 1'b0 };
		cdma_direction_reg                                        <= { {(CDMA_DIRECTION_BITWIDTH-1){1'd0}}, 1'b0 };
		cdma_exram_addr_lsb_reg                                   <= { {(CDMA_EXRAM_ADDR_LSB_BITWIDTH-1){1'd0}}, 1'b0 };
		cdma_exram_addr_msb_reg                                   <= { {(CDMA_EXRAM_ADDR_MSB_BITWIDTH-1){1'd0}}, 1'b0 };
		cdma_exram_c_reg                                          <= { {(CDMA_EXRAM_C_BITWIDTH-1){1'd0}}, 1'b0 };
		cdma_exram_w_reg                                          <= { {(CDMA_EXRAM_W_BITWIDTH-1){1'd0}}, 1'b1 };
		cdma_exram_stride_w_reg                                   <= { {(CDMA_EXRAM_STRIDE_W_BITWIDTH-1){1'd0}}, 1'b0 };
    end else begin
		csr_status_reg                                  <= csr_status_nx;
		csr_control_reg                                 <= csr_control_nx;
		csr_counter_lsb_reg                             <= csr_counter_lsb_nx;
		csr_counter_msb_reg                             <= csr_counter_msb_nx;
		csr_counter_mask_reg                            <= csr_counter_mask_nx;
		csr_exram_based_addr_0_lsb_reg                  <= csr_exram_based_addr_0_lsb_nx;
		csr_exram_based_addr_0_msb_reg                  <= csr_exram_based_addr_0_msb_nx;
		csr_exram_based_addr_1_lsb_reg                  <= csr_exram_based_addr_1_lsb_nx;
		csr_exram_based_addr_1_msb_reg                  <= csr_exram_based_addr_1_msb_nx;
		csr_exram_based_addr_2_lsb_reg                  <= csr_exram_based_addr_2_lsb_nx;
		csr_exram_based_addr_2_msb_reg                  <= csr_exram_based_addr_2_msb_nx;
		csr_exram_based_addr_3_lsb_reg                  <= csr_exram_based_addr_3_lsb_nx;
		csr_exram_based_addr_3_msb_reg                  <= csr_exram_based_addr_3_msb_nx;
		csr_exram_based_addr_4_lsb_reg                  <= csr_exram_based_addr_4_lsb_nx;
		csr_exram_based_addr_4_msb_reg                  <= csr_exram_based_addr_4_msb_nx;
		csr_exram_based_addr_5_lsb_reg                  <= csr_exram_based_addr_5_lsb_nx;
		csr_exram_based_addr_5_msb_reg                  <= csr_exram_based_addr_5_msb_nx;
		csr_exram_based_addr_6_lsb_reg                  <= csr_exram_based_addr_6_lsb_nx;
		csr_exram_based_addr_6_msb_reg                  <= csr_exram_based_addr_6_msb_nx;
		csr_exram_based_addr_7_lsb_reg                  <= csr_exram_based_addr_7_lsb_nx;
		csr_exram_based_addr_7_msb_reg                  <= csr_exram_based_addr_7_msb_nx;
		sdma_sfence_reg                                 <= sdma_sfence_nx;
		sdma_direction_reg                              <= sdma_direction_nx;
		sdma_exram_addr_lsb_reg                         <= sdma_exram_addr_lsb_nx;
		sdma_exram_addr_msb_reg                         <= sdma_exram_addr_msb_nx;
		sdma_shram_addr_reg                             <= sdma_shram_addr_nx;
		sdma_exram_c_reg                                <= sdma_exram_c_nx;
		sdma_exram_w_reg                                <= sdma_exram_w_nx;
		sdma_exram_h_reg                                <= sdma_exram_h_nx;
		sdma_exram_n_reg                                <= sdma_exram_n_nx;
		sdma_exram_stride_w_size_reg                    <= sdma_exram_stride_w_size_nx;
		sdma_exram_stride_h_size_reg                    <= sdma_exram_stride_h_size_nx;
		sdma_exram_stride_n_size_reg                    <= sdma_exram_stride_n_size_nx;
		sdma_shram_c_reg                                <= sdma_shram_c_nx;
		sdma_shram_w_reg                                <= sdma_shram_w_nx;
		sdma_shram_h_reg                                <= sdma_shram_h_nx;
		sdma_shram_n_reg                                <= sdma_shram_n_nx;
		sdma_shram_pad_right_reg                        <= sdma_shram_pad_right_nx;
		sdma_shram_pad_left_reg                         <= sdma_shram_pad_left_nx;
		sdma_shram_pad_up_reg                           <= sdma_shram_pad_up_nx;
		sdma_shram_pad_down_reg                         <= sdma_shram_pad_down_nx;
		sdma_const_value_reg                            <= sdma_const_value_nx;
		sdma_ch_num_reg                                 <= sdma_ch_num_nx;
		sdma_sdma_depadding_by_pass_reg                 <= sdma_sdma_depadding_by_pass_nx;
		sdma_preserved0_reg                             <= sdma_preserved0_nx;
		sdma_preserved1_reg                             <= sdma_preserved1_nx;
		sdma_preserved2_reg                             <= sdma_preserved2_nx;
		sdma_sdma_chsum_sel_reg                         <= sdma_sdma_chsum_sel_nx;
		sdma_shram_stride_w_size_reg                    <= sdma_shram_stride_w_size_nx;
		sdma_shram_stride_h_size_reg                    <= sdma_shram_stride_h_size_nx;
		sdma_shram_stride_n_size_reg                    <= sdma_shram_stride_n_size_nx;
		ldma_sfence_reg                                 <= ldma_sfence_nx;
		ldma_direction_reg                              <= ldma_direction_nx;
		ldma_exram_addr_lsb_reg                         <= ldma_exram_addr_lsb_nx;
		ldma_exram_addr_msb_reg                         <= ldma_exram_addr_msb_nx;
		ldma_shram_addr_reg                             <= ldma_shram_addr_nx;
		ldma_exram_c_reg                                <= ldma_exram_c_nx;
		ldma_exram_w_reg                                <= ldma_exram_w_nx;
		ldma_exram_h_reg                                <= ldma_exram_h_nx;
		ldma_exram_n_reg                                <= ldma_exram_n_nx;
		ldma_exram_stride_w_size_reg                    <= ldma_exram_stride_w_size_nx;
		ldma_exram_stride_h_size_reg                    <= ldma_exram_stride_h_size_nx;
		ldma_exram_stride_n_size_reg                    <= ldma_exram_stride_n_size_nx;
		ldma_shram_c_reg                                <= ldma_shram_c_nx;
		ldma_shram_w_reg                                <= ldma_shram_w_nx;
		ldma_shram_h_reg                                <= ldma_shram_h_nx;
		ldma_shram_n_reg                                <= ldma_shram_n_nx;
		ldma_shram_pad_right_reg                        <= ldma_shram_pad_right_nx;
		ldma_shram_pad_left_reg                         <= ldma_shram_pad_left_nx;
		ldma_shram_pad_up_reg                           <= ldma_shram_pad_up_nx;
		ldma_shram_pad_down_reg                         <= ldma_shram_pad_down_nx;
		ldma_const_value_reg                            <= ldma_const_value_nx;
		ldma_ch_num_reg                                 <= ldma_ch_num_nx;
		ldma_ldma_decomp_padding_by_pass_reg            <= ldma_ldma_decomp_padding_by_pass_nx;
		ldma_ram_padding_value_reg                      <= ldma_ram_padding_value_nx;
		ldma_pad_c_front_reg                            <= ldma_pad_c_front_nx;
		ldma_pad_c_back_reg                             <= ldma_pad_c_back_nx;
		ldma_ldma_chsum_sel_reg                         <= ldma_ldma_chsum_sel_nx;
		ldma_shram_stride_w_size_reg                    <= ldma_shram_stride_w_size_nx;
		ldma_shram_stride_h_size_reg                    <= ldma_shram_stride_h_size_nx;
		ldma_shram_stride_n_size_reg                    <= ldma_shram_stride_n_size_nx;
		fme0_sfence_reg                                 <= fme0_sfence_nx;
		fme0_mode_reg                                   <= fme0_mode_nx;
		fme0_im_dilated_rate_reg                        <= fme0_im_dilated_rate_nx;
		fme0_im_pad_reg                                 <= fme0_im_pad_nx;
		fme0_im_iw_reg                                  <= fme0_im_iw_nx;
		fme0_im_ih_reg                                  <= fme0_im_ih_nx;
		fme0_im_ic_reg                                  <= fme0_im_ic_nx;
		fme0_im_stride_reg                              <= fme0_im_stride_nx;
		fme0_im_kernel_reg                              <= fme0_im_kernel_nx;
		fme0_mode_ex_reg                                <= fme0_mode_ex_nx;
		fme0_em_iw_reg                                  <= fme0_em_iw_nx;
		fme0_em_ih_reg                                  <= fme0_em_ih_nx;
		fme0_em_ic_reg                                  <= fme0_em_ic_nx;
		fme0_om_ow_reg                                  <= fme0_om_ow_nx;
		fme0_om_oh_reg                                  <= fme0_om_oh_nx;
		fme0_om_oc_reg                                  <= fme0_om_oc_nx;
		fme0_im_addr_init_reg                           <= fme0_im_addr_init_nx;
		fme0_kr_addr_init_reg                           <= fme0_kr_addr_init_nx;
		fme0_bs_addr_init_reg                           <= fme0_bs_addr_init_nx;
		fme0_pl_addr_init_reg                           <= fme0_pl_addr_init_nx;
		fme0_em_addr_init_reg                           <= fme0_em_addr_init_nx;
		fme0_om_addr_init_reg                           <= fme0_om_addr_init_nx;
		fme0_em_alignment_iciw_reg                      <= fme0_em_alignment_iciw_nx;
		fme0_om_alignment_ocow_reg                      <= fme0_om_alignment_ocow_nx;
		fme0_alignment_kckwkh_reg                       <= fme0_alignment_kckwkh_nx;
		fme0_alignment_kckw_reg                         <= fme0_alignment_kckw_nx;
		fme0_sc_addr_init_reg                           <= fme0_sc_addr_init_nx;
		fme0_sh_addr_init_reg                           <= fme0_sh_addr_init_nx;
		fme0_im_kc_reg                                  <= fme0_im_kc_nx;
		ldma2_mode_ctrl_reg                             <= ldma2_mode_ctrl_nx;
		ldma2_roll_ic_iw_w_pad_size_reg                 <= ldma2_roll_ic_iw_w_pad_size_nx;
		ldma2_roll_ic_kw_size_reg                       <= ldma2_roll_ic_kw_size_nx;
		ldma2_roll_kr_stride_w_size_reg                 <= ldma2_roll_kr_stride_w_size_nx;
		ldma2_roll_pad_w_left_w_ic_size_reg             <= ldma2_roll_pad_w_left_w_ic_size_nx;
		ldma2_roll_pad_w_right_w_ic_size_reg            <= ldma2_roll_pad_w_right_w_ic_size_nx;
		ldma2_roll_pad_h_size_reg                       <= ldma2_roll_pad_h_size_nx;
		cdma_sfence_reg                                 <= cdma_sfence_nx;
		cdma_direction_reg                              <= cdma_direction_nx;
		cdma_exram_addr_lsb_reg                         <= cdma_exram_addr_lsb_nx;
		cdma_exram_addr_msb_reg                         <= cdma_exram_addr_msb_nx;
		cdma_exram_c_reg                                <= cdma_exram_c_nx;
		cdma_exram_w_reg                                <= cdma_exram_w_nx;
		cdma_exram_stride_w_reg                         <= cdma_exram_stride_w_nx;
    end
end
// autogen_seq_stop

//}}}

//{{{ r/w enable signal
assign wr_taken                            = issue_rf_riuwe & ~issue_rf_riuwstatus;

// autogen_en_start
assign csr_status_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_STATUS_IDX});
assign csr_control_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_CONTROL_IDX});
assign csr_counter_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_COUNTER_LSB_IDX});
assign csr_counter_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_COUNTER_MSB_IDX});
assign csr_counter_mask_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_COUNTER_MASK_IDX});
assign csr_exram_based_addr_0_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_0_LSB_IDX});
assign csr_exram_based_addr_0_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_0_MSB_IDX});
assign csr_exram_based_addr_1_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_1_LSB_IDX});
assign csr_exram_based_addr_1_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_1_MSB_IDX});
assign csr_exram_based_addr_2_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_2_LSB_IDX});
assign csr_exram_based_addr_2_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_2_MSB_IDX});
assign csr_exram_based_addr_3_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_3_LSB_IDX});
assign csr_exram_based_addr_3_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_3_MSB_IDX});
assign csr_exram_based_addr_4_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_4_LSB_IDX});
assign csr_exram_based_addr_4_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_4_MSB_IDX});
assign csr_exram_based_addr_5_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_5_LSB_IDX});
assign csr_exram_based_addr_5_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_5_MSB_IDX});
assign csr_exram_based_addr_6_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_6_LSB_IDX});
assign csr_exram_based_addr_6_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_6_MSB_IDX});
assign csr_exram_based_addr_7_lsb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_7_LSB_IDX});
assign csr_exram_based_addr_7_msb_en = (issue_rf_riurwaddr == {`CSR_ID,`CSR_EXRAM_BASED_ADDR_7_MSB_IDX});
assign sdma_sfence_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SFENCE_IDX});
assign sdma_direction_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_DIRECTION_IDX});
assign sdma_exram_addr_lsb_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_ADDR_LSB_IDX});
assign sdma_exram_addr_msb_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_ADDR_MSB_IDX});
assign sdma_shram_addr_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_ADDR_IDX});
assign sdma_exram_c_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_C_IDX});
assign sdma_exram_w_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_W_IDX});
assign sdma_exram_h_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_H_IDX});
assign sdma_exram_n_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_N_IDX});
assign sdma_exram_stride_w_size_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_STRIDE_W_SIZE_IDX});
assign sdma_exram_stride_h_size_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_STRIDE_H_SIZE_IDX});
assign sdma_exram_stride_n_size_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_EXRAM_STRIDE_N_SIZE_IDX});
assign sdma_shram_c_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_C_IDX});
assign sdma_shram_w_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_W_IDX});
assign sdma_shram_h_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_H_IDX});
assign sdma_shram_n_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_N_IDX});
assign sdma_shram_pad_right_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_PAD_RIGHT_IDX});
assign sdma_shram_pad_left_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_PAD_LEFT_IDX});
assign sdma_shram_pad_up_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_PAD_UP_IDX});
assign sdma_shram_pad_down_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_PAD_DOWN_IDX});
assign sdma_const_value_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_CONST_VALUE_IDX});
assign sdma_ch_num_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_CH_NUM_IDX});
assign sdma_sdma_depadding_by_pass_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SDMA_DEPADDING_BY_PASS_IDX});
assign sdma_preserved0_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_PRESERVED0_IDX});
assign sdma_preserved1_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_PRESERVED1_IDX});
assign sdma_preserved2_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_PRESERVED2_IDX});
assign sdma_sdma_chsum_sel_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SDMA_CHSUM_SEL_IDX});
assign sdma_shram_stride_w_size_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_STRIDE_W_SIZE_IDX});
assign sdma_shram_stride_h_size_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_STRIDE_H_SIZE_IDX});
assign sdma_shram_stride_n_size_en = (issue_rf_riurwaddr == {`SDMA_ID,`SDMA_SHRAM_STRIDE_N_SIZE_IDX});
assign ldma_sfence_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SFENCE_IDX});
assign ldma_direction_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_DIRECTION_IDX});
assign ldma_exram_addr_lsb_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_ADDR_LSB_IDX});
assign ldma_exram_addr_msb_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_ADDR_MSB_IDX});
assign ldma_shram_addr_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_ADDR_IDX});
assign ldma_exram_c_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_C_IDX});
assign ldma_exram_w_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_W_IDX});
assign ldma_exram_h_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_H_IDX});
assign ldma_exram_n_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_N_IDX});
assign ldma_exram_stride_w_size_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_STRIDE_W_SIZE_IDX});
assign ldma_exram_stride_h_size_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_STRIDE_H_SIZE_IDX});
assign ldma_exram_stride_n_size_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_EXRAM_STRIDE_N_SIZE_IDX});
assign ldma_shram_c_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_C_IDX});
assign ldma_shram_w_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_W_IDX});
assign ldma_shram_h_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_H_IDX});
assign ldma_shram_n_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_N_IDX});
assign ldma_shram_pad_right_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_PAD_RIGHT_IDX});
assign ldma_shram_pad_left_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_PAD_LEFT_IDX});
assign ldma_shram_pad_up_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_PAD_UP_IDX});
assign ldma_shram_pad_down_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_PAD_DOWN_IDX});
assign ldma_const_value_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_CONST_VALUE_IDX});
assign ldma_ch_num_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_CH_NUM_IDX});
assign ldma_ldma_decomp_padding_by_pass_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_LDMA_DECOMP_PADDING_BY_PASS_IDX});
assign ldma_ram_padding_value_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_RAM_PADDING_VALUE_IDX});
assign ldma_pad_c_front_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_PAD_C_FRONT_IDX});
assign ldma_pad_c_back_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_PAD_C_BACK_IDX});
assign ldma_ldma_chsum_sel_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_LDMA_CHSUM_SEL_IDX});
assign ldma_shram_stride_w_size_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_STRIDE_W_SIZE_IDX});
assign ldma_shram_stride_h_size_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_STRIDE_H_SIZE_IDX});
assign ldma_shram_stride_n_size_en = (issue_rf_riurwaddr == {`LDMA_ID,`LDMA_SHRAM_STRIDE_N_SIZE_IDX});
assign fme0_sfence_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_SFENCE_IDX});
assign fme0_mode_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_MODE_IDX});
assign fme0_im_dilated_rate_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_DILATED_RATE_IDX});
assign fme0_im_pad_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_PAD_IDX});
assign fme0_im_iw_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_IW_IDX});
assign fme0_im_ih_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_IH_IDX});
assign fme0_im_ic_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_IC_IDX});
assign fme0_im_stride_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_STRIDE_IDX});
assign fme0_im_kernel_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_KERNEL_IDX});
assign fme0_mode_ex_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_MODE_EX_IDX});
assign fme0_em_iw_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_EM_IW_IDX});
assign fme0_em_ih_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_EM_IH_IDX});
assign fme0_em_ic_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_EM_IC_IDX});
assign fme0_om_ow_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_OM_OW_IDX});
assign fme0_om_oh_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_OM_OH_IDX});
assign fme0_om_oc_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_OM_OC_IDX});
assign fme0_im_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_ADDR_INIT_IDX});
assign fme0_kr_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_KR_ADDR_INIT_IDX});
assign fme0_bs_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_BS_ADDR_INIT_IDX});
assign fme0_pl_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_PL_ADDR_INIT_IDX});
assign fme0_em_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_EM_ADDR_INIT_IDX});
assign fme0_om_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_OM_ADDR_INIT_IDX});
assign fme0_em_alignment_iciw_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_EM_ALIGNMENT_ICIW_IDX});
assign fme0_om_alignment_ocow_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_OM_ALIGNMENT_OCOW_IDX});
assign fme0_alignment_kckwkh_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_ALIGNMENT_KCKWKH_IDX});
assign fme0_alignment_kckw_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_ALIGNMENT_KCKW_IDX});
assign fme0_sc_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_SC_ADDR_INIT_IDX});
assign fme0_sh_addr_init_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_SH_ADDR_INIT_IDX});
assign fme0_im_kc_en = (issue_rf_riurwaddr == {`FME0_ID,`FME0_IM_KC_IDX});
assign ldma2_mode_ctrl_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_MODE_CTRL_IDX});
assign ldma2_roll_ic_iw_w_pad_size_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_ROLL_IC_IW_W_PAD_SIZE_IDX});
assign ldma2_roll_ic_kw_size_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_ROLL_IC_KW_SIZE_IDX});
assign ldma2_roll_kr_stride_w_size_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_ROLL_KR_STRIDE_W_SIZE_IDX});
assign ldma2_roll_pad_w_left_w_ic_size_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_IDX});
assign ldma2_roll_pad_w_right_w_ic_size_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_IDX});
assign ldma2_roll_pad_h_size_en = (issue_rf_riurwaddr == {`LDMA2_ID,`LDMA2_ROLL_PAD_H_SIZE_IDX});
assign cdma_sfence_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_SFENCE_IDX});
assign cdma_direction_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_DIRECTION_IDX});
assign cdma_exram_addr_lsb_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_EXRAM_ADDR_LSB_IDX});
assign cdma_exram_addr_msb_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_EXRAM_ADDR_MSB_IDX});
assign cdma_exram_c_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_EXRAM_C_IDX});
assign cdma_exram_w_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_EXRAM_W_IDX});
assign cdma_exram_stride_w_en = (issue_rf_riurwaddr == {`CDMA_ID,`CDMA_EXRAM_STRIDE_W_IDX});
// autogen_en_stop

//}}}

//{{{ write regfile logic
// autogen_nx_start
assign csr_control_nx                                                                                 = (wr_taken & csr_control_en) ? issue_rf_riuwdata[CSR_CONTROL_BITWIDTH-1:0] : csr_control_reg;
assign csr_counter_lsb_nx                                                                             = (wr_taken & csr_counter_lsb_en) ? issue_rf_riuwdata[CSR_COUNTER_LSB_BITWIDTH-1:0] : csr_counter_lsb_reg;
assign csr_counter_msb_nx                                                                             = (wr_taken & csr_counter_msb_en) ? issue_rf_riuwdata[CSR_COUNTER_MSB_BITWIDTH-1:0] : csr_counter_msb_reg;
assign csr_counter_mask_nx                                                                            = (wr_taken & csr_counter_mask_en) ? issue_rf_riuwdata[CSR_COUNTER_MASK_BITWIDTH-1:0] : csr_counter_mask_reg;
assign csr_exram_based_addr_0_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_0_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH-1:0] : csr_exram_based_addr_0_lsb_reg;
assign csr_exram_based_addr_0_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_0_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH-1:0] : csr_exram_based_addr_0_msb_reg;
assign csr_exram_based_addr_1_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_1_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH-1:0] : csr_exram_based_addr_1_lsb_reg;
assign csr_exram_based_addr_1_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_1_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH-1:0] : csr_exram_based_addr_1_msb_reg;
assign csr_exram_based_addr_2_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_2_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH-1:0] : csr_exram_based_addr_2_lsb_reg;
assign csr_exram_based_addr_2_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_2_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH-1:0] : csr_exram_based_addr_2_msb_reg;
assign csr_exram_based_addr_3_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_3_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH-1:0] : csr_exram_based_addr_3_lsb_reg;
assign csr_exram_based_addr_3_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_3_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH-1:0] : csr_exram_based_addr_3_msb_reg;
assign csr_exram_based_addr_4_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_4_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH-1:0] : csr_exram_based_addr_4_lsb_reg;
assign csr_exram_based_addr_4_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_4_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH-1:0] : csr_exram_based_addr_4_msb_reg;
assign csr_exram_based_addr_5_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_5_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH-1:0] : csr_exram_based_addr_5_lsb_reg;
assign csr_exram_based_addr_5_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_5_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH-1:0] : csr_exram_based_addr_5_msb_reg;
assign csr_exram_based_addr_6_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_6_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH-1:0] : csr_exram_based_addr_6_lsb_reg;
assign csr_exram_based_addr_6_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_6_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH-1:0] : csr_exram_based_addr_6_msb_reg;
assign csr_exram_based_addr_7_lsb_nx                                                                  = (wr_taken & csr_exram_based_addr_7_lsb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH-1:0] : csr_exram_based_addr_7_lsb_reg;
assign csr_exram_based_addr_7_msb_nx                                                                  = (wr_taken & csr_exram_based_addr_7_msb_en) ? issue_rf_riuwdata[CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH-1:0] : csr_exram_based_addr_7_msb_reg;
assign sdma_sfence_nx                                                                                 = (wr_taken & sdma_sfence_en) ? issue_rf_riuwdata[SDMA_SFENCE_BITWIDTH-1:0] : sdma_sfence_reg;
assign sdma_direction_nx                                                                              = (wr_taken & sdma_direction_en) ? issue_rf_riuwdata[SDMA_DIRECTION_BITWIDTH-1:0] : sdma_direction_reg;
assign sdma_exram_addr_lsb_nx                                                                         = (wr_taken & sdma_exram_addr_lsb_en) ? issue_rf_riuwdata[SDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0] : sdma_exram_addr_lsb_reg;
assign sdma_exram_addr_msb_nx                                                                         = (wr_taken & sdma_exram_addr_msb_en) ? issue_rf_riuwdata[SDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0] : sdma_exram_addr_msb_reg;
assign sdma_shram_addr_nx                                                                             = (wr_taken & sdma_shram_addr_en) ? issue_rf_riuwdata[SDMA_SHRAM_ADDR_BITWIDTH-1:0] : sdma_shram_addr_reg;
assign sdma_exram_c_nx                                                                                = (wr_taken & sdma_exram_c_en) ? issue_rf_riuwdata[SDMA_EXRAM_C_BITWIDTH-1:0] : sdma_exram_c_reg;
assign sdma_exram_w_nx                                                                                = (wr_taken & sdma_exram_w_en) ? issue_rf_riuwdata[SDMA_EXRAM_W_BITWIDTH-1:0] : sdma_exram_w_reg;
assign sdma_exram_h_nx                                                                                = (wr_taken & sdma_exram_h_en) ? issue_rf_riuwdata[SDMA_EXRAM_H_BITWIDTH-1:0] : sdma_exram_h_reg;
assign sdma_exram_n_nx                                                                                = (wr_taken & sdma_exram_n_en) ? issue_rf_riuwdata[SDMA_EXRAM_N_BITWIDTH-1:0] : sdma_exram_n_reg;
assign sdma_exram_stride_w_size_nx                                                                    = (wr_taken & sdma_exram_stride_w_size_en) ? issue_rf_riuwdata[SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0] : sdma_exram_stride_w_size_reg;
assign sdma_exram_stride_h_size_nx                                                                    = (wr_taken & sdma_exram_stride_h_size_en) ? issue_rf_riuwdata[SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0] : sdma_exram_stride_h_size_reg;
assign sdma_exram_stride_n_size_nx                                                                    = (wr_taken & sdma_exram_stride_n_size_en) ? issue_rf_riuwdata[SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0] : sdma_exram_stride_n_size_reg;
assign sdma_shram_c_nx                                                                                = (wr_taken & sdma_shram_c_en) ? issue_rf_riuwdata[SDMA_SHRAM_C_BITWIDTH-1:0] : sdma_shram_c_reg;
assign sdma_shram_w_nx                                                                                = (wr_taken & sdma_shram_w_en) ? issue_rf_riuwdata[SDMA_SHRAM_W_BITWIDTH-1:0] : sdma_shram_w_reg;
assign sdma_shram_h_nx                                                                                = (wr_taken & sdma_shram_h_en) ? issue_rf_riuwdata[SDMA_SHRAM_H_BITWIDTH-1:0] : sdma_shram_h_reg;
assign sdma_shram_n_nx                                                                                = (wr_taken & sdma_shram_n_en) ? issue_rf_riuwdata[SDMA_SHRAM_N_BITWIDTH-1:0] : sdma_shram_n_reg;
assign sdma_shram_pad_right_nx                                                                        = (wr_taken & sdma_shram_pad_right_en) ? issue_rf_riuwdata[SDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0] : sdma_shram_pad_right_reg;
assign sdma_shram_pad_left_nx                                                                         = (wr_taken & sdma_shram_pad_left_en) ? issue_rf_riuwdata[SDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0] : sdma_shram_pad_left_reg;
assign sdma_shram_pad_up_nx                                                                           = (wr_taken & sdma_shram_pad_up_en) ? issue_rf_riuwdata[SDMA_SHRAM_PAD_UP_BITWIDTH-1:0] : sdma_shram_pad_up_reg;
assign sdma_shram_pad_down_nx                                                                         = (wr_taken & sdma_shram_pad_down_en) ? issue_rf_riuwdata[SDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0] : sdma_shram_pad_down_reg;
assign sdma_const_value_nx[SDMA_CONST_VALUE_BITWIDTH-1:SDMA_CONST_VALUE_BITWIDTH-2]                   = (wr_taken & sdma_const_value_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : sdma_const_value_reg[SDMA_CONST_VALUE_BITWIDTH-1:SDMA_CONST_VALUE_BITWIDTH-2];
assign sdma_const_value_nx[SDMA_CONST_VALUE_BITWIDTH-3:0]                                             = (wr_taken & sdma_const_value_en) ? issue_rf_riuwdata[SDMA_CONST_VALUE_BITWIDTH-3:0]: sdma_const_value_reg[SDMA_CONST_VALUE_BITWIDTH-3:0];
assign sdma_ch_num_nx                                                                                 = (wr_taken & sdma_ch_num_en) ? issue_rf_riuwdata[SDMA_CH_NUM_BITWIDTH-1:0] : sdma_ch_num_reg;
assign sdma_sdma_depadding_by_pass_nx                                                                 = (wr_taken & sdma_sdma_depadding_by_pass_en) ? issue_rf_riuwdata[SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH-1:0] : sdma_sdma_depadding_by_pass_reg;
assign sdma_preserved0_nx                                                                             = (wr_taken & sdma_preserved0_en) ? issue_rf_riuwdata[SDMA_PRESERVED0_BITWIDTH-1:0] : sdma_preserved0_reg;
assign sdma_preserved1_nx                                                                             = (wr_taken & sdma_preserved1_en) ? issue_rf_riuwdata[SDMA_PRESERVED1_BITWIDTH-1:0] : sdma_preserved1_reg;
assign sdma_preserved2_nx                                                                             = (wr_taken & sdma_preserved2_en) ? issue_rf_riuwdata[SDMA_PRESERVED2_BITWIDTH-1:0] : sdma_preserved2_reg;
assign sdma_sdma_chsum_sel_nx                                                                         = (wr_taken & sdma_sdma_chsum_sel_en) ? issue_rf_riuwdata[SDMA_SDMA_CHSUM_SEL_BITWIDTH-1:0] : sdma_sdma_chsum_sel_reg;
assign sdma_shram_stride_w_size_nx                                                                    = (wr_taken & sdma_shram_stride_w_size_en) ? issue_rf_riuwdata[SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0] : sdma_shram_stride_w_size_reg;
assign sdma_shram_stride_h_size_nx                                                                    = (wr_taken & sdma_shram_stride_h_size_en) ? issue_rf_riuwdata[SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0] : sdma_shram_stride_h_size_reg;
assign sdma_shram_stride_n_size_nx                                                                    = (wr_taken & sdma_shram_stride_n_size_en) ? issue_rf_riuwdata[SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0] : sdma_shram_stride_n_size_reg;
assign ldma_sfence_nx                                                                                 = (wr_taken & ldma_sfence_en) ? issue_rf_riuwdata[LDMA_SFENCE_BITWIDTH-1:0] : ldma_sfence_reg;
assign ldma_direction_nx                                                                              = (wr_taken & ldma_direction_en) ? issue_rf_riuwdata[LDMA_DIRECTION_BITWIDTH-1:0] : ldma_direction_reg;
assign ldma_exram_addr_lsb_nx                                                                         = (wr_taken & ldma_exram_addr_lsb_en) ? issue_rf_riuwdata[LDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0] : ldma_exram_addr_lsb_reg;
assign ldma_exram_addr_msb_nx                                                                         = (wr_taken & ldma_exram_addr_msb_en) ? issue_rf_riuwdata[LDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0] : ldma_exram_addr_msb_reg;
assign ldma_shram_addr_nx                                                                             = (wr_taken & ldma_shram_addr_en) ? issue_rf_riuwdata[LDMA_SHRAM_ADDR_BITWIDTH-1:0] : ldma_shram_addr_reg;
assign ldma_exram_c_nx                                                                                = (wr_taken & ldma_exram_c_en) ? issue_rf_riuwdata[LDMA_EXRAM_C_BITWIDTH-1:0] : ldma_exram_c_reg;
assign ldma_exram_w_nx                                                                                = (wr_taken & ldma_exram_w_en) ? issue_rf_riuwdata[LDMA_EXRAM_W_BITWIDTH-1:0] : ldma_exram_w_reg;
assign ldma_exram_h_nx                                                                                = (wr_taken & ldma_exram_h_en) ? issue_rf_riuwdata[LDMA_EXRAM_H_BITWIDTH-1:0] : ldma_exram_h_reg;
assign ldma_exram_n_nx                                                                                = (wr_taken & ldma_exram_n_en) ? issue_rf_riuwdata[LDMA_EXRAM_N_BITWIDTH-1:0] : ldma_exram_n_reg;
assign ldma_exram_stride_w_size_nx                                                                    = (wr_taken & ldma_exram_stride_w_size_en) ? issue_rf_riuwdata[LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH-1:0] : ldma_exram_stride_w_size_reg;
assign ldma_exram_stride_h_size_nx                                                                    = (wr_taken & ldma_exram_stride_h_size_en) ? issue_rf_riuwdata[LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH-1:0] : ldma_exram_stride_h_size_reg;
assign ldma_exram_stride_n_size_nx                                                                    = (wr_taken & ldma_exram_stride_n_size_en) ? issue_rf_riuwdata[LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH-1:0] : ldma_exram_stride_n_size_reg;
assign ldma_shram_c_nx                                                                                = (wr_taken & ldma_shram_c_en) ? issue_rf_riuwdata[LDMA_SHRAM_C_BITWIDTH-1:0] : ldma_shram_c_reg;
assign ldma_shram_w_nx                                                                                = (wr_taken & ldma_shram_w_en) ? issue_rf_riuwdata[LDMA_SHRAM_W_BITWIDTH-1:0] : ldma_shram_w_reg;
assign ldma_shram_h_nx                                                                                = (wr_taken & ldma_shram_h_en) ? issue_rf_riuwdata[LDMA_SHRAM_H_BITWIDTH-1:0] : ldma_shram_h_reg;
assign ldma_shram_n_nx                                                                                = (wr_taken & ldma_shram_n_en) ? issue_rf_riuwdata[LDMA_SHRAM_N_BITWIDTH-1:0] : ldma_shram_n_reg;
assign ldma_shram_pad_right_nx                                                                        = (wr_taken & ldma_shram_pad_right_en) ? issue_rf_riuwdata[LDMA_SHRAM_PAD_RIGHT_BITWIDTH-1:0] : ldma_shram_pad_right_reg;
assign ldma_shram_pad_left_nx                                                                         = (wr_taken & ldma_shram_pad_left_en) ? issue_rf_riuwdata[LDMA_SHRAM_PAD_LEFT_BITWIDTH-1:0] : ldma_shram_pad_left_reg;
assign ldma_shram_pad_up_nx                                                                           = (wr_taken & ldma_shram_pad_up_en) ? issue_rf_riuwdata[LDMA_SHRAM_PAD_UP_BITWIDTH-1:0] : ldma_shram_pad_up_reg;
assign ldma_shram_pad_down_nx                                                                         = (wr_taken & ldma_shram_pad_down_en) ? issue_rf_riuwdata[LDMA_SHRAM_PAD_DOWN_BITWIDTH-1:0] : ldma_shram_pad_down_reg;
assign ldma_const_value_nx[LDMA_CONST_VALUE_BITWIDTH-1:LDMA_CONST_VALUE_BITWIDTH-2]                   = (wr_taken & ldma_const_value_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : ldma_const_value_reg[LDMA_CONST_VALUE_BITWIDTH-1:LDMA_CONST_VALUE_BITWIDTH-2];
assign ldma_const_value_nx[LDMA_CONST_VALUE_BITWIDTH-3:0]                                             = (wr_taken & ldma_const_value_en) ? issue_rf_riuwdata[LDMA_CONST_VALUE_BITWIDTH-3:0]: ldma_const_value_reg[LDMA_CONST_VALUE_BITWIDTH-3:0];
assign ldma_ch_num_nx                                                                                 = (wr_taken & ldma_ch_num_en) ? issue_rf_riuwdata[LDMA_CH_NUM_BITWIDTH-1:0] : ldma_ch_num_reg;
assign ldma_ldma_decomp_padding_by_pass_nx                                                            = (wr_taken & ldma_ldma_decomp_padding_by_pass_en) ? issue_rf_riuwdata[LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH-1:0] : ldma_ldma_decomp_padding_by_pass_reg;
assign ldma_ram_padding_value_nx[LDMA_RAM_PADDING_VALUE_BITWIDTH-1:LDMA_RAM_PADDING_VALUE_BITWIDTH-2] = (wr_taken & ldma_ram_padding_value_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : ldma_ram_padding_value_reg[LDMA_RAM_PADDING_VALUE_BITWIDTH-1:LDMA_RAM_PADDING_VALUE_BITWIDTH-2];
assign ldma_ram_padding_value_nx[LDMA_RAM_PADDING_VALUE_BITWIDTH-3:0]                                 = (wr_taken & ldma_ram_padding_value_en) ? issue_rf_riuwdata[LDMA_RAM_PADDING_VALUE_BITWIDTH-3:0]: ldma_ram_padding_value_reg[LDMA_RAM_PADDING_VALUE_BITWIDTH-3:0];
assign ldma_pad_c_front_nx                                                                            = (wr_taken & ldma_pad_c_front_en) ? issue_rf_riuwdata[LDMA_PAD_C_FRONT_BITWIDTH-1:0] : ldma_pad_c_front_reg;
assign ldma_pad_c_back_nx                                                                             = (wr_taken & ldma_pad_c_back_en) ? issue_rf_riuwdata[LDMA_PAD_C_BACK_BITWIDTH-1:0] : ldma_pad_c_back_reg;
assign ldma_ldma_chsum_sel_nx                                                                         = (wr_taken & ldma_ldma_chsum_sel_en) ? issue_rf_riuwdata[LDMA_LDMA_CHSUM_SEL_BITWIDTH-1:0] : ldma_ldma_chsum_sel_reg;
assign ldma_shram_stride_w_size_nx                                                                    = (wr_taken & ldma_shram_stride_w_size_en) ? issue_rf_riuwdata[LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH-1:0] : ldma_shram_stride_w_size_reg;
assign ldma_shram_stride_h_size_nx                                                                    = (wr_taken & ldma_shram_stride_h_size_en) ? issue_rf_riuwdata[LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH-1:0] : ldma_shram_stride_h_size_reg;
assign ldma_shram_stride_n_size_nx                                                                    = (wr_taken & ldma_shram_stride_n_size_en) ? issue_rf_riuwdata[LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH-1:0] : ldma_shram_stride_n_size_reg;
assign fme0_sfence_nx                                                                                 = (wr_taken & fme0_sfence_en) ? issue_rf_riuwdata[FME0_SFENCE_BITWIDTH-1:0] : fme0_sfence_reg;
assign fme0_mode_nx                                                                                   = (wr_taken & fme0_mode_en) ? issue_rf_riuwdata[FME0_MODE_BITWIDTH-1:0] : fme0_mode_reg;
assign fme0_im_dilated_rate_nx                                                                        = (wr_taken & fme0_im_dilated_rate_en) ? issue_rf_riuwdata[FME0_IM_DILATED_RATE_BITWIDTH-1:0] : fme0_im_dilated_rate_reg;
assign fme0_im_pad_nx                                                                                 = (wr_taken & fme0_im_pad_en) ? issue_rf_riuwdata[FME0_IM_PAD_BITWIDTH-1:0] : fme0_im_pad_reg;
assign fme0_im_iw_nx                                                                                  = (wr_taken & fme0_im_iw_en) ? issue_rf_riuwdata[FME0_IM_IW_BITWIDTH-1:0] : fme0_im_iw_reg;
assign fme0_im_ih_nx                                                                                  = (wr_taken & fme0_im_ih_en) ? issue_rf_riuwdata[FME0_IM_IH_BITWIDTH-1:0] : fme0_im_ih_reg;
assign fme0_im_ic_nx                                                                                  = (wr_taken & fme0_im_ic_en) ? issue_rf_riuwdata[FME0_IM_IC_BITWIDTH-1:0] : fme0_im_ic_reg;
assign fme0_im_stride_nx                                                                              = (wr_taken & fme0_im_stride_en) ? issue_rf_riuwdata[FME0_IM_STRIDE_BITWIDTH-1:0] : fme0_im_stride_reg;
assign fme0_im_kernel_nx                                                                              = (wr_taken & fme0_im_kernel_en) ? issue_rf_riuwdata[FME0_IM_KERNEL_BITWIDTH-1:0] : fme0_im_kernel_reg;
assign fme0_mode_ex_nx                                                                                = (wr_taken & fme0_mode_ex_en) ? issue_rf_riuwdata[FME0_MODE_EX_BITWIDTH-1:0] : fme0_mode_ex_reg;
assign fme0_em_iw_nx                                                                                  = (wr_taken & fme0_em_iw_en) ? issue_rf_riuwdata[FME0_EM_IW_BITWIDTH-1:0] : fme0_em_iw_reg;
assign fme0_em_ih_nx                                                                                  = (wr_taken & fme0_em_ih_en) ? issue_rf_riuwdata[FME0_EM_IH_BITWIDTH-1:0] : fme0_em_ih_reg;
assign fme0_em_ic_nx                                                                                  = (wr_taken & fme0_em_ic_en) ? issue_rf_riuwdata[FME0_EM_IC_BITWIDTH-1:0] : fme0_em_ic_reg;
assign fme0_om_ow_nx                                                                                  = (wr_taken & fme0_om_ow_en) ? issue_rf_riuwdata[FME0_OM_OW_BITWIDTH-1:0] : fme0_om_ow_reg;
assign fme0_om_oh_nx                                                                                  = (wr_taken & fme0_om_oh_en) ? issue_rf_riuwdata[FME0_OM_OH_BITWIDTH-1:0] : fme0_om_oh_reg;
assign fme0_om_oc_nx                                                                                  = (wr_taken & fme0_om_oc_en) ? issue_rf_riuwdata[FME0_OM_OC_BITWIDTH-1:0] : fme0_om_oc_reg;
assign fme0_im_addr_init_nx                                                                           = (wr_taken & fme0_im_addr_init_en) ? issue_rf_riuwdata[FME0_IM_ADDR_INIT_BITWIDTH-1:0] : fme0_im_addr_init_reg;
assign fme0_kr_addr_init_nx                                                                           = (wr_taken & fme0_kr_addr_init_en) ? issue_rf_riuwdata[FME0_KR_ADDR_INIT_BITWIDTH-1:0] : fme0_kr_addr_init_reg;
assign fme0_bs_addr_init_nx                                                                           = (wr_taken & fme0_bs_addr_init_en) ? issue_rf_riuwdata[FME0_BS_ADDR_INIT_BITWIDTH-1:0] : fme0_bs_addr_init_reg;
assign fme0_pl_addr_init_nx                                                                           = (wr_taken & fme0_pl_addr_init_en) ? issue_rf_riuwdata[FME0_PL_ADDR_INIT_BITWIDTH-1:0] : fme0_pl_addr_init_reg;
assign fme0_em_addr_init_nx                                                                           = (wr_taken & fme0_em_addr_init_en) ? issue_rf_riuwdata[FME0_EM_ADDR_INIT_BITWIDTH-1:0] : fme0_em_addr_init_reg;
assign fme0_om_addr_init_nx                                                                           = (wr_taken & fme0_om_addr_init_en) ? issue_rf_riuwdata[FME0_OM_ADDR_INIT_BITWIDTH-1:0] : fme0_om_addr_init_reg;
assign fme0_em_alignment_iciw_nx                                                                      = (wr_taken & fme0_em_alignment_iciw_en) ? issue_rf_riuwdata[FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1:0] : fme0_em_alignment_iciw_reg;
assign fme0_om_alignment_ocow_nx                                                                      = (wr_taken & fme0_om_alignment_ocow_en) ? issue_rf_riuwdata[FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1:0] : fme0_om_alignment_ocow_reg;
assign fme0_alignment_kckwkh_nx                                                                       = (wr_taken & fme0_alignment_kckwkh_en) ? issue_rf_riuwdata[FME0_ALIGNMENT_KCKWKH_BITWIDTH-1:0] : fme0_alignment_kckwkh_reg;
assign fme0_alignment_kckw_nx                                                                         = (wr_taken & fme0_alignment_kckw_en) ? issue_rf_riuwdata[FME0_ALIGNMENT_KCKW_BITWIDTH-1:0] : fme0_alignment_kckw_reg;
assign fme0_sc_addr_init_nx                                                                           = (wr_taken & fme0_sc_addr_init_en) ? issue_rf_riuwdata[FME0_SC_ADDR_INIT_BITWIDTH-1:0] : fme0_sc_addr_init_reg;
assign fme0_sh_addr_init_nx                                                                           = (wr_taken & fme0_sh_addr_init_en) ? issue_rf_riuwdata[FME0_SH_ADDR_INIT_BITWIDTH-1:0] : fme0_sh_addr_init_reg;
assign fme0_im_kc_nx                                                                                  = (wr_taken & fme0_im_kc_en) ? issue_rf_riuwdata[FME0_IM_KC_BITWIDTH-1:0] : fme0_im_kc_reg;
assign ldma2_mode_ctrl_nx                                                                             = (wr_taken & ldma2_mode_ctrl_en) ? issue_rf_riuwdata[LDMA2_MODE_CTRL_BITWIDTH-1:0] : ldma2_mode_ctrl_reg;
assign ldma2_roll_ic_iw_w_pad_size_nx                                                                 = (wr_taken & ldma2_roll_ic_iw_w_pad_size_en) ? issue_rf_riuwdata[LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH-1:0] : ldma2_roll_ic_iw_w_pad_size_reg;
assign ldma2_roll_ic_kw_size_nx                                                                       = (wr_taken & ldma2_roll_ic_kw_size_en) ? issue_rf_riuwdata[LDMA2_ROLL_IC_KW_SIZE_BITWIDTH-1:0] : ldma2_roll_ic_kw_size_reg;
assign ldma2_roll_kr_stride_w_size_nx                                                                 = (wr_taken & ldma2_roll_kr_stride_w_size_en) ? issue_rf_riuwdata[LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH-1:0] : ldma2_roll_kr_stride_w_size_reg;
assign ldma2_roll_pad_w_left_w_ic_size_nx                                                             = (wr_taken & ldma2_roll_pad_w_left_w_ic_size_en) ? issue_rf_riuwdata[LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH-1:0] : ldma2_roll_pad_w_left_w_ic_size_reg;
assign ldma2_roll_pad_w_right_w_ic_size_nx                                                            = (wr_taken & ldma2_roll_pad_w_right_w_ic_size_en) ? issue_rf_riuwdata[LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH-1:0] : ldma2_roll_pad_w_right_w_ic_size_reg;
assign ldma2_roll_pad_h_size_nx                                                                       = (wr_taken & ldma2_roll_pad_h_size_en) ? issue_rf_riuwdata[LDMA2_ROLL_PAD_H_SIZE_BITWIDTH-1:0] : ldma2_roll_pad_h_size_reg;
assign cdma_sfence_nx                                                                                 = (wr_taken & cdma_sfence_en) ? issue_rf_riuwdata[CDMA_SFENCE_BITWIDTH-1:0] : cdma_sfence_reg;
assign cdma_direction_nx                                                                              = (wr_taken & cdma_direction_en) ? issue_rf_riuwdata[CDMA_DIRECTION_BITWIDTH-1:0] : cdma_direction_reg;
assign cdma_exram_addr_lsb_nx                                                                         = (wr_taken & cdma_exram_addr_lsb_en) ? issue_rf_riuwdata[CDMA_EXRAM_ADDR_LSB_BITWIDTH-1:0] : cdma_exram_addr_lsb_reg;
assign cdma_exram_addr_msb_nx                                                                         = (wr_taken & cdma_exram_addr_msb_en) ? issue_rf_riuwdata[CDMA_EXRAM_ADDR_MSB_BITWIDTH-1:0] : cdma_exram_addr_msb_reg;
assign cdma_exram_c_nx                                                                                = (wr_taken & cdma_exram_c_en) ? issue_rf_riuwdata[CDMA_EXRAM_C_BITWIDTH-1:0] : cdma_exram_c_reg;
assign cdma_exram_w_nx                                                                                = (wr_taken & cdma_exram_w_en) ? issue_rf_riuwdata[CDMA_EXRAM_W_BITWIDTH-1:0] : cdma_exram_w_reg;
assign cdma_exram_stride_w_nx                                                                         = (wr_taken & cdma_exram_stride_w_en) ? issue_rf_riuwdata[CDMA_EXRAM_STRIDE_W_BITWIDTH-1:0] : cdma_exram_stride_w_reg;
// autogen_nx_stop

//}}}

//{{{ read regfile logic
// autogen_control_start
assign issue_rf_riurdata =
				  ({RF_RDATA_BITWIDTH{(csr_status_en)}} & {{(RF_RDATA_BITWIDTH-CSR_STATUS_BITWIDTH){                                            1'b0}}, csr_status_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_control_en)}} & {{(RF_RDATA_BITWIDTH-CSR_CONTROL_BITWIDTH){                                          1'b0}}, csr_control_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_counter_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_COUNTER_LSB_BITWIDTH){                                  1'b0}}, csr_counter_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_counter_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_COUNTER_MSB_BITWIDTH){                                  1'b0}}, csr_counter_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_counter_mask_en)}} & {{(RF_RDATA_BITWIDTH-CSR_COUNTER_MASK_BITWIDTH){                                1'b0}}, csr_counter_mask_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_0_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_0_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_0_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_0_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_0_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_0_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_1_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_1_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_1_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_1_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_1_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_1_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_2_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_2_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_2_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_2_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_2_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_2_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_3_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_3_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_3_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_3_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_3_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_3_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_4_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_4_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_4_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_4_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_4_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_4_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_5_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_5_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_5_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_5_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_5_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_5_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_6_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_6_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_6_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_6_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_6_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_6_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_7_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_7_LSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_7_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(csr_exram_based_addr_7_msb_en)}} & {{(RF_RDATA_BITWIDTH-CSR_EXRAM_BASED_ADDR_7_MSB_BITWIDTH){            1'b0}}, csr_exram_based_addr_7_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_sfence_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SFENCE_BITWIDTH){                                          1'b0}}, sdma_sfence_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_direction_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_DIRECTION_BITWIDTH){                                    1'b0}}, sdma_direction_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_addr_lsb_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_ADDR_LSB_BITWIDTH){                          1'b0}}, sdma_exram_addr_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_addr_msb_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_ADDR_MSB_BITWIDTH){                          1'b0}}, sdma_exram_addr_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_addr_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_ADDR_BITWIDTH){                                  1'b0}}, sdma_shram_addr_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_c_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_C_BITWIDTH){                                        1'b0}}, sdma_exram_c_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_w_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_W_BITWIDTH){                                        1'b0}}, sdma_exram_w_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_h_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_H_BITWIDTH){                                        1'b0}}, sdma_exram_h_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_n_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_N_BITWIDTH){                                        1'b0}}, sdma_exram_n_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_stride_w_size_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH){                1'b0}}, sdma_exram_stride_w_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_stride_h_size_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH){                1'b0}}, sdma_exram_stride_h_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_exram_stride_n_size_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH){                1'b0}}, sdma_exram_stride_n_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_c_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_C_BITWIDTH){                                        1'b0}}, sdma_shram_c_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_w_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_W_BITWIDTH){                                        1'b0}}, sdma_shram_w_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_h_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_H_BITWIDTH){                                        1'b0}}, sdma_shram_h_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_n_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_N_BITWIDTH){                                        1'b0}}, sdma_shram_n_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_pad_right_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_PAD_RIGHT_BITWIDTH){                        1'b0}}, sdma_shram_pad_right_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_pad_left_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_PAD_LEFT_BITWIDTH){                          1'b0}}, sdma_shram_pad_left_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_pad_up_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_PAD_UP_BITWIDTH){                              1'b0}}, sdma_shram_pad_up_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_pad_down_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_PAD_DOWN_BITWIDTH){                          1'b0}}, sdma_shram_pad_down_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_const_value_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_CONST_VALUE_BITWIDTH){                                1'b0}}, sdma_const_value_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_ch_num_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_CH_NUM_BITWIDTH){                                          1'b0}}, sdma_ch_num_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_sdma_depadding_by_pass_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SDMA_DEPADDING_BY_PASS_BITWIDTH){          1'b0}}, sdma_sdma_depadding_by_pass_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_preserved0_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_PRESERVED0_BITWIDTH){                                  1'b0}}, sdma_preserved0_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_preserved1_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_PRESERVED1_BITWIDTH){                                  1'b0}}, sdma_preserved1_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_preserved2_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_PRESERVED2_BITWIDTH){                                  1'b0}}, sdma_preserved2_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_sdma_chsum_sel_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SDMA_CHSUM_SEL_BITWIDTH){                          1'b0}}, sdma_sdma_chsum_sel_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_stride_w_size_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH){                1'b0}}, sdma_shram_stride_w_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_stride_h_size_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH){                1'b0}}, sdma_shram_stride_h_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(sdma_shram_stride_n_size_en)}} & {{(RF_RDATA_BITWIDTH-SDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH){                1'b0}}, sdma_shram_stride_n_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_sfence_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SFENCE_BITWIDTH){                                          1'b0}}, ldma_sfence_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_direction_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_DIRECTION_BITWIDTH){                                    1'b0}}, ldma_direction_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_addr_lsb_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_ADDR_LSB_BITWIDTH){                          1'b0}}, ldma_exram_addr_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_addr_msb_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_ADDR_MSB_BITWIDTH){                          1'b0}}, ldma_exram_addr_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_addr_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_ADDR_BITWIDTH){                                  1'b0}}, ldma_shram_addr_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_c_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_C_BITWIDTH){                                        1'b0}}, ldma_exram_c_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_w_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_W_BITWIDTH){                                        1'b0}}, ldma_exram_w_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_h_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_H_BITWIDTH){                                        1'b0}}, ldma_exram_h_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_n_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_N_BITWIDTH){                                        1'b0}}, ldma_exram_n_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_stride_w_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_STRIDE_W_SIZE_BITWIDTH){                1'b0}}, ldma_exram_stride_w_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_stride_h_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_STRIDE_H_SIZE_BITWIDTH){                1'b0}}, ldma_exram_stride_h_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_exram_stride_n_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_EXRAM_STRIDE_N_SIZE_BITWIDTH){                1'b0}}, ldma_exram_stride_n_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_c_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_C_BITWIDTH){                                        1'b0}}, ldma_shram_c_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_w_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_W_BITWIDTH){                                        1'b0}}, ldma_shram_w_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_h_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_H_BITWIDTH){                                        1'b0}}, ldma_shram_h_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_n_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_N_BITWIDTH){                                        1'b0}}, ldma_shram_n_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_pad_right_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_PAD_RIGHT_BITWIDTH){                        1'b0}}, ldma_shram_pad_right_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_pad_left_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_PAD_LEFT_BITWIDTH){                          1'b0}}, ldma_shram_pad_left_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_pad_up_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_PAD_UP_BITWIDTH){                              1'b0}}, ldma_shram_pad_up_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_pad_down_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_PAD_DOWN_BITWIDTH){                          1'b0}}, ldma_shram_pad_down_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_const_value_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_CONST_VALUE_BITWIDTH){                                1'b0}}, ldma_const_value_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_ch_num_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_CH_NUM_BITWIDTH){                                          1'b0}}, ldma_ch_num_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_ldma_decomp_padding_by_pass_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_LDMA_DECOMP_PADDING_BY_PASS_BITWIDTH){1'b0}}, ldma_ldma_decomp_padding_by_pass_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_ram_padding_value_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_RAM_PADDING_VALUE_BITWIDTH){                    1'b0}}, ldma_ram_padding_value_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_pad_c_front_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_PAD_C_FRONT_BITWIDTH){                                1'b0}}, ldma_pad_c_front_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_pad_c_back_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_PAD_C_BACK_BITWIDTH){                                  1'b0}}, ldma_pad_c_back_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_ldma_chsum_sel_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_LDMA_CHSUM_SEL_BITWIDTH){                          1'b0}}, ldma_ldma_chsum_sel_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_stride_w_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_STRIDE_W_SIZE_BITWIDTH){                1'b0}}, ldma_shram_stride_w_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_stride_h_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_STRIDE_H_SIZE_BITWIDTH){                1'b0}}, ldma_shram_stride_h_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma_shram_stride_n_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA_SHRAM_STRIDE_N_SIZE_BITWIDTH){                1'b0}}, ldma_shram_stride_n_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_sfence_en)}} & {{(RF_RDATA_BITWIDTH-FME0_SFENCE_BITWIDTH){                                          1'b0}}, fme0_sfence_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_mode_en)}} & {{(RF_RDATA_BITWIDTH-FME0_MODE_BITWIDTH){                                              1'b0}}, fme0_mode_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_dilated_rate_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_DILATED_RATE_BITWIDTH){                        1'b0}}, fme0_im_dilated_rate_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_pad_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_PAD_BITWIDTH){                                          1'b0}}, fme0_im_pad_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_iw_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_IW_BITWIDTH){                                            1'b0}}, fme0_im_iw_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_ih_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_IH_BITWIDTH){                                            1'b0}}, fme0_im_ih_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_ic_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_IC_BITWIDTH){                                            1'b0}}, fme0_im_ic_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_stride_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_STRIDE_BITWIDTH){                                    1'b0}}, fme0_im_stride_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_kernel_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_KERNEL_BITWIDTH){                                    1'b0}}, fme0_im_kernel_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_mode_ex_en)}} & {{(RF_RDATA_BITWIDTH-FME0_MODE_EX_BITWIDTH){                                        1'b0}}, fme0_mode_ex_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_em_iw_en)}} & {{(RF_RDATA_BITWIDTH-FME0_EM_IW_BITWIDTH){                                            1'b0}}, fme0_em_iw_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_em_ih_en)}} & {{(RF_RDATA_BITWIDTH-FME0_EM_IH_BITWIDTH){                                            1'b0}}, fme0_em_ih_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_em_ic_en)}} & {{(RF_RDATA_BITWIDTH-FME0_EM_IC_BITWIDTH){                                            1'b0}}, fme0_em_ic_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_om_ow_en)}} & {{(RF_RDATA_BITWIDTH-FME0_OM_OW_BITWIDTH){                                            1'b0}}, fme0_om_ow_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_om_oh_en)}} & {{(RF_RDATA_BITWIDTH-FME0_OM_OH_BITWIDTH){                                            1'b0}}, fme0_om_oh_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_om_oc_en)}} & {{(RF_RDATA_BITWIDTH-FME0_OM_OC_BITWIDTH){                                            1'b0}}, fme0_om_oc_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_im_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_kr_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_KR_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_kr_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_bs_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_BS_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_bs_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_pl_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_PL_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_pl_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_em_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_EM_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_em_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_om_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_OM_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_om_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_em_alignment_iciw_en)}} & {{(RF_RDATA_BITWIDTH-FME0_EM_ALIGNMENT_ICIW_BITWIDTH){                    1'b0}}, fme0_em_alignment_iciw_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_om_alignment_ocow_en)}} & {{(RF_RDATA_BITWIDTH-FME0_OM_ALIGNMENT_OCOW_BITWIDTH){                    1'b0}}, fme0_om_alignment_ocow_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_alignment_kckwkh_en)}} & {{(RF_RDATA_BITWIDTH-FME0_ALIGNMENT_KCKWKH_BITWIDTH){                      1'b0}}, fme0_alignment_kckwkh_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_alignment_kckw_en)}} & {{(RF_RDATA_BITWIDTH-FME0_ALIGNMENT_KCKW_BITWIDTH){                          1'b0}}, fme0_alignment_kckw_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_sc_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_SC_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_sc_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_sh_addr_init_en)}} & {{(RF_RDATA_BITWIDTH-FME0_SH_ADDR_INIT_BITWIDTH){                              1'b0}}, fme0_sh_addr_init_reg}) |
				  ({RF_RDATA_BITWIDTH{(fme0_im_kc_en)}} & {{(RF_RDATA_BITWIDTH-FME0_IM_KC_BITWIDTH){                                            1'b0}}, fme0_im_kc_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_mode_ctrl_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_MODE_CTRL_BITWIDTH){                                  1'b0}}, ldma2_mode_ctrl_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_roll_ic_iw_w_pad_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_ROLL_IC_IW_W_PAD_SIZE_BITWIDTH){          1'b0}}, ldma2_roll_ic_iw_w_pad_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_roll_ic_kw_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_ROLL_IC_KW_SIZE_BITWIDTH){                      1'b0}}, ldma2_roll_ic_kw_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_roll_kr_stride_w_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_ROLL_KR_STRIDE_W_SIZE_BITWIDTH){          1'b0}}, ldma2_roll_kr_stride_w_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_roll_pad_w_left_w_ic_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE_BITWIDTH){  1'b0}}, ldma2_roll_pad_w_left_w_ic_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_roll_pad_w_right_w_ic_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE_BITWIDTH){1'b0}}, ldma2_roll_pad_w_right_w_ic_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(ldma2_roll_pad_h_size_en)}} & {{(RF_RDATA_BITWIDTH-LDMA2_ROLL_PAD_H_SIZE_BITWIDTH){                      1'b0}}, ldma2_roll_pad_h_size_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_sfence_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_SFENCE_BITWIDTH){                                          1'b0}}, cdma_sfence_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_direction_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_DIRECTION_BITWIDTH){                                    1'b0}}, cdma_direction_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_exram_addr_lsb_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_EXRAM_ADDR_LSB_BITWIDTH){                          1'b0}}, cdma_exram_addr_lsb_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_exram_addr_msb_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_EXRAM_ADDR_MSB_BITWIDTH){                          1'b0}}, cdma_exram_addr_msb_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_exram_c_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_EXRAM_C_BITWIDTH){                                        1'b0}}, cdma_exram_c_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_exram_w_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_EXRAM_W_BITWIDTH){                                        1'b0}}, cdma_exram_w_reg}) |
				  ({RF_RDATA_BITWIDTH{(cdma_exram_stride_w_en)}} & {{(RF_RDATA_BITWIDTH-CDMA_EXRAM_STRIDE_W_BITWIDTH){                          1'b0}}, cdma_exram_stride_w_reg}) |
// autogen_control_stop
1'b0 ;
//}}}

//{{{ output assign

// autogen_output_start
assign csr_exram_based_addr_0              = {csr_exram_based_addr_0_msb_reg, csr_exram_based_addr_0_lsb_reg};
assign csr_exram_based_addr_1              = {csr_exram_based_addr_1_msb_reg, csr_exram_based_addr_1_lsb_reg};
assign csr_exram_based_addr_2              = {csr_exram_based_addr_2_msb_reg, csr_exram_based_addr_2_lsb_reg};
assign csr_exram_based_addr_3              = {csr_exram_based_addr_3_msb_reg, csr_exram_based_addr_3_lsb_reg};
assign csr_exram_based_addr_4              = {csr_exram_based_addr_4_msb_reg, csr_exram_based_addr_4_lsb_reg};
assign csr_exram_based_addr_5              = {csr_exram_based_addr_5_msb_reg, csr_exram_based_addr_5_lsb_reg};
assign csr_exram_based_addr_6              = {csr_exram_based_addr_6_msb_reg, csr_exram_based_addr_6_lsb_reg};
assign csr_exram_based_addr_7              = {csr_exram_based_addr_7_msb_reg, csr_exram_based_addr_7_lsb_reg};
assign rf_sdma_direction                   = sdma_direction_reg;
assign rf_sdma_shram_addr                  = sdma_shram_addr_reg;
assign rf_sdma_exram_c                     = sdma_exram_c_reg;
assign rf_sdma_exram_w                     = sdma_exram_w_reg;
assign rf_sdma_exram_h                     = sdma_exram_h_reg;
assign rf_sdma_exram_n                     = sdma_exram_n_reg;
assign rf_sdma_exram_stride_w_size         = sdma_exram_stride_w_size_reg;
assign rf_sdma_exram_stride_h_size         = sdma_exram_stride_h_size_reg;
assign rf_sdma_exram_stride_n_size         = sdma_exram_stride_n_size_reg;
assign rf_sdma_shram_c                     = sdma_shram_c_reg;
assign rf_sdma_shram_w                     = sdma_shram_w_reg;
assign rf_sdma_shram_h                     = sdma_shram_h_reg;
assign rf_sdma_shram_n                     = sdma_shram_n_reg;
assign rf_sdma_shram_pad_right             = sdma_shram_pad_right_reg;
assign rf_sdma_shram_pad_left              = sdma_shram_pad_left_reg;
assign rf_sdma_shram_pad_up                = sdma_shram_pad_up_reg;
assign rf_sdma_shram_pad_down              = sdma_shram_pad_down_reg;
assign rf_sdma_const_value                 = sdma_const_value_reg;
assign rf_sdma_ch_num                      = sdma_ch_num_reg;
assign rf_sdma_sdma_depadding_by_pass      = sdma_sdma_depadding_by_pass_reg;
assign rf_sdma_preserved0                  = sdma_preserved0_reg;
assign rf_sdma_preserved1                  = sdma_preserved1_reg;
assign rf_sdma_preserved2                  = sdma_preserved2_reg;
assign rf_sdma_sdma_chsum_sel              = sdma_sdma_chsum_sel_reg;
assign rf_sdma_shram_stride_w_size         = sdma_shram_stride_w_size_reg;
assign rf_sdma_shram_stride_h_size         = sdma_shram_stride_h_size_reg;
assign rf_sdma_shram_stride_n_size         = sdma_shram_stride_n_size_reg;
assign rf_ldma_direction                   = ldma_direction_reg;
assign rf_ldma_shram_addr                  = ldma_shram_addr_reg;
assign rf_ldma_exram_c                     = ldma_exram_c_reg;
assign rf_ldma_exram_w                     = ldma_exram_w_reg;
assign rf_ldma_exram_h                     = ldma_exram_h_reg;
assign rf_ldma_exram_n                     = ldma_exram_n_reg;
assign rf_ldma_exram_stride_w_size         = ldma_exram_stride_w_size_reg;
assign rf_ldma_exram_stride_h_size         = ldma_exram_stride_h_size_reg;
assign rf_ldma_exram_stride_n_size         = ldma_exram_stride_n_size_reg;
assign rf_ldma_shram_c                     = ldma_shram_c_reg;
assign rf_ldma_shram_w                     = ldma_shram_w_reg;
assign rf_ldma_shram_h                     = ldma_shram_h_reg;
assign rf_ldma_shram_n                     = ldma_shram_n_reg;
assign rf_ldma_shram_pad_right             = ldma_shram_pad_right_reg;
assign rf_ldma_shram_pad_left              = ldma_shram_pad_left_reg;
assign rf_ldma_shram_pad_up                = ldma_shram_pad_up_reg;
assign rf_ldma_shram_pad_down              = ldma_shram_pad_down_reg;
assign rf_ldma_const_value                 = ldma_const_value_reg;
assign rf_ldma_ch_num                      = ldma_ch_num_reg;
assign rf_ldma_ldma_decomp_padding_by_pass = ldma_ldma_decomp_padding_by_pass_reg;
assign rf_ldma_ram_padding_value           = ldma_ram_padding_value_reg;
assign rf_ldma_pad_c_front                 = ldma_pad_c_front_reg;
assign rf_ldma_pad_c_back                  = ldma_pad_c_back_reg;
assign rf_ldma_ldma_chsum_sel              = ldma_ldma_chsum_sel_reg;
assign rf_ldma_shram_stride_w_size         = ldma_shram_stride_w_size_reg;
assign rf_ldma_shram_stride_h_size         = ldma_shram_stride_h_size_reg;
assign rf_ldma_shram_stride_n_size         = ldma_shram_stride_n_size_reg;
assign rf_fme0_mode                        = fme0_mode_reg;
assign rf_fme0_im_dilated_rate             = fme0_im_dilated_rate_reg;
assign rf_fme0_im_pad                      = fme0_im_pad_reg;
assign rf_fme0_im_iw                       = fme0_im_iw_reg;
assign rf_fme0_im_ih                       = fme0_im_ih_reg;
assign rf_fme0_im_ic                       = fme0_im_ic_reg;
assign rf_fme0_im_stride                   = fme0_im_stride_reg;
assign rf_fme0_im_kernel                   = fme0_im_kernel_reg;
assign rf_fme0_mode_ex                     = fme0_mode_ex_reg;
assign rf_fme0_em_iw                       = fme0_em_iw_reg;
assign rf_fme0_em_ih                       = fme0_em_ih_reg;
assign rf_fme0_em_ic                       = fme0_em_ic_reg;
assign rf_fme0_om_ow                       = fme0_om_ow_reg;
assign rf_fme0_om_oh                       = fme0_om_oh_reg;
assign rf_fme0_om_oc                       = fme0_om_oc_reg;
assign rf_fme0_im_addr_init                = fme0_im_addr_init_reg;
assign rf_fme0_kr_addr_init                = fme0_kr_addr_init_reg;
assign rf_fme0_bs_addr_init                = fme0_bs_addr_init_reg;
assign rf_fme0_pl_addr_init                = fme0_pl_addr_init_reg;
assign rf_fme0_em_addr_init                = fme0_em_addr_init_reg;
assign rf_fme0_om_addr_init                = fme0_om_addr_init_reg;
assign rf_fme0_em_alignment_iciw           = fme0_em_alignment_iciw_reg;
assign rf_fme0_om_alignment_ocow           = fme0_om_alignment_ocow_reg;
assign rf_fme0_alignment_kckwkh            = fme0_alignment_kckwkh_reg;
assign rf_fme0_alignment_kckw              = fme0_alignment_kckw_reg;
assign rf_fme0_sc_addr_init                = fme0_sc_addr_init_reg;
assign rf_fme0_sh_addr_init                = fme0_sh_addr_init_reg;
assign rf_fme0_im_kc                       = fme0_im_kc_reg;
assign rf_ldma2_mode_ctrl                  = ldma2_mode_ctrl_reg;
assign rf_ldma2_roll_ic_iw_w_pad_size      = ldma2_roll_ic_iw_w_pad_size_reg;
assign rf_ldma2_roll_ic_kw_size            = ldma2_roll_ic_kw_size_reg;
assign rf_ldma2_roll_kr_stride_w_size      = ldma2_roll_kr_stride_w_size_reg;
assign rf_ldma2_roll_pad_w_left_w_ic_size  = ldma2_roll_pad_w_left_w_ic_size_reg;
assign rf_ldma2_roll_pad_w_right_w_ic_size = ldma2_roll_pad_w_right_w_ic_size_reg;
assign rf_ldma2_roll_pad_h_size            = ldma2_roll_pad_h_size_reg;
assign rf_cdma_direction                   = cdma_direction_reg;
assign rf_cdma_exram_c                     = cdma_exram_c_reg;
assign rf_cdma_exram_w                     = cdma_exram_w_reg;
assign rf_cdma_exram_stride_w              = cdma_exram_stride_w_reg;
// autogen_output_stop

// autogen_sfence_start
wire sdma_start_reg_nx = wr_taken & sdma_sfence_en;
reg  sdma_start_reg;
wire sdma_start_reg_en = sdma_start_reg ^ sdma_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) sdma_start_reg <= 1'b0;
    else if (sdma_start_reg_en) sdma_start_reg <= sdma_start_reg_nx;
end
assign rf_sdma_sfence = sdma_start_reg;

wire ldma_start_reg_nx = wr_taken & ldma_sfence_en;
reg  ldma_start_reg;
wire ldma_start_reg_en = ldma_start_reg ^ ldma_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) ldma_start_reg <= 1'b0;
    else if (ldma_start_reg_en) ldma_start_reg <= ldma_start_reg_nx;
end
assign rf_ldma_sfence = ldma_start_reg;

wire fme0_start_reg_nx = wr_taken & fme0_sfence_en;
reg  fme0_start_reg;
wire fme0_start_reg_en = fme0_start_reg ^ fme0_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) fme0_start_reg <= 1'b0;
    else if (fme0_start_reg_en) fme0_start_reg <= fme0_start_reg_nx;
end
assign rf_fme0_sfence = fme0_start_reg;

wire cdma_start_reg_nx = wr_taken & cdma_sfence_en;
reg  cdma_start_reg;
wire cdma_start_reg_en = cdma_start_reg ^ cdma_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) cdma_start_reg <= 1'b0;
    else if (cdma_start_reg_en) cdma_start_reg <= cdma_start_reg_nx;
end
assign rf_cdma_sfence = cdma_start_reg;

// autogen_sfence_stop

wire [ITEM_ID_NUM-1: 0] rf_ip_sfence;
assign rf_ip_sfence = {rf_cdma_sfence, rf_ldma_sfence, 1'b0, 1'b0, rf_fme0_sfence, rf_ldma_sfence, rf_sdma_sfence, 1'b0};

// autogen_baseaddrsel_start

wire [SDMA_BASE_ADDR_SELECT_BITWIDTH-1:0] sdma_base_addr_select_nx;
assign  sdma_base_addr_select_nx           = sdma_sfence_nx[20:18];
wire sdma_base_addr_select_en           = wr_taken & sdma_sfence_en;
reg  [SDMA_BASE_ADDR_SELECT_BITWIDTH-1:0] sdma_base_addr_select_reg;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n)                        sdma_base_addr_select_reg <= {(SDMA_BASE_ADDR_SELECT_BITWIDTH){1'd0}};
    else if (sdma_base_addr_select_en) sdma_base_addr_select_reg <= sdma_base_addr_select_nx;
end
wire [3-1: 0] sdma_base_addr_select;
assign sdma_base_addr_select            = sdma_base_addr_select_reg;


wire [LDMA_BASE_ADDR_SELECT_BITWIDTH-1:0] ldma_base_addr_select_nx;
assign  ldma_base_addr_select_nx           = ldma_sfence_nx[20:18];
wire ldma_base_addr_select_en           = wr_taken & ldma_sfence_en;
reg  [LDMA_BASE_ADDR_SELECT_BITWIDTH-1:0] ldma_base_addr_select_reg;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n)                        ldma_base_addr_select_reg <= {(LDMA_BASE_ADDR_SELECT_BITWIDTH){1'd0}};
    else if (ldma_base_addr_select_en) ldma_base_addr_select_reg <= ldma_base_addr_select_nx;
end
wire [3-1: 0] ldma_base_addr_select;
assign ldma_base_addr_select            = ldma_base_addr_select_reg;


wire [CDMA_BASE_ADDR_SELECT_BITWIDTH-1:0] cdma_base_addr_select_nx;
assign  cdma_base_addr_select_nx           = cdma_sfence_nx[20:18];
wire cdma_base_addr_select_en           = wr_taken & cdma_sfence_en;
reg  [CDMA_BASE_ADDR_SELECT_BITWIDTH-1:0] cdma_base_addr_select_reg;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n)                        cdma_base_addr_select_reg <= {(CDMA_BASE_ADDR_SELECT_BITWIDTH){1'd0}};
    else if (cdma_base_addr_select_en) cdma_base_addr_select_reg <= cdma_base_addr_select_nx;
end
wire [3-1: 0] cdma_base_addr_select;
assign cdma_base_addr_select            = cdma_base_addr_select_reg;

// autogen_baseaddrsel_stop

//}}}

//{{{ scoreboard
// autogen_scoreboard_start
assign scoreboard[7]               = (ip_rf_status_clr[`CDMA_ID]) ? 1'b0 : csr_status_reg[`CDMA_ID];
assign scoreboard[6]               = (ip_rf_status_clr[`LDMA2_ID]) ? 1'b0 : csr_status_reg[`LDMA2_ID];
assign scoreboard[5]               = 1'b0;
assign scoreboard[4]               = 1'b0;
assign scoreboard[3]               = (ip_rf_status_clr[`FME0_ID]) ? 1'b0 : csr_status_reg[`FME0_ID];
assign scoreboard[2]               = (ip_rf_status_clr[`LDMA_ID]) ? 1'b0 : csr_status_reg[`LDMA_ID];
assign scoreboard[1]               = (ip_rf_status_clr[`SDMA_ID]) ? 1'b0 : csr_status_reg[`SDMA_ID];
assign scoreboard[0]               = (ip_rf_status_clr[0]) ? 1'b0 : csr_status_reg[0];
// autogen_scoreboard_stop
//}}}
wire [ITEM_ID_NUM-1:0] sfence_en = { 
// autogen_sfenceen_start
               cdma_sfence_en,
               1'b0,
               1'b0,
               1'b0,
               fme0_sfence_en,
               ldma_sfence_en,
               sdma_sfence_en,
               1'b0
// autogen_sfenceen_stop
};
//{{{ wire status register status_nx
// autogen_statusnx_start
assign csr_status_nx[`CDMA_ID]         = (wr_taken & sfence_en[`CDMA_ID]  ) ? 1'b1 : scoreboard[`CDMA_ID];
assign csr_status_nx[`LDMA2_ID]         = (wr_taken & sfence_en[`LDMA2_ID]  ) ? 1'b1 : scoreboard[`LDMA2_ID];
assign csr_status_nx[5]                = 1'b0;
assign csr_status_nx[4]                = 1'b0;
assign csr_status_nx[`FME0_ID]         = (wr_taken & sfence_en[`FME0_ID]  ) ? 1'b1 : scoreboard[`FME0_ID];
assign csr_status_nx[`LDMA_ID]         = (wr_taken & sfence_en[`LDMA_ID]  ) ? 1'b1 : scoreboard[`LDMA_ID];
assign csr_status_nx[`SDMA_ID]         = (wr_taken & sfence_en[`SDMA_ID]  ) ? 1'b1 : scoreboard[`SDMA_ID];
assign csr_status_nx[0]                = (wr_taken & sfence_en[0]  ) ? 1'b1 : scoreboard[0];
assign csr_status_nx[`CDMA_ID + 8]                = rf_cdma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`CDMA_ID + 8] : csr_status_reg[`CDMA_ID + 8];
assign csr_status_nx[`LDMA2_ID + 8]                = rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`LDMA2_ID + 8] : csr_status_reg[`LDMA2_ID + 8];
assign csr_status_nx[5 + 8]                = 1'b0;
assign csr_status_nx[4 + 8]                = 1'b0;
assign csr_status_nx[`FME0_ID + 8]                = rf_fme0_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`FME0_ID + 8] : csr_status_reg[`FME0_ID + 8];
assign csr_status_nx[`LDMA_ID + 8]                = rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`LDMA_ID + 8] : csr_status_reg[`LDMA_ID + 8];
assign csr_status_nx[`SDMA_ID + 8]                = rf_sdma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`SDMA_ID + 8] : csr_status_reg[`SDMA_ID + 8];
assign csr_status_nx[8]                           = 1'b0;
// autogen_statusnx_stop

assign csr_status_nx[18:16]            = 3'd0;
assign csr_status_nx[19]               = ~(fetch_buffer_free_entry == CDMA_DATA_BUF_DEPTH);
assign csr_status_nx[20]               = (wr_taken & csr_status_en) ? issue_rf_riuwdata[20] :
                                         (wr_taken & (|sfence_en) ) ? issue_rf_riuwdata[21] : csr_status_reg[20];
assign csr_status_nx[21]               = ~(sqr_credit == CREDIT_INIT_VALUE);
//}}}

//{{{ interrupt
// autogen_exceptwire_start
wire cdma_except        = csr_status_reg[`CDMA_ID + 8];
wire cdma_except_mask   = csr_control_reg[`CDMA_ID + 8];
wire fme0_except        = csr_status_reg[`FME0_ID + 8];
wire fme0_except_mask   = csr_control_reg[`FME0_ID + 8];
wire ldma_except        = csr_status_reg[`LDMA_ID + 8];
wire ldma_except_mask   = csr_control_reg[`LDMA_ID + 8];
wire sdma_except        = csr_status_reg[`SDMA_ID + 8];
wire sdma_except_mask   = csr_control_reg[`SDMA_ID + 8];
// autogen_exceptwire_stop
wire intr_cmd_enable    = csr_status_reg[ 20];
wire fetch_early_status = csr_status_reg[ 21];
wire intr_cmd_mask      = csr_control_reg[20];

wire intr_cmd = intr_cmd_enable & intr_cmd_mask;

wire hardware_interrupt = 1'b0 |
// autogen_interrupt_start
                          (cdma_except & cdma_except_mask) |
                          (fme0_except & fme0_except_mask) |
                          (ldma_except & ldma_except_mask) |
                          (sdma_except & sdma_except_mask) |
// autogen_interrupt_stop
                          1'b0 ;

assign rf_block_intr = (intr_cmd & ~(|scoreboard[ITEM_ID_NUM-2 : 0])) | hardware_interrupt;

//}}}

//{{{ output issue_rf_riuwstatus
// autogen_riurwaddr_start
wire riurwaddr_bit7                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `CDMA_ID);
wire riurwaddr_bit6                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `LDMA2_ID);
wire riurwaddr_bit5                      = 1'b0;
wire riurwaddr_bit4                      = 1'b0;
wire riurwaddr_bit3                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `FME0_ID);
wire riurwaddr_bit2                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `LDMA_ID);
wire riurwaddr_bit1                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `SDMA_ID);
wire riurwaddr_bit0                      = 1'b0;
// autogen_riurwaddr_stop
wire [ITEM_ID_NUM-1 :0] riurwaddr_item_onehot = { 
                                             riurwaddr_bit7,
                                             riurwaddr_bit6,
                                             riurwaddr_bit5,
                                             riurwaddr_bit4,
                                             riurwaddr_bit3,
                                             riurwaddr_bit2,
                                             riurwaddr_bit1,
                                             riurwaddr_bit0 };

wire [ITEM_ID_NUM-1:0] fence_status = {ITEM_ID_NUM{( |sfence_en )}} & issue_rf_riuwdata[ITEM_ID_NUM-1:0];

assign issue_rf_riuwstatus =  ((intr_cmd & ~(issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `CSR_ID) ) |
                               ( |(scoreboard[ITEM_ID_NUM-1:0] & riurwaddr_item_onehot) ) |
                               ( |(scoreboard[ITEM_ID_NUM-1:0] & fence_status         ) ) );
//}}}

//{{{ CDMA base_addr
wire [AXI_ADDR_WIDTH-1:0] cdma_exram_addr_tmp;
assign cdma_exram_addr_tmp = {cdma_exram_addr_msb_reg, cdma_exram_addr_lsb_reg};

base_addr # (
     .RF_BASE_ADDR_BITWIDTH        (32                           ) //(base_addr) i ()
    ,.RF_ADDR_BITWIDTH             (AXI_ADDR_WIDTH               ) //(base_addr) i ()
    ,.AXI_ADDR_BITWIDTH            (AXI_ADDR_WIDTH               ) //(base_addr) i ()
    ,.EXRAM_ADDR_RESERVED_BITWIDTH (12                           ) //(base_addr) i ()
) cdma_base_addr (
     .exram_base_addr_0            (csr_exram_based_addr_0        ) //(base_addr) i ()
    ,.exram_base_addr_1            (csr_exram_based_addr_1        ) //(base_addr) i ()
    ,.exram_base_addr_2            (csr_exram_based_addr_2        ) //(base_addr) i ()
    ,.exram_base_addr_3            (csr_exram_based_addr_3        ) //(base_addr) i ()
    ,.exram_base_addr_4            (csr_exram_based_addr_4        ) //(base_addr) i ()
    ,.exram_base_addr_5            (csr_exram_based_addr_5        ) //(base_addr) i ()
    ,.exram_base_addr_6            (csr_exram_based_addr_6        ) //(base_addr) i ()
    ,.exram_base_addr_7            (csr_exram_based_addr_7        ) //(base_addr) i ()
    ,.exram_addr                   (cdma_exram_addr_tmp          ) //(base_addr) i ()
    ,.base_addr_select             (cdma_base_addr_select        ) //(base_addr) i ()
    ,.system_bus_addr              (rf_cdma_exram_addr              ) //(base_addr) o (andla_ldma_axi_data_process, )
);
//}}}

//{{{ SDMA base_addr
wire [AXI_ADDR_WIDTH-1:0] sdma_exram_addr_tmp;
assign sdma_exram_addr_tmp = {sdma_exram_addr_msb_reg, sdma_exram_addr_lsb_reg};

base_addr # (
     .RF_BASE_ADDR_BITWIDTH        (32                           ) //(base_addr) i ()
    ,.RF_ADDR_BITWIDTH             (AXI_ADDR_WIDTH               ) //(base_addr) i ()
    ,.AXI_ADDR_BITWIDTH            (AXI_ADDR_WIDTH               ) //(base_addr) i ()
    ,.EXRAM_ADDR_RESERVED_BITWIDTH (12                           ) //(base_addr) i ()
) sdma_base_addr (
     .exram_base_addr_0            (csr_exram_based_addr_0        ) //(base_addr) i ()
    ,.exram_base_addr_1            (csr_exram_based_addr_1        ) //(base_addr) i ()
    ,.exram_base_addr_2            (csr_exram_based_addr_2        ) //(base_addr) i ()
    ,.exram_base_addr_3            (csr_exram_based_addr_3        ) //(base_addr) i ()
    ,.exram_base_addr_4            (csr_exram_based_addr_4        ) //(base_addr) i ()
    ,.exram_base_addr_5            (csr_exram_based_addr_5        ) //(base_addr) i ()
    ,.exram_base_addr_6            (csr_exram_based_addr_6        ) //(base_addr) i ()
    ,.exram_base_addr_7            (csr_exram_based_addr_7        ) //(base_addr) i ()
    ,.exram_addr                   (sdma_exram_addr_tmp          ) //(base_addr) i ()
    ,.base_addr_select             (sdma_base_addr_select        ) //(base_addr) i ()
    ,.system_bus_addr              (rf_sdma_exram_addr              ) //(base_addr) o (andla_ldma_axi_data_process, )
);
//}}}

//{{{ CDMA base_addr
wire [AXI_ADDR_WIDTH-1:0] ldma_exram_addr_tmp;
assign ldma_exram_addr_tmp = {ldma_exram_addr_msb_reg, ldma_exram_addr_lsb_reg};

base_addr # (
     .RF_BASE_ADDR_BITWIDTH        (32                           ) //(base_addr) i ()
    ,.RF_ADDR_BITWIDTH             (AXI_ADDR_WIDTH               ) //(base_addr) i ()
    ,.AXI_ADDR_BITWIDTH            (AXI_ADDR_WIDTH               ) //(base_addr) i ()
    ,.EXRAM_ADDR_RESERVED_BITWIDTH (12                           ) //(base_addr) i ()
) ldma_base_addr (
     .exram_base_addr_0            (csr_exram_based_addr_0        ) //(base_addr) i ()
    ,.exram_base_addr_1            (csr_exram_based_addr_1        ) //(base_addr) i ()
    ,.exram_base_addr_2            (csr_exram_based_addr_2        ) //(base_addr) i ()
    ,.exram_base_addr_3            (csr_exram_based_addr_3        ) //(base_addr) i ()
    ,.exram_base_addr_4            (csr_exram_based_addr_4        ) //(base_addr) i ()
    ,.exram_base_addr_5            (csr_exram_based_addr_5        ) //(base_addr) i ()
    ,.exram_base_addr_6            (csr_exram_based_addr_6        ) //(base_addr) i ()
    ,.exram_base_addr_7            (csr_exram_based_addr_7        ) //(base_addr) i ()
    ,.exram_addr                   (ldma_exram_addr_tmp          ) //(base_addr) i ()
    ,.base_addr_select             (ldma_base_addr_select        ) //(base_addr) i ()
    ,.system_bus_addr              (rf_ldma_exram_addr              ) //(base_addr) o (andla_ldma_axi_data_process, )
);
//}}}





endmodule
//}}}
