#!/usr/bin/perl
use strict;
use warnings;

# Define file paths
my $input_file = 'input/regfile_map.tmp.h';
# my $output_file = '../../../../andes_vip/patterns/andeshape/andla/common/program/andla.h';
my $output_file = 'output/regfile_map.h';
my $reg_file = 'output/regfile_dictionary.log';

# Open input and output files
open my $in, '<', $input_file or die "Cannot open $input_file: $!";
open my $out, '>', $output_file or die "Cannot open $output_file: $!";

my @dest_entries;
my @buffer_dest;
my %seen_entries;
# (8) 針對 dest  的部分
open my $dest_reg, '<', $reg_file or die "Cannot open $reg_file: $!";

my $current_item = '';
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
my $in_dest_autogen = 0;
while (my $line = <$in>) {

    if ($line =~ /^\/\/\s*autogen_dest_start\s*$/) {
        print $out $line;
        $in_dest_autogen = 1;
        foreach my $entry (@dest_entries) {
            print $out "$entry";
        }
    } elsif ($in_dest_autogen && $line =~ /^\/\/\s*autogen_dest_stop\s*$/) {
        print $out $line;
        $in_dest_autogen = 0;
    } else {
        print $out $line;
    }
}

# Close filehandles
close $in;
close $out;
