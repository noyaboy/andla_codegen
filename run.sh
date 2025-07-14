echo "Generating Regfile ..."
#cp $PVC_LOCALDIR/andes_ip/andla/hdl/include/andla_config.vh $PVC_LOCALDIR/andes_ip/andla/tools/code_generation_v2/output/andla_config.vh

# python3 csv2df.py
# python3 gen_vh.py
# python3 gen_h.py
# python3 gen_common_h.py
# python3 gen_map.py
# python3 gen_regfile.py
# python3 gen_init.py
# python3 gen_reg_constraint_h.py
# python3 gen_regfile_cov_sv.py
# python3 gen_empty.py

python3 gen_doc.py
# cp output/programming_model.adoc output/programming_model.adoc.bak

# declare -A files=(
#   ["output/andla.vh"]="andes_ip/andla/hdl/include/andla.vh"
#   ["output/andla.h"]="andes_vip/dv_lib/andla.h"
#   ["output/andla_common.h"]="andes_vip/dv_lib/andla_common.h"
#   ["output/regfile_map.h"]="andes_vip/dv_lib/regfile_map.h"
#   ["output/andla_regfile.v"]="andes_ip/andla/hdl/andla_regfile.v"
#   ["output/reg_constraint.h"]="andes_vip/dv/pattern/c/fme/reg_constraint.h"
#   ["output/regfile_init.h"]="andes_vip/dv_lib/regfile_init.h"
# )

# for src in "${!files[@]}"; do
#   dst="$PVC_LOCALDIR/${files[$src]}"
#   if cp "$src" "$dst"; then
#     echo "Successfully copied $src to $dst"
#   else
#     echo "Failed to copy $src to $dst"
#   fi
# done

# echo "Successfully Generated Regfile."
