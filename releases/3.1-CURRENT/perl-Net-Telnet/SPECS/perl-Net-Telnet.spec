#
# spec file for package perl-Net-Telnet
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Net-Telnet
%define revision	$Rev$
%define name		perl-%{module}
%define	version		3.03
%define	release		%_revrel

Summary: 	%{module} module for Perl
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/J/JR/JROGERS/Net-Telnet-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Net::Telnet allows you to make client connections to a TCP port and do network
I/O, especially to a port using the TELNET protocol.  Simple I/O methods such
as print, get, and getline are provided.  More sophisticated interactive
features are provided because connecting to a TELNET port ultimately means
communicating with a program designed for human interaction.  These interactive
features include the ability to specify a timeout and to wait for patterns to
appear in the input stream, such as the prompt from a shell.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,755)
%{_mandir}/man3/*
%{perl_vendorlib}/Net/*


%changelog
* Sun Feb 17 2008 Vincent Danen <vdanen-at-build.annvix.org> 3.03
- first Annvix build for mrtg-contribs

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
