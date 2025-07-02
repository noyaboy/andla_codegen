#!/usr/bin/perl
use strict;
use warnings;

# Define file paths
my $input_file = 'input/andla.tmp.h';
# my $output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla.h';
my $output_file = 'output/andla.h';
my $reg_file = 'output/regfile_dictionary.log';

# Open input and output files
open my $in, '<', $input_file or die "Cannot open $input_file: $!";
open my $out, '>', $output_file or die "Cannot open $output_file: $!";

# -------------------------------
# 1. 解析 regfile_dictionary.log 產生 enum 與 typedef struct 的內容
# -------------------------------

my @idx_entries;
my @reg_entries;
my @base_entries;
my @dest_entries;
my @item_entries;
my @devreg_entries;
my @extreg_entries;
my $current_item = "";
my @buffer_idx;
my @buffer_reg;
my @buffer_base;
my @buffer_dest;
my @buffer_item;
my @buffer_devreg;
my @buffer_extreg;
my %seen_entries;
my %seen_items;

# (1) 針對 enum 的部分
open my $idx_reg, '<', $reg_file or die "Cannot open $reg_file: $!";
while (my $line = <$idx_reg>) {
    chomp $line;
    # 假設 log 格式為: 'Item': 'XXX', 'Register': 'YYY', 'SubRegister': 'LSB' 或 'MSB'
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);

        my $entry = $item . "_" . $register;

        # 記錄 item，確保不重複
        $seen_items{$item} = 1;

        # 若 SubRegister 為 LSB 或 MSB，則加上
        if (defined $subreg && ($subreg eq "LSB" || $subreg eq "MSB")) {
            $entry .= "_$subreg";
        }

        # 避免 enum 內部重複
        next if $seen_entries{$entry};
        $seen_entries{$entry} = 1;

        if ($item ne $current_item) {
            # 遇到新 item 時，先把前一組輸出
            if (@buffer_idx) {
                push @idx_entries, "SMART_ENUM($current_item\n" . join("\n", @buffer_idx) . "\n);\n";
                @buffer_idx = ();
            }
            $current_item = $item;
            %seen_entries = ();  # 清空以免不同 enum 互相影響
        }
        push @buffer_idx, "    ,$entry";
    }
}
# 輸出最後一組
if (@buffer_idx) {
    push @idx_entries, "SMART_ENUM($current_item\n" . join("\n", @buffer_idx) . "\n);\n";
}

close $idx_reg;

# (2) 針對 typedef struct 的部分
open my $reg_reg, '<', $reg_file or die "Cannot open $reg_file: $!";
%seen_entries = ();  # 重新清空
$current_item = "";
while (my $line = <$reg_reg>) {
    chomp $line;
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);
        my $entry = lc($register);

        # 若 SubRegister 為 LSB 或 MSB，則加上
        if (defined $subreg && ($subreg eq "LSB" || $subreg eq "MSB")) {
            $subreg = lc($subreg);
            $entry .= "_$subreg";
        }

        # 避免重複
        next if $seen_entries{$entry};
        $seen_entries{$entry} = 1;

        if ($item ne $current_item) {
            if (@buffer_reg) {
                my $item_lc = lc($current_item);
                push @reg_entries, "typedef struct andla_${item_lc}_reg_t {\n" . join("\n", @buffer_reg) . "\n} andla_${item_lc}_reg_s;\n";
                @buffer_reg = ();
            }
            $current_item = $item;
            %seen_entries = ();
        }
        push @buffer_reg, "    __IO uint32_t $entry;";
    }
}
if (@buffer_reg) {
    my $item_lc = lc($current_item);
    push @reg_entries, "typedef struct andla_${item_lc}_reg_t {\n" . join("\n", @buffer_reg) . "\n} andla_${item_lc}_reg_s;\n";
}
close $reg_reg;

# (3) 針對 physical base addr 的部分
open my $base_reg, '<', $reg_file or die "Cannot open $reg_file: $!";

$current_item = '';
my ($base, $subbase);

while (my $line = <$base_reg>) {
    chomp $line;
    # 只處理有 Item, Register, SubRegister 的行
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);

        # 忽略同一 item 已經處理過的第一筆
        next if $seen_entries{$item}++;
        
        # 如果是新 item，先 flush 掉上一個 item 的 buffer
        if ($item ne $current_item) {
            if (@buffer_base) {
                push @base_entries,
                     "#define ANDLA_"
                   . $current_item 
                   . "_REG_BASE (ANDLA_REG_BASE + 0x$subbase)\n";
                @buffer_base = ();
            }
            $current_item = $item;
            %seen_entries = ();    # 為下一個 item 重置 duplicate 判斷

            # 現在才抓這個新 item 的第一個 Physical Address
            if ($line =~ /'Physical Address':\s*'(\w+)'/) {
                $base    = $1;
                $subbase = substr($base, -3);
            }
        }

        push @buffer_base, $item;
    }
}

# loop 結束後，別忘了把最後一個 item flush 出來
if (@buffer_base) {
    push @base_entries,
         "#define ANDLA_"
       . $current_item 
       . "_REG_BASE (ANDLA_REG_BASE + 0x$subbase)\n";
}

close $base_reg;

# (5) 針對 item 的部分
open my $item_reg, '<', $reg_file or die "Cannot open $reg_file: $!";
%seen_entries = ();  # 重新清空
$current_item = "";
my $current_id_value = 0;
push @item_entries, "SMART_ENUM(ITEM\n";
while (my $line = <$item_reg>) {
    chomp $line;
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);
        my $entry = lc($register);
        my $id_value;

        # 避免重複
        next if $seen_entries{$item};
        $seen_entries{$item} = 1;
        if ($line =~ /'ID':\s*(\d+)/) {
            $id_value = $1;
        }
        if ($item ne $current_item) {
            if (@buffer_item) {
                my $item_lc = $current_item;
                push @item_entries, "   ,${item_lc}\n";
                if ($id_value - $current_id_value > 1) {    
                    for (my $i = $current_id_value+1; $i < $id_value; $i++) {
                        push @item_entries, "   ,RESERVED_${i}\n";
                    }
                }
                @buffer_item = ();
            }
            $current_id_value = $id_value;
            $current_item = $item;
            %seen_entries = ();
        }
        push @buffer_item, "    __IO uint32_t $entry;";
    }
}
if (@buffer_item) {
    my $item_lc = $current_item;
    push @item_entries, "   ,${item_lc}\n";
}
push @item_entries, ");\n";
close $item_reg;



# (6) 針對 devreg 的部分
open my $devreg_reg, '<', $reg_file or die "Cannot open $reg_file: $!";
%seen_entries = ();  # 重新清空
$current_item = "";
while (my $line = <$devreg_reg>) {
    chomp $line;
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);
        my $entry = lc($register);


        # 避免重複
        next if $seen_entries{$item};
        $seen_entries{$item} = 1;

        if ($item ne $current_item) {
            if (@buffer_devreg) {
                my $item_lc = lc($current_item);
                my $item_uc = uc($current_item);
                push @devreg_entries, "#define DEV_ANDLA_${item_uc}_REG     ((andla_${item_lc}_reg_s*)      ANDLA_${item_uc}_REG_BASE  )\n";  
                @buffer_devreg = ();
            }
            $current_item = $item;
            %seen_entries = ();
        }
        push @buffer_devreg, "    __IO uint32_t $entry;";
    }
}
if (@buffer_devreg) {
    my $item_lc = lc($current_item);
    my $item_uc = uc($current_item);
    push @devreg_entries, "#define DEV_ANDLA_${item_uc}_REG     ((andla_${item_lc}_reg_s*)      ANDLA_${item_uc}_REG_BASE  )\n";  
}
close $devreg_reg;


# (7) 針對 extreg 的部分
open my $extreg_reg, '<', $reg_file or die "Cannot open $reg_file: $!";
%seen_entries = ();  # 重新清空
$current_item = "";
while (my $line = <$extreg_reg>) {
    chomp $line;
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);
        my $entry = lc($register);


        # 避免重複
        next if $seen_entries{$item};
        $seen_entries{$item} = 1;

        if ($item ne $current_item) {
            if (@buffer_extreg) {
                my $item_lc = lc($current_item);
                my $item_uc = uc($current_item);
                push @extreg_entries, "extern andla_${item_lc}_reg_s        *andla_${item_lc}_reg_p;\n";  
                @buffer_extreg = ();
            }
            $current_item = $item;
            %seen_entries = ();
        }
        push @buffer_extreg, "    __IO uint32_t $entry;";
    }
}
if (@buffer_extreg) {
    my $item_lc = lc($current_item);
    my $item_uc = uc($current_item);
    push @extreg_entries, "extern andla_${item_lc}_reg_s        *andla_${item_lc}_reg_p;\n";  
}
close $extreg_reg;


# (8) 針對 dest  的部分
open my $dest_reg, '<', $reg_file or die "Cannot open $reg_file: $!";

$current_item = '';
my ($dest, $subdest);
my $current_id = 0;
while (my $line = <$dest_reg>) {
    chomp $line;
    # 只處理有 Item, Register, SubRegister 的行
    if ($line =~ /'Item':\s*'(\w+)',\s*'Register':\s*'(\w+)',\s*'SubRegister':\s*(?:'(\w+)'|nan)/) {
        my ($item, $register, $subreg) = ($1, $2, $3);
        my $id;
        # 忽略同一 item 已經處理過的第一筆
        next if $seen_entries{$item}++;
        if ($line =~ /'ID':\s*(\d+)/) {
            $id = int($1);
        }

        # 如果是新 item，先 flush 掉上一個 item 的 buffer
        if ($item ne $current_item) {
            if (@buffer_dest) {
                push @dest_entries,
                    "#define " . $current_item . "_DEST               (0x1 <<  " . $current_id . ")\n";
                if ($id - $current_id > 1) {
                    for (my $idx = $current_id+1; $idx < $id; $idx++) {
                        push @dest_entries,
                            "#define RESERVED_" . $idx . "_DEST               (0x1 <<  " . $idx . ")\n";

                    }
                }

                @buffer_dest = ();
            }
            $current_item = $item;
            %seen_entries = ();    # 為下一個 item 重置 duplicate 判斷

            # 現在才抓這個新 item 的第一個 Physical Address
            if ($line =~ /'Physical Address':\s*'(\w+)'/) {
                $dest    = $1;
                $subdest = substr($dest, -3);
            }
        }
        
        push @buffer_dest, $item;
        $current_id = $id;
    }
}

# loop 結束後，別忘了把最後一個 item flush 出來
if (@buffer_dest) {
    push @dest_entries,
                    "#define " . $current_item . "_DEST               (0x1 <<  " . $current_id . ")\n";
}

close $dest_reg;



# -------------------------------
# 9 input/andla.tmp.h，將原檔內容與自動生成區段結合
# -------------------------------
my $in_idx_autogen  = 0;
my $in_reg_autogen  = 0;
my $in_base_autogen = 0;
my $in_dest_autogen = 0;
my $in_item_autogen = 0;
my $in_devreg_autogen = 0;
my $in_extreg_autogen = 0;

while (my $line = <$in>) {
    if ($line =~ /^\/\/\s*autogen_idx_start\s*$/) {
        print $out $line;
        $in_idx_autogen = 1;
        foreach my $entry (@idx_entries) {
            print $out "$entry\n";
        }
    } elsif ($in_idx_autogen && $line =~ /^\/\/\s*autogen_idx_stop\s*$/) {
        print $out $line;
        $in_idx_autogen = 0;

    } elsif ($line =~ /^\/\/\s*autogen_reg_start\s*$/) {
        print $out $line;
        $in_reg_autogen = 1;
        foreach my $entry (@reg_entries) {
            print $out "$entry\n";
        }
    } elsif ($in_reg_autogen && $line =~ /^\/\/\s*autogen_reg_stop\s*$/) {
        print $out $line;
        $in_reg_autogen = 0;

    } elsif ($line =~ /^\/\/\s*autogen_base_start\s*$/) {
        print $out $line;
        $in_base_autogen = 1;
        foreach my $entry (@base_entries) {
            print $out "$entry";
        }
    } elsif ($in_base_autogen && $line =~ /^\/\/\s*autogen_base_stop\s*$/) {
        print $out $line;
        $in_base_autogen = 0;
    } elsif ($line =~ /^\/\/\s*autogen_dest_start\s*$/) {
        print $out $line;
        $in_dest_autogen = 1;
        foreach my $entry (@dest_entries) {
            print $out "$entry";
        }
    } elsif ($in_dest_autogen && $line =~ /^\/\/\s*autogen_dest_stop\s*$/) {
        print $out $line;
        $in_dest_autogen = 0;
    } elsif ($line =~ /^\/\/\s*autogen_item_start\s*$/) {
        print $out $line;
        $in_item_autogen = 1;
        foreach my $entry (@item_entries) {
            print $out "$entry";
        }
    } elsif ($in_item_autogen && $line =~ /^\/\/\s*autogen_item_stop\s*$/) {
        print $out $line;
        $in_item_autogen = 0;
    } elsif ($line =~ /^\/\/\s*autogen_devreg_start\s*$/) {
        print $out $line;
        $in_devreg_autogen = 1;
        foreach my $entry (@devreg_entries) {
            print $out "$entry";
        }
    } elsif ($in_devreg_autogen && $line =~ /^\/\/\s*autogen_devreg_stop\s*$/) {
        print $out $line;
        $in_devreg_autogen = 0;
    } elsif ($line =~ /^\/\/\s*autogen_extreg_start\s*$/) {
        print $out $line;
        $in_extreg_autogen = 1;
        foreach my $entry (@extreg_entries) {
            print $out "$entry";
        }
    } elsif ($in_extreg_autogen && $line =~ /^\/\/\s*autogen_extreg_stop\s*$/) {
        print $out $line;
        $in_extreg_autogen = 0;
    } else {
        print $out $line;
    }
}

# Close filehandles
close $in;
close $out;
