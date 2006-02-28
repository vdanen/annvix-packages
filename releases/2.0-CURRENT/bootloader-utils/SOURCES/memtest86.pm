#!/usr/bin/perl
# -*- Mode: cperl -*-
#--------------------------------------------------------------------
# Copyright (C) 2000, 2001 by MandrakeSoft.
# Chmouel Boudjnah <chmouel@mandrakesoft.com>.
#
# Redistribution of this file is permitted under the terms of the GNU 
# Public License (GPL)
#--------------------------------------------------------------------
# $Id: lilo,v 1.17 2001/10/05 14:56:23 chmouel Exp $
#--------------------------------------------------------------------
## description: 
#	      Add/check entry for memtest into bootloader.

use strict;
use lib qw(/usr/share/loader/);
use common;

my $debug = 0;
my $boot = "/boot/";

my $grub_conf = $ENV{GRUB_CONF} ? $ENV{GRUB_CONF} : "/boot/grub/menu.lst";
my $lilo_conf = $ENV{LILO_CONF} ? $ENV{LILO_CONF} : "/etc/lilo.conf";

my ($lilo, $grub);
my (%main, %entry);

my ($blank, $remove);

while  ($ARGV[0] =~ /^-/ ) {
    $_ = shift;
    if (m/^-g/) {
	$grub=1;
    } elsif (m/^-l/) {
	$lilo=1;
    } elsif (m/^-r/) {
	$remove=1;
    } else {
	die "unknow option $_\n";
    }
}
if (not defined($grub) and not defined($lilo)) {
    my $detected = `/usr/sbin/detectloader -q`;
    if ($detected =~ /lilo/i) {
	$lilo=1;
    } elsif ($detected =~ /grub/i) {
	$grub=1;
    } else {
	die "Cannot detect your bootloader\n";
    }
}

my $version = shift or die "Need a memtest version\n";
die "/boot/memtest-${version}.bin doen't exist\n" unless -f "/boot/memtest-${version}.bin" or defined($remove);

parse_lilo_conf() if $lilo;
parse_grub_conf() if $grub;

check();

if (not $remove) {
    add_grub_conf() if $grub;
    add_lilo_conf() if $lilo;
    system("/sbin/lilo") if $lilo;
}

if ($remove) {
    remove_grub_conf() if $grub;
    remove_lilo_conf() if $lilo;
}    

sub add_grub_conf {
    my $grub_partition;

    unless ($grub_partition = grub_convert_grub_part(grub_get_boot_partitions())) {
	die "Can't convert grub_partition\n";
    }
    unless ($debug) {
	open F, ">>$grub_conf" or die "Can't write to $grub_conf\n";
	select F;
    }
    print "\n" if $blank;
    print << "EOF";
title memtest-$version
kernel $grub_partition${boot}memtest-$version.bin
EOF

    close F;
    select STDOUT;
}    

sub add_lilo_conf {
    unless ($debug) {
	open F, ">>$lilo_conf" or die "Can't write to $lilo_conf\n";
	select F;
    }

    print "\n" if $blank;
	print << "EOF";
image=/boot/memtest-$version.bin
	label=memtest-$version
EOF

    unless ($debug) {
	close F;
	select STDOUT;
    }
    
}

sub parse_lilo_conf {
    my ($initrd, $root, $vga, $label, $image);
    
    open F, $lilo_conf or die "Can't open $lilo_conf\n";
    while (<F>) {
	$blank = "\n" if eof and $_ !~ /^\s*$/;
	
	next if /^\s*#/;
	
	$main{default} = $1 if m/^default=(.*)/;
	$main{vga} = $1 if m/^vga=(.*)/;
	
	$initrd = $1 if /initrd=(.*)/;
	$root = $1 if /root=(.*)/;
	$vga = $1 if /vga=(.*)/;
	
	if ( /^(image|other)=/ || eof ) {
	    $entry{$label}{initrd} = $initrd if not $entry{$label}{initrd};
	    $entry{$label}{root} = $root if not $entry{$label}{root};
	    $entry{$label}{vga} = $vga if not $entry{$label}{vga};
	    undef $initrd;undef $root;
	}
	
	$image=$1 if /^image=(.*)/;
	if (/label=(.*)/) { 
	    $label=$1; 
	    $entry{$label}{label}=$label;
	    $entry{$label}{kernel}=$image;
	    $entry{$label}{initrd}=$initrd;
	    $entry{$label}{vga}=$vga;
	    $entry{$label}{root}=$root;
	}
    }
    close F;
}

sub parse_grub_conf {
    my ($title, $cnt);

    open F, $grub_conf or die "Can't open $grub_conf\n";
    
    while (<F>) {
	$blank = "\n" if eof and $_ !~ /^\s*$/;
	
	next if /^\s*#/;
	$main{default} = $1 if /^default (\d+)/;
	
	if (/^title\s+(.*)/) {
	    $title=$1;
	    $entry{$title}{cnt} = $cnt;
	    $main{default} = $title if $entry{$title}{cnt} == $main{default};
	    $cnt++;
	}
	
	if (m/kernel\s+(\(.*\))([^ 	]+)\s+(.*)/) {
	    $entry{$title}{label}=$title;
	    $entry{$title}{partition} = $1;
	    $entry{$title}{kernel} = $2;
	    $entry{$title}{options} = $3;
	}
	$entry{$title}{initrd} = $1 if m/\s*initrd.*\)(.*)/;
    }
    close F;
}

sub remove_grub_conf  {
    local $/;
    `cp -f $grub_conf ${grub_conf}.old` if -f $grub_conf and not $debug;
    my $output = `mktemp /tmp/.grub.XXXXXX`;chop $output;
    open F, $grub_conf;
    open O, ">$output";
    select O;
    while (<F>) {
	if (m@title memtest(-$version)?\nkernel.*/boot/memtest-$version.bin.*?(?=(title|$))@s) {
 	    if (m@title memtest(-$version)?\nkernel.*/boot/memtest-$version.bin.*title@s) {
 		$_ =~ s@title memtest(-$version)?\nkernel.*/boot/memtest-$version.bin.*?(?=title)@@s;
 	    } else {
 		$_ =~ s@title memtest(-$version)?\nkernel.*/boot/memtest-$version.bin.*$@@s;
 	    }
 	}
	print;
    }
    close F;
    close O;
    system("mv -f $output $grub_conf");
}

sub remove_lilo_conf  {
    local $/;
    `cp -f $lilo_conf ${lilo_conf}.old` if -f $lilo_conf and not $debug;
    my $output = `mktemp /tmp/.lilo.XXXXXX`;chop $output;
    open F, $lilo_conf;
    open O, ">$output";
    select O;
    while (<F>) {
	if (m@image=/boot/memtest-$version.bin.*label=memtest.*(?=(image|other|$))@s) {
	    if (m@image=/boot/memtest-$version.bin.*(image|other)=@s) {
		$_ =~ s@image=/boot/memtest-$version.bin.*?(?=(image|other))@@s;
	    } else {
		$_ =~ s|image=/boot/memtest-$version.bin.*||s;
	    }
	}
	print;
    }
    close F;
    close O;
    select STDOUT;
    system("mv -f $output $lilo_conf");
}

sub check {
    my $check;
    
    for (keys %entry) {
	die "Entry $entry{$_}{label}: you have already an entry for /boot/memtest-$version.bin\n"
	  if ($entry{$_}{kernel} =~ m|(/boot/)?memtest-$version.bin| and not $remove);
	$check=1
	  if ($entry{$_}{kernel} =~ m|(/boot/)?memtest-$version.bin| and $remove);
    }
    die "There is not entry for /boot/memtest-$version.bin file\n" if not $check and $remove;
}

sub grub_convert_grub_part {
    my $fpart = shift;
    my $map_file = "/boot/grub/device.map";
    my ($disk, $part, $grub_part);
    do { $disk = $1; $part = $2 - 1 } if ($fpart =~ m|([^\d+]*)(\d+)|);
    local *F;
    open (F, $map_file) or die "Can't open $map_file\n";
    while (<F>) { $grub_part=$1  if (m|([^ \t]+)\s*$disk$|);}
    close F;
    $grub_part =~ s|\)|,$part\)|;
    return $grub_part =~ /\(([\w\d]+)d\d+,\d+\)/ ? $grub_part : undef;
}


sub grub_get_boot_partitions {
    my $part;
    local *F;
    open F, '/etc/fstab'; 
    while (<F>) {
 	my @s = split ' ';
	$part = $s[0] if $s[1] =~ m|/$| and not $part;
	if ($s[1] =~ m|/boot$|) {
	    $boot="/";
	    $part = $s[0];
	}
    }; 
    close F;
    return  $part
}
