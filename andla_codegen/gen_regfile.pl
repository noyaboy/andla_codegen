#!/usr/bin/perl
use strict;
use warnings;

#─┐
#│  Author Information
#│  Author      : Hao Chun (Noah) Liang
#│  Affiliation : Bachelor of EE, National Tsing Hua University
#│  Position    : CA Group RD-CA-CAA Intern
#│  Email       : science103555@gmail.com
#│  Date        : 2024/12/31 (Tuesday)
#│  Description : Automatic Code Generation for the AnDLA
#│                Register File RTL code.
#└────────────────────────────────────────────────────────────────────

# 檔案路徑設定
my $input_filename       = 'input/andla_regfile.tmp.v';
my $output_filename      = 'output/andla_regfile.v';
our $dictionary_filename = 'output/regfile_dictionary.log';

###########################################
# InterruptWriter package
############################################
{
    package InterruptWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_interrupt {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($key eq 'ldma2' || $key eq 'csr') {
            
            } 
            else {
                print { $self->{outfile} }
           "                          (${key}_except & ${key}_except_mask) |\n" 
            }

            $current_value = $value;
        }

        close($dict_fh);
    }
    1;
}
###########################################
# ExceptwireWriter package
############################################
{
    package ExceptwireWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_exceptwire {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($key eq 'ldma2' || $key eq 'csr') {
            
            } 
            else {
                print { $self->{outfile} }
"wire ${key}_except        = csr_status_reg[`${uckey}_ID + 8];\n"
            }

            $current_value = $value;
        }

        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($key eq 'ldma2' || $key eq 'csr') {
            
            } 
            else {
                print { $self->{outfile} }
"wire ${key}_except_mask   = csr_control_reg[`${uckey}_ID + 8];\n"
            }

            $current_value = $value;
        }

        close($dict_fh);
    }
    1;
}

############################################
# ExceptportWriter package
############################################
{
    package ExceptioWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_exceptio {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($key eq 'ldma2' || $key eq 'csr') {
            
            } 
            else {
                print { $self->{outfile} }
                    "input                 rf_${key}_except_trigger;\n"
            }

            $current_value = $value;
        }


        close($dict_fh);
    }
    1;
}

############################################
# ExceptportWriter package
############################################
{
    package ExceptportWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_exceptport {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($key eq 'ldma2' || $key eq 'csr') {
            
            } 
            else {
                print { $self->{outfile} }
                    ",rf_${key}_except_trigger\n"
            }

            $current_value = $value;
        }


        close($dict_fh);
    }
    1;
}

############################################
# RiurwaddrWriter package
############################################
{
    package RiurwaddrWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_riurwaddr {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($current_value - $value > 1) {
                for (my $idx = $current_value - 1; $idx > $value; $idx--) {
                    print { $self->{outfile} }
                    "wire riurwaddr_bit${idx}                      = 1'b0;\n"
                }
            }

            if ($key eq 'csr') {
                print { $self->{outfile} }
                    "wire riurwaddr_bit${value}                      = 1'b0;\n"
            } else {
                print { $self->{outfile} }
                    "wire riurwaddr_bit${value}                      = (issue_rf_riurwaddr[(RF_ADDR_BITWIDTH-1) -: ITEM_ID_BITWIDTH] == `${uckey}_ID);\n"
            }
            $current_value = $value;
        }


        close($dict_fh);
    }
    1;
}

############################################
# StatusnxWriter package
############################################
{
    package StatusnxWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_statusnx {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($current_value - $value > 1) {
                for (my $idx = $current_value - 1; $idx > $value; $idx--) {
                    print { $self->{outfile} }
                        "assign csr_status_nx[$idx]                = 1'b0;\n"
                }
            }

            if ($key eq 'csr') {
                print { $self->{outfile} }
                    "assign csr_status_nx[0]                = (wr_taken & sfence_en[0]  ) ? 1'b1 : scoreboard[0];\n"
            } else {
                print { $self->{outfile} }
                    "assign csr_status_nx[`${uckey}_ID]         = (wr_taken & sfence_en[`${uckey}_ID]  ) ? 1'b1 : scoreboard[`${uckey}_ID];\n"
            }
            $current_value = $value;
        }
        $entrance = 0;
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($current_value - $value > 1) {
                for (my $idx = $current_value - 1; $idx > $value; $idx--) {
                    print { $self->{outfile} }
                        "assign csr_status_nx[$idx + 8]                       = 1'b0;\n"
                }
            }

            if ($key eq 'csr') {
                print { $self->{outfile} }
                    "assign csr_status_nx[8]                           = 1'b0;\n"
                }
            elsif ($key eq 'ldma2') {
                print { $self->{outfile} }
                    "assign csr_status_nx[`${uckey}_ID + 8]                = rf_ldma_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`${uckey}_ID + 8] : csr_status_reg[`${uckey}_ID + 8];\n"
            } else {
                print { $self->{outfile} }
                    "assign csr_status_nx[`${uckey}_ID + 8]                = rf_${key}_except_trigger ? 1'b1 : (wr_taken & csr_status_en) ? issue_rf_riuwdata[`${uckey}_ID + 8] : csr_status_reg[`${uckey}_ID + 8];\n"
            }
            $current_value = $value;
        }


        close($dict_fh);
    }
    1;
}



############################################
# SfenceenWriter package
############################################
{
    package SfenceenWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_sfenceen {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($current_value - $value > 1) {
                for (my $idx = $current_value - 1; $idx > $value; $idx--) {
                    print { $self->{outfile} }
                        "               1'b0,\n"
                }
            }

            if ($key eq 'csr') {
                print { $self->{outfile} }
                    "               1'b0\n"
            } 
            elsif ($key eq 'ldma2') {
                print { $self->{outfile} }
                    "               1'b0,\n"
            } 
            else {
                print { $self->{outfile} }
                    "               ${key}_sfence_en,\n"
            }

            $current_value = $value;
        }


        close($dict_fh);
    }
    1;
}


############################################
# ScoreboardWriter package
############################################
{
    package ScoreboardWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_item => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_scoreboard {
        my ($self) = @_;
        my $current_value;
        my $entrance = 0;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            my $item;
            my $id;
            if ($line =~ /'Item': '([^']*)'/) {
                $item     = lc($1);
                if ($line =~ /'ID':\s*(\d+),/) {
                    $id = int($1);
                }
                $self->{seen_item}->{$item} = $id;
            }
        }
        foreach my $key (
            sort { $self->{seen_item}{$b} <=> $self->{seen_item}{$a} }
            keys %{ $self->{seen_item} }
        ) {
            my $value = $self->{seen_item}{$key};
            my $uckey = uc($key);
            if ($entrance eq 0) {
                $entrance = 1;
                $current_value = $value;
            }
            if ($current_value - $value > 1) {
                for (my $idx = $current_value - 1; $idx > $value; $idx--) {
                    print { $self->{outfile} }
                        "assign scoreboard[$idx]               = 1'b0;\n"
                }
            }

            if ($key eq 'csr') {
                print { $self->{outfile} }
                    "assign scoreboard[$value]               = (ip_rf_status_clr[0]) ? 1'b0 : csr_status_reg[0];\n"
            } else {
                print { $self->{outfile} }
                    "assign scoreboard[$value]               = (ip_rf_status_clr[`${uckey}_ID]) ? 1'b0 : csr_status_reg[`${uckey}_ID];\n"
            }

            $current_value = $value;
        }


        close($dict_fh);
    }
    1;
}

############################################
# BaseaddrselbitwidthWriter package
############################################
{
    package BaseaddrselbitwidthWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_dma => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_baseaddrselbitwidth {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)'/) {
                my $item     = lc($1);
                next if (index($item, 'dma') == -1 || $item eq 'ldma2');
                $self->{seen_dma}->{$item} = 1;
            }
        }
        foreach my $keys ( keys %{ $self->{seen_dma}  }  ) {
            my $uckeys = uc($keys);
            print {$self->{outfile}} "localparam ${uckeys}_BASE_ADDR_SELECT_BITWIDTH = 3;\n"
        }

        close($dict_fh);
    }
    1;
}
############################################
# BaseaddrselioWriter package
############################################
{
    package BaseaddrselioWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_dma => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_baseaddrselio {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)'/) {
                my $item     = lc($1);
                next if (index($item, 'dma') == -1 || $item eq 'ldma2');
                $self->{seen_dma}->{$item} = 1;
            }
        }
        foreach my $keys ( keys %{ $self->{seen_dma}  }  ) {
            my $uckeys = uc($keys);
            print {$self->{outfile}} "output [${uckeys}_BASE_ADDR_SELECT_BITWIDTH-           1:0] ${keys}_base_addr_select;\n"
        }

        close($dict_fh);
    }
    1;
}
############################################
# BaseaddrselportWriter package
############################################
{
    package BaseaddrselportWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_dma => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_baseaddrselport {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)'/) {
                my $item     = lc($1);
                next if (index($item, 'dma') == -1 || $item eq 'ldma2');
                $self->{seen_dma}->{$item} = 1;
            }
        }
        foreach my $keys ( keys %{ $self->{seen_dma}  }  ) {
            my $uckeys = uc($keys);
            print {$self->{outfile}} ",${keys}_base_addr_select\n"
        }

        close($dict_fh);
    }
    1;
}

############################################
# BaseaddrselWriter package
############################################
{
    package BaseaddrselWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_dma => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_baseaddrsel {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)'/) {
                my $item     = lc($1);
                next if (index($item, 'dma') == -1 || $item eq 'ldma2');
                $self->{seen_dma}->{$item} = 1;
            }
        }
        foreach my $keys ( keys %{ $self->{seen_dma}  }  ) {
            my $uckeys = uc($keys);
            print {$self->{outfile}} "
wire [${uckeys}_BASE_ADDR_SELECT_BITWIDTH-1:0] ${keys}_base_addr_select_nx;
assign  ${keys}_base_addr_select_nx           = ${keys}_sfence_nx[20:18];
wire ${keys}_base_addr_select_en           = wr_taken & ${keys}_sfence_en;
reg  [${uckeys}_BASE_ADDR_SELECT_BITWIDTH-1:0] ${keys}_base_addr_select_reg;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n)                        ${keys}_base_addr_select_reg <= {(${uckeys}_BASE_ADDR_SELECT_BITWIDTH){1'd0}};
    else if (${keys}_base_addr_select_en) ${keys}_base_addr_select_reg <= ${keys}_base_addr_select_nx;
end
assign ${keys}_base_addr_select            = ${keys}_base_addr_select_reg;\n\n"
        }

        close($dict_fh);
    }
    1;
}



############################################
# SfenceWriter package
############################################
{
    package SfenceWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_sfence => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_sfence {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
                my $item     = lc($1);
                my $register = lc($2);
                next if (${register} ne 'sfence');
                $self->{seen_sfence}->{$item} = 1;
            }
        }
        foreach my $keys ( keys %{ $self->{seen_sfence}  }  ) {
            print {$self->{outfile}} "wire ${keys}_start_reg_nx = wr_taken & ${keys}_sfence_en;
reg  ${keys}_start_reg;
wire ${keys}_start_reg_en = ${keys}_start_reg ^ ${keys}_start_reg_nx;
always @(posedge clk or negedge rst_n) begin
    if (~rst_n) ${keys}_start_reg <= 1'b0;
    else if (${keys}_start_reg_en) ${keys}_start_reg <= ${keys}_start_reg_nx;
end
assign rf_${keys}_sfence = ${keys}_start_reg;\n\n"
        }

        close($dict_fh);
    }
    1;
}

############################################
# IpnumWriter package
############################################
{
    package IpnumWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_items => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_ipnum {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
                my $item     = lc($1);
                my $register = lc($2);
                my $key = "${item}";
                next if (exists $self->{seen_items}->{$key});
                #print {$self->{outfile}} ", ${item}_${register}\n";
                $self->{seen_items}->{$key} = 1;
            }
        }
        #print {$self->{outfile}} "localparam IP_NUM = ", scalar keys %{ $self->{seen_items} }, ";\n";
        print {$self->{outfile}} "localparam ITEM_ID_NUM = `ITEM_ID_NUM;\n";
        close($dict_fh);
    }
    1;
}


############################################
# PortWriter package
############################################
{
    package PortWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_items => {},
            outfile    => $outfile,
        };
        bless $self, $class;
        return $self;
    }

    sub write_port {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
                my $item     = lc($1);
                my $register = lc($2);
                my $type; 
                if ($line =~ /'Type': '([^']*)'/) {
                    $type     = lc($1);
                }

                next if ($item eq 'csr' && ($type ne 'rw' || $register eq 'counter' || $register eq 'counter_mask' || $register eq 'status' || $register eq 'control'  ) );
                my $key = "${item}_$register";
                next if (exists $self->{seen_items}->{$key});
                print {$self->{outfile}} ", rf_${item}_${register}\n";
                $self->{seen_items}->{$key} = 1;
            }
        }
        close($dict_fh);
    }
    1;
}

############################################
# BitwidthWriter package
############################################
{
    package BitwidthWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_items      => {},
            seen_cases      => {},
            bitwidth_lines  => [],
            outfile         => $outfile,
            item            => '',
            register        => '',
            subregister     => '',
            key             => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}        = uc($1);
            $self->{register}    = uc($2);
            $self->{subregister} = uc($3);
            $self->{key}         = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = uc($1);
            $self->{register} = uc($2);
            $self->{subregister} = '';
            $self->{key}         = $self->{item} . "_" . $self->{register};
        }
    }

    sub _process_sub {
        my ($self) = @_;

        if ($self->{subregister} ne 'MSB' && $self->{subregister} ne 'LSB') {
            return if exists $self->{seen_cases}->{$self->{item}, $self->{register}};

            push @{$self->{bitwidth_lines}},
              "localparam $self->{item}_$self->{register}_BITWIDTH = `".$self->{item}."_".$self->{register}."_BITWIDTH;";
            $self->{seen_cases}->{$self->{item}, $self->{register}} = 1;
        }
        elsif (!exists $self->{seen_items}->{$self->{key}."_".$self->{subregister}}) {
            push @{$self->{bitwidth_lines}},
            "localparam $self->{item}_$self->{register}_$self->{subregister}_BITWIDTH = `".$self->{item}."_".$self->{register}."_".$self->{subregister}."_BITWIDTH;";
            $self->{seen_items}->{$self->{key}."_".$self->{subregister}} = 1;

            if ($self->{subregister} eq 'MSB') {
                push @{$self->{bitwidth_lines}},
                "localparam $self->{item}_$self->{register}_BITWIDTH = `".$self->{item}."_".$self->{register}."_BITWIDTH;";
            }
        }
    }

    sub _process_re {
        my ($self) = @_;
        if (! exists $self->{seen_items}->{$self->{key}}) {
            if ($self->{register} eq 'CREDIT') {
                push @{$self->{bitwidth_lines}},
                  "localparam $self->{item}_$self->{register}_BITWIDTH = 22;";
                $self->{seen_items}->{$self->{key}} = 1;
            } else {
                push @{$self->{bitwidth_lines}},
                  "localparam $self->{item}_$self->{register}_BITWIDTH = `".$self->{item}."_".$self->{register}."_BITWIDTH;";
                $self->{seen_items}->{$self->{key}} = 1;
            }
        }
    }

    sub write_bitwidth {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{subregister} ne '') {
                $self->_process_sub();
            }
            elsif ($self->{register} ne '') {
                $self->_process_re();
            }
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $l (@{$self->{bitwidth_lines}}) {
            my ($left, undef) = split(/=/, $l, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        foreach my $l (@{$self->{bitwidth_lines}}) {
            my ($left, $right) = split(/=/, $l, 2);
            printf {$self->{outfile}} "%-*s = %s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# IOWriter package
############################################
{
    package IOWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            seen_items => {},
            io_lines   => [],
            outfile    => $outfile,
            item       => '',
            register   => '',
            key        => '',
            type       => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }
        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type} = lc($1);
        }
    }

    sub _skip {
        my ($self) = @_;
        return 1 if ($self->{item} eq 'csr' && ($self->{type} ne 'rw' || $self->{register} eq 'counter' || $self->{register} eq 'counter_mask' || $self->{register} eq 'status' || $self->{register} eq 'control'  ) );
        return 1 if (exists $self->{seen_items}->{$self->{key}});
        return 0;
    }

    sub _process {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{type} eq 'ro') {
                push @{$self->{io_lines}}, "input\t" . " [" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-1:0] rf_" . $self->{item} . "_" . $self->{register} . ";";
                $self->{seen_items}->{$self->{key}} = 1;
            }
            else {
                if ($self->{register} eq 'sfence') {
                    push @{$self->{io_lines}}, "output\t" . " [1-1:0] rf_" . $self->{item} . "_" . $self->{register} . ";";
                    $self->{seen_items}->{$self->{key}} = 1;
                } else { 
                    push @{$self->{io_lines}}, "output\t" . " [" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-1:0] rf_" . $self->{item} . "_" . $self->{register} . ";";
                    $self->{seen_items}->{$self->{key}} = 1;
                }
            }
        }
    }



    sub write_io {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            $self->_process();
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $l (@{$self->{io_lines}}) {
            my ($left, undef) = split(/\t/, $l, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        foreach my $l (@{$self->{io_lines}}) {
            my ($left, $right) = split(/\t/, $l, 2);
            printf {$self->{outfile}} "%-*s\t%s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# RegWriter package
############################################
{
    package RegWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            reg_lines  => [],
            seen_items => {},
            seen_cases => {},
            outfile    => $outfile,
            item       => '',
            register   => '',
            subregister=> '',
            key        => '',
            type       => ''
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= lc($3);
            $self->{key}        = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }

        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type}     = lc($1)
        }

    }

    sub _skip {
        my ($self) = @_;
        #return 1 if ( ($self->{type} ne 'rw' && $self->{item} ne 'csr') || ($self->{type} eq 'wo') );
        return 1 if ( ($self->{type} ne 'rw') );
        return 0;
    }

    sub _process_sub {
        my ($self) = @_;
        unless ($self->_skip()) {
            
            if ($self->{subregister} eq 'lsb' || $self->{subregister} eq 'msb') {
                push @{$self->{reg_lines}},
                "reg\t[".uc($self->{item})."_".uc($self->{register})."_".uc($self->{subregister})."_BITWIDTH-1:0] ".
                $self->{item}."_".$self->{register}."_".$self->{subregister}."_reg;";
                return;
            } 
            elsif (!exists $self->{seen_items}->{$self->{key}}) {
                push @{$self->{reg_lines}},
                "reg\t[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-1:0] ".
                $self->{item}."_".$self->{register}."_reg;";
                $self->{seen_items}->{$self->{key}} = 1;
            }
        }
    }

    sub _process_re {
        my ($self) = @_;
        unless ($self->_skip()) {
            push @{$self->{reg_lines}},
              "reg\t[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-1:0] ".
              $self->{item}."_".$self->{register}."_reg;";
        }
    }

    sub write_reg {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{subregister} ne '') {
                $self->_process_sub();
            }
            elsif ($self->{register} ne '') {
                $self->_process_re();
            }
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $l (@{$self->{reg_lines}}) {
            my ($left, undef) = split(/\] /, $l, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        foreach my $l (@{$self->{reg_lines}}) {
            my ($left, $right) = split(/\] /, $l, 2);
            printf {$self->{outfile}} "%-*s] \t%s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# WireNxWriter package
############################################
{
    package WireNxWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            wire_lines       => [],
            seen_items       => {},
            outfile          => $outfile,
            item             => '',
            register         => '',
            subregister      => '',
            key              => '',
            item_upper       => '',
            register_upper   => '',
            subregister_upper=> '',
            type             => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}        = lc($1);
            $self->{register}    = lc($2);
            $self->{subregister} = lc($3);
            $self->{key}         = $self->{item} . "_" . $self->{register};
            $self->{item_upper}  = uc($self->{item});
            $self->{register_upper} = uc($self->{register});
            $self->{subregister_upper}= uc($self->{subregister});
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= '';
            $self->{key}        = $self->{item} . "_" . $self->{register};
            $self->{item_upper} = uc($self->{item});
            $self->{register_upper} = uc($self->{register});
            $self->{subregister_upper} = '';
        }

        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type} = lc($1)
        }

    }

    sub _skip {
        my ($self) = @_;
        return 1 if ( ($self->{type} ne 'rw') );
        if ( ($self->{subregister} ne 'msb' && $self->{subregister} ne 'lsb' )
            and exists $self->{seen_items}->{$self->{key}}) {
            return 1;
        }
        $self->{seen_items}->{$self->{key}} = 1;
        return 0;
    }

    sub _process_sub {
        my ($self) = @_;
        unless ($self->_skip()) {

            if ($self->{subregister} eq 'lsb' || $self->{subregister} eq 'msb') {
                push @{$self->{wire_lines}},
                "wire\t[".$self->{item_upper}."_".$self->{register_upper}."_".$self->{subregister_upper}."_BITWIDTH-1:0] ".
                $self->{item}."_".$self->{register}."_".$self->{subregister}."_nx;";
                return;
            }
            else {
                push @{$self->{wire_lines}},
                "wire\t[".$self->{item_upper}."_".$self->{register_upper}."_BITWIDTH-1:0] ".
                $self->{item}."_".$self->{register}."_nx;";
            }
        }
    }

    sub _process_re {
        my ($self) = @_;
        unless ($self->_skip()) {
            push @{$self->{wire_lines}},
              "wire\t[".$self->{item_upper}."_".$self->{register_upper}."_BITWIDTH-1:0] ".
              $self->{item}."_".$self->{register}."_nx;";
        }
    }

    sub write_wire_nx {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{subregister} ne '') {
                $self->_process_sub();
            }
            elsif ($self->{register} ne '') {
                $self->_process_re();
            }
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $l (@{$self->{wire_lines}}) {
            my ($left, undef) = split(/\] /, $l, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        foreach my $l (@{$self->{wire_lines}}) {
            my ($left, $right) = split(/\] /, $l, 2);
            printf {$self->{outfile}} "%-*s]   %s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# WireEnWriter package
############################################
{
    package WireEnWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            outfile          => $outfile,
            seen_items       => {},
            item             => '',
            register         => '',
            subregister      => '',
            key              => '',
            wire_name        => '',
            type             => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = lc($3);
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }
        
        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type}     = lc($1)
        }
    }

    sub _skip {
        my ($self) = @_;
        if ($self->{subregister} ne 'msb' && $self->{subregister} ne 'lsb') {
                if (exists $self->{seen_items}->{$self->{key}}) {
                    return 1;
                } else {
                    $self->{seen_items}->{$self->{key}} = 1;
                }
        }
        return 1 if ($self->{type} ne 'rw');
        return 0;
    }

    sub _process_sub {
        my ($self) = @_;
        if ($self->{subregister} ne 'msb' and $self->{subregister} ne 'lsb') {
            $self->{wire_name} = $self->{item} . "_" . $self->{register} . "_en";
        } else {
            $self->{wire_name} = $self->{item} . "_" . $self->{register} . "_" . $self->{subregister} . "_en";
        }

    }

    sub _process_re {
        my ($self) = @_;
        $self->{wire_name} = $self->{item} . "_" . $self->{register} . "_en";
    }

    sub write_wire_en {
        my ($self) = @_;
        $self->{seen_items} = {};
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            unless ($self->_skip()) {
                if ($self->{subregister} ne '') {
                    $self->_process_sub();
                    print {$self->{outfile}} "wire   $self->{wire_name};\n";
                }
                else {
                    $self->_process_re();
                    print {$self->{outfile}} "wire   $self->{wire_name};\n";
                }
            }
        }
        close($dict_fh);
    }
    1;
}


############################################
# SeqWriter package
############################################
{
    package SeqWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            outfile    => $outfile,
            reg_lines  => [],
            seen_items => {},
            item       => '',
            register   => '',
            subregister=> '',
            key        => '',
            prefix     => '',
            type       => '',
        };
        bless $self, $class;
        return $self;
    }

    sub _skip {
        my ($self) = @_;
        return 1 if ( ($self->{type} ne 'rw') );
        if (exists $self->{seen_items}->{$self->{key}} and
            ($self->{subregister} ne 'msb' and $self->{subregister} ne 'lsb')) {
            return 1;
        }
        $self->{seen_items}->{$self->{key}} = 1;
        return 0;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= lc($3);
            $self->{key}        = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }
        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type}     = lc($1);

        }
    }

    sub _process_sub {
        my ($self, $line) = @_;
        unless ($self->_skip()) {
            my $default = '';
            if ($line =~ /'Default Value': '([^']*)'/) {
                $default = $1;
            }
            my $final_assignment;
            if ($default =~ /^0x/) {
                $final_assignment = $default;
                $final_assignment =~ s/^0x/32'h/;
            }
            elsif ($self->{subregister} eq 'msb' or $self->{subregister} eq 'lsb') {
                my $final_bit = ($default eq '1') ? "1'b1" : "1'b0";
                $final_assignment = "{ {(" . uc($self->{item}) . "_" . uc($self->{register}) . "_" . uc($self->{subregister}) . "_BITWIDTH-1){1'd0}}, $final_bit }";
            }
            else {
                my $final_bit = ($default eq '1') ? "1'b1" : "1'b0";
                $final_assignment = "{ {(" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-1){1'd0}}, $final_bit }";

            }
            if ($self->{subregister} ne 'lsb' and $self->{subregister} ne 'msb' 
            ) {
                push @{$self->{reg_lines}},
                sprintf("\t\t%-50s<= %s;", $self->{item} . "_" . $self->{register} . "_reg", $final_assignment);
            }
            else {
                push @{$self->{reg_lines}},
                sprintf("\t\t%-50s<= %s;", $self->{item} . "_" . $self->{register} . "_" . $self->{subregister} . "_reg", $final_assignment);
            }
        }
    }

    sub _process_re {
        my ($self, $line) = @_;
        unless ($self->_skip()) {
            my $default = '';
            if ($line =~ /'Default Value': '([^']*)'/) {
                $default = $1;
            }
            my $final_assignment;
            if ($default =~ /^0x/) {
                $final_assignment = $default;
                $final_assignment =~ s/^0x/32'h/;
            }
            else {
                my $final_bit = ($default eq '1') ? "1'b1" : "1'b0";
                $final_assignment = "{ {(" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-1){1'd0}}, $final_bit }";
            }
            push @{$self->{reg_lines}},
              sprintf("\t\t%-50s<= %s;", $self->{item} . "_" . $self->{register} . "_reg", $final_assignment);
        }
    }

    sub write_seq {
        my ($self) = @_;
        print {$self->{outfile}} "always @(posedge clk or negedge rst_n) begin\n";
        print {$self->{outfile}} "    if(~rst_n) begin\n";
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{subregister} ne '') {
                $self->_process_sub($line);
            }
            elsif ($self->{register} ne '') {
                $self->_process_re($line);
            }
        }
        close($dict_fh);
        foreach my $l (@{$self->{reg_lines}}) {
            print {$self->{outfile}} "$l\n";
        }
        print {$self->{outfile}} "    end else begin\n";
        foreach my $l (@{$self->{reg_lines}}) {
            if ($l =~ /<=/) {
                my ($reg_name) = split(/<=/, $l);
                $reg_name =~ s/^\s+|\s+$//g;
                my $wire_name = $reg_name;
                $wire_name =~ s/_reg$/_nx/;
                printf {$self->{outfile}} "\t\t%-48s<= %s;\n", $reg_name, $wire_name;
            }
        }
        print {$self->{outfile}} "    end\n";
        print {$self->{outfile}} "end\n";
    }
    1;
}

############################################
# EnWriter package
############################################
{
    package EnWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            outfile    => $outfile,
            seen_items => {},
            item       => '',
            register   => '',
            subregister=> '',
            key        => '',
            assignment => '',
            type       => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_term {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= lc($3);
            $self->{key}        = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }
        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type}       = lc($1);
        }
    }

    sub _skip {
        my ($self) = @_;

        return 1 if ($self->{type} ne 'rw');

        return 1 if ( exists $self->{seen_items}->{$self->{key}} and
            ($self->{subregister} ne 'msb' and  $self->{subregister} ne 'lsb' )
        );

        $self->{seen_items}->{$self->{key}} = 1;
        return 0;
    }

    sub _process_sub {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{subregister} ne 'msb' and  $self->{subregister} ne 'lsb' 
            ) {          
                $self->{assignment} =
              "assign ".$self->{item}."_".$self->{register}."_en = (issue_rf_riurwaddr == {`".uc($self->{item})."_ID,`".uc($self->{item})."_".uc($self->{register})."_IDX});";
            }
            else {            
                $self->{assignment} =
              "assign ".$self->{item}."_".$self->{register}."_".$self->{subregister}."_en = (issue_rf_riurwaddr == {`".uc($self->{item})."_ID,`".uc($self->{item})."_".uc($self->{register})."_".uc($self->{subregister})."_IDX});";
            }
        }
    }

    sub _process_re {
        my ($self) = @_;
        unless ($self->_skip()) {
            $self->{assignment} =
              "assign ".$self->{item}."_".$self->{register}."_en = (issue_rf_riurwaddr == {`".uc($self->{item})."_ID,`".uc($self->{item})."_".uc($self->{register})."_IDX});";
        }
    }

    sub write_en {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->{assignment} = '';
            $self->fetch_term($line);
            if ($self->{subregister} ne '') {
                $self->_process_sub();
            }
            elsif ($self->{register} ne '') {
                $self->_process_re();
            }
            next if ($self->{assignment} eq '');
            my $equal_index = index($self->{assignment}, '=');
            my $left  = substr($self->{assignment}, 0, $equal_index);
            my $right = substr($self->{assignment}, $equal_index);

            printf {$self->{outfile}} "%-50s%s\n", $left, $right;
        }
        close($dict_fh);
    }
    1;
}

############################################
# NxWriter package
############################################
{
    package NxWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            outfile      => $outfile,
            assignments  => [],
            seen_items   => {},
            item         => '',
            register     => '',
            subregister  => '',
            type         => '',
            key          => '',
            assignment   => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= lc($3);
            $self->{key}        = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }
        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type} = lc($1);
        }
        else {
            $self->{type} = '';
        }
    }

    sub _skip {
        my ($self) = @_;

        return 1 if ( ($self->{type} ne 'rw') );
        if ($self->{register} eq 'status') {
            return 1;
        }
        return 1 if ( exists $self->{seen_items}->{$self->{key}} and
            ($self->{subregister} ne 'msb' and $self->{subregister} ne 'lsb' )
        );
        $self->{seen_items}->{$self->{key}} = 1;

        return 0;
    }

    sub _process_ro {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{register} eq 'credit' and $self->{item} eq 'csr') {
                $self->{assignment} =
                  "assign ".$self->{item}."_".$self->{register}."_nx = sqr_credit;";
                push @{$self->{assignments}}, $self->{assignment};
            } else {
                $self->{assignment} =
                  "assign ".$self->{item}."_".$self->{register}."_nx = { { (32 - ".uc($self->{item})."_".uc($self->{register})."_BITWIDTH) { 1'b0 } }, ".uc($self->{register})."_DATA};";
                push @{$self->{assignments}}, $self->{assignment};
            }
        }
    }

    sub _process_sub {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{register} eq 'const_value' or $self->{register} eq 'ram_padding_value') {
                $self->{assignment} =
                "assign ".$self->{item}."_".$self->{register}."_nx[" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-1:" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-2] = (wr_taken & ".$self->{item}."_".$self->{register}."_en) ? issue_rf_riuwdata[RF_WDATA_BITWIDTH-1:RF_WDATA_BITWIDTH-2] : ".$self->{item}."_".$self->{register}."_reg[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-1:".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-2];";
                push @{$self->{assignments}}, $self->{assignment};
                $self->{assignment} =
                "assign ".$self->{item}."_".$self->{register}."_nx[" . uc($self->{item}) . "_" . uc($self->{register}) . "_BITWIDTH-3:0] = (wr_taken & ".$self->{item}."_".$self->{register}."_en) ? issue_rf_riuwdata[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-3:0]: ".$self->{item}."_".$self->{register}."_reg[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-3:0];";
                push @{$self->{assignments}}, $self->{assignment};
            }
            elsif (
                $self->{subregister} ne 'msb' and $self->{subregister} ne 'lsb'
            ) {                
                $self->{assignment} =
                "assign ".$self->{item}."_".$self->{register}."_nx = (wr_taken & ".$self->{item}."_".$self->{register}."_en) ? issue_rf_riuwdata[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-1:0] : ".$self->{item}."_".$self->{register}."_reg;";
                push @{$self->{assignments}}, $self->{assignment};  
            }
            else {
                $self->{assignment} =
                "assign ".$self->{item}."_".$self->{register}."_".$self->{subregister}."_nx = (wr_taken & ".$self->{item}."_".$self->{register}."_".$self->{subregister}."_en) ? issue_rf_riuwdata[".uc($self->{item})."_".uc($self->{register})."_".uc($self->{subregister})."_BITWIDTH-1:0] : ".$self->{item}."_".$self->{register}."_".$self->{subregister}."_reg;";
                push @{$self->{assignments}}, $self->{assignment};
            }
        }
    }

    sub _process_re {
        my ($self) = @_;
        unless ($self->_skip()) {
            $self->{assignment} =
              "assign ".$self->{item}."_".$self->{register}."_nx = (wr_taken & ".$self->{item}."_".$self->{register}."_en) ? issue_rf_riuwdata[".uc($self->{item})."_".uc($self->{register})."_BITWIDTH-1:0] : ".$self->{item}."_".$self->{register}."_reg;";
            push @{$self->{assignments}}, $self->{assignment};
        }
    }

    sub write_nx {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{type} eq 'ro' and $self->{register}) {
                $self->_process_ro();
            }
            elsif ($self->{subregister} ne '') {
                $self->_process_sub();
            }
            elsif ($self->{register} ne '') {
                $self->_process_re();
            }
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $a (@{$self->{assignments}}) {
            my ($left, undef) = split(/\s*=\s*/, $a, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        
        foreach my $a (@{$self->{assignments}}) {
            my ($left, $right) = split(/\s*=\s*/, $a, 2);
            printf {$self->{outfile}} "%-*s = %s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# CTRLWriter package
############################################
{
    package CTRLWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            outfile   => $outfile,
            io_lines  => [],
            seen_pair => {},
            item      => '',
            register  => '',
            subregister => '',
            key       => '',
            type      => '',
        };
        bless $self, $class;
        return $self;
    }

    sub _skip {
        my ($self) = @_;
        if ($self->{subregister} ne 'msb' and $self->{subregister} ne 'lsb') {
            if (exists $self->{seen_pair}->{$self->{key}}) {
                $self->{seen_pair}->{$self->{key}} = 1;
                return 1;
            }
        }

        return 1 if ($self->{type} ne 'rw');
        
        $self->{seen_pair}->{$self->{key}} = 1;
        
        return 0;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= lc($3);
            $self->{key}        = $self->{item} . "_" . $self->{register};
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
            $self->{key}      = $self->{item} . "_" . $self->{register};
        }

        if ($line =~ /'Type': '([^']*)'/) {
            $self->{type} = lc($1)
        }
    }

    sub _process_sub {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{subregister} ne 'msb' and $self->{subregister} ne 'lsb') {
                my $signal_name = $self->{item} . "_" . $self->{register} . "_en";
                my $reg_name    = $self->{item} . "_" . $self->{register} . "_reg";
                my $bitwidth    = uc($self->{item})."_".uc($self->{register})."_BITWIDTH";
                my $output = "\t\t\t\t  ({RF_RDATA_BITWIDTH{($signal_name)}} & {{(RF_RDATA_BITWIDTH-".$bitwidth."){1'b0}}, $reg_name}) |";
                push @{$self->{io_lines}}, $output;
            }
            else {
                my $signal_name = $self->{item} . "_" . $self->{register} . "_" . $self->{subregister} . "_en";
                my $reg_name    = $self->{item} . "_" . $self->{register} . "_" . $self->{subregister} . "_reg";
                my $bitwidth    = uc($self->{item})."_".uc($self->{register})."_".uc($self->{subregister})."_BITWIDTH";
                my $output = "\t\t\t\t  ({RF_RDATA_BITWIDTH{($signal_name)}} & {{(RF_RDATA_BITWIDTH-".$bitwidth."){1'b0}}, $reg_name}) |";
                push @{$self->{io_lines}}, $output;
            }
        }
    }

    sub _process_re {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{register} eq 'ldma_chsum_data' or $self->{register} eq 'sdma_chsum_data' ) {                
                my $signal_name = $self->{item} . "_" . $self->{register} . "_en";
                my $reg_name    = $self->{item} . "_" . $self->{register};
                my $bitwidth    = uc($self->{item})."_".uc($self->{register})."_BITWIDTH";
                my $output = "\t\t\t\t  ({RF_RDATA_BITWIDTH{($signal_name)}} & {{(RF_RDATA_BITWIDTH-".$bitwidth."){1'b0}}, $reg_name}) |";
                push @{$self->{io_lines}}, $output;
            }
            else {
                my $signal_name = $self->{item} . "_" . $self->{register} . "_en";
                my $reg_name    = $self->{item} . "_" . $self->{register} . "_reg";
                my $bitwidth    = uc($self->{item})."_".uc($self->{register})."_BITWIDTH";
                my $output = "\t\t\t\t  ({RF_RDATA_BITWIDTH{($signal_name)}} & {{(RF_RDATA_BITWIDTH-".$bitwidth."){1'b0}}, $reg_name}) |";
                push @{$self->{io_lines}}, $output;
            }
        }
    }

    sub write_control {
        my ($self) = @_;
        print {$self->{outfile}} "assign issue_rf_riurdata =\n";
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{subregister} ne '') {
                $self->_process_sub();
            }
            elsif ($self->{register} ne '') {
                $self->_process_re();
            }
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $l (@{$self->{io_lines}}) {
            my ($left, undef) = split(/1'b0/, $l, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        foreach my $l (@{$self->{io_lines}}) {
            my ($left, $right) = split(/1'b0/, $l, 2);
            printf {$self->{outfile}} "%-*s1'b0%s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# OutputWriter package
############################################
{
    package OutputWriter;
    sub new {
        my ($class, $outfile) = @_;
        my $self = {
            outfile       => $outfile,
            seen_pair     => {},
            bitwidth_lines=> [],
            ignore_pair   => {
                'csr_id'           => 1,
                'csr_revision'     => 1,
                'csr_status'       => 1,
                'csr_control'      => 1,
                'csr_credit'       => 1,
                'csr_counter'      => 1,
                'csr_counter_mask' => 1,
                'csr_nop'          => 1,
                'sdma_sfence'      => 1,
                'sdma_sdma_chsum_data' => 1,
                'ldma_sfence'      => 1,
                'ldma_ldma_chsum_data' => 1,
                'cdma_sfence'      => 1,
                'cdma_exram_addr'  => 1,
                'fme0_sfence'  => 1,
            },
            item     => '',
            register => '',
        };
        bless $self, $class;
        return $self;
    }

    sub fetch_terms {
        my ($self, $line) = @_;
        if ($line =~ /'Item': '([^']*)', 'Register': '([^']*)', 'SubRegister': '([^']*)'/) {
            $self->{item}       = lc($1);
            $self->{register}   = lc($2);
            $self->{subregister}= lc($3);
        }
        elsif ($line =~ /'Item': '([^']*)', 'Register': '([^']*)'/) {
            $self->{item}     = lc($1);
            $self->{register} = lc($2);
            $self->{subregister} = '';
        }
    }

    sub _skip {
        my ($self) = @_;
        if ($self->{register}) {
            my $key = $self->{item} . "_" . $self->{register};
            return 1 if (exists $self->{ignore_pair}->{$key});
            return 1 if (exists $self->{seen_pair}->{$key});
            $self->{seen_pair}->{$key} = 1;
            return 0;
        }
        return 0;
    }

    sub _process {
        my ($self) = @_;
        unless ($self->_skip()) {
            if ($self->{subregister}) {
                if ($self->{item} eq 'csr' and 
                        ( 
                        $self->{register} eq 'exram_based_addr_0' or
                        $self->{register} eq 'exram_based_addr_1' or
                        $self->{register} eq 'exram_based_addr_2' or
                        $self->{register} eq 'exram_based_addr_3' or
                        $self->{register} eq 'exram_based_addr_4' or
                        $self->{register} eq 'exram_based_addr_5' or
                        $self->{register} eq 'exram_based_addr_6' or
                        $self->{register} eq 'exram_based_addr_7'
                        ) 
                    )
                {
                    my $output_register_name = $self->{register}; # 複製一份
                    $output_register_name =~ s/_based_/_based_/;    # 將 _based_ 替換為 _base_                
                    my $assignment = "assign rf_".$self->{item}."_".$output_register_name." = {" . $self->{item} . "_" . $self->{register} . "_msb_reg, " . $self->{item} . "_" . $self->{register} . "_lsb_reg};";
                    push @{$self->{bitwidth_lines}}, $assignment;
                }
                elsif ($self->{subregister} eq 'msb' or $self->{subregister} eq 'lsb') {
                    my $assignment = "assign rf_".$self->{item}."_".$self->{register}." = {" . $self->{item} . "_" . $self->{register} . "_msb_reg, " . $self->{item} . "_" . $self->{register} . "_lsb_reg};";
                    push @{$self->{bitwidth_lines}}, $assignment;
                } else {
                    my $assignment = "assign rf_".$self->{item}."_".$self->{register}." = ".$self->{item}."_".$self->{register}."_reg;";
                    push @{$self->{bitwidth_lines}}, $assignment;
                }
            }
            else {
                my $assignment = "assign rf_".$self->{item}."_".$self->{register}." = ".$self->{item}."_".$self->{register}."_reg;";
                push @{$self->{bitwidth_lines}}, $assignment;
            }

        }
    }

    sub write_output {
        my ($self) = @_;
        open(my $dict_fh, '<', $main::dictionary_filename)
          or die "Cannot open $main::dictionary_filename: $!";
        while (my $line = <$dict_fh>) {
            chomp $line;
            $self->fetch_terms($line);
            if ($self->{register} ne '') {
                $self->_process();
            }
        }
        close($dict_fh);
        my $max_length = 0;
        foreach my $l (@{$self->{bitwidth_lines}}) {
            my ($left, undef) = split(/=/, $l, 2);
            $max_length = length($left) if (length($left) > $max_length);
        }
        foreach my $l (@{$self->{bitwidth_lines}}) {
            my ($left, $right) = split(/=/, $l, 2);
            printf {$self->{outfile}} "%-*s = %s\n", $max_length, $left, $right;
        }
    }
    1;
}

############################################
# Main function
############################################
package main;
use File::Basename;

sub gen_regfile {
    open(my $in_fh, '<', $input_filename)
      or die "Cannot open $input_filename: $!";
    my @lines = <$in_fh>;
    close($in_fh);

    my ($found_ipnum, $found_port, $found_bitwidth, $found_io, $found_reg,
        $found_wire_nx, $found_wire_en, $found_seq, $found_en,
        $found_nx, $found_control, $found_output, $found_sfence, $found_baseaddrsel, 
        $found_baseaddrselport, $found_baseaddrselio, $found_baseaddrselbitwidth,
        $found_scoreboard, $found_sfenceen, $found_statusnx, $found_riurwaddr, $found_exceptport,
        $found_exceptio, $found_exceptwire, $found_interrupt) = (0) x 25;

    open(my $out_fh, '>', $output_filename)
      or die "Cannot open $output_filename: $!";
    foreach my $line (@lines) {
        print $out_fh $line;
        if (!$found_ipnum && $line =~ /^\/\/ autogen_ipnum_start/) {
            my $pw = IpnumWriter->new($out_fh);
            $pw->write_ipnum();
            $found_ipnum = 1;
        }
        if (!$found_port && $line =~ /^\/\/ autogen_port_start/) {
            my $pw = PortWriter->new($out_fh);
            $pw->write_port();
            $found_port = 1;
        }
        if (!$found_bitwidth && $line =~ /^\/\/ autogen_bitwidth_start/) {
            my $bw = BitwidthWriter->new($out_fh);
            $bw->write_bitwidth();
            $found_bitwidth = 1;
        }
        if (!$found_io && $line =~ /^\/\/ autogen_io_start/) {
            my $io = IOWriter->new($out_fh);
            $io->write_io();
            $found_io = 1;
        }
        if (!$found_reg && $line =~ /^\/\/ autogen_reg_start/) {
            my $rg = RegWriter->new($out_fh);
            $rg->write_reg();
            $found_reg = 1;
        }
        if (!$found_wire_nx && $line =~ /^\/\/ autogen_wire_nx_start/) {
            my $wnx = WireNxWriter->new($out_fh);
            $wnx->write_wire_nx();
            $found_wire_nx = 1;
        }
        if (!$found_wire_en && $line =~ /^\/\/ autogen_wire_en_start/) {
            my $wen = WireEnWriter->new($out_fh);
            $wen->write_wire_en();
            $found_wire_en = 1;
        }
        if (!$found_seq && $line =~ /^\/\/ autogen_seq_start/) {
            my $sq = SeqWriter->new($out_fh);
            $sq->write_seq();
            $found_seq = 1;
        }
        if (!$found_en && $line =~ /^\/\/ autogen_en_start/) {
            my $en = EnWriter->new($out_fh);
            $en->write_en();
            $found_en = 1;
        }
        if (!$found_nx && $line =~ /^\/\/ autogen_nx_start/) {
            my $nx = NxWriter->new($out_fh);
            $nx->write_nx();
            $found_nx = 1;
        }
        if (!$found_control && $line =~ /^\/\/ autogen_control_start/) {
            my $ctrl = CTRLWriter->new($out_fh);
            $ctrl->write_control();
            $found_control = 1;
        }
        if (!$found_output && $line =~ /^\/\/ autogen_output_start/) {
            my $outw = OutputWriter->new($out_fh);
            $outw->write_output();
            $found_output = 1;
        }
        if (!$found_sfence && $line =~ /^\/\/ autogen_sfence_start/) {
            my $outw = SfenceWriter->new($out_fh);
            $outw->write_sfence();
            $found_sfence = 1;
        }
        if (!$found_baseaddrsel && $line =~ /^\/\/ autogen_baseaddrsel_start/) {
            my $outw = BaseaddrselWriter->new($out_fh);
            $outw->write_baseaddrsel();
            $found_baseaddrsel = 1;
        }
        if (!$found_baseaddrselport && $line =~ /^\/\/ autogen_baseaddrselport_start/) {
            my $outw = BaseaddrselportWriter->new($out_fh);
            $outw->write_baseaddrselport();
            $found_baseaddrselport = 1;
        }
        if (!$found_baseaddrselio && $line =~ /^\/\/ autogen_baseaddrselio_start/) {
            my $outw = BaseaddrselioWriter->new($out_fh);
            $outw->write_baseaddrselio();
            $found_baseaddrselio = 1;
        }
        if (!$found_baseaddrselbitwidth && $line =~ /^\/\/ autogen_baseaddrselbitwidth_start/) {
            my $outw = BaseaddrselbitwidthWriter->new($out_fh);
            $outw->write_baseaddrselbitwidth();
            $found_baseaddrselbitwidth = 1;
        }
        if (!$found_scoreboard && $line =~ /^\/\/ autogen_scoreboard_start/) {
            my $outw = ScoreboardWriter->new($out_fh);
            $outw->write_scoreboard();
            $found_scoreboard = 1;
        }
        if (!$found_sfenceen && $line =~ /^\/\/ autogen_sfenceen_start/) {
            my $outw = SfenceenWriter->new($out_fh);
            $outw->write_sfenceen();
            $found_sfenceen = 1;
        }
        if (!$found_statusnx && $line =~ /^\/\/ autogen_statusnx_start/) {
            my $outw = StatusnxWriter->new($out_fh);
            $outw->write_statusnx();
            $found_statusnx = 1;
        }
        if (!$found_riurwaddr && $line =~ /^\/\/ autogen_riurwaddr_start/) {
            my $outw = RiurwaddrWriter->new($out_fh);
            $outw->write_riurwaddr();
            $found_riurwaddr = 1;
        }
        if (!$found_exceptport && $line =~ /^\/\/ autogen_exceptport_start/) {
            my $outw = ExceptportWriter->new($out_fh);
            $outw->write_exceptport();
            $found_exceptport = 1;
        }
        if (!$found_exceptio && $line =~ /^\/\/ autogen_exceptio_start/) {
            my $outw = ExceptioWriter->new($out_fh);
            $outw->write_exceptio();
            $found_exceptio = 1;
        }
        if (!$found_interrupt && $line =~ /^\/\/ autogen_interrupt_start/) {
            my $outw = InterruptWriter->new($out_fh);
            $outw->write_interrupt();
            $found_interrupt = 1;
        }
        if (!$found_exceptwire && $line =~ /^\/\/ autogen_exceptwire_start/) {
            my $outw = ExceptwireWriter->new($out_fh);
            $outw->write_exceptwire();
            $found_exceptwire = 1;
        }
    }
    close($out_fh);
}

gen_regfile();
1;

