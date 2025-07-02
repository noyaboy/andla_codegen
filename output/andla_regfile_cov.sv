module andla_regfile_cov (
     input clk
    ,input rst_n
);

    covergroup FME0_reg_value @(posedge andla_regfile.fme0_sfence);
        // auto_gen_fme0 
        FME0_MODE_EXE_MODE_CP
        : coverpoint andla_regfile.fme0_mode [ 1 : 0 ] { bins b[] = { 0, 1, 2 }; }

        FME0_MODE_MM_ATTRIBUTE_CP
        : coverpoint andla_regfile.fme0_mode [ 3 : 2 ] { bins b[] = { 0, 1, 2 }; }

        FME0_MODE_EDP_ACT_CP
        : coverpoint andla_regfile.fme0_mode [ 5 : 4 ] { bins b[] = { 0, 1, 2, 3 }; }

        FME0_MODE_EDP_DST_DOMAIN_CP
        : coverpoint andla_regfile.fme0_mode [ 8 : 6 ] { bins b[] = { 1, 2 }; }

        FME0_MODE_EDP_SRC_DOMAIN_CP
        : coverpoint andla_regfile.fme0_mode [ 11 : 9 ] { bins b[] = { 1, 2 }; }

        FME0_MODE_EDP_EW_OP_CP
        : coverpoint andla_regfile.fme0_mode [ 14 : 12 ] { bins b[] = { 0, 1, 2, 4, 5 }; }

        FME0_MODE_EDP_FLOW_CP
        : coverpoint andla_regfile.fme0_mode [ 16 : 15 ] { bins b[] = { 1, 2, 3 }; }

        FME0_MODE_LOAD_MODE_CP
        : coverpoint andla_regfile.fme0_mode [ 18 : 17 ] { bins b[] = { 0, 1, 2, 3 }; }

        FME0_MODE_GEMM_DOMAIN_CP
        : coverpoint andla_regfile.fme0_mode [ 20 : 19 ] { bins b[] = { 0, 1, 2 }; }

        FME0_IM_PAD_IM_PU_CP
        : coverpoint andla_regfile.fme0_im_pad [ 2 : 0 ] { bins b[] = { 0, 1, 2, 3, 4, 5, 6, 7 }; }

        FME0_IM_PAD_IM_PD_CP
        : coverpoint andla_regfile.fme0_im_pad [ 5 : 3 ] { bins b[] = { 0, 1, 2, 3, 4, 5, 6, 7 }; }

        FME0_IM_PAD_IM_PL_CP
        : coverpoint andla_regfile.fme0_im_pad [ 8 : 6 ] { bins b[] = { 0, 1, 2, 3, 4, 5, 6, 7 }; }

        FME0_IM_PAD_IM_PR_CP
        : coverpoint andla_regfile.fme0_im_pad [ 11 : 9 ] { bins b[] = { 0, 1, 2, 3, 4, 5, 6, 7 }; }

        FME0_IM_STRIDE_IM_SW_CP
        : coverpoint andla_regfile.fme0_im_stride [ 4 : 0 ] { bins b[] = [ 0 : 31 ]; }

        FME0_IM_STRIDE_IM_SH_CP
        : coverpoint andla_regfile.fme0_im_stride [ 9 : 5 ] { bins b[] = [ 0 : 31 ]; }

        FME0_IM_STRIDE_TW_CP
        : coverpoint andla_regfile.fme0_im_stride [ 11 : 10 ] { bins b[] = { 0, 1 }; }

        FME0_IM_STRIDE_TH_CP
        : coverpoint andla_regfile.fme0_im_stride [ 13 : 12 ] { bins b[] = { 0, 1 }; }

        FME0_IM_KERNEL_IM_KW_CP
        : coverpoint andla_regfile.fme0_im_kernel [ 4 : 0 ] { bins b[] = [ 0 : 31 ]; }

        FME0_IM_KERNEL_IM_KH_CP
        : coverpoint andla_regfile.fme0_im_kernel [ 9 : 5 ] { bins b[] = [ 0 : 31 ]; }

        FME0_IM_KERNEL_IM_KWKH_CP
        : coverpoint andla_regfile.fme0_im_kernel [ 19 : 10 ] { bins b[] = [ 0 : 960 ]; }

        FME0_IM_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_im_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_KR_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_kr_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_BS_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_bs_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_PL_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_pl_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_EM_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_em_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_OM_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_om_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_SC_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_sc_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        FME0_SH_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_sh_addr_init [ 21 : 0 ] { bins b[] = [ 0 : 4194303 ]; }

        

    endgroup : FME0_reg_value

    FME0_reg_value FME0_reg_value_inst;

    function void active();
        FME0_reg_value_inst = new();
    endfunction

endmodule

bind andla_regfile andla_regfile_cov andla_regfile_cov0 (
    .clk   (clk   )
    ,.rst_n (rst_n )
);
