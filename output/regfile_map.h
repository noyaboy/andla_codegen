#ifndef _REGFILE_MAP_H
#define _REGFILE_MAP_H

#include <andla.h>

// Status & Fence destination
#define GEMM_DEST              (0x1 << 3)
#define EDP_DEST               (0x1 << 4)
#define INTR_DEST              (0x1 << 21)
#define CTRL_HW_INTR_DEST      (0x1 << 20)

// autogen_dest_start
#define CSR_DEST        (0x1 << 0)
#define SDMA_DEST       (0x1 << 1)
#define LDMA_DEST       (0x1 << 2)
#define FME0_DEST       (0x1 << 3)
#define RESERVED_4_DEST (0x1 << 4)
#define RESERVED_5_DEST (0x1 << 5)
#define LDMA2_DEST      (0x1 << 6)
#define CDMA_DEST       (0x1 << 7)
// autogen_dest_stop



#endif //_REGFILE_MAP_H
