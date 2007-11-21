#
# spec file for package tetex
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tetex
%define version		3.0
%define release		%_revrel

%define pkgname		%{name}
%define docversion	3.0
%define pkgversion	3.0
%define tetexversion	3.0
%define texmfversion	3.0
%define texmfsrcversion	3.0
%define texmfggversion	3.0d
%define xmltexname	xmltex
%define xmltexversion	1.9
%define csidxversion	19990820

%define vartexfonts	/var/lib/texmf
%define texmfsysvar	%{_datadir}/texmf-var

%define _unpackaged_files_terminate_build 0
%define _requires_exceptions /usr/local/bin/perl

Summary:	The TeX text formatting system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		Publishing
URL:		http://www.tug.org/teTeX/
Source0:	ftp://cam.ctan.org/tex-archive/systems/unix/teTeX/2.0/distrib/sources/%{name}-src-%{tetexversion}.tar.bz2
Source1:	ftp://cam.ctan.org/tex-archive/systems/unix/teTeX/2.0/distrib/sources/%{name}-texmf-%{texmfversion}.tar.bz2
Source2:	ftp://cam.ctan.org/tex-archive/systems/unix/teTeX/2.0/distrib/sources/%{name}-texmfsrc-%{texmfsrcversion}.tar.bz2
Source3:	http://peoples.mandrakesoft.com/~ghibo/%{name}-texmf-extras-gg-%{texmfggversion}.tar.bz2
Source4:	http://peoples.mandrakesoft.com/~ghibo/%{name}-texmfsrc-extras-gg-%{texmfggversion}.tar.bz2
Source5:	ftp://ftp.dante.de/pub/tex/macros/xmltex.tar.bz2
Source6:	tetex.cron
Source7:	ftp://math.feld.cvut.cz/pub/cstex/tetex-rpm/mandrake/csindex-%{csidxversion}.tar.bz2
Source8:	dvipdfpress

Patch0:		tetex-3.0-texmfcnf.patch
Patch1:		tetex-3.0-fmtutil.patch
Patch3:		tetex-3.0-mf-mainmemory.patch
Patch4:		tetex-3.0-mp-mainmemory.patch
Patch5:		tetex-3.0-xdvik-dot.patch
Patch6:		tetex-3.0-epstopdf-dct.patch
Patch11:	tetex-3.0-badscript.patch
Patch12:	tetex-3.0-dvipdfm-security.patch
Patch14:	tetex-3.0-mfw.patch
Patch15:	tetex-3.0-CAN-2004-0888.patch
Patch16:	tetex-3.0-CAN-2005-0064.patch
Patch17:	tetex-3.0-xpdf-CAN-2005-0206.patch
Patch18:	tetex-src-3.0-pic.patch
Patch20:	tetex-1.0-texmf-dvipsgeneric.patch
Patch21:	tetex-3.0-xdvi-www.patch
# security
Patch28:	xpdf-3.00-CVE-2005-3191_2_3.patch
Patch29:	xpdf-3.00-goo-overflow.patch
Patch30:	xpdf-3.00-chris-overflows.patch
Patch31:	tetex-src-3.0-gd-CAN-2004-0941.patch
Patch32:	tetex-src-3.0-gd-CVE-2006-2906.patch
Patch33:	gd-2.0.33-CVE-2007-0455.patch
Patch34:	gd-cvs-CVE-2007-2756.patch
Patch35:	tetex-3.0-CVE-2007-0650.patch
Patch36:	xpdf-3.01-CVE-2007-3387.patch
Patch37:	gd-2.0.33_CVE-2007-3472.patch
Patch38:	gd-2.0.33_CVE-2007-3473.patch
Patch39:	gd-2.0.33_CVE-2007-3474.patch
Patch40:	gd-2.0.33_CVE-2007-3475.patch
Patch41:	gd-2.0.33_CVE-2007-3476.patch
Patch42:	gd-2.0.33_CVE-2007-3477.patch
Patch43:	gd-2.0.33_CVE-2007-3478.patch
Patch44:	xpdf-3.00-CVE-2007-4352_5392_5393.patch
Patch45:	tetex-deb-dvips-CVE-2007-5935.patch
Patch46:	t1lib-5.1.0-ub-CVE-2007-4033.patch
Patch47:	tetex-3.0-gentoo-mdv-CVE-2007-5936_5937-cs4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	ed
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	autoconf2.1
BuildRequires:	automake1.7
BuildRequires:	ncurses-devel
BuildRequires:	png-devel
BuildRequires:	xpm-devel
BuildRequires:	libx11-devel
BuildRequires:	libxt-devel

Requires:	tmpwatch
Requires:	dialog
Requires:	ed
Requires:	info-install
Requires:	libxau
Requires:	libxdmcp
Obsoletes:	cweb
Provides:	cweb = %{version}

%description
teTeX is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
typesetter independent .dvi (DeVice Independent) file as output.
Usually, TeX is used in conjunction with a higher level formatting
package like LaTeX or PlainTeX, since TeX by itself is not very
user-friendly.


%package latex
Summary:	The LaTeX front end for the TeX text formatting system
Group:		Publishing
Requires:	tetex = %{version}
Requires:	tetex-context
Provides:	prosper = %{version}
Obsoletes:	prosper
Provides:	latex-xcolor = %{version}
Obsoletes:	latex-xcolor
Provides:	latex-pgf = %{version}
Obsoletes:	latex-pgf

%description latex
LaTeX is a front end for the TeX text formatting system.  Easier to use
than TeX, LaTeX is essentially a set of TeX macros which provide
convenient, predefined document formats for users.


%package dvips
Summary:	A DVI to PostScript converter for the TeX text formatting system
Group:		Publishing
Requires:	tetex = %{version}

%description dvips
Dvips converts .dvi files produced by the TeX text formatting system
(or by another processor like GFtoDVI) to PostScript(TM) format.
Normally the PostScript file is sent directly to your printer.


%package dvilj
Summary:	A DVI to HP PCL (Printer Control Language) converter
Group:		Publishing
Requires:	tetex = %{version}

%description dvilj
Dvilj and dvilj's siblings (included in this package) will convert TeX
text formatting system output .dvi files to HP PCL (HP Printer Control
Language) commands.  Using dvilj, you can print TeX files to HP
LaserJet+ and fully compatible printers.  With dvilj2p, you can print
to HP LaserJet IIP and fully compatible printers. And with dvilj4, you
can print to HP LaserJet4 and fully compatible printers.


%package afm
Summary:	A converter for PostScript(TM) font metric files, for use with TeX
Group:		Publishing
Requires:	tetex = %{version}

%description afm
tetex-afm provides afm2tfm, a converter for PostScript font metric files. 
PostScript fonts are accompanied by .afm font metric files which describe
the characteristics of each font.  To use PostScript fonts with TeX, TeX
needs .tfm files that contain similar information.  Afm2tfm will convert
.afm files to .tfm files.  


%package dvipdfm
Summary:	A DVI to PDF converter
Group:		Publishing
Requires:	tetex = %{version}
Requires:	tetex-dvips = %{version}

%description dvipdfm
dvidpfm is a DVI to PDF translator for use with TeX.


%package devel
Summary:	Development libraries (kpathsea) for teTeX
Group:		Development/C
Requires:	tetex = %{version}

%description devel
This package contains C headers and libraries, for developing TeX
applications using kpathsea library.


%package -n %{xmltexname}
Summary:	Namespace-aware XML parser written in TeX
Version: 	%{xmltexversion}
Release:	%{release}
Group:		Publishing
License: 	LaTeX Project Public License
URL: 		http://www.dcarlisle.demon.co.uk/xmltex/manual.html
Requires: 	tetex >= 1.0.7-52mdk
Requires: 	tetex-latex >= 1.0.7-52mdk

%description -n %{xmltexname}
Namespace-aware XML parser written in TeX. This package
also includes passivetex macros, which can be used to process an XML
document which results from an XSL trasformation to formatting objects.


%package context
Summary:	Document engineering system based on TeX
Group:		Publishing
Requires:	tetex >= 2.0.2

%description context
CONTeXT is a document engineering system based on TeX. TeX is a
typesetting system and a program to typeset and produce documents.
CONTeXT is easy to use and enables you to make complex paper and
electronic documents.


%package texi2html
Summary:	Convert texinfo (GNU docs) directly to HTML for easy reading
Group:		Publishing
License:	GPL

%description texi2html
This package converts the GNU standard form of documentation (texinfo) into
HTML files which can be read with any WWW browser.


%prep
%setup -q -n %{name}-src-%{tetexversion} -a 7
chmod 0755 csindex-%{csidxversion}
%patch0 -p1 -b .texmfcnf
%patch1 -p1 -b .fmtutil
%patch3 -p1 -b .mf-mainmem
%patch4 -p1 -b .mp-mainmem
%patch5 -p1 -b .xdvikdot
%patch6 -p1 -b .epstopdf
%patch11 -p1 -b .badscript
%patch12 -p1 -b .dvipdfm
%patch14 -p1 -b .mfw
%patch15 -p1 -b .CAN-2004-0888
%patch16 -p1 -b .CAN-2005-0064
%patch17 -p1 -b .xpdf-CAN-2005-0206
%patch18 -p1 -b .pic

mkdir -p texmf
bzip2 -cd %{_sourcedir}/%{name}-src-%{tetexversion}.tar.bz2 | tar xf - -C texmf
bzip2 -cd %{_sourcedir}/%{name}-texmf-extras-gg-%{texmfggversion}.tar.bz2 | tar xf - -C texmf

# dvips config.generic
%patch20 -p1

# www-browser instead of netscape
%patch21 -p1 

# security
pushd libs/xpdf
%patch28 -p1 -b .cve-2005-3191_2_3
%patch29 -p1 -b .goo_overflow
%patch30 -p1 -b .chris_overflows
%patch36 -p1 -b .cve-2007-3387
%patch44 -p0 -b .cve-2007-4352_5392_5393
popd
%patch31 -p1 -b .can-2004-0941
%patch32 -p1 -b .cve-2006-2906
pushd libs/gd
%patch33 -p1 -b .cve-2007-0455
%patch34 -p0 -b .cve-2007-2756
%patch37 -p1 -b .cve-2007-3472
%patch38 -p1 -b .cve-2007-3473
%patch39 -p1 -b .cve-2007-3474
%patch40 -p1 -b .cve-2007-3475
%patch41 -p1 -b .cve-2007-3476
%patch42 -p1 -b .cve-2007-3477
%patch43 -p1 -b .cve-2007-3478
popd
%patch35 -p1 -b .cve-2007-0650

pushd texk/dvipsk
%patch45 -p0 -b .cve-2007-5935
popd

pushd libs/t1lib
%patch46 -p3 -b .cve-2007-4033
popd

%patch47 -p0 -b .cve-2007-5936_5937

## cputoolize to get updated config.{sub,guess}
#%{?__cputoolize: %{__cputoolize} -c libs/ncurses}
#%{?__cputoolize: %{__cputoolize} -c libs/libwww}
#%{?__cputoolize: %{__cputoolize} -c texk}
#%{?__cputoolize: %{__cputoolize} -c utils/texinfo}


%build
perl -pi -e 's@^vartexfonts\s*=\s.*@vartexfonts = %vartexfonts@g' texk/make/paths.mk
sh ./reautoconf
%configure \
    --with-system-ncurses \
    --with-system-zlib \
    --with-system-pnglib \
    --disable-multiplatform \
    --without-dialog \
    --without-texinfo \
    --without-xdvik

make all

# xmltex
CURRENTDIR=`pwd`
mkdir -p $CURRENTDIR/texmf/tex/xmltex/{base,config,passivetex}
mkdir -p $CURRENTDIR/texmf/doc/xmltex/{base,passivetex}

# csindex
pushd csindex-%{csidxversion}
    make CC="gcc %{optflags}"
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/texmf \
    %{buildroot}%{texmfsysvar} \
    %{buildroot}%{vartexfonts} \
    %{buildroot}/usr/local/share/texmf

tar cf - texmf | tar xf - -C %{buildroot}%{_datadir}

export TEXMFLOCAL=%{buildroot}/usr/local/share/texmf
export TEXMFSYSVAR=%{buildroot}%{texmfsysvar}
export VARTEXFONTS=%{buildroot}%{vartexfonts}
export PATH=%{buildroot}/%{_bindir}:$PATH
export TEXMF=%{buildroot}%{_datadir}/texmf
%makeinstall texmf=%{buildroot}%{_datadir}/texmf

# clean initial %{vartexfonts}
rm -rf %{buildroot}%{vartexfonts}/*

pushd csindex-%{csidxversion}
    install -c -s -m 0755 csindex %{buildroot}%{_bindir}/
popd

rm -f %{buildroot}%{_infodir}/dir
bzip2 -9f %{buildroot}%{_infodir}/*info* || true

# these are links

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
install -m 0755 %{_sourcedir}/tetex.cron %{buildroot}%{_sysconfdir}/cron.daily

# Fix permission for directory "/usr/share/texmf/fonts/tfm/jknappen"
find %{buildroot}%{_datadir}/texmf -type d -print | xargs chmod 755

# call the spec-helper before creating the file list
# (thanks to Pixel).
s=/usr/share/spec-helper/spec-helper ; [ -x $s ] && $s

# remove unwanted files
rm -f %{buildroot}%{_bindir}/{readlink,a2ping}
rm -f %{buildroot}%{_mandir}/man1/readlink.1*

### Files list
find %{buildroot} -type f -or -type l | \
    sed -e "s|%{buildroot}||g" | \
    grep -v "^/etc" | grep -v ".orig$" | \
    sed -e "s|%{_datadir}/texmf/dvips/config/config\.ps$|%config(noreplace) &|" \
        -e "s|%{_datadir}/texmf/dvips/config/config\.\(generic\|pdf\|www\)$|%config &|" \
        -e "s|%{_datadir}/texmf/dvipdfm/config/config|%config(noreplace) &|" \
        -e "s|%{_datadir}/texmf/xdvi/XDvi|%config &|" \
        -e "s|%{_datadir}/texmf/tex/generic/config/.*|%config &|" \
        -e "s|%{_datadir}/texmf/tex/dvips/config/updmap$|%config(noreplace) &|" \
        -e "s|^%{_mandir}\(.*\)|%attr(644,root,root) \%{_mandir}\1|" > filelist.full

find %{buildroot}%{_datadir}/texmf* \
    %{buildroot}%{_includedir}/kpathsea -type d | \
    sed "s|^%{buildroot}|\%attr(-,root,root) \%dir |" >> filelist.full

# dir for TEXMFLOCAL
echo "%attr(755,root,root) %dir /usr/local/share/texmf" >> filelist.full

# subpackages
grep -v "/doc/" filelist.full | grep latex | \
    grep -v "%{_datadir}/texmf/tex/latex/context" | \
    grep -v "%{_datadir}/context/data/latex-scite.properties" \
    > filelist.latex

grep -v "/doc/" filelist.full | grep xmltex > filelist.xmltex

grep -v "/doc/" filelist.full | \
    grep "%{_includedir}" > filelist.devel
echo "%attr(-,root,root) %dir %{_includedir}/kpathsea" >> filelist.devel
echo "%{_libdir}/libkpathsea.la" >> filelist.devel
echo "%{_libdir}/libkpathsea.a" >> filelist.devel

grep -v "/doc/" filelist.full | grep dvips | \
     grep -v "%{_datadir}/texmf/tex" | \
    grep -v "%{_datadir}/texmf/dvips/config/config.ps" > filelist.dvips
echo "%{_bindir}/dvired" >> filelist.dvips
echo "%{_bindir}/dvi2fax" >> filelist.dvips

grep -v "/doc/" filelist.full | grep dvipdfm | \
    grep -v "%{_datadir}/texmf/tex"	|
    grep -v "%{_datadir}/texmf/dvipdfm/config/config" |
    grep -v "%{_datadir}/texmf/dvips" > filelist.dvipdfm
echo "%{_bindir}/ebb" >> filelist.dvipdfm
echo "%{_bindir}/dvipdft" >> filelist.dvipdfm

grep -v "/doc/" filelist.full | grep dvilj | \
    grep -v "%{_datadir}/texmf/tex/latex" > filelist.dvilj

grep -v "/doc/" filelist.full | grep afm > filelist.afm

grep "/doc/" filelist.full > filelist.doc
echo "%{_bindir}/texdoc" >> filelist.doc
echo "%{_bindir}/texdoctk" >> filelist.doc

cat >> filelist.context <<EOF
%{_bindir}/mptopdf
EOF

cat > filelist.texi2html <<EOF
%{_bindir}/texi2html
%attr(644,root,root) %{_mandir}/man1/texi2html.1.bz2
%{_datadir}/texinfo/html/texi2html.html
%{_infodir}/texi2html.info.bz2
EOF

# now files listed only once, i.e. not included in any subpackage, will
# go in the main package
cat filelist.full \
    filelist.latex \
    filelist.devel \
    filelist.dvips \
    filelist.dvilj \
    filelist.afm \
    filelist.doc \
    filelist.dvipdfm \
    filelist.xmltex \
    filelist.context \
    filelist.texi2html $EXTRACAT | \
    sort | uniq -u > filelist.main

# %_docdir link.
mkdir -p %{buildroot}%{_datadir}/doc
ln -sf ../../..%{_datadir}/texmf/doc %{buildroot}%{_datadir}/doc/tetex-doc-%{docversion}

# add dvipdfpress
cp %{_sourcedir}/dvipdfpress %{buildroot}%{_bindir}/dvipdfpress


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f filelist.*


%post
%_install_info web2c.info
%_install_info kpathsea.info


%post latex
%_install_info latex.info


%post dvips
%_install_info dvips.info


%post texi2html
%_install_info texi2html.info


%preun
%_remove_install_info kpathsea.info
%_remove_install_info web2c.info


%preun dvips
%_remove_install_info dvips.info


%preun latex
%_remove_install_info latex.info


%preun texi2html
%_remove_install_info texi2html.info



%files -f filelist.main
%defattr(-,root,root)
%attr(1777,root,root) %dir %{vartexfonts}
%{_sysconfdir}/cron.daily/tetex.cron

%files -f filelist.latex latex
%defattr(-,root,root)

%files -f filelist.dvips dvips
%defattr(-,root,root)

%files -f filelist.dvilj dvilj
%defattr(-,root,root)

%files -f filelist.afm afm
%defattr(-,root,root)

%files -f filelist.dvipdfm dvipdfm
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/dvipdfpress

%files -f filelist.devel devel
%defattr(-,root,root)

%files -f filelist.xmltex -n %{xmltexname}
%defattr(-,root,root)

%files -f filelist.context context
%defattr(-,root,root)

%files -f filelist.texi2html texi2html
%defattr(-,root,root)


%changelog
* Tue Nov 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- P44: security fix for CVE-2007-{4352,5392,5393}
- P45: security fix for CVE-2007-5935
- P46: security fix for CVE-2007-4033
- P47: security fix for CVE-2007-{5936,5937}

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- P36: security fix for CVE-2007-3387
- P37: security fix for CVE-2007-3472
- P38: security fix for CVE-2007-3473
- P39: security fix for CVE-2007-3474
- P40: security fix for CVE-2007-3475
- P41: security fix for CVE-2007-3476
- P42: security fix for CVE-2007-3477
- P43: security fix for CVE-2007-3478

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- P33: security fix for CVE-2007-0455
- P34: security fix for CVE-2007-2756
- P35: security fix for CVE-2007-0650

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- requires libxau and libxdmcp

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- rebuild against modular X
- we don't build xdvik, so don't allow it to be enabled in configure
  and want libXaw
- cleanup some provides/obsoletes
- make /usr/local/bin/perl exempt from being included as a requires
  (there are a few scripts in the tetex-src directory thus)
- don't mark .cnf files in /usr/share/texmf as config files
- don't make the cron script a config file

* Sat Dec 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- rebuild against new gettext

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- P31: security fix for CAN-2005-0941 (embedded gd)
- P32: security fix for CVE-2006-2906 (embedded gd)
- drop P25, P26, P27 (passivetex)
- some spec fixes
- rebuild against new ncurses

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- don't call env after every %%post script
- use the %%_info_install and friends macros

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- drop S20, we don't ship or build ttf2pk
- buildrequires: automake1.7
- rebuild with gcc4

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- P28: security fixes for CVE-2005-319[123]
- P29: fix an overflow in goo/gmem.c
- P30: security fixes for CVE-2005-362[45678]

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- Obfuscate email addresses and new tagging
- Uncompress patches
- get rid of the xmltexrelease delta crud

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-1avx
- 3.0
- merge with cooker 3.0-12mdk:
  - lots of little changes
  - remove texi2html 1.64 source as mainstream contains 1.76
  - fixes for CAN-2004-0888, CAN-2005-0064, CAN-2005-0206 (none of
    which should impact a typical Annvix install)
- NOTE: we could/should probably trim this sucker done some more
- drop P10 (ttf2pk, which we don't have)
- build against new libpng and libxpm

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-18avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-17avx
- rebuild for new gcc
- drop S4 (icons)
- don't build a menu entry we're never going to use
- spec cleanups

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-16avx
- bootstrap build

* Sat Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-15avx
- Annvix build

* Fri Apr 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.2-14sls
- sync with cooker 15mdk:
  - texmfgg archive updated to release 2.0.2d: (ghibo)
    - updated pause.sty to version (fixes bug #6216)
    - added swedish hyphenation pattern file, as now license is free LPPL
    - added Catalan hyphenation pattern file
    - added Gaeilge (Irish) hyphenation pattern file
    - pdfpages.sty 0.21 -> 0.3e
    - modified prosper.cls so that RequirePackage{graphicx} is loaded after
      the seminar package (fixes bug #5857)
    - caption.sty 1.4b -> 3.0a
    - layouts.sty 2.6 -> 2.6b
      - tex/latex/carlisle/* updated
    - hyperref 6.74h -> 6.74m
    - rotfloat.sty 1.1 -> 1.2
  - merged 'badc' patch from RH (ghibo)
  - added patch for passivetex 1.25 (ghibo)
  - added Requires: tetex-context into latex subpackage (ghibo)
  - Provides/Obsoletes: prosper for latex (Guillaume Rousse)
- remove %%haveghost6 macro since it's unused

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.0.2-13sls
- minor spec cleanups
- remove %%build_opensls macro

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.0.2-12sls
- don't build jadetex for %%build_opensls

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.0.2-11sls
- OpenSLS build
- tidy spec
- use %%build_opensls to exclude packaging xdvi, mfwin, and doc
- use %%build_opensls to not build ttf2pk; no BuildRequires: freetype-devel
- remove support for mdk 9.0
- don't terminate build on unpackaged file finding
- explicitly remove readlink and it's manpage (conflicts with coreutils)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
