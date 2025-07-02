#ifndef __ANDLA_COMMON_H__
#define __ANDLA_COMMON_H__

#ifndef BLK_C 
void inital_reg_file (reg_file_s *reg_file) {
//{{{ inital_reg_file
// autogen_start
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
