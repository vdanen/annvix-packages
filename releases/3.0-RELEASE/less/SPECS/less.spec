#
# spec file for package less
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		less
%define version		416
%define release		%_revrel

%define lessp_ver	1.53

Summary:	A text file browser similar to more, but better
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://www.greenwoodsoftware.com/less
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
Source1:	faq_less.html
Source2:	http://www-zeuthen.desy.de/~friebel/unix/less/lesspipe-%{lessp_ver}.tar.bz2
Patch0:		less-374-mdv-manpages.patch
Patch1:		lesspipe.lynx_for_html-mdv.patch
Patch2:		lesspipe-1.53-mdv-posix.patch
Patch3:		less-382-fdr-fixline.patch
Patch4:		less-392-fdr-Foption.patch
Patch5:		lesspipe-1.53-mdv-no-o3read.patch

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

# lesspipe.sh requires file
Requires:	file

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi). 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 2
%patch0 -p1
pushd lesspipe-%{lessp_ver}
%patch1 -p1
%patch2 -p1
%patch5 -p1
chmod a+r *
popd

%patch3 -p1 -b .fixline
%patch4 -p1 -b .Foption


%build
CFLAGS=$(echo "%{optflags} -DHAVE_LOCALE" | sed -e s/-fomit-frame-pointer//)
%configure2_5x
%make 

pushd lesspipe-%{lessp_ver}
    ./configure --yes
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
# faq
install -m 0644 %{_sourcedir}/faq_less.html .

pushd lesspipe-%{lessp_ver}
    %makeinstall PREFIX=%{buildroot}%{_prefix}
popd

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/20less.sh
CHARSET=\$(locale charmap 2> /dev/null) 
case "\$CHARSET" in 
       UTF-8) 
               export LESSCHARSET="\${LESSCHARSET:-utf-8}" 
       ;; 
       * ) 
               export LESSCHARSET="\${LESSCHARSET:-koi8-r}" 
       ;; 
esac
# Make a filter for less
export LESSOPEN="|/usr/bin/lesspipe.sh %s"
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/20less.csh
if ! ( \$?LESSCHARSET ) then
	set CHARSET=\ocale charmap\
+	if ( "\$CHARSET" == "UTF-8" ) then
		setenv LESSCHARSET utf-8
	else
		setenv LESSCHARSET koi8-r
	endif
endif
# Make a filter for less
setenv LESSOPEN "|/usr/bin/lesspipe.sh %s"
EOF

cat << EOF > README.avx
This version of less includes lesspipe.sh from Wolfgang Friebel
( http://www-zeuthen.desy.de/~friebel//unix/less/ ).

This enables you to view gz, zip, rpm and html files
among others with less. It works by setting the LESSOPEN 
environment variable, see the man pages for details.

If you want to disable this behavior, either use 'unset LESSOPEN' or
use an alias ( alias less='less -l' ).

less will open html files with lynx, then html2text, then cat if
none of the previous were found.
EOF


install -m 0644 lessecho.1 %{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_sysconfdir}/profile.d/*

%files doc
%defattr(-,root,root)
%doc faq_less.html lesspipe-%{lessp_ver}/{BUGS,COPYING,ChangeLog,README,english.txt}
%doc README.avx


%changelog
* Sat Dec 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 416
- order the profile.d/ scripts and drop executable bit

* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 416
- rebuild against new ncurses

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 416
- 416

* Fri Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 394
- rebuild against new ncurses

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 394
- 394
- lesspipe 1.53
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcedir/file instead of %%{SOURCEx}
- rediffed P2 from Mandriva
- P3: fix display of bogus newline for growing files (fedora)
- P4: fix the -F option (fedora)
- P5: improved less config (mdv)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 382
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 382
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-4avx
- lesspipe 1.52
- use lesspipe's included manpage
- move LESSOPEN variable to the profile.d scripts and remove less wrapper
  (waschk)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-2avx
- bootstrap build

* Wed Sep 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 382-1avx
- 382
- spec cleanups

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 381-5avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 381-4sls
- minor spec cleanups

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 381-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
