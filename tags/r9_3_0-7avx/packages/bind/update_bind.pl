#!/usr/bin/perl -W

#----------------------------------------------------------------------
# copyright (C) 2001 Florin Grad
# 
# This is a really silly program that is supposed to allow an update of 
# a dhcp-2* server to a dhcp-3* server
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

#search for a ddns-update-style entry in /etc/dhcpd.conf file
my $conf_file = "/etc/named.conf"; #$ARGV[0];
my $conf_file_orig = "/etc/named.conf.orig";
my $i=0;
open (NAMEDCONF, "< $conf_file") or die "Can't open the $conf_file file for reading";
while (<NAMEDCONF>) {
	if (/pid-file/) {
		$i++;
	};
};
close (NAMEDCONF);

if ($i == 0) {  #we are on a bind8 
	my $pid_line = 0;
	rename("$conf_file","$conf_file_orig") || die "Can't rename $conf_file: $!";
	open (NAMEDCONF_ORIG, "< $conf_file_orig") or die "Can't open the $conf_file_orig file for reading";
	open (NAMEDCONF, "> $conf_file") or die "Can't open the $conf_file file for writing";	
	while (<NAMEDCONF_ORIG>) {
		if (/options/) {
	                $pid_line++;  
			print NAMEDCONF "$_"; # copy the current line in the new file 
			next;
		};
		if ($pid_line == 0) { # didn't reach the the options section yet
			print NAMEDCONF "$_"; # copy the current line in the new file 
		} else { 
			print NAMEDCONF "\tpid-file \"/var/run/named/named.pid\"\;\n"; #add the missing line 
			$pid_line = 0;
			print NAMEDCONF "$_";	
		};
	};	
	close (NAMEDCONF_ORIG);
	close (NAMEDCONF);
}
