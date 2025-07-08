#ifndef _REG_CONSTRAINT_H
#define _REG_CONSTRAINT_H

#include <stdint.h> // For uint32_t


uint32_t FME0_MODE_EXE_MODE_CONSTRAINT[3]       = {0,1,2};
uint32_t FME0_MODE_MM_ATTRIBUTE_CONSTRAINT[3]   = {0,1,2};
uint32_t FME0_MODE_EDP_ACT_CONSTRAINT[4]        = {0,1,2,3};
uint32_t FME0_MODE_EDP_DST_DOMAIN_CONSTRAINT[2] = {1,2};
uint32_t FME0_MODE_EDP_SRC_DOMAIN_CONSTRAINT[2] = {1,2};
uint32_t FME0_MODE_EDP_EW_OP_CONSTRAINT[5]      = {0,1,2,4,5};
uint32_t FME0_MODE_EDP_FLOW_CONSTRAINT[3]       = {1,2,3};
uint32_t FME0_MODE_LOAD_MODE_CONSTRAINT[4]      = {0,1,2,3};
uint32_t FME0_MODE_GEMM_DOMAIN_CONSTRAINT[3]    = {0,1,2};
uint32_t FME0_IM_PAD_IM_PU_CONSTRAINT[8]        = {0,1,2,3,4,5,6,7};
uint32_t FME0_IM_PAD_IM_PD_CONSTRAINT[8]        = {0,1,2,3,4,5,6,7};
uint32_t FME0_IM_PAD_IM_PL_CONSTRAINT[8]        = {0,1,2,3,4,5,6,7};
uint32_t FME0_IM_PAD_IM_PR_CONSTRAINT[8]        = {0,1,2,3,4,5,6,7};
uint32_t FME0_IM_IW_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_IM_IH_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_IM_IC_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_IM_STRIDE_IM_SW_CONSTRAINT[3]     = {0xffffffff, 0, 1 << 5};
uint32_t FME0_IM_STRIDE_IM_SH_CONSTRAINT[3]     = {0xffffffff, 0, 1 << 5};
uint32_t FME0_IM_STRIDE_TW_CONSTRAINT[2]        = {0,1};
uint32_t FME0_IM_STRIDE_TH_CONSTRAINT[2]        = {0,1};
uint32_t FME0_IM_KERNEL_IM_KW_CONSTRAINT[3]     = {0xffffffff, 0, 1 << 5};
uint32_t FME0_IM_KERNEL_IM_KH_CONSTRAINT[3]     = {0xffffffff, 0, 1 << 5};
uint32_t FME0_IM_KERNEL_IM_KWKH_CONSTRAINT[3]   = {0xffffffff, 0, 961};
uint32_t FME0_EM_IW_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_EM_IH_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_EM_IC_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_OM_OW_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_OM_OH_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_OM_OC_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};
uint32_t FME0_IM_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_KR_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_BS_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_PL_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_EM_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_OM_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_EM_ALIGNMENT_ICIW_CONSTRAINT[3]   = {0xffffffff, 0, 1 << 22};
uint32_t FME0_OM_ALIGNMENT_OCOW_CONSTRAINT[3]   = {0xffffffff, 0, 1 << 22};
uint32_t FME0_ALIGNMENT_KCKWKH_CONSTRAINT[3]    = {0xffffffff, 0, 1 << 22};
uint32_t FME0_ALIGNMENT_KCKW_CONSTRAINT[3]      = {0xffffffff, 0, 1 << 22};
uint32_t FME0_SC_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_SH_ADDR_INIT_CONSTRAINT[3]        = {0xffffffff, 0, 1 << 22};
uint32_t FME0_IM_KC_CONSTRAINT[3]               = {0xffffffff, 0, 1 << 14};

#endif /* _REG_CONSTRAINT_H  */
