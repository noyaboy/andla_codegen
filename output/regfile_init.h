#ifndef _REGFILE_INIT_H
#define _REGFILE_INIT_H

void reg_init(reg_file_s* regfile){
// autogen_start
    regfile->item[CSR].reg[CSR_STATUS].data                                       = 0;
    regfile->item[CSR].reg[CSR_CONTROL].data                                      = 0;
    regfile->item[CSR].reg[CSR_COUNTER_LSB].data                                  = 0;
    regfile->item[CSR].reg[CSR_COUNTER_MSB].data                                  = 0;
    regfile->item[CSR].reg[CSR_COUNTER_MASK].data                                 = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_0_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_0_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_1_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_1_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_2_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_2_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_3_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_3_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_4_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_4_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_5_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_5_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_6_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_6_MSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_7_LSB].data                       = 0;
    regfile->item[CSR].reg[CSR_EXRAM_BASED_ADDR_7_MSB].data                       = 0;
    regfile->item[SDMA].reg[SDMA_SFENCE].data                                     = 0;
    regfile->item[SDMA].reg[SDMA_DIRECTION].data                                  = 1;
    regfile->item[SDMA].reg[SDMA_EXRAM_ADDR_LSB].data                             = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_ADDR_MSB].data                             = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_ADDR].data                                 = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_C].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_W].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_H].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_N].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_STRIDE_W_SIZE].data                        = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_STRIDE_H_SIZE].data                        = 0;
    regfile->item[SDMA].reg[SDMA_EXRAM_STRIDE_N_SIZE].data                        = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_C].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_W].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_H].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_N].data                                    = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_PAD_RIGHT].data                            = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_PAD_LEFT].data                             = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_PAD_UP].data                               = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_PAD_DOWN].data                             = 0;
    regfile->item[SDMA].reg[SDMA_CONST_VALUE].data                                = 0;
    regfile->item[SDMA].reg[SDMA_CH_NUM].data                                     = 0;
    regfile->item[SDMA].reg[SDMA_SDMA_DEPADDING_BY_PASS].data                     = 1;
    regfile->item[SDMA].reg[SDMA_PRESERVED0].data                                 = 0;
    regfile->item[SDMA].reg[SDMA_PRESERVED1].data                                 = 0;
    regfile->item[SDMA].reg[SDMA_PRESERVED2].data                                 = 0;
    regfile->item[SDMA].reg[SDMA_SDMA_CHSUM_SEL].data                             = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_STRIDE_W_SIZE].data                        = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_STRIDE_H_SIZE].data                        = 0;
    regfile->item[SDMA].reg[SDMA_SHRAM_STRIDE_N_SIZE].data                        = 0;
    regfile->item[LDMA].reg[LDMA_SFENCE].data                                     = 0;
    regfile->item[LDMA].reg[LDMA_DIRECTION].data                                  = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_ADDR_LSB].data                             = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_ADDR_MSB].data                             = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_ADDR].data                                 = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_C].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_W].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_H].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_N].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_STRIDE_W_SIZE].data                        = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_STRIDE_H_SIZE].data                        = 0;
    regfile->item[LDMA].reg[LDMA_EXRAM_STRIDE_N_SIZE].data                        = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_C].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_W].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_H].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_N].data                                    = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_PAD_RIGHT].data                            = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_PAD_LEFT].data                             = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_PAD_UP].data                               = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_PAD_DOWN].data                             = 0;
    regfile->item[LDMA].reg[LDMA_CONST_VALUE].data                                = 0;
    regfile->item[LDMA].reg[LDMA_CH_NUM].data                                     = 0;
    regfile->item[LDMA].reg[LDMA_LDMA_DECOMP_PADDING_BY_PASS].data                = 1;
    regfile->item[LDMA].reg[LDMA_RAM_PADDING_VALUE].data                          = 0;
    regfile->item[LDMA].reg[LDMA_PAD_C_FRONT].data                                = 0;
    regfile->item[LDMA].reg[LDMA_PAD_C_BACK].data                                 = 0;
    regfile->item[LDMA].reg[LDMA_LDMA_CHSUM_SEL].data                             = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_STRIDE_W_SIZE].data                        = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_STRIDE_H_SIZE].data                        = 0;
    regfile->item[LDMA].reg[LDMA_SHRAM_STRIDE_N_SIZE].data                        = 0;
    regfile->item[FME0].reg[FME0_SFENCE].data                                     = 0;
    regfile->item[FME0].reg[FME0_MODE].data                                       = 0;
    regfile->item[FME0].reg[FME0_IM_DILATED_RATE].data                            = 0;
    regfile->item[FME0].reg[FME0_IM_PAD].data                                     = 0;
    regfile->item[FME0].reg[FME0_IM_IW].data                                      = 0;
    regfile->item[FME0].reg[FME0_IM_IH].data                                      = 0;
    regfile->item[FME0].reg[FME0_IM_IC].data                                      = 0;
    regfile->item[FME0].reg[FME0_IM_STRIDE].data                                  = 0;
    regfile->item[FME0].reg[FME0_IM_KERNEL].data                                  = 0;
    regfile->item[FME0].reg[FME0_MODE_EX].data                                    = 0;
    regfile->item[FME0].reg[FME0_EM_IW].data                                      = 0;
    regfile->item[FME0].reg[FME0_EM_IH].data                                      = 0;
    regfile->item[FME0].reg[FME0_EM_IC].data                                      = 0;
    regfile->item[FME0].reg[FME0_OM_OW].data                                      = 0;
    regfile->item[FME0].reg[FME0_OM_OH].data                                      = 0;
    regfile->item[FME0].reg[FME0_OM_OC].data                                      = 0;
    regfile->item[FME0].reg[FME0_IM_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_KR_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_BS_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_PL_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_EM_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_OM_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_EM_ALIGNMENT_ICIW].data                          = 0;
    regfile->item[FME0].reg[FME0_OM_ALIGNMENT_OCOW].data                          = 0;
    regfile->item[FME0].reg[FME0_ALIGNMENT_KCKWKH].data                           = 0;
    regfile->item[FME0].reg[FME0_ALIGNMENT_KCKW].data                             = 0;
    regfile->item[FME0].reg[FME0_SC_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_SH_ADDR_INIT].data                               = 0;
    regfile->item[FME0].reg[FME0_IM_KC].data                                      = 0;
    regfile->item[LDMA2].reg[LDMA2_MODE_CTRL].data                                = 0;
    regfile->item[LDMA2].reg[LDMA2_ROLL_IC_IW_W_PAD_SIZE].data                    = 0;
    regfile->item[LDMA2].reg[LDMA2_ROLL_IC_KW_SIZE].data                          = 0;
    regfile->item[LDMA2].reg[LDMA2_ROLL_KR_STRIDE_W_SIZE].data                    = 0;
    regfile->item[LDMA2].reg[LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE].data                = 0;
    regfile->item[LDMA2].reg[LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE].data               = 0;
    regfile->item[LDMA2].reg[LDMA2_ROLL_PAD_H_SIZE].data                          = 0;
    regfile->item[CDMA].reg[CDMA_SFENCE].data                                     = 0;
    regfile->item[CDMA].reg[CDMA_DIRECTION].data                                  = 0;
    regfile->item[CDMA].reg[CDMA_EXRAM_ADDR_LSB].data                             = 0;
    regfile->item[CDMA].reg[CDMA_EXRAM_ADDR_MSB].data                             = 0;
    regfile->item[CDMA].reg[CDMA_EXRAM_C].data                                    = 4;
    regfile->item[CDMA].reg[CDMA_EXRAM_W].data                                    = 1;
    regfile->item[CDMA].reg[CDMA_EXRAM_STRIDE_W].data                             = 4;
// autogen_stop
}
#endif // _REGFILE_INIT_H
