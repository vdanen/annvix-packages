#!/usr/bin/awk
# chroot-setup.awk
#
# setup the chroot environment in master.cf change all lines except pipe
# local and proxymap to run chrooted
BEGIN			{ OFS="\t"; }
/^#/			{ print; next; }
/^ /			{ print; next; }
$8 ~ /(local|pipe|proxymap)/	{ print; next; }
			{ $5="y"; print $0; }
