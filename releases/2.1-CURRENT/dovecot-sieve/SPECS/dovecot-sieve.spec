#
# spec file for package dovecot-sieve
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision        $Rev$
%define name		dovecot-sieve
%define version		1.0.2
%define release		%_revrel

Summary:	Sieve plugin for dovecot
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Servers
URL:		http://www.dovecot.org/
Source0:	http://dovecot.org/releases/sieve/%{name}-%{version}.tar.gz
Source1:	http://dovecot.org/releases/sieve/%{name}-%{version}.tar.gz.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dovecot-devel >= %{version}

Requires:	dovecot >= %{version}

%description
Sieve is a language that can be used to create filters for electronic
mail. It owes its creation to the CMU Cyrus Project, creators of Cyrus
IMAP server.

This dovecot plugin is derived from Cyrus IMAP v2.2.12.


%prep
%setup -q -n %{name}-%{version}


%build
%configure \
    --with-dovecot=%{_includedir}/dovecot \
    --libdir=%{_datadir}
for f in `find . -name Makefile`
do
    mv -f $f $f.orig
    sed -e's/\-I\$(dovecotdir)\/src/\-I\$(dovecotdir)/g' \
        -e's/\-I\$(dovecot_incdir)\/src/\-I\$(dovecot_incdir)/g' \
        -e's/\$(dovecotdir)\/src\(\/lib\/.*\.a\)/\$(libdir)\/dovecot\1/g' \
        < $f.orig > $f
done

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}/%{_datadir}/dovecot/lda/*.a


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_datadir}/dovecot/lda/*.so
%{_datadir}/dovecot/lda/*.la


%changelog
* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvi.org> 1.0.2
- 1.0.2
- rebuild against new dovecot
- include gpg sig
- fix requires as the plugin isn't parallel to main dovecot versioning
- fix the build

* Thu Jun 28 2007 Lauris Bukšis-Haberkorns <lafriks-at-gmail.com> 1.0.1
- Initial version
