#ifndef __ANDLA_COMMON_H__
#define __ANDLA_COMMON_H__

#ifndef BLK_C 
void inital_reg_file (reg_file_s *reg_file) {
//{{{ inital_reg_file
// autogen_start
    reg_file->item[CSR].reg[CSR_ID].bitwidth                                      = 32;
    reg_file->item[CSR].reg[CSR_ID].index                                         = CSR_ID;

    reg_file->item[CSR].reg[CSR_REVISION].bitwidth                                = 32;
    reg_file->item[CSR].reg[CSR_REVISION].index                                   = CSR_REVISION;

    reg_file->item[CSR].reg[CSR_STATUS].bitwidth                                  = 22;
    reg_file->item[CSR].reg[CSR_STATUS].index                                     = CSR_STATUS;

    reg_file->item[CSR].reg[CSR_CONTROL].bitwidth                                 = 22;
    reg_file->item[CSR].reg[CSR_CONTROL].index                                    = CSR_CONTROL;

    reg_file->item[CSR].reg[CSR_CREDIT].bitwidth                                  = 11;
    reg_file->item[CSR].reg[CSR_CREDIT].index                                     = CSR_CREDIT;

    reg_file->item[CSR].reg[CSR_COUNTER_LSB].bitwidth                             = 22;
    reg_file->item[CSR].reg[CSR_COUNTER_LSB].index                                = CSR_COUNTER_LSB;

    reg_file->item[CSR].reg[CSR_COUNTER_MSB].bitwidth                             = 10;
    reg_file->item[CSR].reg[CSR_COUNTER_MSB].index                                = CSR_COUNTER_MSB;

    reg_file->item[CSR].reg[CSR_COUNTER_MASK].bitwidth                            = 22;
    reg_file->item[CSR].reg[CSR_COUNTER_MASK].index                               = CSR_COUNTER_MASK;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_0_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_0_LSB].index                     = CSR_EXRAM_BASED_ADDR_0_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_0_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_0_MSB].index                     = CSR_EXRAM_BASED_ADDR_0_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_1_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_1_LSB].index                     = CSR_EXRAM_BASED_ADDR_1_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_1_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_1_MSB].index                     = CSR_EXRAM_BASED_ADDR_1_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_2_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_2_LSB].index                     = CSR_EXRAM_BASED_ADDR_2_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_2_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_2_MSB].index                     = CSR_EXRAM_BASED_ADDR_2_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_3_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_3_LSB].index                     = CSR_EXRAM_BASED_ADDR_3_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_3_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_3_MSB].index                     = CSR_EXRAM_BASED_ADDR_3_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_4_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_4_LSB].index                     = CSR_EXRAM_BASED_ADDR_4_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_4_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_4_MSB].index                     = CSR_EXRAM_BASED_ADDR_4_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_5_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_5_LSB].index                     = CSR_EXRAM_BASED_ADDR_5_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_5_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_5_MSB].index                     = CSR_EXRAM_BASED_ADDR_5_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_6_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_6_LSB].index                     = CSR_EXRAM_BASED_ADDR_6_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_6_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_6_MSB].index                     = CSR_EXRAM_BASED_ADDR_6_MSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_7_LSB].bitwidth                  = 22;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_7_LSB].index                     = CSR_EXRAM_BASED_ADDR_7_LSB;

    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_7_MSB].bitwidth                  = 10;
    reg_file->item[CSR].reg[CSR_EXRAM_BASED_ADDR_7_MSB].index                     = CSR_EXRAM_BASED_ADDR_7_MSB;

    reg_file->item[CSR].reg[CSR_NOP].bitwidth                                     = 22;
    reg_file->item[CSR].reg[CSR_NOP].index                                        = CSR_NOP;

    reg_file->item[SDMA].reg[SDMA_SFENCE].bitwidth                                = 22;
    reg_file->item[SDMA].reg[SDMA_SFENCE].index                                   = SDMA_SFENCE;

    reg_file->item[SDMA].reg[SDMA_DIRECTION].bitwidth                             = 0;
    reg_file->item[SDMA].reg[SDMA_DIRECTION].index                                = SDMA_DIRECTION;

    reg_file->item[SDMA].reg[SDMA_EXRAM_ADDR_LSB].bitwidth                        = 22;
    reg_file->item[SDMA].reg[SDMA_EXRAM_ADDR_LSB].index                           = SDMA_EXRAM_ADDR_LSB;

    reg_file->item[SDMA].reg[SDMA_EXRAM_ADDR_MSB].bitwidth                        = 10;
    reg_file->item[SDMA].reg[SDMA_EXRAM_ADDR_MSB].index                           = SDMA_EXRAM_ADDR_MSB;

    reg_file->item[SDMA].reg[SDMA_SHRAM_ADDR].bitwidth                            = 19;
    reg_file->item[SDMA].reg[SDMA_SHRAM_ADDR].index                               = SDMA_SHRAM_ADDR;

    reg_file->item[SDMA].reg[SDMA_EXRAM_C].bitwidth                               = 20;
    reg_file->item[SDMA].reg[SDMA_EXRAM_C].index                                  = SDMA_EXRAM_C;

    reg_file->item[SDMA].reg[SDMA_EXRAM_W].bitwidth                               = 16;
    reg_file->item[SDMA].reg[SDMA_EXRAM_W].index                                  = SDMA_EXRAM_W;

    reg_file->item[SDMA].reg[SDMA_EXRAM_H].bitwidth                               = 16;
    reg_file->item[SDMA].reg[SDMA_EXRAM_H].index                                  = SDMA_EXRAM_H;

    reg_file->item[SDMA].reg[SDMA_EXRAM_N].bitwidth                               = 16;
    reg_file->item[SDMA].reg[SDMA_EXRAM_N].index                                  = SDMA_EXRAM_N;

    reg_file->item[SDMA].reg[SDMA_EXRAM_STRIDE_W_SIZE].bitwidth                   = 22;
    reg_file->item[SDMA].reg[SDMA_EXRAM_STRIDE_W_SIZE].index                      = SDMA_EXRAM_STRIDE_W_SIZE;

    reg_file->item[SDMA].reg[SDMA_EXRAM_STRIDE_H_SIZE].bitwidth                   = 22;
    reg_file->item[SDMA].reg[SDMA_EXRAM_STRIDE_H_SIZE].index                      = SDMA_EXRAM_STRIDE_H_SIZE;

    reg_file->item[SDMA].reg[SDMA_EXRAM_STRIDE_N_SIZE].bitwidth                   = 22;
    reg_file->item[SDMA].reg[SDMA_EXRAM_STRIDE_N_SIZE].index                      = SDMA_EXRAM_STRIDE_N_SIZE;

    reg_file->item[SDMA].reg[SDMA_SHRAM_C].bitwidth                               = 20;
    reg_file->item[SDMA].reg[SDMA_SHRAM_C].index                                  = SDMA_SHRAM_C;

    reg_file->item[SDMA].reg[SDMA_SHRAM_W].bitwidth                               = 16;
    reg_file->item[SDMA].reg[SDMA_SHRAM_W].index                                  = SDMA_SHRAM_W;

    reg_file->item[SDMA].reg[SDMA_SHRAM_H].bitwidth                               = 16;
    reg_file->item[SDMA].reg[SDMA_SHRAM_H].index                                  = SDMA_SHRAM_H;

    reg_file->item[SDMA].reg[SDMA_SHRAM_N].bitwidth                               = 16;
    reg_file->item[SDMA].reg[SDMA_SHRAM_N].index                                  = SDMA_SHRAM_N;

    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_RIGHT].bitwidth                       = 4;
    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_RIGHT].index                          = SDMA_SHRAM_PAD_RIGHT;

    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_LEFT].bitwidth                        = 4;
    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_LEFT].index                           = SDMA_SHRAM_PAD_LEFT;

    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_UP].bitwidth                          = 4;
    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_UP].index                             = SDMA_SHRAM_PAD_UP;

    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_DOWN].bitwidth                        = 4;
    reg_file->item[SDMA].reg[SDMA_SHRAM_PAD_DOWN].index                           = SDMA_SHRAM_PAD_DOWN;

    reg_file->item[SDMA].reg[SDMA_CONST_VALUE].bitwidth                           = 18;
    reg_file->item[SDMA].reg[SDMA_CONST_VALUE].index                              = SDMA_CONST_VALUE;

    reg_file->item[SDMA].reg[SDMA_CH_NUM].bitwidth                                = 20;
    reg_file->item[SDMA].reg[SDMA_CH_NUM].index                                   = SDMA_CH_NUM;

    reg_file->item[SDMA].reg[SDMA_SDMA_DEPADDING_BY_PASS].bitwidth                = 0;
    reg_file->item[SDMA].reg[SDMA_SDMA_DEPADDING_BY_PASS].index                   = SDMA_SDMA_DEPADDING_BY_PASS;

    reg_file->item[SDMA].reg[SDMA_PRESERVED0].bitwidth                            = 0;
    reg_file->item[SDMA].reg[SDMA_PRESERVED0].index                               = SDMA_PRESERVED0;

    reg_file->item[SDMA].reg[SDMA_PRESERVED1].bitwidth                            = 0;
    reg_file->item[SDMA].reg[SDMA_PRESERVED1].index                               = SDMA_PRESERVED1;

    reg_file->item[SDMA].reg[SDMA_PRESERVED2].bitwidth                            = 0;
    reg_file->item[SDMA].reg[SDMA_PRESERVED2].index                               = SDMA_PRESERVED2;

    reg_file->item[SDMA].reg[SDMA_SDMA_CHSUM_SEL].bitwidth                        = 22;
    reg_file->item[SDMA].reg[SDMA_SDMA_CHSUM_SEL].index                           = SDMA_SDMA_CHSUM_SEL;

    reg_file->item[SDMA].reg[SDMA_SDMA_CHSUM_DATA].bitwidth                       = 32;
    reg_file->item[SDMA].reg[SDMA_SDMA_CHSUM_DATA].index                          = SDMA_SDMA_CHSUM_DATA;

    reg_file->item[SDMA].reg[SDMA_SHRAM_STRIDE_W_SIZE].bitwidth                   = 19;
    reg_file->item[SDMA].reg[SDMA_SHRAM_STRIDE_W_SIZE].index                      = SDMA_SHRAM_STRIDE_W_SIZE;

    reg_file->item[SDMA].reg[SDMA_SHRAM_STRIDE_H_SIZE].bitwidth                   = 19;
    reg_file->item[SDMA].reg[SDMA_SHRAM_STRIDE_H_SIZE].index                      = SDMA_SHRAM_STRIDE_H_SIZE;

    reg_file->item[SDMA].reg[SDMA_SHRAM_STRIDE_N_SIZE].bitwidth                   = 19;
    reg_file->item[SDMA].reg[SDMA_SHRAM_STRIDE_N_SIZE].index                      = SDMA_SHRAM_STRIDE_N_SIZE;

    reg_file->item[LDMA].reg[LDMA_SFENCE].bitwidth                                = 22;
    reg_file->item[LDMA].reg[LDMA_SFENCE].index                                   = LDMA_SFENCE;

    reg_file->item[LDMA].reg[LDMA_DIRECTION].bitwidth                             = 0;
    reg_file->item[LDMA].reg[LDMA_DIRECTION].index                                = LDMA_DIRECTION;

    reg_file->item[LDMA].reg[LDMA_EXRAM_ADDR_LSB].bitwidth                        = 22;
    reg_file->item[LDMA].reg[LDMA_EXRAM_ADDR_LSB].index                           = LDMA_EXRAM_ADDR_LSB;

    reg_file->item[LDMA].reg[LDMA_EXRAM_ADDR_MSB].bitwidth                        = 10;
    reg_file->item[LDMA].reg[LDMA_EXRAM_ADDR_MSB].index                           = LDMA_EXRAM_ADDR_MSB;

    reg_file->item[LDMA].reg[LDMA_SHRAM_ADDR].bitwidth                            = 19;
    reg_file->item[LDMA].reg[LDMA_SHRAM_ADDR].index                               = LDMA_SHRAM_ADDR;

    reg_file->item[LDMA].reg[LDMA_EXRAM_C].bitwidth                               = 20;
    reg_file->item[LDMA].reg[LDMA_EXRAM_C].index                                  = LDMA_EXRAM_C;

    reg_file->item[LDMA].reg[LDMA_EXRAM_W].bitwidth                               = 16;
    reg_file->item[LDMA].reg[LDMA_EXRAM_W].index                                  = LDMA_EXRAM_W;

    reg_file->item[LDMA].reg[LDMA_EXRAM_H].bitwidth                               = 16;
    reg_file->item[LDMA].reg[LDMA_EXRAM_H].index                                  = LDMA_EXRAM_H;

    reg_file->item[LDMA].reg[LDMA_EXRAM_N].bitwidth                               = 16;
    reg_file->item[LDMA].reg[LDMA_EXRAM_N].index                                  = LDMA_EXRAM_N;

    reg_file->item[LDMA].reg[LDMA_EXRAM_STRIDE_W_SIZE].bitwidth                   = 22;
    reg_file->item[LDMA].reg[LDMA_EXRAM_STRIDE_W_SIZE].index                      = LDMA_EXRAM_STRIDE_W_SIZE;

    reg_file->item[LDMA].reg[LDMA_EXRAM_STRIDE_H_SIZE].bitwidth                   = 22;
    reg_file->item[LDMA].reg[LDMA_EXRAM_STRIDE_H_SIZE].index                      = LDMA_EXRAM_STRIDE_H_SIZE;

    reg_file->item[LDMA].reg[LDMA_EXRAM_STRIDE_N_SIZE].bitwidth                   = 22;
    reg_file->item[LDMA].reg[LDMA_EXRAM_STRIDE_N_SIZE].index                      = LDMA_EXRAM_STRIDE_N_SIZE;

    reg_file->item[LDMA].reg[LDMA_SHRAM_C].bitwidth                               = 20;
    reg_file->item[LDMA].reg[LDMA_SHRAM_C].index                                  = LDMA_SHRAM_C;

    reg_file->item[LDMA].reg[LDMA_SHRAM_W].bitwidth                               = 16;
    reg_file->item[LDMA].reg[LDMA_SHRAM_W].index                                  = LDMA_SHRAM_W;

    reg_file->item[LDMA].reg[LDMA_SHRAM_H].bitwidth                               = 16;
    reg_file->item[LDMA].reg[LDMA_SHRAM_H].index                                  = LDMA_SHRAM_H;

    reg_file->item[LDMA].reg[LDMA_SHRAM_N].bitwidth                               = 16;
    reg_file->item[LDMA].reg[LDMA_SHRAM_N].index                                  = LDMA_SHRAM_N;

    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_RIGHT].bitwidth                       = 4;
    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_RIGHT].index                          = LDMA_SHRAM_PAD_RIGHT;

    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_LEFT].bitwidth                        = 4;
    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_LEFT].index                           = LDMA_SHRAM_PAD_LEFT;

    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_UP].bitwidth                          = 4;
    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_UP].index                             = LDMA_SHRAM_PAD_UP;

    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_DOWN].bitwidth                        = 4;
    reg_file->item[LDMA].reg[LDMA_SHRAM_PAD_DOWN].index                           = LDMA_SHRAM_PAD_DOWN;

    reg_file->item[LDMA].reg[LDMA_CONST_VALUE].bitwidth                           = 18;
    reg_file->item[LDMA].reg[LDMA_CONST_VALUE].index                              = LDMA_CONST_VALUE;

    reg_file->item[LDMA].reg[LDMA_CH_NUM].bitwidth                                = 20;
    reg_file->item[LDMA].reg[LDMA_CH_NUM].index                                   = LDMA_CH_NUM;

    reg_file->item[LDMA].reg[LDMA_LDMA_DECOMP_PADDING_BY_PASS].bitwidth           = 0;
    reg_file->item[LDMA].reg[LDMA_LDMA_DECOMP_PADDING_BY_PASS].index              = LDMA_LDMA_DECOMP_PADDING_BY_PASS;

    reg_file->item[LDMA].reg[LDMA_RAM_PADDING_VALUE].bitwidth                     = 18;
    reg_file->item[LDMA].reg[LDMA_RAM_PADDING_VALUE].index                        = LDMA_RAM_PADDING_VALUE;

    reg_file->item[LDMA].reg[LDMA_PAD_C_FRONT].bitwidth                           = 14;
    reg_file->item[LDMA].reg[LDMA_PAD_C_FRONT].index                              = LDMA_PAD_C_FRONT;

    reg_file->item[LDMA].reg[LDMA_PAD_C_BACK].bitwidth                            = 14;
    reg_file->item[LDMA].reg[LDMA_PAD_C_BACK].index                               = LDMA_PAD_C_BACK;

    reg_file->item[LDMA].reg[LDMA_LDMA_CHSUM_SEL].bitwidth                        = 22;
    reg_file->item[LDMA].reg[LDMA_LDMA_CHSUM_SEL].index                           = LDMA_LDMA_CHSUM_SEL;

    reg_file->item[LDMA].reg[LDMA_LDMA_CHSUM_DATA].bitwidth                       = 32;
    reg_file->item[LDMA].reg[LDMA_LDMA_CHSUM_DATA].index                          = LDMA_LDMA_CHSUM_DATA;

    reg_file->item[LDMA].reg[LDMA_SHRAM_STRIDE_W_SIZE].bitwidth                   = 19;
    reg_file->item[LDMA].reg[LDMA_SHRAM_STRIDE_W_SIZE].index                      = LDMA_SHRAM_STRIDE_W_SIZE;

    reg_file->item[LDMA].reg[LDMA_SHRAM_STRIDE_H_SIZE].bitwidth                   = 19;
    reg_file->item[LDMA].reg[LDMA_SHRAM_STRIDE_H_SIZE].index                      = LDMA_SHRAM_STRIDE_H_SIZE;

    reg_file->item[LDMA].reg[LDMA_SHRAM_STRIDE_N_SIZE].bitwidth                   = 19;
    reg_file->item[LDMA].reg[LDMA_SHRAM_STRIDE_N_SIZE].index                      = LDMA_SHRAM_STRIDE_N_SIZE;

    reg_file->item[FME0].reg[FME0_SFENCE].bitwidth                                = 22;
    reg_file->item[FME0].reg[FME0_SFENCE].index                                   = FME0_SFENCE;

    reg_file->item[FME0].reg[FME0_MODE].bitwidth                                  = 22;
    reg_file->item[FME0].reg[FME0_MODE].index                                     = FME0_MODE;

    reg_file->item[FME0].reg[FME0_IM_DILATED_RATE].bitwidth                       = 3;
    reg_file->item[FME0].reg[FME0_IM_DILATED_RATE].index                          = FME0_IM_DILATED_RATE;

    reg_file->item[FME0].reg[FME0_IM_PAD].bitwidth                                = 12;
    reg_file->item[FME0].reg[FME0_IM_PAD].index                                   = FME0_IM_PAD;

    reg_file->item[FME0].reg[FME0_IM_IW].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_IM_IW].index                                    = FME0_IM_IW;

    reg_file->item[FME0].reg[FME0_IM_IH].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_IM_IH].index                                    = FME0_IM_IH;

    reg_file->item[FME0].reg[FME0_IM_IC].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_IM_IC].index                                    = FME0_IM_IC;

    reg_file->item[FME0].reg[FME0_IM_STRIDE].bitwidth                             = 14;
    reg_file->item[FME0].reg[FME0_IM_STRIDE].index                                = FME0_IM_STRIDE;

    reg_file->item[FME0].reg[FME0_IM_KERNEL].bitwidth                             = 20;
    reg_file->item[FME0].reg[FME0_IM_KERNEL].index                                = FME0_IM_KERNEL;

    reg_file->item[FME0].reg[FME0_MODE_EX].bitwidth                               = 22;
    reg_file->item[FME0].reg[FME0_MODE_EX].index                                  = FME0_MODE_EX;

    reg_file->item[FME0].reg[FME0_EM_IW].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_EM_IW].index                                    = FME0_EM_IW;

    reg_file->item[FME0].reg[FME0_EM_IH].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_EM_IH].index                                    = FME0_EM_IH;

    reg_file->item[FME0].reg[FME0_EM_IC].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_EM_IC].index                                    = FME0_EM_IC;

    reg_file->item[FME0].reg[FME0_OM_OW].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_OM_OW].index                                    = FME0_OM_OW;

    reg_file->item[FME0].reg[FME0_OM_OH].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_OM_OH].index                                    = FME0_OM_OH;

    reg_file->item[FME0].reg[FME0_OM_OC].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_OM_OC].index                                    = FME0_OM_OC;

    reg_file->item[FME0].reg[FME0_IM_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_IM_ADDR_INIT].index                             = FME0_IM_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_KR_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_KR_ADDR_INIT].index                             = FME0_KR_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_BS_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_BS_ADDR_INIT].index                             = FME0_BS_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_PL_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_PL_ADDR_INIT].index                             = FME0_PL_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_EM_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_EM_ADDR_INIT].index                             = FME0_EM_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_OM_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_OM_ADDR_INIT].index                             = FME0_OM_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_EM_ALIGNMENT_ICIW].bitwidth                     = 19;
    reg_file->item[FME0].reg[FME0_EM_ALIGNMENT_ICIW].index                        = FME0_EM_ALIGNMENT_ICIW;

    reg_file->item[FME0].reg[FME0_OM_ALIGNMENT_OCOW].bitwidth                     = 19;
    reg_file->item[FME0].reg[FME0_OM_ALIGNMENT_OCOW].index                        = FME0_OM_ALIGNMENT_OCOW;

    reg_file->item[FME0].reg[FME0_ALIGNMENT_KCKWKH].bitwidth                      = 19;
    reg_file->item[FME0].reg[FME0_ALIGNMENT_KCKWKH].index                         = FME0_ALIGNMENT_KCKWKH;

    reg_file->item[FME0].reg[FME0_ALIGNMENT_KCKW].bitwidth                        = 19;
    reg_file->item[FME0].reg[FME0_ALIGNMENT_KCKW].index                           = FME0_ALIGNMENT_KCKW;

    reg_file->item[FME0].reg[FME0_SC_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_SC_ADDR_INIT].index                             = FME0_SC_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_SH_ADDR_INIT].bitwidth                          = 19;
    reg_file->item[FME0].reg[FME0_SH_ADDR_INIT].index                             = FME0_SH_ADDR_INIT;

    reg_file->item[FME0].reg[FME0_IM_KC].bitwidth                                 = 14;
    reg_file->item[FME0].reg[FME0_IM_KC].index                                    = FME0_IM_KC;

    reg_file->item[LDMA2].reg[LDMA2_MODE_CTRL].bitwidth                           = 0;
    reg_file->item[LDMA2].reg[LDMA2_MODE_CTRL].index                              = LDMA2_MODE_CTRL;

    reg_file->item[LDMA2].reg[LDMA2_ROLL_IC_IW_W_PAD_SIZE].bitwidth               = 20;
    reg_file->item[LDMA2].reg[LDMA2_ROLL_IC_IW_W_PAD_SIZE].index                  = LDMA2_ROLL_IC_IW_W_PAD_SIZE;

    reg_file->item[LDMA2].reg[LDMA2_ROLL_IC_KW_SIZE].bitwidth                     = 4;
    reg_file->item[LDMA2].reg[LDMA2_ROLL_IC_KW_SIZE].index                        = LDMA2_ROLL_IC_KW_SIZE;

    reg_file->item[LDMA2].reg[LDMA2_ROLL_KR_STRIDE_W_SIZE].bitwidth               = 4;
    reg_file->item[LDMA2].reg[LDMA2_ROLL_KR_STRIDE_W_SIZE].index                  = LDMA2_ROLL_KR_STRIDE_W_SIZE;

    reg_file->item[LDMA2].reg[LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE].bitwidth           = 6;
    reg_file->item[LDMA2].reg[LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE].index              = LDMA2_ROLL_PAD_W_LEFT_W_IC_SIZE;

    reg_file->item[LDMA2].reg[LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE].bitwidth          = 6;
    reg_file->item[LDMA2].reg[LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE].index             = LDMA2_ROLL_PAD_W_RIGHT_W_IC_SIZE;

    reg_file->item[LDMA2].reg[LDMA2_ROLL_PAD_H_SIZE].bitwidth                     = 6;
    reg_file->item[LDMA2].reg[LDMA2_ROLL_PAD_H_SIZE].index                        = LDMA2_ROLL_PAD_H_SIZE;

    reg_file->item[CDMA].reg[CDMA_SFENCE].bitwidth                                = 22;
    reg_file->item[CDMA].reg[CDMA_SFENCE].index                                   = CDMA_SFENCE;

    reg_file->item[CDMA].reg[CDMA_DIRECTION].bitwidth                             = 0;
    reg_file->item[CDMA].reg[CDMA_DIRECTION].index                                = CDMA_DIRECTION;

    reg_file->item[CDMA].reg[CDMA_EXRAM_ADDR_LSB].bitwidth                        = 22;
    reg_file->item[CDMA].reg[CDMA_EXRAM_ADDR_LSB].index                           = CDMA_EXRAM_ADDR_LSB;

    reg_file->item[CDMA].reg[CDMA_EXRAM_ADDR_MSB].bitwidth                        = 10;
    reg_file->item[CDMA].reg[CDMA_EXRAM_ADDR_MSB].index                           = CDMA_EXRAM_ADDR_MSB;

    reg_file->item[CDMA].reg[CDMA_EXRAM_C].bitwidth                               = 22;
    reg_file->item[CDMA].reg[CDMA_EXRAM_C].index                                  = CDMA_EXRAM_C;

    reg_file->item[CDMA].reg[CDMA_EXRAM_W].bitwidth                               = 16;
    reg_file->item[CDMA].reg[CDMA_EXRAM_W].index                                  = CDMA_EXRAM_W;

    reg_file->item[CDMA].reg[CDMA_EXRAM_STRIDE_W].bitwidth                        = 22;
    reg_file->item[CDMA].reg[CDMA_EXRAM_STRIDE_W].index                           = CDMA_EXRAM_STRIDE_W;

    reg_file->item[CDMA].id                                                       = CDMA;
    reg_file->item[CDMA].base_addr_ptr                                            = andla_cdma_reg_p;
    reg_file->item[CDMA].reg_num                                                  = 0;

    reg_file->item[CSR].id                                                        = CSR;
    reg_file->item[CSR].base_addr_ptr                                             = andla_csr_reg_p;
    reg_file->item[CSR].reg_num                                                   = 0;

    reg_file->item[FME0].id                                                       = FME0;
    reg_file->item[FME0].base_addr_ptr                                            = andla_fme0_reg_p;
    reg_file->item[FME0].reg_num                                                  = 0;

    reg_file->item[SDMA].id                                                       = SDMA;
    reg_file->item[SDMA].base_addr_ptr                                            = andla_sdma_reg_p;
    reg_file->item[SDMA].reg_num                                                  = 0;

    reg_file->item[LDMA2].id                                                      = LDMA2;
    reg_file->item[LDMA2].base_addr_ptr                                           = andla_ldma2_reg_p;
    reg_file->item[LDMA2].reg_num                                                 = 0;

    reg_file->item[LDMA].id                                                       = LDMA;
    reg_file->item[LDMA].base_addr_ptr                                            = andla_ldma_reg_p;
    reg_file->item[LDMA].reg_num                                                  = 0;

// autogen_stop
}

//{{{ dev_sim_control_gen
void dev_sim_control_gen (uint32_t TEMP4, uint32_t TEMP5, uint32_t TEMP6, uint32_t TEMP7, uint32_t COMMAND, uint8_t show_info){
#if (!FPGA_EMU)
    #ifndef BLK_VERIFY
    DEV_SIM_CONTROL->TEMP4 = TEMP4;
    DEV_SIM_CONTROL->TEMP5 = TEMP5;
    DEV_SIM_CONTROL->TEMP6 = TEMP6;
    DEV_SIM_CONTROL->TEMP7 = TEMP7;

    switch (COMMAND) {
        case  0: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_0;   break;
        case  1: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_1;   break;
        case  2: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_2;   break;
        case  3: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_3;   break;
        case  4: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_4;   break;
        case  5: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_5;   break;
        case  6: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_6;   break;
        case  7: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_7;   break;
        case  8: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_8;   break;
        case  9: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_9;   break;
        case 10: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_10;  break;
        case 11: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_11;  break;
        case 12: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_12;  break;
        case 13: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_13;  break;
        case 14: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_14;  break;
        case 15: DEV_SIM_CONTROL->COMMAND = SIM_CONTROL_EVENT_15;  break;
    }
    #endif
#else
// cpu_write_reg
    //show_info = 0;
    if (COMMAND == 1) {
        if (show_info==1) {
            printf ("AXI2TLULBRG write item = %5d, index = %5d, physical_addr = %10x, data = %10x\n", TEMP4, TEMP5, TEMP6, TEMP7);
            fflush(stdout);
        }
    }
//cpu_read_reg
    else if (COMMAND == 2) {
        show_info = 1;
        if (show_info==1) {
            printf ("AXI2TLULBRG read  item = %5d, index = %5d, physical_addr = %10x, data = %10x\n", TEMP4, TEMP5, TEMP6, TEMP7);
            fflush(stdout);
        }
    }
//compare
    else if (COMMAND == 3) {
        if (TEMP4 == TEMP5) {
            if (show_info==1){
                printf ("AXI2TLULBRG compare (PASS) data = %7x, data_answer = %7x  ", TEMP4, TEMP5);
                fflush(stdout);
            }

    		if (show_info==1){
                printf ("---- SIMULATION PASSED ----\n");
                fflush(stdout);
            }
        } else {
            if (show_info==1){
                printf ("AXI2TLULBRG compare (FAIL) data = %7x, data_answer = %7x  ", TEMP4, TEMP5);
                fflush(stdout);
            }
    		if (show_info==1){
                printf ("---- Error ----\n");
                fflush(stdout);
            }
        }
    }
    else if (COMMAND == 5) {
        if (show_info==1){
            printf ("CDMA write : cmd = %8x, pattern = %8x, sizeof(cmd array) = %4d\n", TEMP4, TEMP5, TEMP6);
            fflush(stdout);
        }
    }
    else if (COMMAND == 6) {
        if (show_info==1) {
            printf ("CDMA write cmd: dest = %2d, item_id=%2d, index=%4d, data=%7x\n", TEMP4, TEMP5, TEMP6, TEMP7);
            fflush(stdout);
        }
    }
#endif
}
//}}}
//{{{ fpga sim compare
void  fpga_sim_output_compare(const uint32_t out_tensor_size,
                              const uint8_t * input_array,
                              const uint8_t * golden_array,
                              const uint8_t * output_array,
                              const uint8_t verbose)
{
    uint32_t error_cnt=0;
    uint32_t cnt = 0;

    printf("Output size = %x\n", out_tensor_size);
    fflush(stdout);
    int i;
    for(i=0; i<out_tensor_size; i++)
    {
        //if(verbose == 1)
        //{
            printf("No:%6d | ", i+1);
            fflush(stdout);
            printf("input: %p %2x | ", (input_array+i), *(input_array+i));
            fflush(stdout);
            printf("golden: %p %2x | output: %p  %2x | ", (golden_array+i), *(golden_array+i), (output_array+i),  *(output_array+i));
            fflush(stdout);
        //}

            if(golden_array[i] != output_array[i])
            {
                error_cnt += 1;
                //if(verbose == 1){printf("==ERROR==\n");}
                printf("==ERROR==\n");
                fflush(stdout);
            }
            else
            {
                //if(verbose == 1){printf("==MATCH==\n");}
                printf("==MATCH==\n");
                fflush(stdout);
            }
        }
    printf("error count: %d\n", error_cnt);
    if(error_cnt>0){ printf("ERROR!\n"); fflush(stdout); }
    else           { printf("PASS!\n"); fflush(stdout);}

    //fflush(stdout);
}
//}}}
//}}}
#endif
#endif
