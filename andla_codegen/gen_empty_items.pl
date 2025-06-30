#!/usr/bin/env perl
use strict;
use warnings;

# 原始檔案
my $input_file = './output/andla_empty.v';

# 在這裡填入你要的子字串清單
my @subs = qw(cdma ldma sdma ldma2 csr fme0);

# 為了避免 ldma 和 ldma2 互相誤判，分別編譯不同的正規表示式
my %patterns;
foreach my $s (@subs) {
    if ($s eq 'ldma') {
        # 只匹配 ldma 而不匹配 ldma2
        $patterns{$s} = qr/ldma(?!2)/i;
    } else {
        $patterns{$s} = qr/\Q$s\E/i;
    }
}

# 針對每個子字串，產生一份對應的檔案
foreach my $keep (@subs) {
    my $out_file = "./output/andla_${keep}.empty.v";
    open my $in_fh,  '<', $input_file
        or die "Cannot open '$input_file': $!";
    open my $out_fh, '>', $out_file
        or die "Cannot write '$out_file': $!";

    while (<$in_fh>) {
        my $line = $_;

        # 先處理 module 名稱：module andla_empty (  → module andla_empty_<keep> (
        if ($line =~ /^\s*module\s+andla_empty\s*\(/i) {
            $line =~ s/andla_empty/andla_$keep/i;
        }

        # 檢查是否包含「其他」關鍵字，若是就跳過不寫入
        my $skip = 0;
        for my $sub (@subs) {
            next if $sub eq $keep;
            if ($line =~ $patterns{$sub}) {
                $skip = 1;
                last;
            }
        }
        next if $skip;

        print $out_fh $line;
    }

    close $in_fh;
    close $out_fh;
    print "Generated $out_file\n";
}

print "All done.\n";

