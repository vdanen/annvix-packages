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

Summary:	The TeX text formatting system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		Publishing
URL:		http://www.tug.org/teTeX/
Source0:	ftp://cam.ctan.org/tex-archive/systems/unix/teTeX/2.0/distrib/sources/%{name}-src-%{tetexversion}.tar.bz2
Source1:	ftp://cam.ctan.org/tex-archive/systems/unix/teTeX/2.0/distrib/sources/%{name}-texmf-%{texmfversion}.tar.bz2
Source3:	ftp://cam.ctan.org/tex-archive/systems/unix/teTeX/2.0/distrib/sources/%{name}-texmfsrc-%{texmfsrcversion}.tar.bz2
Source5:	http://peoples.mandrakesoft.com/~ghibo/%{name}-texmf-extras-gg-%{texmfggversion}.tar.bz2
Source6:	http://peoples.mandrakesoft.com/~ghibo/%{name}-texmfsrc-extras-gg-%{texmfggversion}.tar.bz2
Source8:	ftp://ftp.dante.de/pub/tex/macros/xmltex.tar.bz2
Source10:	tetex.cron
Source11:	ftp://math.feld.cvut.cz/pub/cstex/tetex-rpm/mandrake/csindex-%{csidxversion}.tar.bz2
Source20:	ttf2pk.tar.bz2
Source21:	dvipdfpress

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
Patch25:	passivetex-1.23.patch
Patch26:	passivetex-1.24.patch
Patch27:	passivetex-1.25.patch
# security
Patch28:	xpdf-3.00-CVE-2005-3191_2_3.patch
Patch29:	xpdf-3.00-goo-overflow.patch
Patch30:	xpdf-3.00-chris-overflows.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison, ed, flex, gettext-devel, autoconf2.1
BuildRequires:	ncurses-devel, png-devel, xpm-devel, XFree86-devel

Requires:	tmpwatch, dialog, ed, info-install
Obsoletes:	cweb
Provides:	cweb

%description
teTeX is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
typesetter independent .dvi (DeVice Independent) file as output.
Usually, TeX is used in conjunction with a higher level formatting
package like LaTeX or PlainTeX, since TeX by itself is not very
user-friendly.

Install teTeX if you want to use the TeX text formatting system.  If
you are installing teTeX, you will also need to install tetex-afm (a
PostScript(TM) font converter for TeX), tetex-dvilj (for converting
.dvi files to HP PCL format for printing on HP and HP compatible
printers), tetex-dvips (for converting .dvi files to PostScript format
for printing on PostScript printers), tetex-latex (a higher level
formatting package which provides an easier-to-use interface for TeX)
and tetex-xdvi (for previewing .dvi files in X).  Unless you're an
expert at using TeX, you'll also want to install the tetex-doc
package, which includes the documentation for TeX.


%package latex
Summary:	The LaTeX front end for the TeX text formatting system
Group:		Publishing
Requires:	tetex = %{version}
Requires:	tetex-context
Provides:	prosper
Obsoletes:	prosper
Provides:	latex-xcolor
Obsoletes:	latex-xcolor
Provides:	latex-pgf
Obsoletes:	latex-pgf

%description latex
LaTeX is a front end for the TeX text formatting system.  Easier to use
than TeX, LaTeX is essentially a set of TeX macros which provide
convenient, predefined document formats for users.

If you are installing teTeX, so that you can use the TeX text formatting
system, you will also need to install tetex-latex.  In addition, you will
need to install tetex-afm (for converting PostScript font description
files), tetex-dvilj (for converting .dvi files to HP PCL format for
printing on HP and HP compatible printers), tetex-dvips (for converting
.dvi files to PostScript format for printing on PostScript printers) and
tetex-xdvi (for previewing .dvi files in X).  If you're not an expert
at TeX, you'll probably also want to install the tetex-doc package,
which contains documentation for TeX.


%package dvips
Summary:	A DVI to PostScript converter for the TeX text formatting system
Group:		Publishing
Requires:	tetex = %{version}

%description dvips
Dvips converts .dvi files produced by the TeX text formatting system
(or by another processor like GFtoDVI) to PostScript(TM) format.
Normally the PostScript file is sent directly to your printer.

If you are installing teTeX, so that you can use the TeX text formatting
system, you will also need to install tetex-dvips.  In addition, you will
need to install tetex-afm (for converting PostScript font description
files), tetex-dvilj (for converting .dvi files to HP PCL format for
printing on HP and HP compatible printers), tetex-latex (a higher level
formatting package which provides an easier-to-use interface for TeX) and
tetex-xdvi (for previewing .dvi files in X).  If you're installing TeX
and you're not an expert at it, you'll also want to install the tetex-doc
package, which contains documentation for the TeX system.


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

If you are installing teTeX, so that you can use the TeX text formatting
system, you will also need to install tetex-dvilj.  In addition, you will
need to install tetex-afm (for converting PostScript font description
files), tetex-dvips (for converting .dvi files to PostScript format for
printing on PostScript printers), tetex-latex (a higher level formatting
package which provides an easier-to-use interface for TeX) and tetex-xdvi
(for previewing .dvi files in X).  If you're installing TeX and you're
not a TeX expert, you'll also want to install the tetex-doc package,
which contains documentation for TeX.


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

If you are installing tetex in order to use the TeX text formatting system,
you will need to install tetex-afm.  You will also need to install
tetex-dvilj (for converting .dvi files to HP PCL format for printing on HP
and HP compatible printers), tetex-dvips (for converting .dvi files to
PostScript format for printing on PostScript printers), tetex-latex (a
higher level formatting package which provides an easier-to-use interface
for TeX) and tetex-xdvi (for previewing .dvi files in X).  Unless you're
an expert at using TeX, you'll probably also want to install the tetex-doc
package, which includes documentation for TeX.


%package dvipdfm
Summary:	A DVI to PDF converter
Group:		Publishing
Requires:	tetex = %{version}, tetex-dvips = %{version}

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
Provides:	texi2html
Obsoletes:	texi2html

%description texi2html
This package converts the GNU standard form of documentation (texinfo) into
HTML files which can be read with any WWW browser.


%prep
%setup -q -n %{name}-src-%{tetexversion} -a 8 -a 11
chmod 755 csindex-%{csidxversion}
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
bzip2 -cd %{SOURCE1} | tar xf - -C texmf
bzip2 -cd %{SOURCE5} | tar xf - -C texmf
cp -p texmf/metafont/config/mf.ini texmf/metafont/config/mf-nowin.ini

# dvips config.generic
%patch20 -p1

# www-browser instead of netscape
%patch21 -p1 

# passivetex 1.25
%patch25 -p1
%patch26 -p1
%patch27 -p1

# security
pushd libs/xpdf
%patch28 -p1 -b .cve-2005-3191_2_3
%patch29 -p1 -b .goo_overflow
%patch30 -p1 -b .chris_overflows
popd

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
    --without-texinfo

make all

# xmltex
CURRENTDIR=`pwd`
mkdir -p $CURRENTDIR/texmf/tex/xmltex/{base,config,passivetex}
mkdir -p $CURRENTDIR/texmf/doc/xmltex/{base,passivetex}
pushd %{xmltexname}/base
    cp -p xmltex.tex *.xmt $CURRENTDIR/texmf/tex/xmltex/base
    cp -p *.ini xmltex.cfg $CURRENTDIR/texmf/tex/xmltex/config
    cp -p *.xml manual.tex test*.tex test*.cfg $CURRENTDIR/texmf/doc/xmltex/base
popd
pushd %{xmltexname}/contrib/passivetex
    cp -p *.xmt *.sty $CURRENTDIR/texmf/tex/xmltex/passivetex
popd

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
install -m 755 %{SOURCE10} %{buildroot}%{_sysconfdir}/cron.daily

## update map files
#TEXMFMAIN=%{buildroot}%{_datadir}/texmf \
#    %{buildroot}%{_bindir}/updmap --cnffile \
#    %{buildroot}%{_datadir}/texmf/web2c/updmap.cfg

# Fix permission for directory "/usr/share/texmf/fonts/tfm/jknappen"
find %{buildroot}%{_datadir}/texmf -type d -print | xargs chmod 755

# We keep the .log files for format .fmt files (useful to know how
# they are generated (included files, memory, etc.);
# strip buildroot path from .log files.
perl -pi -e "s@%{buildroot}@@g" %{buildroot}%{texmfsysvar}/web2c/*.log

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
    sed -e "s|.*\.cnf$|%config(noreplace) &|" \
        -e "s|%{_datadir}/texmf/dvips/config/config\.ps$|%config(noreplace) &|" \
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

grep -v "/doc/" filelist.full | grep -v fonts | \
    grep -v dvips | \
    grep -v pdftex/config | \
    grep context > filelist.context

cat >> filelist.context <<EOF
%{_bindir}/mptopdf
%{texmfsysvar}/web2c/cont-en.fmt
%{texmfsysvar}/web2c/cont-en.log
%{texmfsysvar}/web2c/metafun.log
%{texmfsysvar}/web2c/metafun.mem
%{texmfsysvar}/web2c/mptopdf.fmt
%{texmfsysvar}/web2c/mptopdf.log
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
cp %{SOURCE21} %{buildroot}%{_bindir}/dvipdfpress


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f filelist.*


# make sure ls-R used by teTeX is updated after an install
%post
/sbin/install-info %{_infodir}/web2c.info.bz2 %{_infodir}/dir
/sbin/install-info %{_infodir}/kpathsea.info.bz2 %{_infodir}/dir
/usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post latex
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
/sbin/install-info %{_infodir}/latex.info.bz2 %{_infodir}/dir
exit 0

%post dvips
/sbin/install-info %{_infodir}/dvips.info.bz2 %{_infodir}/dir
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post dvilj
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post afm
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0


%post dvipdfm
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post -n %{xmltexname}
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post context
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%post texi2html
/sbin/install-info %{_infodir}/texi2html.info.bz2 %{_infodir}/dir

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun latex
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun dvips
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun dvilj
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun afm
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun dvipdfm
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun -n %{xmltexname}
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun context
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/kpathsea.info.bz2 %{_infodir}/dir
    /sbin/install-info --delete %{_infodir}/web2c.info.bz2 %{_infodir}/dir
fi

%preun dvips
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/dvips.info.bz2 %{_infodir}/dir
fi

%preun latex
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/latex.info.bz2 %{_infodir}/dir
fi

%preun texi2html
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/texi2html.info.bz2 %{_infodir}/dir
fi


%files -f filelist.main
%defattr(-,root,root)
%attr(1777,root,root) %dir %{vartexfonts}
%config %{_sysconfdir}/cron.daily/tetex.cron

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

* Wed Sep 10 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-10mdk
- texmfgg archive to release 2.0.2b:
	- updated latex unicode macro package to fix missed 
	  characters (bug #5497).

* Sat Sep 06 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-9mdk
- Fixed Patch7 so that texconfig will call mf-nowin instead mf as default.
- Added mf-nowin man page.

* Sat Aug 30 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-8mdk
- Use /usr/share/local/texmf for variable TEXMFLOCAL, instead of
  /usr/share/texmf-local, (fixed Patch0).
- Fixed errors in fontname in typeface.map (Numbus -> Nimbus, Patch27).
- Fixed texi2html.1.bz2 in filelist.texi2html (avoid files listed twice)

* Wed Aug 27 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-7mdk
- Obsoletes: cweb.
- Fixed dependency of tetex-context subpackage.

* Thu Aug 21 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-6mdk
- Updated texi2html to release 1.64.

* Thu Aug 21 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-5mdk
- Added Patch8 (xdvi to release 22.40y).
- texmfgg archive to release 2.0.2a:
	- listings 1.1a.
	- prosper 1.5.
	- hyperref 6.73n -> 6.74h.
- Merged "security" patches from RH (badscript, xpdf, dvipdfm),
  Patch11, 12, 13.

* Thu Aug 07 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.0.2-4mdk
- made context a subpackage to reduce perl dependencies

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.2-3mdk
- cputoolize

* Wed Jun 18 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.2-2mdk
- fix build when tetex is not allready installed (can be usefull!)
 
* Mon Jun 16 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-1mdk
- passivetex 1.24.

* Thu Mar 13 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.1-6mdk
- Added missed xmltex.cfg (fixes problem reported by
  Sèbastien Ducoulombier) with xmltex.

* Thu Mar 06 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.1-5mdk
- Rebuilt because of server problems with release 2.0.1-4mdk.

* Mon Mar 03 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.1-4mdk
- Added Patch7 to texconfig, so that texconfig should no longer try to call
  "fmtutil --byfmt mfw" and thus causing error.

* Sat Mar 01 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.1-3mdk
- moved texdoc, texdoctk to tetex-doc package.
- dvipdfm/config/config now in main tree, so removed from SPEC file.
- removed algorithm.sty from *-extras-gg-* archives because of
  nonfree license, and removed files merged in 2.0.2 tree.
- use 2.0.2 trees with following fixes:
	- pdftex 1.10b.
	- fix two bugs in texdoctk.
	- mktexmf fix for CJK fonts.
	- add search patchs for non"k"-xdvi to texmf.in.
	- fix bug in texk/etc/autoconf/acspecific.m4.
	- update ragged2e.
	- support uppercase mathtime fonts via aliases.
	- removed g-brief package due to nonfree license.
	- update shadow.sty.
	- add package mparhack and jurabib.
	- SIunits.cfg updated (only comments changed)
	- replace old README by new readme in doc/latex/pdfpages
	- added sihyph23.tex

* Sun Feb 16 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.1-2mdk
- updated *-extras-gg-* archives.

* Sun Feb 16 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.1-1mdk
- Release 2.0.1.
- Readapted Patch1 (fmtutil.in) to remove things merged.
- Removed Patch2 (mfwbase), now merged in main sources.
- Removed Patch7 (updmap), now merged in main sources.
- Removed Patch8 (typo), now merged in main sources.
- Removed Patch9 (texlinks), now merged in main sources.
- Removed Patch11 (dvipdfm), now merged in main sources.
- PassiveTeX 1.23.
- Added dvipdft to binary filelist.

* Sat Feb 15 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-6mdk
- Added Patch11 to dvipdfm (fixes a segfault).

* Thu Feb 06 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-5mdk
- Fixed MAILCAPLIBDIR, MIMELIBDIR path in texmf.cnf (report by Michael
  Reinsch).

* Wed Feb 05 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-4mdk
- Added Patch9 (texlinks-mfw), so that texlinks produces the correct
  mf -> mfw link.

* Tue Feb 04 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-3mdk
- Fixed a typo in %postun mfwin.
- Moved dvipdfm/config to dvipdfm/config/config.
- added texmf-texmfsrc-gg-2.0 (Source6).
- Fixed Added %pre to dvipdfm subpackage for rpm upgrading (Götz).
- Reorderding patch numbers:
	Patch5 -> Patch1.
	Patch2 -> Patch22.
 	Patch6 -> Patch2.
	Patch54 -> Patch3.
	Patch55 -> Patch4.
	Patch20 -> Patch5.
	Patch36 -> Patch6.
	Patch12 -> Patch20.
	Patch39 -> Patch21.
	Patch45 -> Patch23.
	Patch47 -> Patch24.

* Tue Feb 04 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-2mdk
- removed unused dvi-to-ps.fpi rhs-printfilters.
- Removed Patch30 (ttf2tfm), merged into new Patch0.
- Removed Patch32 (ttf2pk).
- Added -devel package.

* Mon Feb 03 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0-1mdk
- Release: 2.0.
- Removed Patch0 (varconfig).
- Removed Patch16 (trie), now merged.
- Removed Patch3 (arm).
- Removed Patch11 (pdftex truecm), now merged.
- Removed Patch4 (texmfcnf), merged into new Patch0.
- Removed Patch13 (Tektronix).
- Removed Patch14 (going-i18n), merged into new Patch2.
- Removed Patch21 (protos).
- Removed Patch22 (dvipsk), no longer needed.
- Removed Patch23 (thumbpdf), no longer needed.
- Removed Patch24 (thumbpdf), no longer needed.
- Removed Patch31 (texmfcnf-latex209), merged into new Patch0.
- Removed Patch33 (badscript).
- Removed Patch34 (autoconf-gc), no longer needed.
- Removed Patch35 (epstopdf), no longer needed.
- Removed Patch38 (texmfcnf-xmltex), merged into new Patch0.
- Removed Patch40 (dvipsk-586f), no longer needed.
- Removed Patch41 (dvipsk-590a), no longer needed.
- Removed Patch42 (texmfcnf-misc), merged into new Patch0.
- Removed Patch43 (texmfcnf), merged into new Patch0.
- Removed Patch46 (dvips-secure), unused.
- Removed Patch50 (20020207-security), no longer needed.
- Removed Patch51 (texmfcnf-new), merged into new Patch0.
- Removed Patch52 (fmtutil-jobname), no longer needed.
- Removed Patch53 (maxstrings), no longer needed.
- Added Patch0 (texmfcnf).
- Readapted Patch5 (fmtutil).
- Readapted Patch2 (langs).
- Readapted Patch20 (xdvik-dot).
- Readapted Patch36 (epstopdf-dct).
- Readapted Patch39 (xdvi-mozilla).
- Readapted Patch54 (mf-mainmemory).
- Readapted Patch55 (mpost-mainmemory).
- Added Patch6 (mfwbase) for having mfw.base linked to mf.base, to have
  main tetex RPM package not depending on X11 libs.
- Added Patch7 (updmap) for cm-super with dvipdfm.

* Thu Jan 23 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-67mdk
- tetex 2.0rc1 for pdftex.
- removed patch53 for increasing max_strings parameters (now merged
  into main tree).
- Use -R in dvi-to-ps.fpi.
- tetex-texmf-gg 1.0.7n:
	- updated marvosym.pfb to avoid problems with ghostscript 7.05
          (bug #531 reported by Frédéric Vivien).
	- hyperref 6.73i -> 6.73m.

* Mon Jan 13 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-66mdk
- Snapshot 20030112 for pdftex.

* Mon Jan 13 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-65mdk
- tetex-texmf-gg 1.0.7m:
	- fancyhdr 2.1 -> 1.9 (for doxygen documentation).

* Sat Jan 10 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-64mdk
- Snapshot 20030107 for pdftex.
- Removed Patch48 (20020828) now merged.
- Increased pdfTeX max_strings parameters (request for Camille manuals)
  (Patches 52->56).
- Patched fmtutil for newer -jobname pdftex switch.
- Added xdvi.cfg.
- Added eurosym.map to Patch12 (dvipsgeneric).
- Removed Patch49 (now in tetex-texmf-gg 1.0.7l)
- Added missed filelist.xmltex from processing filelist.full.
- tetex-texmf-gg 1.0.7l:
	- hyperref 6.72w -> 6.73i.
	- subeqn.sty 2.0a.
	- subeqnarray.sty 2.1b.
	- subfloat.sty 2.13.
	- footmisc.sty 4.0a -> 5.0.
	- pdfpages.sty 0.2i -> 0.2l.
	- refcheck 1.8.
	- fancyhdr 1.9 -> 2.1.
	- yfonts.sty 1.2 -> 1.3.
	- added feymr/eurosym pfb.

* Fri Nov 08 2002 Giuseppe Ghibò <ghibo@mandraesoft.com> 1.0.7-63mdk
- Rebuilt.

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.7-62mdk
- fix doc subpackage group

* Fri Oct 18 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.0.7-61mdk
- security patch (P50)

* Fri Aug 30 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-60mdk
- added dvipdfpress to tetex-dvipdfm. Act as dvipdf but doesn't perform
  strong DCT downsampling of bitmap images.
- backported patch from hyperref 6.72w to 6.72v:
	- Bug fix: option bookmarksnumbered is now respected if slidesec is
          used.
	- "\let\pdfoutput\@undefined" removed.

* Fri Aug 30 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-59mdk
- disabled dvips RH secure patch (Patch46) because it doesn't allow pipes on
  entries like "o |lpr" in config.ps.

* Thu Aug 29 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-58mdk
- backported patch from tetex 20020825 (uses hash tables for map file
  loading in pdftex).
- added link in %{_datadir}/share/doc.

* Thu Aug 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-57mdk
- really rebuild with latest gcc 3.2-0.3mdk
- autoincr jaderelease as well

* Thu Aug 14 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-56mdk
- added xmltexrelease as delta (from Gwenole).

* Tue Aug 06 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-54mdk
- updated teTeX-1.0-arch.patch.bz2.
- added Tim Waugh <twaugh@redhat.com> theta patch to jadetex 3.12.
- tetex-texmf-gg-1.0.3k:
	- hyperref 6.72s -> 6.72v.
	- subfigure 2.1.3 -> 2.1.4.
	- supertabular 4.0a -> 4.1e.
	- SIunits 1.25 -> 1.33.
	- pdfpages 0.2h -> 0.2i.
	- booktabs 1.00 -> 1.61.
	- unicode.sty 2002-04-07.
	- conTeXt upgraded to release 020726.

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-53mdk
- Automated rebuild with gcc3.2

* Fri Jul 05 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-52mdk
- Use newer xdvi/oxdvi.
- Added russian hyphenation in LaTeX .fmt files.
- dvips -R (default).
- Added dvips "secure" patch (Patch46), from RedHat, but removed the 
  added "-insecure" option, because the same thing can be achieved with -R0.
- Use conditional %buildfor_mdk90 (Gwenole).
- Added XDVIINPUTS to Patch42.
- Added xmltex 1.9.
- Merged Patch37 (basque hyphenation) in Patch14 (i18n).

* Wed Jul 02 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-51mdk
- added missed pdfjadetex.ini.
- added mktexfmt.

* Tue Jul 02 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-50mdk
- fixed permission for dir "/usr/share/texmf/fonts/tfm/jknappen".
- updated thumbpdf, thumbpdf.sty, thumbpdf.tex to version 3.2.
- removed useless thumbpdf.{sty,tex}.thumb backup files in texmf tree.
- readlink conditional (for backward release compatibility).
- added jadetex 3.12.
- texmf-gg-1.0.3j:
	- added ecrm1000.tfm for jadetex.

* Tue Jul 02 2002 Pixel <pixel@mandrakesoft.com> 1.0.7-49mdk
- remove "readlink" (and its man page) since "readlink" is now in fileutils
  (otherwise it would conflict)

* Mon Jul 01 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-48mdk
- updated pdfTeX to version 1.00b-pretest.
- fixed patch13 (trie).
- added Patch43.

* Sun Jun 30 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-47mdk
- added Czech support.
- updated patch 'teTeX-texmf-dvipsgeneric.diff'.
- sligtly increase pdftex array sizes in texmf.cnf.
- trie_size increased to 250000.
- added array sizes for cslatex.
- tuned sizes for other format files.
- updated texmf-gg to version 1.0.3i:
	- added support for Czech (csplain/cslatex).
	- hyperref 6.72e -> 6.72s.
	- crop.sty 1.7 -> 1.7.
	- ccaption 3.0 -> 3.1a.
	- subfigure 2.0 -> 2.1.3.
	- added pdfpages 0.2h.

* Thu Jun 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-46mdk
- Macroszification (aka use %%configure and %%makeinstall).

* Tue May 21 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-45mdk
- Automated rebuild with gcc 3.1-1mdk

* Tue Mar 12 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-44mdk
- added a missed %%endif in .spec file.

* Mon Mar 05 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-43mdk
- removed .xpm icons from tetex-xdvi.

* Sat Mar 02 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-42mdk
- dvipsk to 5.86f so for better supporting charstring Subr.
- fixed a bug in txpxfonts Patch (removed updmap patch, fixed
  utmr8a.pfb.pfb -> utmr8a.pfb).
- updated texmf-gg to version 1.0.3h:
	- modes.mf 3.4 -> 3.5.
	- use txr4.map instead of txr.map in updmap.
	- amsrefs 1.18 -> 1.23.
	- pdftex.def 0.03h -> 0.03i.
	- hyperref 6.71e -> 6.72e (fixes bug with harvard).
	- added web.sty 2.0 (LPPL).

* Tue Feb 26 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-41mdk
- fixed resource for XDvi, replacing netscape with mozilla.
- updated texmf-gg to version 1.0.3g:
	- updated a few .map files in fontname (special, adobe, variant,
	  supplier, typeface, bitstrea).
	- draftcopy 2.12 -> 2.16.
        - amsrefs 1.15 -> 1.18.
	- pdfcwebmac.tex 3.43 -> cwebmac.tex 3.64
- mark texmf/tex/generic/config/* and texmf/dvips/config/updmap as %%config.

* Wed Feb 20 2002 Stefan van der Eijk <stefan@eijk.nu> 1.0.7-40mdk
- BuildRequires (added gcc -> != obvious, removed spec-helper ->
  = obvious).

* Tue Feb 19 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-39mdk
- fixed -38mdk %%changelog with real changelog-er.
- removed BuildRequires: gcc (obvious)
- put back spec-helper & libxpm-devel in BuildRequires.
- removed major dependency from libs in BuildRequires when not needed.

* Tue Feb 19 2002 Stefan Siegel <siegel@mandrakesoft.com> 1.0.7-38mdk
- unrolled & sorted BuildRequires.
- added autoconf, automake, gcc to BuildRequires.
- specified libmajor version in BuildRequires.

* Sun Feb 17 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-37mdk
- update texmf-gg to version 1.0.3f:
	- updated marvosym (and relative fonts) to version 2.0 (better
	  euro symbols).
	- added eurosym.sty v1.1 (with Debian license file).

* Sat Feb 16 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-36mdk
- added support for basque hyphenation.
- modified epstopdf to avoid downsampled jpeg compression in
  converted EPS bitmapped images (taken from Siep Kroonenberg suggestion).
- added support for xmltex (Patch38).
- png icons.
- update texmf-gg to version 1.0.3e:
	- added basque hyphenation file.
        - added pdfscreen.sty 1.2.
        - added truncate.sty 3.6.
	- added pdfslide.sty 0.50.
        - updated rotfloat.sty from release 1.0 to version 1.1,
        - updated cite.sty from release 3.8 to 3.9.
        - updated drftcite.sty from release 3.5 to 3.7.
	- updated overcite.sty from release 3.8 to 3.9.
	- updated crop.sty from release 1.3a to 1.6.
	- added amsrefs 1.15 clases for amslatex.
	- tex/plain/amsfonts/amssym.def: upgraded to release 2.2b.
	- tex/plain/amsfonts/cyracc.def: upgraded to release 2.2b.
	- tex/latex/amsfonts/*: upgraded to release 2.2d

* Fri Jan 11 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-35mdk
- updated epstopdf to version 2.7.
- modified epstopdf to force PDF 1.2 for pdftex/pdflatex.

* Sat Dec 29 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-34mdk
- added Patch33 to build tempfile filenames using mktemp (security
  fix from Vincent Danen <vdanen@mandrakesoft.com>
  and originally from Tim Waugh <twaugh@redhat.com>).
- added Patch34 to have reautoconf working with Guillaume's autoconf
  macro.
- updated texmf-gg to version 1.0.3d:
	- updated LaTeX to release 2001/06/01.
	- updated float package to release 1.3d.
	- updated tools package to release of 2001/09/04.
	- updated graphics package to release of 2001/07/07.
	- updated psnfss to version 8.2.
	- added mathpazo fonts 1.001 (for psnfss).
	- update crop.sty from release 1.3a to 1.6.
        - babel 3.7h: new bulgarian.ldf, frenchb.ldf (version 1.5g),
	  frenchb.cfg, icelandic.ldf, latin.ldf (version 2.0d).
        - updated cyrillic package to release June 2001.

* Thu Oct 11 2001 Stefan van der Eijk <stefan@eijk.nu> 1.0.7-33mdk
- BuildRequires: gettext-devel xpm-devel.
- Removed redundant BuildRequires.

* Tue Oct  9 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-32mdk
- Rebuild against latest libpng.
- Add BuildRequires: freetype-devel (ttf2pk).
- Patch32: fix ttf2pk build from nihil (take local kpathsea includes and lib).

* Mon Sep 17 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-31mdk
- updated teTeX-1.0-texmf-gg to version 1.0.3c. Changes includes:
  - added missed hebtech.cls
  - fixed babel he* files from babel 3.7h.

* Sat Sep 01 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-30mdk
- update teTeX-1.0-texmf-gg to version 1.0.3b. Changes includes:
  - texmf/tex/doc/help/Catalogue: updated to version 20010901.
  - texmf/tex/latex/misc/changebar.sty: updated version 3.3i to 3.4.
  - texmf/tex/latex/graphics/dvipdfm.def: updated from dvipdfm-0.13.2c archive.
  - texmf/tex/latex/misc/fancybox.sty: updated from version 1.2 to version 1.3
  - texmf/tex/latex/calrsfs: added. 
  - texmf/tex/latex/oberdiek: updated
  - texmf/tex/latex/booklet: added version 0.5
  - texmf/tex/latex/misc/float.sty: updated from version 1.2d to version 1.3a
  - texmf/tex/latex/misc/verse.sty: added version 1.1
  - texmf/tex/latex/misc/SIunits.sty moved to
    texmf/tex/latex/SIunits/ and updated from version 0.06 to version 1.25
  - texmf/tex/latex/misc/ccaption.sty: added version 3.0a
  - texmf/tex/latex/bitfield/bitfield.sty: added version 1.19
  - texmf/tex/latex/dashbox/dashbox.sty: added version 1.13            
  - texmf/tex/latex/misc/picins.sty: removed trailing ^Z
- fixed changelog (metric files for agaramon, bembo, etc., were not
  included).
- added Patch31.

* Tue Jul 24 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-29mdk
- package rebuilt.

* Tue Jul 24 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-28mdk
- fixed _iconsdir in %file section.

* Sun Jul 22 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-27mdk
- update thumbpdf to version 2.10.
- updated teTeX-1.0-texmf-gg to version 1.0.3a. Changes includes:
  - texmf/tex/latex/seminar/sem-a4.sty changed \def\paperwidth... to
    \setlength{\paperwidth}... (report by Chris Fox <foxcj@dcs.kcl.ac.uk>).
  - texmf/tex/latex/misc/url.sty upgraded from 1.4 to version 1.5.
  - texmf/tex/latex/misc/wrapfig.sty upgraded from version 3.2 to version 3.3.
  - texmf/tex/latex/footmisc.sty upgraded from 3.3j2 to 4.0a.
  - added texmf/tex/fonts/{sources,tfm}/public/mfextra fonts for
    bold typewriter.
  - updated babel from 3.7g to 3.7h.
  - added texmf/tex/latex/srcltx.
  - texmf/fonts/source/public/misc/black.mf: replaced blackcx to blacklj to
    have it METAFONTbook compliant (report by Adam Buchbinder
    <gdrago23@yahoo.com>).
  - texmf/fonts/source/public/misc/gray.mf: replaced graycx to graylj to
    have it METAFONTbook compliant (report by Adam Buchbinder
    <gdrago23@yahoo.com>).
  - added epsf.tex to texmf/tex/texinfo.
  - texmf/tex/latex/hyperref updated from version 6.71a to vesion 6.71e.

* Sun Jul 22 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-26mdk
- patch to thumbpdf for perl 5.6 (reported by Chris Fox <foxcj@dcs.kcl.ac.uk>).

* Sat Jul 21 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-25mdk
- updated dvipsk from 5.86 to 5.86e (with S. Rahtz changes).

* Thu Jul 19 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-24mdk
- updated dvipdfm to version 0.13.2c.

* Sun Jun 03 2001 Jesse Kuang <kjx@mandrakesoft.com> 1.0.7-23mdk
- remove mktexnam patches.

* Sat Jun 02 2001 Jesse Kuang <kjx@mandrakesoft.com> 1.0.7-22mdk
- merge TrueType support package ttf2pk.

* Sat Mar 24 2001 Francis Galiegue <fg@mandrakesoft.com> 1.0.7-21mdk
- Fix ia64 build.
- Chicken and egg pb was on all archs, not just Alpha.

* Mon Mar 19 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-20mdk
- fixed 'egg & ckicken' problem for building on Alpha.
- fixed path for 'ghibo' CTAN archives.

* Sun Mar 11 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-19mdk
- updated 'gg' archives.
- added PSNFSS 8.1.

* Sat Mar 10 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-18mdk
- use LaTeX 01/06/2000 sources and new 'gg' archives.
- merged RH xdvik-dot and protos patches.

* Fri Mar 09 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-17mdk
- added new release of texnansi.enc and texnansx.enc.

* Thu Feb 22 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-16mdk
- added patch for better supporting of px and tx fonts with dvipdfm,
  dvips and pdftex.

* Mon Feb 19 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-15mdk
- added dvipdfm.
- added pxfonts (Palatino + Math).
- added txfonts (Times + Math).

* Fri Nov 17 2000 David BAUDENS <baudens@mandrakesoft.com> 1.0.7-14mdk
- Rebuild with gcc-2.96 & glibc-2.2.

* Sun Oct 22 2000 David BAUDENS <baudens@mandrakesoft.com> 1.0.7-13mdk
- BuildRequires: ed.

* Tue Oct 17 2000 David BAUDENS <baudens@mandrakesoft.com> 1.0.7-12mdk
- Allow to build (aka fix filelist).

* Tue Oct 03 2000 Daouda Lo <daouda@mandrakesoft.com> 1.0.7-11mdk
- add icons to xdvi menu entry.

* Mon Sep 25 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-10mdk
- included some of changes to SPEC files made by Alexander Skwar <ASkware@DigitalProjectcs.com>
  (more macros, fixed location of some manpage).

* Mon Aug 28 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-9mdk
- changed mandir to %%{_mandir}, and infodir to %%{_infodir}.
- xdvi menu name coherent.

* Fri Aug 25 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-8mdk
- added %noreplace to *.cnf (Preston Brown <pbrown@redhat.com>)
- added %noreplace to config.ps file.
- removed bzip2 of man pages (now handled by spec-helper).
- removed perl script to handle bzip2 files for filelists (now handled
  by spec-helper).
- increased trie size for allowing more hyphenation patterns (i18n).

* Fri Jun 02 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-7mdk
- updated the LaTeX hyperref package to version 6.70f for getting jadetex
  working.
- added support for spanish, portuguese and sweden pattern hyphenation in the
  default LaTeX format files (hope trie values are enough...).

* Fri May 05 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-6mdk
- fixed man pages permission.

* Sat Apr 29 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-5mdk
- changed arrays texmf.cnf the array value for jadetex, pdfjadetex, according to
  the Christoph, Rahtz, Pepping's "Installing JadeTeX" document.

* Sat Apr 01 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-4mdk
- change group (now "Publishing") according to the new scheme.
- removed wmconfig and .desktop entries for xdvi, and added the new menu
  entry.

* Fri Mar 03 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.7-3mdk
- updated teTeX-texmf to version 1.0.2.

* Fri Feb 11 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com>
- updated to version 1.0.7.
- merged k6 and arm patches into teTeX-1.0-arch.patch
- sligtly increased internal array main_memory, so that latex
  doesn't have problems with big macro packages such as pstricks
  or Xy-TeX.
- integrate teTeX-1.0-tektrokix.patch (fixes a typo) from Jeff
  Johnson <jbj@redhat.com>.

* Wed Dec 08 1999 - David BAUDENS <baudens@mandrakesoft.com>
- AMD K6 is not an i686 processor (another)
- Replace $RPM_ARCH by %%{_target_cpu}

* Thu Nov 11 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- mark /usr/share/texmf/dvips/config.ps as %config
  (Jeff Johnson <jbj@redhat.com>, #4842)
- mark also config.pdf, config.www and config.generic as %config.
- added BuildPreReq.

* Thu Aug 26 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- fine tuning subpackage package list.
- added teTeX dependence to package xdvi (it cannot works without fonts).

* Wed Aug 25 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- cleaned %clean. Now spec file support buildroot.
- added support for 'resolution' in dvi-to-ps.fpi as well as
  the config.generic file.
- fixed a problem in manpage links (reported by Dusan
  Gabrijelcic <dusan@kamra.e5.ijs.si>).
- moved mfw to tetex-xdvi to have main tetex package rpm indepedendent from 
  X11 libraries (Jeff Johnson <jbj@redhat.com> in rawhide).
- added PAPERSIZE option to dvi-to-ps.fpi (Jeff Jonhson <jfj@redhat.com>
  in rawhide).

* Wed Aug 04 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- fixed VARTEXFONTS path in config file.

* Wed Jul 14 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- updated to 1.0.6.
- used src-1.0.6 archive and thus removed some patches.

* Sat Jun 26 1999 Giuseppe Ghibò <ghibo@caesar.polito.it>
- mandrake adaptions.
- speed up TEXMFCNF path.

* Fri Jun 25 1999 Giuseppe Ghibò <ghibo@caesar.polito.it>
- fixed new bugs reported by Thomas Esser (included
  patch 1.0.5-1.0.6-pre).
- added amstex, bamstex and bplain to the list of format files to build.

* Wed Jun 23 1999 Giuseppe Ghibò <ghibo@caesar.polito.it>
- fixed and removed unneeded things in teTeX-1.0-texmfcnf.patch,
  according to Thomas Esser suggestions.

* Sun Jun 20 1999 Giuseppe Ghibò <ghibo@caesar.polito.it>
- upgraded to teTeX 1.0.5.
- merged .spec file with Jeff Johnson's 1.0.1 .spec file from rawhide. 

* Sun Jun 13 1999 Giuseppe Ghibò <ghibo@caesar.polito.it>
- upgraded to teTeX 1.0 final.
- removed texmf.cnf external config file, and provided
  as patch.
- removed ``texconfig init'' (now it's included into 'make install').
- moved texmf unpacking to buildroot before 'make install'.
- added italian hyphenation.

* Thu Jun 03 1999 Kayvan A. Sylvan <kayvan@sylvan.com>
- upgraded snapshot
- Fixed PATH setting for ``texconfig init''. As it was, you could
  not build a working teTeX on a machine with teTeX installed.

* Thu Apr 01 1999 Cristian Gafton <gafton@redhat.com>
- upgraded snapshot

* Tue Mar 23 1999 Erik Troan <ewt@redhat.com>
- set limits for jadetex

* Tue Mar 23 1999 Cristian Gafton <gafton@redhat.com>
- I think I have got the buildroot problems right this time
- auto rebuild in the new build environment (release 15)

* Fri Mar 19 1999 Cristian Gafton <gafton@redhat.com>
- fix buildroot problems

* Mon Mar 15 1999 Michael Maher <mike@redhat.com>
- fixed BUG: 978

* Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
- slight changes in the packaging (unpack texmf directly into the buildroot
  and build it there)
- added texmfsrc source tarball to comply with the license

* Mon Mar 07 1999 Michael Maher <mike@redhat.com>
- updated package

* Mon Jan 11 1999 Cristian Gafton <gafton@redhat.com>
- add patch to make it compile on the arm (RmS)
- build for glibc 2.1
- use tar hack instead of the cp -a to overcome cp's brokeness re: symlinks
  handling

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- enable italian formatting

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- requires ed
- Fixed obsoletes line
- credted the doc subpackage
- fully buildroot
- require dialog in the main package
- add support for wmconfig in for the xdvi package

* Fri Sep 11 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to 0.9
- texmf-src package is gone
- use /var/lib/texmf instead of /var/tmp/texmf

* Sat Aug 22 1998 Jeff Johnson <jbj@redhat.com>
- make sub-packages depend on teTeX (problem #214)

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- eliminate environment when running texhash (problem #849)

* Mon Aug 17 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Feb  5 1998 Otto Hammersmith <otto@redhat.com>
- added install-info support (dvips, fontname and kpathsea)
- combined the two changelogs in the spec file.

* Tue Oct 14 1997 Michael Fulbright <msf@redhat.com>
- Fixed dvi-to-ps.fpi to create temp files more safely.

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr  8 1997 Michael Fulbright <msf@redhat.com>
- Removed afmdoit from file list (mistakenly added in release 3 rpm)

* Mon Mar 24 1997 Michael Fulbright <msf@redhat.com>
- Upgraded to tetex-lib to 0.4pl8 and fixed cron tmpwatch entry to not
  delete /var/lib/texmf/fonts and /var/lib/texmf/texfonts

* Fri Mar 07 1997 Michael Fulbright <msf@redhat.com>
- Upgraded to 0.4pl7.

* Mon Feb 17 1997 Michael Fulbright <msf@redhat.com>
- Upgraded to 0.4pl6, and fixed file permissions on /var/lib/texmf/texfonts
  so normal users could create fonts on demand.
