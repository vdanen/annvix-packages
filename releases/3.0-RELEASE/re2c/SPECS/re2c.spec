#
# spec file for package re2c
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		re2c
%define version		0.13.1
%define release		%_revrel

Summary:	A tool for generating C-based recognizers from regular expressions
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Development/Other
URL:		http://re2c.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/re2c/re2c-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
re2c is a great tool for writing fast and flexible lexers. It has served many
people well for many years and it deserves to be maintained more actively. re2c
is on the order of 2-3 times faster than a flex based scanner, and its input
model is much more flexible.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# fix attributes
chmod 0644 doc/* examples/*.c examples/*.re examples/rexx/* CHANGELOG README

find lessons -type f -exec chmod 0644 {} \;
find test -type f -exec chmod 0644 {} \;

# don't ship windows code
rm -rf lessons/001_upn_calculator/windows


%build
%configure2_5x

%make

# regenerate file scanner.cc
rm -f scanner.cc
./re2c scanner.re > scanner.cc
rm -f re2c scanner.o
%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/re2c
%{_mandir}/man1/re2c.1*

%files doc
%defattr(-,root,root)
%doc doc/* examples CHANGELOG README lessons


%changelog
* Wed Dec 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.13.1
- first Annvix build (needed by spamassassin)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
