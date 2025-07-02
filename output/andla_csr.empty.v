`include "andla.vh"

module andla_csr (

clk
,rst_n
// autogen_exceptport_start
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
// autogen_io_stop

// autogen_exceptio_start
// autogen_exceptio_stop

endmodule
