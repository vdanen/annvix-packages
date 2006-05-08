#
# spec file for package ghostscript
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ghostscript
%define version		8.15.2
%define release		%_revrel

Summary:	PostScript/PDF interpreter and renderer
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Publishing
URL:		http://www.cups.org/espgs/index.php
Source0:	ftp://ftp2.easysw.com/pub/ghostscript/espgs-%{version}-source.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext-devel


%description
Ghostscript is a set of software that provides a PostScript(TM) interpreter,
a set of C procedures (the Ghostscript library, which implements the
graphics capabilities in the PostScript language) and an interpreter for
Portable Document Format (PDF) files. Ghostscript translates PostScript code
into many common, bitmapped formats, like those understood by your printer
or screen. Ghostscript is normally used to display PostScript files and to
print PostScript files to non-PostScript printers.
Most applications use PostScript for printer output.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n espgs-%{version}


%build
%configure \
    --without-x \
    --enable-dynamic

make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_libdir}/ghostscript,%{_sysconfdir},%{_mandir}/man1,%{_docdir}/ghostscript-%{version}}

make prefix=%{buildroot}%{_prefix} \
    install_prefix=%{buildroot} \
    gssharedir=%{buildroot}%{_libdir}/ghostscript/%{version} \
    docdir=%{_docdir}/ghostscript-%{version} \
    bindir=%{buildroot}%{_bindir} \
    mandir=%{buildroot}%{_mandir} \
    install

ln -sf gs.1.bz2 %{buildroot}%{_mandir}/man1/ghostscript.1.bz2
ln -sf gs %{buildroot}%{_bindir}/ghostscript

mkdir -p %{buildroot}{%{_libdir}/cups/filter,%{_datadir}/cups/model,%{_sysconfdir}/cups}
install -m 0755 pstoraster/pstoraster %{buildroot}%{_libdir}/cups/filter
install -m 0755 pstoraster/pstopxl %{buildroot}%{_libdir}/cups/filter
install -m 0755 pstoraster/*.ppd %{buildroot}%{_datadir}/cups/model
install -m 0644 pstoraster/pstoraster.convs %{buildroot}%{_sysconfdir}/cups

rm -rf %{buildroot}%{_mandir}/de


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_datadir}/ghostscript
%{_bindir}/*
%{_mandir}/man1/*
%attr(0755,root,root) %{_libdir}/cups/filter/*
%dir %{_datadir}/ghostscript/8.15
%{_datadir}/ghostscript/8.15/*
%{_datadir}/cups/model/*
%config(noreplace) %{_sysconfdir}/cups/pstoraster.convs

%files doc
%defattr(-,root,root)
%doc %{_docdir}/ghostscript-%{version}


%changelog
* Mon May 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.15.2
- first Annvix build
