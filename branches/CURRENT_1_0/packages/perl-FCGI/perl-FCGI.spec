%define modname	FCGI
%define name	perl-%{modname}
%define version	0.67
%define release 5sls

Summary:	A Fast CGI module for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		Development/Perl
URL:		http://cpan.valueclick.com/authors/id/SKIMO/
Source0:	%{modname}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	perl, perl-devel

Requires:	perl

%description
This is a Fast CGI module for perl. It's based on the FCGI module that
comes with Open Market's FastCGI Developer's Kit, but does not require
you to recompile perl.

See <http://www.fastcgi.com/> for more information about fastcgi.
Lincoln D. Stein's perl CGI module also contains some information
about fastcgi programming.

%prep
%setup -q -n %{modname}-%{version}
chmod 0644 LICENSE.TERMS

%build
# Choose not to build a pure Perl implementation
# (default answer [n] -> return)
echo | CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE.TERMS ChangeLog
%{_mandir}/*/*
%{perl_vendorarch}/FCGI*
%{perl_vendorarch}/auto/FCGI

%changelog
* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 0.67-5sls
- rebuild for new perl
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.67-4sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.67-3mdk
- rebuild for new perl
- use %%makeinstall_std macro

* Sun May 18 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.67-2mdk
- rebuild for autoprov

* Fri Jan 17 2003 François Pons <fpons@mandrakesoft.com> 0.67-1mdk
- 0.67.

* Fri Nov 08 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.66-1mdk
- 0.66

* Fri Jul 12 2002 Pixel <pixel@mandrakesoft.com> 0.65-2mdk
- rebuild for new perl 5.8.0

* Fri Mar 01 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.65-1mdk
- 0.65

* Thu Aug 23 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.60-1mdk
- updated to 0.60

* Thu May 17 2001 David BAUDENS <baudens@mandrakesoft.com> 0.59-3mdk
- Allow build on non ix86 cpus

* Thu Apr 12 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.59-2mdk
- updated summary, description, files

* Thu Apr 12 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.59-1mdk
- First Mandrake package
