#
# spec file for package lynx
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		lynx
%define version 	2.8.5
%define release		%_revrel
%define epoch		1

%define versio_		2-8-5

Summary:	Text based browser for the world wide web
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Networking/WWW
URL:		http://lynx.isc.org
Source0:	http://lynx.isc.org/current/%{name}%{version}.tar.bz2
Patch0:		lynx2-8-5-adapt-to-modern-file-localizations.patch
Patch1:		lynx-2.8.5-avx-config.patch
Patch2:		lynx2-8-4-fix-ugly-color.patch
Patch10:	lynx2-8-5-tmp_dir.patch
Patch11:	lynx2-8-5-don-t-accept-command-line-args-to-telnet.patch
Patch12:	lynx-2.8.5-CAN-2005-3120.patch
Patch13:	lynx-2.8.5-CVE-2005-2929.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	gettext
BuildRequires:	ncurses-devel

Provides:	webclient
Provides:	lynx-ssl
Obsoletes:	lynx-ssl

%description
This a terminal based WWW browser. While it does not make any attempt
at displaying graphics, it has good support for HTML text formatting,
forms, and tables.

This version includes support for SSL encryption.


%prep
%setup  -q -n %{name}%{versio_}
%patch0 -p1
%patch1 -p1
%patch2 -p1 
%patch10 -p1
%patch11 -p1
%patch12 -p1 -b .can-2005-3120
%patch13 -p1 -b .cve-2005-2929


%build
%configure \
    --libdir=/usr/share/lynx \
    --enable-warnings \
    --with-screen=ncurses \
    --enable-8bit-toupper \
    --enable-externs \
    --enable-cgi-links \
    --enable-persistent-cookies \
    --enable-nls \
    --enable-prettysrc \
    --enable-source-cache \
    --enable-charset-choice \
    --enable-default-colors \
    --enable-ipv6 \
    --enable-nested-tables \
    --enable-read-eta \
    --with-zlib \
    --enable-internal-links \
    --enable-libjs \
    --enable-scrollbar \
    --enable-file-upload \
    --with-ssl \
    --enable-addrlist-page \
    --enable-justify-elts \
    --enable-color-style \
    --enable-nsl-fork

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std install-help

install -d %{buildroot}%{_sysconfdir}
cat >%{buildroot}%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang lynx


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f lynx.lang
%defattr(-,root,root)
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg
%{_mandir}/*/*
%{_bindir}/*
%{_datadir}/lynx


%changelog
* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5
- rebuild against new openssl 
- spec cleanups

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5
- remove doc
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Dec 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-7avx
- P13: fix for CVE-2005-2929
- drop compressed patches

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-6avx
- updated P12 to fully fix the issue

* Sat Oct 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-5avx
- P12: fix for CAN-2005-3120

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-3avx
- rebuild

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-2avx
- update P1 so startfile points to our site

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-1avx
- 2.8.5

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-0.dev.12.17avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 2.8.5-0.dev.12.16sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.8.5-0.dev.12.15sls
- OpenSLS build
- tidy spec
- Epoch: 1 because we make the release tag make more sense
