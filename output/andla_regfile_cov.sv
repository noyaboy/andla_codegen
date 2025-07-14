module andla_regfile_cov (
     input clk
    ,input rst_n
);

    covergroup FME0_reg_value @(posedge andla_regfile.fme0_sfence);
        // auto_gen_fme0 
        FME0_IM_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_im_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_KR_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_kr_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_BS_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_bs_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_PL_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_pl_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_EM_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_em_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_OM_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_om_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_SC_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_sc_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        FME0_SH_ADDR_INIT_CP
        : coverpoint andla_regfile.fme0_sh_addr_init [21:0] { bins b[] = [ 0 : 4194303 ]; }

        

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
