#
# spec file for package groff
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# mdk-1.19.1-1mdk
#
# $Id$

%define revision	$Rev$
%define name		groff
%define version		1.19.2
%define release		%_revrel

Summary:	A document formatting system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text Tools
URL:		http://www.gnu.org/directory/GNU/groff.html
Source0:	http://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz
#ftp://prep.ai.mit.edu/pub/gnu/groff/%{name}-%{version}.tar.bz2
Source1:	troff-to-ps.fpi
Source2:	README.A4
Patch0:		groff-1.18-info.patch
Patch1:		groff-1.19.1-nohtml.patch
# keeps apostrophes and dashes as ascii, but only for man pages
# -- pablo
Patch4:		groff-1.19-dashes.patch
Patch5:		groff-1.19.2-CAN-2004-0969.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	byacc
BuildRequires:	texinfo >= 4.3
BuildRequires:	xpm-devel
BuildRequires:	imake
BuildRequires:	netpbm
BuildRequires:	netpbm-devel

Requires:	mktemp
Requires:	groff-for-man = %{version}-%{release}
Requires(post):	info-install
Requires(preun): info-install
Obsoletes:	groff-tools
Provides:	groff-tools

%description
Groff is a document formatting system.  Groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer. 
Groff's formatting commands allow you to specify font type and size, bold
type, italic type, the number and size of columns on a page, and more.


%package for-man
Summary:	Parts of the groff formatting system that is required for viewing manpages
Group:		Text Tools
Conflicts:	groff < 1.19-7avx

%description for-man
The groff-for-man package contains the parts of the groff text processor
package that are required for viewing manpages.
For a full groff package, install package groff.


%package perl
Summary:	Parts of the groff formatting system that require Perl
Group:		Text Tools

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, and the
troff-to-ps print filter.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .nohtml
%patch4 -p1 -b ._dashes
%patch5 -p1 -b .can-2004-0969

cp -f %{_sourcedir}/README.A4 .

WANT_AUTOCONF_2_5=1 autoconf


%build
export MAKEINFO=$HOME/cvs/texinfo/makeinfo/makeinfo
%configure2_5x
make top_builddir=$PWD top_srcdir=$PWD
pushd doc
    makeinfo groff.texinfo
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_prefix},%{_infodir},%{_bindir},%{_libdir}/%{name},%{_docdir}/%{name}/%{version}/html/momdoc}
%makeinstall manroot=%{buildroot}%{_mandir} top_builddir=$PWD top_srcdir=$PWD common_words_file=%{buildroot}%{_datadir}/%{name}/%{version} mkinstalldirs=mkdir
install -m 0644 doc/groff.info* %{buildroot}%{_infodir}

for i in s.tmac mse.tmac m.tmac; do
    ln -s $i %{buildroot}%{_datadir}/groff/%{version}/tmac/g$i
done
for i in troff tbl pic eqn neqn refer lookbib indxbib soelim nroff; do
    ln -s $i %{buildroot}%{_bindir}/g$i
done

# Build system is compressing man-pages
for i in eqn.1 indxbib.1 lookbib.1 nroff.1 pic.1 refer.1 soelim.1 tbl.1 troff.1; do
    ln -s $i%{_extension} %{buildroot}%{_mandir}/man1/g$i%{_extension}
done

mkdir -p %{buildroot}/%{_libdir}/rhs/rhs-printfilters
install -m 0755 %{_sourcedir}/troff-to-ps.fpi %{buildroot}%{_libdir}/rhs/rhs-printfilters

# call spec-helper before creating the file list
s=/usr/share/spec-helper/spec-helper ; [ -x $s ] && $s

cat <<EOF > groff.list
%dir %{_libdir}/groff
%{_libdir}/groff/groffer/groffer2.sh
%{_datadir}/groff/%{version}/eign
%{_datadir}/groff/%{version}/font/devdvi
%{_datadir}/groff/%{version}/font/devhtml
%{_datadir}/groff/%{version}/font/devlbp
%{_datadir}/groff/%{version}/font/devlj4
%{_datadir}/groff/%{version}/font/devps
EOF

cat <<EOF > groff-for-man.list
%{_bindir}/eqn
%{_bindir}/troff
%{_bindir}/nroff
%{_bindir}/tbl
%{_bindir}/geqn
%{_bindir}/gtbl
%{_bindir}/gnroff
%{_bindir}/grotty
%{_bindir}/groff
%{_bindir}/gtroff
%dir %{_datadir}/groff
%dir %{_datadir}/groff/%{version}
%{_datadir}/groff/%{version}/tmac
%dir %{_datadir}/groff/%{version}/font
%{_datadir}/groff/%{version}/font/devascii
%{_datadir}/groff/%{version}/font/devlatin1
%{_datadir}/groff/%{version}/font/devutf8
%dir %{_datadir}/groff/site-tmac
%{_datadir}/groff/site-tmac/man.local
%{_datadir}/groff/site-tmac/mdoc.local
EOF

cat <<EOF > groff-perl.list
%{_bindir}/grog
%{_bindir}/mmroff
%{_bindir}/afmtodit
%{_mandir}/man1/afmtodit.1.bz2
%{_mandir}/man1/grog.1.bz2
%{_mandir}/man1/mmroff.1.bz2
EOF

dirs=usr/share/man/*
(cd %{buildroot} ; find usr/bin usr/share/man usr/share/groff/%{version}/tmac ! -type d -printf "/%%p\n") >> %{name}.list
(cd %{buildroot} ; find usr/share/groff/%{version}/tmac/* -type d -printf "%%%%dir /%%p\n") >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}-for-man.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}.list
perl -ni -e 'BEGIN { open F, "%{name}-perl.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}.list
# japanese environment is crazy; doc.tmac seems superior than docj.tmac
ln -sf doc.tmac %{buildroot}%{_datadir}/groff/%{version}/tmac/docj.tmac

#TV cp -a {,%{buildroot}%{_datadir}/groff/%{version}/}font/devkoi8-r

for i in $(find %{buildroot} -empty -type f); do echo " ">> $i;done

rm -rf %{buildroot}%{_docdir}/groff/%{version}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}

%preun
%_remove_install_info %{name}


%files -f groff.list
%defattr(-,root,root)
%{_infodir}/groff*

%files for-man -f groff-for-man.list
%defattr(-,root,root)

%files perl -f groff-perl.list
%defattr(-,root,root)
%{_libdir}/rhs/*/*

%files doc
%defattr(-,root,root)
%doc BUG-REPORT COPYING NEWS PROBLEMS README README.A4 TODO VERSION


%changelog
* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.19.2
- 1.19.2 (fixes build with gcc4.1)
- rediff P5
- build against rebuilt libxpm
- drop P2, P3
- fix buildreq's

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- really add -doc subpackage

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcdir/file instead of %%{SOURCEx}

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- renumber patches
- P5: security fix for CAN-2004-0969

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1-2avx
- remove BuildReq on xorg-x11 (aka rman) and don't build xditview

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1-1avx
- 1.19.1
- drop unapplied P3
- drop P7
- update P5 (waschk)
- explicit groff-for-man conflict with older groff due to eqn (pixel)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19-8avx
- rebuild for new gcc

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19-7avx
- bootstrap build
- change buildrequires from texinfo < 4.7 to >= 4.3
- make groff depends on groff-for-man %%{version}-%%{release}
- spec cleanups

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.19-6avx
- require packages not files
- Annvix build
- merge from amd64-branch: build fixes (gbeauchesne)

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.19-5sls
- remove %%build_opensls macro
- minor spec cleanups
- don't need COPYING in each file

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.19-4sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build gxditview
- if %%build_opensls don't BuildReq: netpbm, netpbm-devel, psutils

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
