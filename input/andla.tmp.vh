`ifndef ANDLA_VH
`define ANDLA_VH

`include "andla_config.vh"

`ifdef AE350_CONFIG_VH
    `include "config.inc"
    `ifdef ANDLA_BUS_AXI
        `define ANDLA_AXI_SLVID_WIDTH      (`AE350_AXI_ID_WIDTH + 4)
        `define ANDLA_AXI_MSTID_WIDTH      (`AE350_AXI_ID_WIDTH + 0)
        `define ANDLA_AXI_DATA_WIDTH        `NDS_BIU_DATA_WIDTH
        `define ANDLA_DMA_FIFO_DEPTH                         8
        `define ANDLA_AHB_DATA_WIDTH     `NDS_BIU_DATA_WIDTH
        `define ANDLA_AHB_ADDR_WIDTH     `NDS_BIU_ADDR_WIDTH
        `ifdef PLATFORM_FORCE_4GB_SPACE
            `define ANDLA_AXI_ADDR_WIDTH                             32
        `else
            `define ANDLA_AXI_ADDR_WIDTH    `NDS_BIU_ADDR_WIDTH
        `endif // PLATFORM_FORCE_4GB_SPACE
    `else // NDS_IO_AHB
        `define ANDLA_AXI_SLVID_WIDTH      8
        `define ANDLA_AXI_MSTID_WIDTH      8
        `define ANDLA_DMA_FIFO_DEPTH       8
        `ifdef PLATFORM_FORCE_4GB_SPACE 
            `define ANDLA_AXI_ADDR_WIDTH       32
        `else
            `define ANDLA_AXI_ADDR_WIDTH       32
        `endif // PLATFORM_FORCE_4GB_SPACE
        `define ANDLA_AXI_DATA_WIDTH     64
        `define ANDLA_AHB_DATA_WIDTH     `NDS_BIU_DATA_WIDTH
		`ifndef NDS_BIU_ADDR_WIDTH // For Chiuhuahua environment
        	`define ANDLA_AHB_ADDR_WIDTH     32 //`NDS_BIU_ADDR_WIDTH
		`else
        	`define ANDLA_AHB_ADDR_WIDTH     `NDS_BIU_ADDR_WIDTH
        `endif
    `endif
`else
        `define ANDLA_AXI_SLVID_WIDTH                            8
        `define ANDLA_AXI_MSTID_WIDTH                            4
        `define ANDLA_AXI_DATA_WIDTH                            `ANDLA_BLK_BIU_DATA_WIDTH
        `define ANDLA_DMA_FIFO_DEPTH                         8
        `define ANDLA_AXI_ADDR_WIDTH                            `ANDLA_BIU_ADDR_WIDTH
        `define ANDLA_AHB_DATA_WIDTH     `ANDLA_BLK_BIU_DATA_WIDTH
        `define ANDLA_AHB_ADDR_WIDTH     `ANDLA_BIU_ADDR_WIDTH
`endif // AE350_CONFIG

`define ITEM_ID_NUM                     8

`define ANDLA_MAX_PW                    4
`define ANDLA_MAX_PH                    2
`define ANDLA_DLA_OUTSTANDING_DEPTH     4  // defualt 4
`define ANDLA_DLA_SLV_OUTSTANDING_DEPTH     1 
`define ANDLA_DLA_KERNEL_SIZE_BITWIDTH  4  // defualt 15
`define ANDLA_DLA_IMAGE_SIZE_BITWIDTH   10 // defualt 1023
`define ANDLA_DLA_DATA_BITWIDTH         64 // defualt 8
`define ANDLA_DLA_CACC_DATA_BITWIDTH    40 // defualt 40b
`define ANDLA_DLA_BS_DATA_BITWIDTH      32 // defualt 32b
`define ANDLA_DLA_SC_DATA_BITWIDTH      32 // default 32b
`define ANDLA_DLA_TC_DATA_BITWIDTH      32 // defualt 32b

`define ANDLA_IBMC_OUTSTANDING_DEPTH    2
`define ANDLA_MST_NUM                   6
`define ANDLA_MST_NUM_BITWIDTH          3

//LDMA AR/R SETTING
`define ANDLA_LDMA_AR_PENDING_EN  0
`define ANDLA_LDMA_AR_PIPELINE_EN 1
`define ANDLA_LDMA_R_PENDING_EN   1
`define ANDLA_LDMA_R_PIPELINE_EN  1
//LDMA RAM A SETTING
`define ANDLA_LDMA_RAM_ENG_PENDING_EN  1
`define ANDLA_LDMA_RAM_ENG_PIPELINE_EN 0
`define ANDLA_LDMA_RAM_ENG_D_PENDING_EN  1
`define ANDLA_LDMA_RAM_ENG_D_PIPELINE_EN 1
//SDMA AW/W/B SETTING
`define ANDLA_SDMA_AW_PENDING_EN  0
`define ANDLA_SDMA_AW_PIPELINE_EN 1
`define ANDLA_SDMA_W_PENDING_EN   0
`define ANDLA_SDMA_W_PIPELINE_EN  1
`define ANDLA_SDMA_B_PENDING_EN   0
`define ANDLA_SDMA_B_PIPELINE_EN  0

//DMA DATA BUF
`define ANDLA_DMA_SRAM_BUF_EN 1

//`define ANDLA_CDMA_SRAM_BUF_EN `ANDLA_DMA_SRAM_BUF_EN
`define ANDLA_SDMA_SRAM_BUF_EN `ANDLA_DMA_SRAM_BUF_EN
`define ANDLA_LDMA_SRAM_BUF_EN `ANDLA_DMA_SRAM_BUF_EN

`define ITEMID2BASE(x)  ((x << 5) + `ANDLA_REG_BASE

`define ANDLA_SQR_CDMA_FIFO_DEPTH             8
`define ANDLA_SQR_OUTSTANDING_FIFO_DEPTH      2
`define ANDLA_SQR_OUTSTANDING_BUF_DEPTH       2

`define ANDLA_MEM_BASE_ADDRESS                  `ANDLA_AXI_ADDR_WIDTH'hd000_0000
`define ANDLA_REG_BASE_ADDRESS                  `ANDLA_AXI_ADDR_WIDTH'hde00_0000
`define ANDLA_END_ADDRESS                       `ANDLA_AXI_ADDR_WIDTH'hde00_03ff

`define ANDLA_SQR_CREDIT_BITWIDTH             $clog2(`ANDLA_FETCH_FIFO_DEPTH) + 1
`define ANDLA_SQR_INIT_VALUE                  `ANDLA_SQR_CREDIT_BITWIDTH + 2

`define ANDLA_DISP_FIFO_DEPTH                 1024
`define ANDLA_CMD_BITWIDTH                    32
`define ANDLA_RF_WDATA_BITWIDTH               22
`define ANDLA_RF_RDATA_BITWIDTH               32
`define ANDLA_RF_ADDR_BITWIDTH                8
`define ANDLA_RF_ID_BITWIDTH                  3
`define ANDLA_RF_INDEX_BITWIDTH               5

`define ROR_REG_REVISION_PHY_ADDR        `ANDLA_ROR_BASE_ADDRESS + {{(`ANDLA_AXI_ADDR_WIDTH-`ANDLA_RF_INDEX_BITWIDTH-2){1'd0}},(`ANDLA_RF_INDEX_BITWIDTH'd0 << 2)}
`define ROR_REG_ID_PHY_ADDR              `ANDLA_ROR_BASE_ADDRESS + {{(`ANDLA_AXI_ADDR_WIDTH-`ANDLA_RF_INDEX_BITWIDTH-2){1'd0}},(`ANDLA_RF_INDEX_BITWIDTH'd1 << 2)}
`define ROR_REG_STATUS_PHY_ADDR          `ANDLA_ROR_BASE_ADDRESS + {{(`ANDLA_AXI_ADDR_WIDTH-`ANDLA_RF_INDEX_BITWIDTH-2){1'd0}},(`ANDLA_RF_INDEX_BITWIDTH'd2 << 2)}

// autogen_itemid_start
// autogen_itemid_stop

`define GEMM_ID                            `ANDLA_RF_ID_BITWIDTH'd5
`define EDP_ID                             `ANDLA_RF_ID_BITWIDTH'd4

`define ANDLA_RF_DDMA_C_SIZE_BITWIDTH           32
`define ANDLA_RF_DDMA_W_SIZE_BITWIDTH           16
`define ANDLA_RF_DDMA_H_SIZE_BITWIDTH           16
`define ANDLA_RF_DDMA_N_SIZE_BITWIDTH           16
`define ANDLA_RF_DDMA_STRIDE_BITWIDTH           32
`define ANDLA_RF_DDMA_PAD_BITWIDTH              4
`define ANDLA_RF_STATUS_BITWIDTH                22
`define ANDLA_RF_CONTROL_BITWIDTH               22
`define ANDLA_RF_CONST_VALUE_BITWIDTH           9

// autogen_provide_common_h_start
`define MODE_BITWIDTH               22
`define CONST_VALUE_BITWIDTH        18
`define RAM_PADDING_VALUE_BITWIDTH  18
`define DILATED_RATE_BITWIDTH       3
`define PAD_SIZE_BITWIDTH           3
`define IM_SIZE_BITWIDTH            14
`define IC_SIZE_BITWIDTH            14
`define KR_SIZE_BITWIDTH            5
// autogen_provide_common_h_stop

`define KC_SIZE_BITWIDTH 14
`define OCBYTE_SIZE_BITWIDTH 14
`define UBMC_ADDR_BITWIDTH `ANDLA_IBMC_ADDR_BITWIDTH

// autogen_bitwidth_start
// autogen_bitwidth_stop

// autogen_idx_start
// autogen_idx_stop


`ifdef ANDLA_4M_SHRAM
    `define ANDLA_DLA_CHANNEL_SIZE_BITWIDTH `ANDLA_IBMC_ADDR_BITWIDTH
    `define LDMA_EXRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH
    `define LDMA_SHRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH
    `define LDMA_CH_NUM_BITWIDTH            `UBMC_ADDR_BITWIDTH
    `define SDMA_EXRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH
    `define SDMA_SHRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH
    `define SDMA_CH_NUM_BITWIDTH            `UBMC_ADDR_BITWIDTH
`else
    `define ANDLA_DLA_CHANNEL_SIZE_BITWIDTH `ANDLA_IBMC_ADDR_BITWIDTH+1
    `define LDMA_EXRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH+1
    `define LDMA_SHRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH+1
    `define LDMA_CH_NUM_BITWIDTH            `UBMC_ADDR_BITWIDTH+1
    `define SDMA_EXRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH+1
    `define SDMA_SHRAM_C_BITWIDTH           `UBMC_ADDR_BITWIDTH+1
    `define SDMA_CH_NUM_BITWIDTH            `UBMC_ADDR_BITWIDTH+1
`endif

`endif
