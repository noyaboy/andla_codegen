module andla_regfile_cov (
     input clk
    ,input rst_n
);

    covergroup FME0_reg_value @(posedge andla_regfile.fme0_sfence);
        // auto_gen_fme0 
        

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
