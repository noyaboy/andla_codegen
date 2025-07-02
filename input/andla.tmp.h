#ifndef __ANDLA_H__
#define __ANDLA_H__

#include <string.h>
#include <inttypes.h>
#include "andla_env.h"
#include "andla_config.h"
#include "common.h"
#include <platform.h>
#include <smart_enum.h>
#ifndef BLK_C
#define C_MAIN main
#endif
#ifndef PAT_ITER_ROUND
    #define PAT_ITER_ROUND 1
#endif


#ifdef SW_ENV
    #include "pat2sw.h"
#endif

#ifdef UVM_ML
    FILE *fcdma;
    FILE *fddma;
    #define printf vpi_printf
#endif

#define CACHE_ON	  1
#define GEN_CODE
#define INT_NO_ANDLA 21
#define REG_OFFSET              2

//For 1.0 uvm_ml Env
#define ANDLA_AXI_DATA_WIDTH                      64
#define ANDLA_BASE                                0xd0000000
#define ANDLA_SHRAM_BASE        (ANDLA_BASE     + 0x00000000)
#define ANDLA_REG_BASE          (ANDLA_BASE     + 0x0e000000)
#define ANDLA_GEMM_REG_BASE     (ANDLA_REG_BASE + 0x280)
#define ANDLA_EDP_REG_BASE      (ANDLA_REG_BASE + 0x200)
#define ANDLA_AXI2TL_BASE        ANDLA_BASE
#define BIT_MASK(n) ((1 << n) - 1)

// autogen_base_start
// autogen_base_stop

#if (FPGA_EMU)
    #ifndef SLVPORT_BASE
        #define SLVPORT_BASE 0xa0000000
    #endif
#endif

#define data_to22lsb(data) ( data & 0x3FFFFF )
#define data_to10msb(data) ( (data >> 22) & 0x3FF )

// Status & Fence destination
#define GEMM_DEST               (0x1 <<  3)
#define EDP_DEST                (0x1 <<  4)
#define INTR_DEST               (0x1 << 21)
#define CTRL_HW_INTR_DEST       (0x1 << 20)

// autogen_dest_start
// autogen_dest_stop

#define WRITE          0x1
#define READ           0x0
#define DYNAMIC          1
#define STATIC           0
#define SHRAM            1
#define REG_FILE         0
#define TOTAL_ITEM_NUM   8

#define CPU_MODE  0
#define DMA_MODE  1

#ifndef __IO
#define __IO volatile
#endif

// autogen_item_start
// autogen_item_stop

typedef struct reg_t {
    volatile uint32_t *phy_addr;
    uint32_t data;
    uint8_t  bitwidth;
    uint8_t  index;
} reg_s;

typedef struct item_t {
    volatile reg_s reg [64];
    uint32_t *base_addr_ptr;
    uint8_t  id;
    uint8_t  reg_num;
} item_s;

typedef struct reg_file_t {
    volatile item_s item [ITEM_SIZE];
} reg_file_s;

// autogen_idx_start
// autogen_idx_stop

// autogen_reg_start
// autogen_reg_stop

// ======================================================
// ANDLA access macro
// ======================================================
#define DEV_ANDLA_SHRAM        ((uint8_t                    *)      ANDLA_SHRAM_BASE     )

// autogen_devreg_start
// autogen_devreg_stop

// declare andla shram structure
extern uint8_t                      *andla_shram           ;

// autogen_extreg_start
// autogen_extreg_stop

// declare andla register structure

// ======================================================
// ANDLA value macro
// ======================================================

#endif
