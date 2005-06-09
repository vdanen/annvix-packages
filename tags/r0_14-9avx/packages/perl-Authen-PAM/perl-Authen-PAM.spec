%define module 	Authen-PAM
%define name	perl-%{module}
%define version 0.14
%define release 9avx

Summary:	Perl interface to the PAM library
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cs.kuleuven.ac.be/~pelov/pam/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	pam-devel perl-devel

%description
The Authen::PAM module provides a Perl interface to the PAM library.
The only difference with the standard PAM interface is that the perl
one is simpler.

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README MANIFEST Changes
%{_mandir}/*/*
%{perl_vendorarch}/auto/Authen/*
%{perl_vendorarch}/Authen/*


%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.14-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 0.14-8avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 0.14-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.14-6sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 0.14-5sls
- rebuild for new perl
- small spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.14-4sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.14-3mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro
- use %%make macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.14-2mdk
- rebuild for new auto{prov,req}

* Fri Apr 18 2003 Fran�ois Pons <fpons@mandrakesoft.com> 0.14-1mdk
- 0.14.

* Wed Jan 29 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.13-4mdk
- enhanced summary & description

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 0.13-3mdk
- rebuild for perl thread-multi

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 0.13-2mdk
- rebuild for perl 5.8.0
- remove the filelist

* Thu Apr 11 2002 Fran�ois Pons <fpons@mandrakesoft.com> 0.13-1mdk
- 0.13.

* Thu Nov 08 2001 Fran�ois Pons <fpons@mandrakesoft.com> 0.12-1mdk
- 0.12.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 0.11-3mdk
- BuildRequires: pam-devel perl-devel

* Mon Jul  2 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.11-2mdk
- rebuild

* Thu Apr 19 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 0.11-1.1mdk
- removed samples from doc
- changed spec name

* Thu Apr 12 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 0.11-1mdk
- First Mandrake release






