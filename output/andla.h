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
#define ANDLA_CDMA_REG_BASE  (ANDLA_REG_BASE + 0x380)
#define ANDLA_LDMA2_REG_BASE (ANDLA_REG_BASE + 0x300)
#define ANDLA_FME0_REG_BASE  (ANDLA_REG_BASE + 0x180)
#define ANDLA_LDMA_REG_BASE  (ANDLA_REG_BASE + 0x100)
#define ANDLA_SDMA_REG_BASE  (ANDLA_REG_BASE + 0x080)
#define ANDLA_CSR_REG_BASE   (ANDLA_REG_BASE + 0x000)
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
#define CDMA_DEST       (0x1 <<   7)
#define LDMA2_DEST      (0x1 <<   6)
#define RESERVED_5_DEST (0x1 <<   5)
#define RESERVED_4_DEST (0x1 <<   4)
#define FME0_DEST       (0x1 <<   3)
#define LDMA_DEST       (0x1 <<   2)
#define SDMA_DEST       (0x1 <<   1)
#define CSR_DEST        (0x1 <<   0)
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
SMART_ENUM(ITEM
   ,CSR
   ,SDMA
   ,LDMA
   ,FME0
   ,RESERVED_4
   ,RESERVED_5
   ,LDMA2
   ,CDMA
);
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
SMART_ENUM(CSR
    ,CSR_ID
    ,CSR_REVISION
    ,CSR_STATUS
    ,CSR_CONTROL
    ,CSR_CREDIT
    ,CSR_COUNTER_LSB
    ,CSR_COUNTER_MSB
    ,CSR_COUNTER_MASK
    ,CSR_EXRAM_BASED_ADDR_0_LSB
    ,CSR_EXRAM_BASED_ADDR_0_MSB
    ,CSR_EXRAM_BASED_ADDR_1_LSB
    ,CSR_EXRAM_BASED_ADDR_1_MSB
    ,CSR_EXRAM_BASED_ADDR_2_LSB
    ,CSR_EXRAM_BASED_ADDR_2_MSB
    ,CSR_EXRAM_BASED_ADDR_3_LSB
    ,CSR_EXRAM_BASED_ADDR_3_MSB
    ,CSR_EXRAM_BASED_ADDR_4_LSB
    ,CSR_EXRAM_BASED_ADDR_4_MSB
    ,CSR_EXRAM_BASED_ADDR_5_LSB
    ,CSR_EXRAM_BASED_ADDR_5_MSB
    ,CSR_EXRAM_BASED_ADDR_6_LSB
    ,CSR_EXRAM_BASED_ADDR_6_MSB
    ,CSR_EXRAM_BASED_ADDR_7_LSB
    ,CSR_EXRAM_BASED_ADDR_7_MSB
    ,CSR_NOP
);
SMART_ENUM(SDMA
    ,SDMA_SFENCE
    ,SDMA_DIRECTION
    ,SDMA_EXRAM_ADDR_LSB
    ,SDMA_EXRAM_ADDR_MSB
    ,SDMA_SHRAM_ADDR
    ,SDMA_EXRAM_C
    ,SDMA_EXRAM_W
    ,SDMA_EXRAM_H
    ,SDMA_EXRAM_N
    ,SDMA_EXRAM_STRIDE_W_SIZE
    ,SDMA_EXRAM_STRIDE_H_SIZE
    ,SDMA_EXRAM_STRIDE_N_SIZE
    ,SDMA_SHRAM_C
    ,SDMA_SHRAM_W
    ,SDMA_SHRAM_H
    ,SDMA_SHRAM_N
    ,SDMA_SHRAM_PAD_RIGHT
    ,SDMA_SHRAM_PAD_LEFT
    ,SDMA_SHRAM_PAD_UP
    ,SDMA_SHRAM_PAD_DOWN
    ,SDMA_CONST_VALUE
    ,SDMA_CH_NUM
    ,SDMA_SDMA_DEPADDING_BY_PASS
    ,SDMA_PRESERVED0
    ,SDMA_PRESERVED1
    ,SDMA_PRESERVED2
    ,SDMA_SDMA_CHSUM_SEL
    ,SDMA_SDMA_CHSUM_DATA
    ,SDMA_SHRAM_STRIDE_W_SIZE
    ,SDMA_SHRAM_STRIDE_H_SIZE
    ,SDMA_SHRAM_STRIDE_N_SIZE
);
SMART_ENUM(LDMA
    ,LDMA_SFENCE
    ,LDMA_DIRECTION
    ,LDMA_EXRAM_ADDR_LSB
    ,LDMA_EXRAM_ADDR_MSB
    ,LDMA_SHRAM_ADDR
    ,LDMA_EXRAM_C
    ,LDMA_EXRAM_W
    ,LDMA_EXRAM_H
    ,LDMA_EXRAM_N
    ,LDMA_EXRAM_STRIDE_W_SIZE
    ,LDMA_EXRAM_STRIDE_H_SIZE
    ,LDMA_EXRAM_STRIDE_N_SIZE
    ,LDMA_SHRAM_C
    ,LDMA_SHRAM_W
    ,LDMA_SHRAM_H
    ,LDMA_SHRAM_N
    ,LDMA_SHRAM_PAD_RIGHT
    ,LDMA_SHRAM_PAD_LEFT
    ,LDMA_SHRAM_PAD_UP
    ,LDMA_SHRAM_PAD_DOWN
    ,LDMA_CONST_VALUE
    ,LDMA_CH_NUM
    ,LDMA_LDMA_DECOMP_PADDING_BY_PASS
    ,LDMA_RAM_PADDING_VALUE
    ,LDMA_PAD_C_FRONT
    ,LDMA_PAD_C_BACK
    ,LDMA_LDMA_CHSUM_SEL
    ,LDMA_LDMA_CHSUM_DATA
    ,LDMA_SHRAM_STRIDE_W_SIZE
    ,LDMA_SHRAM_STRIDE_H_SIZE
    ,LDMA_SHRAM_STRIDE_N_SIZE
);
SMART_ENUM(FME0
    ,FME0_SFENCE
    ,FME0_MODE
    ,FME0_IM_PAD
    ,FME0_IM_IW
    ,FME0_IM_IH
    ,FME0_IM_IC
    ,FME0_IM_STRIDE
    ,FME0_IM_KERNEL
    ,FME0_OM_OW
    ,FME0_OM_OH
    ,FME0_OM_OC
    ,FME0_IM_ADDR_INIT
    ,FME0_KR_ADDR_INIT
    ,FME0_BS_ADDR_INIT
    ,FME0_PL_ADDR_INIT
    ,FME0_EM_ADDR_INIT
    ,FME0_OM_ADDR_INIT
    ,FME0_EM_ALIGNMENT_ICIW
    ,FME0_OM_ALIGNMENT_OCOW
    ,FME0_ALIGNMENT_KCKWKH
    ,FME0_ALIGNMENT_KCKW
    ,FME0_SC_ADDR_INIT
    ,FME0_SH_ADDR_INIT
);
SMART_ENUM(LDMA2
    ,LDMA2_MODE_CTRL
    ,LDMA2_ROLL_IC_IW_W_PAD_SIZE
    ,LDMA2_ROLL_IC_KW_SIZE
    ,LDMA2_ROLL_KR_STRIDE_W_SIZE
    ,LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE
    ,LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE
    ,LDMA2_ROLL_PAD_H_SIZE
);
SMART_ENUM(CDMA
    ,CDMA_SFENCE
    ,CDMA_DIRECTION
    ,CDMA_EXRAM_ADDR_LSB
    ,CDMA_EXRAM_ADDR_MSB
    ,CDMA_EXRAM_C
    ,CDMA_EXRAM_W
    ,CDMA_EXRAM_STRIDE_W
);
// autogen_idx_stop

// autogen_reg_start
typedef struct andla_csr_reg_t {
    __IO uint32_t id;
    __IO uint32_t revision;
    __IO uint32_t status;
    __IO uint32_t control;
    __IO uint32_t credit;
    __IO uint32_t counter_lsb;
    __IO uint32_t counter_msb;
    __IO uint32_t counter_mask;
    __IO uint32_t exram_based_addr_0_lsb;
    __IO uint32_t exram_based_addr_0_msb;
    __IO uint32_t exram_based_addr_1_lsb;
    __IO uint32_t exram_based_addr_1_msb;
    __IO uint32_t exram_based_addr_2_lsb;
    __IO uint32_t exram_based_addr_2_msb;
    __IO uint32_t exram_based_addr_3_lsb;
    __IO uint32_t exram_based_addr_3_msb;
    __IO uint32_t exram_based_addr_4_lsb;
    __IO uint32_t exram_based_addr_4_msb;
    __IO uint32_t exram_based_addr_5_lsb;
    __IO uint32_t exram_based_addr_5_msb;
    __IO uint32_t exram_based_addr_6_lsb;
    __IO uint32_t exram_based_addr_6_msb;
    __IO uint32_t exram_based_addr_7_lsb;
    __IO uint32_t exram_based_addr_7_msb;
    __IO uint32_t nop;
} andla_csr_reg_s;
typedef struct andla_sdma_reg_t {
    __IO uint32_t sfence;
    __IO uint32_t direction;
    __IO uint32_t exram_addr_lsb;
    __IO uint32_t exram_addr_msb;
    __IO uint32_t shram_addr;
    __IO uint32_t exram_c;
    __IO uint32_t exram_w;
    __IO uint32_t exram_h;
    __IO uint32_t exram_n;
    __IO uint32_t exram_stride_w_size;
    __IO uint32_t exram_stride_h_size;
    __IO uint32_t exram_stride_n_size;
    __IO uint32_t shram_c;
    __IO uint32_t shram_w;
    __IO uint32_t shram_h;
    __IO uint32_t shram_n;
    __IO uint32_t shram_pad_right;
    __IO uint32_t shram_pad_left;
    __IO uint32_t shram_pad_up;
    __IO uint32_t shram_pad_down;
    __IO uint32_t const_value;
    __IO uint32_t ch_num;
    __IO uint32_t sdma_depadding_by_pass;
    __IO uint32_t preserved0;
    __IO uint32_t preserved1;
    __IO uint32_t preserved2;
    __IO uint32_t sdma_chsum_sel;
    __IO uint32_t sdma_chsum_data;
    __IO uint32_t shram_stride_w_size;
    __IO uint32_t shram_stride_h_size;
    __IO uint32_t shram_stride_n_size;
} andla_sdma_reg_s;
typedef struct andla_ldma_reg_t {
    __IO uint32_t sfence;
    __IO uint32_t direction;
    __IO uint32_t exram_addr_lsb;
    __IO uint32_t exram_addr_msb;
    __IO uint32_t shram_addr;
    __IO uint32_t exram_c;
    __IO uint32_t exram_w;
    __IO uint32_t exram_h;
    __IO uint32_t exram_n;
    __IO uint32_t exram_stride_w_size;
    __IO uint32_t exram_stride_h_size;
    __IO uint32_t exram_stride_n_size;
    __IO uint32_t shram_c;
    __IO uint32_t shram_w;
    __IO uint32_t shram_h;
    __IO uint32_t shram_n;
    __IO uint32_t shram_pad_right;
    __IO uint32_t shram_pad_left;
    __IO uint32_t shram_pad_up;
    __IO uint32_t shram_pad_down;
    __IO uint32_t const_value;
    __IO uint32_t ch_num;
    __IO uint32_t ldma_decomp_padding_by_pass;
    __IO uint32_t ram_padding_value;
    __IO uint32_t pad_c_front;
    __IO uint32_t pad_c_back;
    __IO uint32_t ldma_chsum_sel;
    __IO uint32_t ldma_chsum_data;
    __IO uint32_t shram_stride_w_size;
    __IO uint32_t shram_stride_h_size;
    __IO uint32_t shram_stride_n_size;
} andla_ldma_reg_s;
typedef struct andla_fme0_reg_t {
    __IO uint32_t sfence;
    __IO uint32_t mode;
    __IO uint32_t im_pad;
    __IO uint32_t im_iw;
    __IO uint32_t im_ih;
    __IO uint32_t im_ic;
    __IO uint32_t im_stride;
    __IO uint32_t im_kernel;
    __IO uint32_t om_ow;
    __IO uint32_t om_oh;
    __IO uint32_t om_oc;
    __IO uint32_t im_addr_init;
    __IO uint32_t kr_addr_init;
    __IO uint32_t bs_addr_init;
    __IO uint32_t pl_addr_init;
    __IO uint32_t em_addr_init;
    __IO uint32_t om_addr_init;
    __IO uint32_t em_alignment_iciw;
    __IO uint32_t om_alignment_ocow;
    __IO uint32_t alignment_kckwkh;
    __IO uint32_t alignment_kckw;
    __IO uint32_t sc_addr_init;
    __IO uint32_t sh_addr_init;
} andla_fme0_reg_s;
typedef struct andla_ldma2_reg_t {
    __IO uint32_t mode_ctrl;
    __IO uint32_t roll_ic_iw_w_pad_size;
    __IO uint32_t roll_ic_kw_size;
    __IO uint32_t roll_kr_stride_w_size;
    __IO uint32_t roll_pad_w_left_w_ic_size;
    __IO uint32_t roll_pad_w_right_w_ic_size;
    __IO uint32_t roll_pad_h_size;
} andla_ldma2_reg_s;
typedef struct andla_cdma_reg_t {
    __IO uint32_t sfence;
    __IO uint32_t direction;
    __IO uint32_t exram_addr_lsb;
    __IO uint32_t exram_addr_msb;
    __IO uint32_t exram_c;
    __IO uint32_t exram_w;
    __IO uint32_t exram_stride_w;
} andla_cdma_reg_s;
// autogen_reg_stop

// ======================================================
// ANDLA access macro
// ======================================================
#define DEV_ANDLA_SHRAM        ((uint8_t                    *)      ANDLA_SHRAM_BASE     )

// autogen_devreg_start
#define DEV_ANDLA_CSR_REG     ((andla_csr_reg_s*)      ANDLA_CSR_REG_BASE  )
#define DEV_ANDLA_SDMA_REG    ((andla_sdma_reg_s*)      ANDLA_SDMA_REG_BASE  )
#define DEV_ANDLA_LDMA_REG    ((andla_ldma_reg_s*)      ANDLA_LDMA_REG_BASE  )
#define DEV_ANDLA_FME0_REG    ((andla_fme0_reg_s*)      ANDLA_FME0_REG_BASE  )
#define DEV_ANDLA_LDMA2_REG   ((andla_ldma2_reg_s*)      ANDLA_LDMA2_REG_BASE  )
#define DEV_ANDLA_CDMA_REG    ((andla_cdma_reg_s*)      ANDLA_CDMA_REG_BASE  )
// autogen_devreg_stop

// declare andla shram structure
extern uint8_t                      *andla_shram           ;

// autogen_extreg_start
extern andla_csr_reg_s        *andla_csr_reg_p;
extern andla_sdma_reg_s        *andla_sdma_reg_p;
extern andla_ldma_reg_s        *andla_ldma_reg_p;
extern andla_fme0_reg_s        *andla_fme0_reg_p;
extern andla_ldma2_reg_s        *andla_ldma2_reg_p;
extern andla_cdma_reg_s        *andla_cdma_reg_p;
// autogen_extreg_stop

// declare andla register structure

// ======================================================
// ANDLA value macro
// ======================================================

#endif
