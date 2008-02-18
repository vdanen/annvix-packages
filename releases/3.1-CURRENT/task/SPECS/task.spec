#
# spec file for package task
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#

%define revision	$Rev$
%define name		task
%define version		1.0
%define release		%_revrel

Summary:	Virtual packages to install RPM packages by task
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2
Group:		System/Servers
URL:		http://annvix.org/

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
This is a meta-package to install other RPM packages by task.


%package lamp
Summary:	Installs packages for LAMP (Linux, Apache, MySQL, PHP/Perl/Python)
Group:		System/Servers
Requires:	httpd
Requires:	httpd-mod_perl
Requires:	httpd-mod_php
Requires:	php-cli
Requires:	perl
Requires:	python
Requires:	mysql
Requires:	mysql-client
Requires:	perl-DBD-mysql

%description lamp
This meta-package installs the LAMP stack (Linux, Apache, MySQL,
PHP/Perl/Python).


%package audit
Summary:	Installs packages for system auditing
Group:		System/Base
Requires:	audit
Requires:	apparmor
Requires:	aide
Requires:	nmap
Requires:	rsec

%description audit
This meta-package installs packages useful for system auditing, such as
AppArmor, AIDE, and nmap.


%package mail
Summary:	Installs packages for a full mail server
Group:		System/Servers
Requires:	smtpdaemon
Requires:	spamassassin-spamd
Requires:	imaps-server
Requires:	pop3s-server
Requires:	procmail

%description mail
This meta-package installs packages for a full mail server (SMTP server,
POP3S/IMAPS servers, SpamAssassin).


%files lamp
%defattr(-,root,root)

%files audit
%defattr(-,root,root)

%files mail
%defattr(-,root,root)


%changelog
* Mon Feb 18 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- first task meta-package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
