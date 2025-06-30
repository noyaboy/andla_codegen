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
,issue_except_trigger
,fetch_buffer_free_entry
,sqr_credit

// autogen_exceptport_start
// autogen_exceptport_stop

// autogen_baseaddrselport_start
// autogen_baseaddrselport_stop

// autogen_port_start
// autogen_port_stop
);
//}}}

//{{{ parameters
// autogen_bitwidth_start
// autogen_bitwidth_stop

// autogen_baseaddrselbitwidth_start
// autogen_baseaddrselbitwidth_stop

// autogen_ipnum_start
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
// autogen_io_stop

// autogen_baseaddrselio_start
// autogen_baseaddrselio_stop

input  [CDMA_DATA_BUF_WIDTH-                      1:0] fetch_buffer_free_entry; 
input  [CSR_CREDIT_BITWIDTH-                          1:0] sqr_credit;
input                                                  issue_except_trigger;

// autogen_exceptio_start
// autogen_exceptio_stop
//}}}

//{{{ regs
// autogen_reg_start
// autogen_reg_stop

//}}}

//{{{ wires
// autogen_wire_nx_start
// autogen_wire_nx_stop

wire   [ITEM_ID_NUM- 1:0]              scoreboard;
wire   wr_taken;

// autogen_wire_en_start
// autogen_wire_en_stop

//}}}

//{{{ FF register
// autogen_seq_start
// autogen_seq_stop

//}}}

//{{{ r/w enable signal
assign wr_taken                            = issue_rf_riuwe & ~issue_rf_riuwstatus;

// autogen_en_start
// autogen_en_stop

//}}}

//{{{ write regfile logic
// autogen_nx_start
// autogen_nx_stop

//}}}

//{{{ read regfile logic
// autogen_control_start
// autogen_control_stop
1'b0 ;
//}}}

//{{{ output assign

// autogen_output_start
// autogen_output_stop

// autogen_sfence_start
// autogen_sfence_stop

wire [ITEM_ID_NUM-1: 0] rf_ip_sfence;
assign rf_ip_sfence = {rf_cdma_sfence, rf_ldma_sfence, 1'b0, 1'b0, rf_fme0_sfence, rf_ldma_sfence, rf_sdma_sfence, 1'b0};

// autogen_baseaddrsel_start
// autogen_baseaddrsel_stop

//}}}

//{{{ scoreboard
// autogen_scoreboard_start
// autogen_scoreboard_stop
//}}}
wire [ITEM_ID_NUM-1:0] sfence_en = { 
// autogen_sfenceen_start
// autogen_sfenceen_stop
};
//{{{ wire status register status_nx
// autogen_statusnx_start
// autogen_statusnx_stop

assign csr_status_nx[18:16]            = 3'd0;
assign csr_status_nx[19]               = ~(fetch_buffer_free_entry == CDMA_DATA_BUF_DEPTH);
assign csr_status_nx[20]               = (wr_taken & csr_status_en) ? issue_rf_riuwdata[20] :
                                         (wr_taken & (|sfence_en) ) ? issue_rf_riuwdata[21] : csr_status_reg[20];
assign csr_status_nx[21]               = ~(sqr_credit == CREDIT_INIT_VALUE);
//}}}

//{{{ interrupt
// autogen_exceptwire_start
// autogen_exceptwire_stop
wire intr_cmd_enable    = csr_status_reg[ 20];
wire fetch_early_status = csr_status_reg[ 21];
wire intr_cmd_mask      = csr_control_reg[20];

wire intr_cmd = intr_cmd_enable & intr_cmd_mask;

wire hardware_interrupt = 1'b0 |
// autogen_interrupt_start
// autogen_interrupt_stop
                          1'b0 ;

assign rf_block_intr = (intr_cmd & ~(|scoreboard[ITEM_ID_NUM-2 : 0])) | hardware_interrupt;

//}}}

//{{{ output issue_rf_riuwstatus
// autogen_riurwaddr_start
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
     .exram_base_addr_0            (rf_csr_exram_based_addr_0        ) //(base_addr) i ()
    ,.exram_base_addr_1            (rf_csr_exram_based_addr_1        ) //(base_addr) i ()
    ,.exram_base_addr_2            (rf_csr_exram_based_addr_2        ) //(base_addr) i ()
    ,.exram_base_addr_3            (rf_csr_exram_based_addr_3        ) //(base_addr) i ()
    ,.exram_base_addr_4            (rf_csr_exram_based_addr_4        ) //(base_addr) i ()
    ,.exram_base_addr_5            (rf_csr_exram_based_addr_5        ) //(base_addr) i ()
    ,.exram_base_addr_6            (rf_csr_exram_based_addr_6        ) //(base_addr) i ()
    ,.exram_base_addr_7            (rf_csr_exram_based_addr_7        ) //(base_addr) i ()
    ,.exram_addr                   (cdma_exram_addr_tmp          ) //(base_addr) i ()
    ,.base_addr_select             (cdma_base_addr_select        ) //(base_addr) i ()
    ,.system_bus_addr              (rf_cdma_exram_addr              ) //(base_addr) o (andla_ldma_axi_data_process, )
);
//}}}

endmodule
//}}}
