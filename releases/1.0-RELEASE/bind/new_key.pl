#!/usr/bin/perl -W

#----------------------------------------------------------------------
# copyright (C) 2001 Florin Grad
# 
# This is a really silly program that is supposed to generate a new key 
# and update the existing one in /etc/rndc.conf or /etc/named.conf
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#       
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#------------------------------------------------------------------------

my $key ="";

#generate the key
system ("dns-keygen > /etc/rndc.key") ;
open (KEY, "< /etc/rndc.key") or die "Can't open the/etc/rdnc.key_file file for reading";
while (<KEY>) {
	chomp($_);
	my @list = $_;
	$key = $list[0];
}
close(KEY);
system ("rm -rf /etc/rndc.key");

#update the /etc/rndc.conf file
my $conf_file = "/etc/rndc.conf";
my $conf_file_backup = $conf_file.".backup";

open (CONF, "< $conf_file") or die "Can't open the $conf_file file for reading";
open (CONF_new, "> $conf_file_backup") or die "Can't open the $conf_file_backup file for writing";
while (<CONF>) {
	chomp($_);
	my @line = split (/\s+|\t+/,$_) ;
	if ($line[1] && ($line[1] eq "secret") && $line[2] && ($line[2] ne "must")) {
		print CONF_new "\tsecret \"".$key."\";\n";
		next;
	};
	print CONF_new "$_\n";
};
close (CONF_new);
close (CONF);
rename ("$conf_file","$conf_file".".orig");
rename ("$conf_file_backup","$conf_file");

#update the /etc/.named file
$conf_file = "/etc/named.conf";
$conf_file_backup = $conf_file.".backup";

open (CONF, "< $conf_file") or die "Can't open the $conf_file file for reading";
open (CONF_new, "> $conf_file_backup") or die "Can't open the $conf_file_backup file for writing";
while (<CONF>) {
	chomp($_);
	my @line = split (/\s+|\t+/,$_) ;
	if ($line[1] && ($line[1] eq "secret") && $line[2] && ($line[2] ne "must")) {
		print CONF_new "\tsecret \"".$key."\";\n";
		next;
	};
	print CONF_new "$_\n";
};
close (CONF_new);
close (CONF);
rename ("$conf_file","$conf_file".".orig");
rename ("$conf_file_backup","$conf_file");

#fix permissions
system "chmod 0600 /etc/rndc.conf /etc/named.conf";
system "chown named.named /etc/rndc.conf /etc/named.conf";


