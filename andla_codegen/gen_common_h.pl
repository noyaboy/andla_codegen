#!/usr/bin/perl
use strict;
use warnings;

# Define file paths
my $input_file = 'input/andla_common.tmp.h';
# my $output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla_common.c';
my $output_file = 'output/andla_common.h';
my $reg_file = 'output/regfile_dictionary.log';

# Open input and output files
open my $in, '<', $input_file or die "Cannot open $input_file: $!";
open my $out, '>', $output_file or die "Cannot open $output_file: $!";

# Flag to track if we're between autogen_start and autogen_stop
my $in_autogen = 0;

# 用來統計各個 item 出現的次數
my %item_count;

# 設定 "=" 的目標對齊位置
my $target_equal_pos = 82;

# Function: 將 `=` 之前的字串對齊到 $target_equal_pos
sub format_line {
    my ($prefix, $value) = @_;
    my $prefix_length = length($prefix);
    my $spaces_needed = $target_equal_pos - $prefix_length;
    $spaces_needed = 1 if $spaces_needed < 1;  # 確保至少有 1 個空格
    return $prefix . (' ' x $spaces_needed) . "= " . $value . ";\n";
}
sub replace_clog2 {
    my ($str) = @_;
    $str =~ s/\$clog2\((\d+)\)/ _calc_clog2($1) /eg;
    return $str;
}

# 輔助函數：輸入必是 2 的次方，回傳對應的指數
sub _calc_clog2 {
    my $n = shift;
    die "'$n' 不是 2 的次方！" unless $n > 0 && ($n & ($n-1)) == 0;

    my $exp = 0;
    # 不斷右移直到 n==1，次數即為 log2 原值
    $exp++ while $n > 1 && ($n >>= 1);
    return $exp;
}
# 讀取檔案並解析 define
sub parse {
    my ($file1, $file2) = @_;
    open my $fh1, '<', $file1
      or die "無法開啟檔案 '$file1': $!";

    my %defines;

    while (my $line = <$fh1>) {
        chomp $line;

        if ($line =~ /^`define\s+(\w+)\s+(\d+)\b/) {
            my ($name, $val) = ($1, $2);
            $defines{$name} = $val;
        }
    }

    close $fh1;
    open my $fh2, '<', $file2
      or die "無法開啟檔案 '$file2': $!";


    while (my $line = <$fh2>) {
        chomp $line;

        if ($line =~ /^`define\s+(\w+)\s+(\d+)\b/) {
            my ($name, $val) = ($1, $2);
            $defines{$name} = $val;
        }
    }

    close $fh2;
    return \%defines;  # 回傳 hash reference
}

# Process the input file line by line
while (my $line = <$in>) {
    if ($line =~ /^\/\/\s*autogen_start\s*$/) {
        # Write the autogen_start line
        print $out $line;
        $in_autogen = 1;

        my %seen_sub = ();

        # Insert contents of regfile_dictionary.log in the new format
        open my $reg, '<', $reg_file or die "Cannot open $reg_file: $!";
        while (my $reg_line = <$reg>) {
            chomp $reg_line; # Remove newline
            
            # 解析 Python 字典格式
            my %data;
            while ($reg_line =~ /'([^']+)': '([^']+)'/g) {
                $data{$1} = $2;
            }
            # 提取必要的字段
            my $item = $data{'Item'} // 'UNKNOWN';
            my $register = $data{'Register'} // 'UNKNOWN';
            my $subregister = $data{'SubRegister'} // 'nan';  # 讀取 SubRegister
            my $index_name = ( $subregister eq 'nan' or ( $subregister ne 'nan' and ($subregister ne 'LSB' and $subregister ne 'MSB') ) )? 
                    "${item}_${register}": "${item}_${register}_${subregister}";
            my $bitwidth = 0;

            $seen_sub{"${item}_${register}"} = 0 if !exists ( $seen_sub{"${item}_${register}"} );
            
            if ( $subregister ne 'nan'
              && $subregister ne 'LSB'
              && $subregister ne 'MSB' )
            {
                next if $seen_sub{"${item}_${register}"} eq 1;
                $seen_sub{"${item}_${register}"} = 1;
            }
            # 計算 Bit Locate 位寬
            if ($data{'Bit Locate'} && $data{'Bit Locate'} =~ /\[([0-9]+):([0-9]+)\]/) {
                my ($high_bit, $low_bit) = ($1, $2);
                $bitwidth = $high_bit - $low_bit + 1;
            }

            my $final_register = ( $subregister eq 'nan' or ( $subregister ne 'nan' and ($subregister ne 'LSB' and $subregister ne 'MSB') ) )? 
                    "${item}_${register}": "${item}_${register}_${subregister}";
            
            # 轉換 `item` 和 `register` 為小寫
            my $item_lower = lc($item);

            my $register_lower = ( $subregister eq 'nan' or ( $subregister ne 'nan' and ($subregister ne 'LSB' and $subregister ne 'MSB') ) )? 
                    lc(${register}): lc("${register}_${subregister}");
            
            if ( defined $data{'Bitwidth configuare'}) {
                if (substr($data{'Bitwidth configuare'}, 0, 1) eq '`' or substr($data{'Bitwidth configuare'}, 0, 1) eq '$' ) {
                    # 已經取得的 hashref
                    my $defs = parse('./output/andla.vh', './output/andla_config.vh');
                    
                    # 原始字串
                    my $str = $data{'Bitwidth configuare'};
                    
                    # 先把所有 define key 拼成一個正規表達式
                    my $keys_rx = join '|', map { quotemeta } keys %$defs;
                    
                    # 找到首個出現的 key（可帶或不帶前導 `）並做替換
                    $str =~ s/`?($keys_rx)/$defs->{$1}/ge;
                    $str = replace_clog2($str);
                    # 如果整個 $str 都是由數字和 + - * / 組成，直接計算出結果
                    if ( $str =~ /^[\d+\-*\/]+$/ ) {
                        my $result = eval $str;
                        die "Invalid expression '$str': $@" if $@;
                        $str = $result;
                    }                   
                    # 最後把處理後的 $str 傳給 format_line
                    print $out format_line(
                        "    reg_file->item[$item].reg[$final_register].bitwidth",
                        $str
                    );
                }
                else {
                    print $out format_line("    reg_file->item[$item].reg[$final_register].bitwidth", $bitwidth);
                }
            }
            else {
                print $out format_line("    reg_file->item[$item].reg[$final_register].bitwidth", $bitwidth);
            }

            print $out format_line("    reg_file->item[$item].reg[$final_register].index", $index_name);
            print $out format_line("    reg_file->item[$item].reg[$final_register].phy_addr", "&(andla_${item_lower}_reg_p->$register_lower)");
            print $out "\n";
        }
        close $reg;
    } elsif ($in_autogen && $line =~ /^\/\/\s*autogen_stop\s*$/) {

        my %seen_item;
        open my $reg, '<', $reg_file or die "Cannot open $reg_file: $!";
        while (my $reg_line = <$reg>) {
            # 解析 Python 字典格式
            my %data;
            while ($reg_line =~ /'([^']+)': '([^']+)'/g) {
                $data{$1} = $2;
            }
            # 提取必要的字段
            my $item = $data{'Item'};
            $seen_item{$item} = 0 if ! defined $seen_item{$item};
            next if $seen_item{$item} eq 1;
            $seen_item{$item} = 1;
        }

        while (my ($key, $value) = each %seen_item) {
            my $low_key = lc($key);
            print $out format_line("    reg_file->item[$key].id", $key);
            print $out format_line("    reg_file->item[$key].base_addr_ptr", "andla_${low_key}_reg_p");
            print $out format_line("    reg_file->item[$key].reg_num", "0");
            
            print $out "\n";
        }

        # Write the autogen_stop line and exit autogen section
        print $out $line;
        $in_autogen = 0;
    } elsif (!$in_autogen) {
        # Write lines outside the autogen section
        print $out $line;
    }
}

# Close filehandles
close $in;
close $out;

