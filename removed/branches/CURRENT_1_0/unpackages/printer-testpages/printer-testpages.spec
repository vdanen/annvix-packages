%define name	printer-testpages
%define version	1.1
%define release	2sls

Summary:	Test pages to check the output quality of printers
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Publishing
URL:		http://www.linuxprinting.org/
Source:		printer-testpages.tar.bz2

BuildRoot:	%_tmppath/%name-%version-%release-root

%description
These are sample files to check the output quality of printers. Thers
is the CUPS test page with colour gradients, the Red Hat test page
with image position checks, a photo test page and a text test page.

%prep
%setup -q

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/printer-testpages
cp *.ps *.jpg *.asc %{buildroot}%{_datadir}/printer-testpages

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/printer-testpages

%changelog
* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.1-2sls
- rebuild

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.1-1sls
- first OpenSLS package (breakout testpages from the monolithic
  printer-drivers package)
- use our own tarball with files so we don't need fig2dev to make the ps
  files (if we ever need the originals, they're in the mdk package)
