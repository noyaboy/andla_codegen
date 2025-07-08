`include "andla.vh"

module andla_fme0 (

clk
,rst_n
// autogen_exceptport_start
,rf_fme0_except_trigger
// autogen_exceptport_stop

// autogen_port_start
, rf_fme0_sfence
, rf_fme0_mode
, rf_fme0_im_pad
, rf_fme0_im_iw
, rf_fme0_im_ih
, rf_fme0_im_ic
, rf_fme0_im_stride
, rf_fme0_im_kernel
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
// autogen_port_stop
);

// autogen_bitwidth_start
localparam FME0_SFENCE_BITWIDTH            = `FME0_SFENCE_BITWIDTH;
localparam FME0_MODE_BITWIDTH              = `FME0_MODE_BITWIDTH;
localparam FME0_IM_PAD_BITWIDTH            = `FME0_IM_PAD_BITWIDTH;
localparam FME0_IM_IW_BITWIDTH             = `FME0_IM_IW_BITWIDTH;
localparam FME0_IM_IH_BITWIDTH             = `FME0_IM_IH_BITWIDTH;
localparam FME0_IM_IC_BITWIDTH             = `FME0_IM_IC_BITWIDTH;
localparam FME0_IM_STRIDE_BITWIDTH         = `FME0_IM_STRIDE_BITWIDTH;
localparam FME0_IM_KERNEL_BITWIDTH         = `FME0_IM_KERNEL_BITWIDTH;
localparam FME0_OM_OW_BITWIDTH             = `FME0_OM_OW_BITWIDTH;
localparam FME0_OM_OH_BITWIDTH             = `FME0_OM_OH_BITWIDTH;
localparam FME0_OM_OC_BITWIDTH             = `FME0_OM_OC_BITWIDTH;
localparam FME0_IM_ADDR_INIT_BITWIDTH      = `FME0_IM_ADDR_INIT_BITWIDTH;
localparam FME0_KR_ADDR_INIT_BITWIDTH      = `FME0_KR_ADDR_INIT_BITWIDTH;
localparam FME0_BS_ADDR_INIT_BITWIDTH      = `FME0_BS_ADDR_INIT_BITWIDTH;
localparam FME0_PL_ADDR_INIT_BITWIDTH      = `FME0_PL_ADDR_INIT_BITWIDTH;
localparam FME0_EM_ADDR_INIT_BITWIDTH      = `FME0_EM_ADDR_INIT_BITWIDTH;
localparam FME0_OM_ADDR_INIT_BITWIDTH      = `FME0_OM_ADDR_INIT_BITWIDTH;
localparam FME0_EM_ALIGNMENT_ICIW_BITWIDTH = `FME0_EM_ALIGNMENT_ICIW_BITWIDTH;
localparam FME0_OM_ALIGNMENT_OCOW_BITWIDTH = `FME0_OM_ALIGNMENT_OCOW_BITWIDTH;
localparam FME0_ALIGNMENT_KCKWKH_BITWIDTH  = `FME0_ALIGNMENT_KCKWKH_BITWIDTH;
localparam FME0_ALIGNMENT_KCKW_BITWIDTH    = `FME0_ALIGNMENT_KCKW_BITWIDTH;
localparam FME0_SC_ADDR_INIT_BITWIDTH      = `FME0_SC_ADDR_INIT_BITWIDTH;
localparam FME0_SH_ADDR_INIT_BITWIDTH      = `FME0_SH_ADDR_INIT_BITWIDTH;
// autogen_bitwidth_stop

input                                                  clk;
input                                                  rst_n;

// autogen_io_start
input	 [1-1:0] rf_fme0_sfence;
input	 [FME0_MODE_BITWIDTH-1:0] rf_fme0_mode;
input	 [FME0_IM_PAD_BITWIDTH-1:0] rf_fme0_im_pad;
input	 [FME0_IM_IW_BITWIDTH-1:0] rf_fme0_im_iw;
input	 [FME0_IM_IH_BITWIDTH-1:0] rf_fme0_im_ih;
input	 [FME0_IM_IC_BITWIDTH-1:0] rf_fme0_im_ic;
input	 [FME0_IM_STRIDE_BITWIDTH-1:0] rf_fme0_im_stride;
input	 [FME0_IM_KERNEL_BITWIDTH-1:0] rf_fme0_im_kernel;
input	 [FME0_OM_OW_BITWIDTH-1:0] rf_fme0_om_ow;
input	 [FME0_OM_OH_BITWIDTH-1:0] rf_fme0_om_oh;
input	 [FME0_OM_OC_BITWIDTH-1:0] rf_fme0_om_oc;
input	 [FME0_IM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_im_addr_init;
input	 [FME0_KR_ADDR_INIT_BITWIDTH-1:0] rf_fme0_kr_addr_init;
input	 [FME0_BS_ADDR_INIT_BITWIDTH-1:0] rf_fme0_bs_addr_init;
input	 [FME0_PL_ADDR_INIT_BITWIDTH-1:0] rf_fme0_pl_addr_init;
input	 [FME0_EM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_em_addr_init;
input	 [FME0_OM_ADDR_INIT_BITWIDTH-1:0] rf_fme0_om_addr_init;
input	 [FME0_EM_ALIGNMENT_ICIW_BITWIDTH-1:0] rf_fme0_em_alignment_iciw;
input	 [FME0_OM_ALIGNMENT_OCOW_BITWIDTH-1:0] rf_fme0_om_alignment_ocow;
input	 [FME0_ALIGNMENT_KCKWKH_BITWIDTH-1:0] rf_fme0_alignment_kckwkh;
input	 [FME0_ALIGNMENT_KCKW_BITWIDTH-1:0] rf_fme0_alignment_kckw;
input	 [FME0_SC_ADDR_INIT_BITWIDTH-1:0] rf_fme0_sc_addr_init;
input	 [FME0_SH_ADDR_INIT_BITWIDTH-1:0] rf_fme0_sh_addr_init;
// autogen_io_stop

// autogen_exceptio_start
output                 rf_fme0_except_trigger;
// autogen_exceptio_stop

endmodule
