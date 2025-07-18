# Regfile Automatic Code Generation Tool User Guide

## Overview

This tool is used to automatically generate Regfile-related code, including Verilog and C header files. It uses a standardized CSV input file to define registers, then utilizes scripts to automatically generate the required output files and deploy them to their respective directories within the project.

## Directory Structure

- **Tool Path**: `$PVC_LOCALDIR/andes_ip/andla/tools/code_generation_v2/`
- **Core Scripts**:
    - `run.sh`: The main execution script that calls other Perl/Python scripts.
    - Various `.pl` (Perl) and `.py` (Python) files: Contain the logic for code generation.
- **Directories**:
    - `input/`: Contains template files (`.tmp.*`) for manual modifications (hand-coding).
    - `output/`: Contains the files automatically generated by the tool.

## Basic Usage

Navigate to the tool directory and simply execute `run.sh`.

```bash
cd $PVC_LOCALDIR/andes_ip/andla/tools/code_generation_v2/
./run.sh
```
This script will perform the following three actions:

1.  Read the register definition file.
2.  Generate all target files in the `output/` directory.
3.  Automatically copy the files from `output/` to their predefined project paths.

---

## Features

### 1. How to Add a New Register?

To add a new register, you need to modify the following CSV file:

- **File Path**: `$PVC_LOCALDIR/andes_ip/andla/doc/register_allocation.csv`

**Instructions**:
In the `register_allocation.csv` file, simply add a new row to define your new register. Follow the existing format and specific rules to fill in the required fields. After saving the file, re-run `./run.sh`, and the new register will be included in the auto-generated code. The rule of adding a new register is attached below:

1. **Index Column Continuity**  
   - Ensure the Index column runs continuously from `0` to `31`.  
   - If any indices are missing, add a reserved row labeled `RESERVE<index>` (e.g., `RESERVE23`) with `Type` set to `NA`.

2. **Enumeration Entries**  
   - Add an enumeration entry for each index in the format `<index>:<ENUM_NAME>`, for example:  
     ```text
     0:FME_MODE
     1:OTHER_MODE
     …
     17:RESERVED17
     ```  
   - List reserved entries individually (e.g., `17:RESERVED17`).

3. **Bitwidth Configuration for Subregisters**  
   - If a register contains subregisters (excluding simple LSB/MSB fields), specify the total register bitwidth in its first row under **Bitwidth Configuration**:  
     - Use a plain integer (e.g., `7`)  
     - Or wrap a macro definition in backticks (e.g., `` `ANDLA_IBMC_ADDR_BITWIDTH+1 ``)  
   - **Do not** omit the backticks around macro definitions.

4. **Usercase Rule Definition**  
   - Define the usercase rule as a list or a Python range, for example:  
     - List: `[1, 3, 7]`  
     - Range: `range(1, 8)`

5. **Subregister Splitting Order**  
   - After splitting, list subregisters from LSB to MSB in ascending order.  
   - Reserved bit-fields may be omitted.

6. **Handling of `NA` Types**  
   - Registers with `Type = NA`:  
     - **Will not** be generated in RTL or in the datasheet.  
     - **Will** be generated in the C source code.

7. **Description Column Usage**  
   - All content in the **Description** column is intended for the final datasheet.

8. **Default Value Formatting**  
   - Fill in only decimal integers or hexadecimal codes, for example:  
     ```text
     0x60451000
     42
     ```


### 2. How to Modify the Destination Path of Generated Files?

The `./run.sh` script defines an associative array that maps the generated source files to their final destination paths.

**Instructions**:
1.  Open `./run.sh` in a text editor.
2.  Locate the `declare -A files=` block.

```bash
# Snippet from run.sh

  declare -A files=(
    ["output/andla.vh"]="andes_ip/andla/hdl/include/andla.vh"
    ["output/andla.h"]="andes_vip/dv_lib/andla.h"
    ["output/andla_common.h"]="andes_vip/dv_lib/andla_common.h"
    ["output/regfile_map.h"]="andes_vip/dv_lib/regfile_map.h"
    ["output/andla_regfile.v"]="andes_ip/andla/hdl/andla_regfile.v"
    ["output/reg_constraint.h"]="andes_vip/dv/pattern/c/fme/reg_constraint.h"
    ["output/regfile_init.h"]="andes_vip/dv_lib/regfile_init.h"
  )

```

**Modification Details**:
-   The `key` (the part in `[...]`) is the source file in the `output/` directory, e.g., `output/andla.h`.
-   The `value` (the part after `=`) is the destination path where the file will be copied.
-   The prefix for all destination paths is automatically set to `$PVC_LOCALDIR`.
-   To change the destination for `andla.h`, you only need to modify the `"andes_vip/dv_lib/andla.h"` string.

**Generated Files**:
-   andla.h
-   andla.vh
-   andla_common.h
-   andla_regfile.v
-   andla_regfile_cov.sv
-   reg_constraint.h
-   regfile_init.h
-   regfile_map.h
-   andla_cdma.empty.v
-   andla_fme0.empty.v
-   andla_ldma.empty.v
-   andla_ldma2.empty.v
-   andla_sdma.empty.v





### 3. How to Hand-code (Manually Modify) Generated Files?

Sometimes, you may need to add temporary or custom code to the auto-generated files. To prevent these manual changes from being overwritten the next time you run the script, please follow these steps.

**Instructions**:
1.  Navigate to the `input/` directory.
2.  Find the corresponding template file. For example, to modify `andla.h`, you would edit `input/andla.tmp.h`.
3.  Inside the template file, you will see markers like the ones below:

    ```c
    // ... other code ...

    // autogen_some_name_start
    // The content between these markers will be overwritten by
    // the auto-generated code when you run run.sh.
    // autogen_some_name_stop

    // ... other code ...
    ```

4.  **Place your manual code outside the `// autogen_*_start` and `// autogen_*_stop` block.**

    ```c
    // Example: Adding hand-code in andla.tmp.h
    
    // --- You can add your manual code here (before the block) ---
    #define MY_CUSTOM_MACRO 123
    // --- End of manual code ---
    
    // autogen_some_name_start
    // (Do not modify content here)
    // autogen_some_name_stop
    
    // --- Or you can add your manual code here (after the block) ---
    int my_custom_function(void);
    // --- End of manual code ---
    ```
5.  After saving the file, re-run `./run.sh`. The tool will preserve all your modifications outside the `autogen` blocks and integrate them into the final generated file.
