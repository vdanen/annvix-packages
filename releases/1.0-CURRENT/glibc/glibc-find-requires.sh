#!/bin/bash

#
# Auto-generate requirements for executables (both ELF and a.out) and library
# sonames, script interpreters, and perl modules.
#

ulimit -c 0

#
# --- Set needed to 0 for traditional find-requires behavior.
needed=0
if [ X"$1" = Xldd ]; then
    needed=0
elif [ X"$1" = Xobjdump ]; then
    needed=1
fi

#
# --- Mandrake Linux specific part

#
# --- Grab the file manifest and classify files.
filelist=`sed "s/['\"]/\\\&/g"`
exelist=`echo $filelist | xargs -r file | egrep -v ":.* (commands|script) " | \
	grep ":.*executable" | cut -d: -f1`
scriptlist=`echo $filelist | grep -v /usr/doc | grep -v /usr/share/doc | xargs -r file | \
	egrep ":.* (commands|script) " | cut -d: -f1`
liblist=`echo $filelist | xargs -r file | \
	grep ":.*shared object" | cut -d : -f1`

interplist=
perllist=
pythonlist=
tcllist=

#
# --- Alpha does not mark 64bit dependencies
case `uname -m` in
  alpha*)	mark64="" ;;
  *)		mark64="()(64bit)" ;;
esac

if [ "$needed" -eq 0 ]; then
#
# --- Executable dependency sonames.
  for f in $exelist; do
    [ -r $f -a -x $f ] || continue
    lib64=`if file -L $f 2>/dev/null | \
	grep "ELF 64-bit" >/dev/null; then echo "$mark64"; fi`
    ldd $f | awk '/=>/ {
	if ($1 !~ /libNoVersion.so/ && $1 !~ /4[um]lib.so/ && $1 !~ /libredhat-kernel.so/) {
	    gsub(/'\''"/,"\\&",$1);
	    printf "%s'$lib64'\n", $1
	}
    }'
  done | xargs -r -n 1 basename | sort -u | grep -v 'libsafe|libfakeroot'

#
# --- Library dependency sonames.
  for f in $liblist; do
    [ -r $f ] || continue
    lib64=`if file -L $f 2>/dev/null | \
	grep "ELF 64-bit" >/dev/null; then echo "$mark64"; fi`
    ldd $f | awk '/=>/ {
	if ($1 !~ /libNoVersion.so/ && $1 !~ /4[um]lib.so/ && $1 !~ /libredhat-kernel.so/) {
	    gsub(/'\''"/,"\\&",$1);
	    printf "%s'$lib64'\n", $1
	}
    }'
  done | xargs -r -n 1 basename | sort -u | grep -v 'libsafe|libfakeroot'
fi

#
# --- Perl or python deps

#
# --- Script interpreters.
for f in $scriptlist; do
    [ -r $f -a -x $f ] || continue
    interp=`head -1 $f | sed -e 's/^\#\![ 	]*//' | cut -d" " -f1`
    interplist="$interplist $interp"
    case $interp in
    */perl)	perllist="$perllist $f" ;;
    esac
done
if [ -n "$interplist" ]; then
    for i in `echo "$interplist" | tr '[:blank:]' \\\n | sort -u`; do
	if ! rpm -qf $i --qf '%{NAME}\n' 2>/dev/null; then
	    echo $i
	fi
    done | sort -u | grep -v 'libsafe|libfakeroot'
fi

#
# --- Add perl module files to perllist.
for f in $filelist; do
    [ -r $f -a "${f%.pm}" != "${f}" ] && perllist="$perllist $f"
done

#
# --- Weak symbol versions (from glibc).
[ -n "$mark64" ] && mark64="(64bit)"
for f in $liblist $exelist ; do
    [ -r $f ] || continue
    lib64=`if file -L $f 2>/dev/null | \
	grep "ELF 64-bit" >/dev/null; then echo "$mark64"; fi`
    objdump -p $f | awk 'BEGIN { START=0; LIBNAME=""; needed='$needed'; }
	/^$/ { START=0; }
	/^Dynamic Section:$/ { START=1; }
	(START==1) && /NEEDED/ {
	    if (needed) { print $2 ; }
	}
	/^Version References:$/ { START=2; }
	(START==2) && /required from/ {
	    sub(/:/, "", $3);
	    LIBNAME=$3;
	}
	(START==2) && (LIBNAME!="") && ($4!="") && (($4~/^GLIBC_*/) || ($4~/^GCC_*/)) {
	    print LIBNAME "(" $4 ")'$lib64'";
	}
    '
done | sort -u | grep -v 'libsafe|libfakeroot'

#
# --- Perl modules.
#[ -x /usr/lib/rpm/perl.req -a -n "$perllist" ] && \
#    echo $perllist | tr '[:blank:]' \\n | /usr/lib/rpm/perl.req | sort -u

#
# --- Python modules.
[ -x /usr/lib/rpm/python.req -a -n "$pythonlist" ] && \
    echo $pythonlist | tr '[:blank:]' \\n | /usr/lib/rpm/python.req | sort -u

#
# --- Tcl modules.
[ -x /usr/lib/rpm/tcl.req -a -n "$tcllist" ] && \
    echo $tcllist | tr '[:blank:]' \\n | /usr/lib/rpm/tcl.req | sort -u

exit 0
