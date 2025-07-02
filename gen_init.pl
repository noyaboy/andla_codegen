#!/usr/bin/perl
use strict;
use warnings;

# Define file paths
my $input_file = 'input/regfile_init.tmp.h';
# my $output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla_common.c';
my $output_file = 'output/regfile_init.h';
my $reg_file = 'output/regfile_dictionary.log';

# Open input and output files
open my $in, '<', $input_file or die "Cannot open $input_file: $!";
open my $out, '>', $output_file or die "Cannot open $output_file: $!";

# Flag to track if we're between autogen_start and autogen_stop
my $in_autogen = 0;

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
            my $default = $data{'Default Value'};
            my $type = $data{'Type'};
            my $index_name = ( $subregister eq 'nan' or ( $subregister ne 'nan' and ($subregister ne 'LSB' and $subregister ne 'MSB') ) )? 
                    "${item}_${register}": "${item}_${register}_${subregister}";

            $seen_sub{"${item}_${register}"} = 0 if !exists ( $seen_sub{"${item}_${register}"} );
            
            next if $type ne 'RW';
            if ( $subregister ne 'nan'
              && $subregister ne 'LSB'
              && $subregister ne 'MSB' )
            {
                next if $seen_sub{"${item}_${register}"} eq 1;
                $seen_sub{"${item}_${register}"} = 1;
            }

            my $final_register = ( $subregister eq 'nan' or ( $subregister ne 'nan' and ($subregister ne 'LSB' and $subregister ne 'MSB') ) )? 
                    "${item}_${register}": "${item}_${register}_${subregister}";
            
            # 轉換 `item` 和 `register` 為小寫
            my $item_lower = lc($item);

            my $register_lower = ( $subregister eq 'nan' or ( $subregister ne 'nan' and ($subregister ne 'LSB' and $subregister ne 'MSB') ) )? 
                    lc(${register}): lc("${register}_${subregister}");
            print $out format_line("    regfile->item[$item].reg[$final_register].data", $default);
        }
        close $reg;
    } elsif ($in_autogen && $line =~ /^\/\/\s*autogen_stop\s*$/) {

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

