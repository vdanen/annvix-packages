%define name perl-%{real_name}
%define real_name HTML-Parser
%define version 3.31
%define release 1mdk

Summary: 	HTML-Parser module for perl (World_Wide_Web_HTML_HTTP_CGI/HTML)
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
Source: 	ftp://ftp.cpan.org/pub/perl/CPAN/modules/by-module/HTML/%{real_name}-%{version}.tar.bz2
Url: 		http://www.cpan.org
BuildRequires:	perl-devel perl-HTML-Tagset
BuildRoot: 	%{_tmppath}/%{name}-buildroot/
Requires: 	perl perl-HTML-Tagset >= 3.03

%description
HTML-Parser module for perl to parse and extract information
from HTML documents.

%prep
%setup -q -n %{real_name}-%{version}

%build
# compile with default options (prompt() checks for STDIN being a terminal).
# yes to not ask for automate rebuild
yes | %{__perl} Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="$RPM_OPT_FLAGS"
make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO Changes
%{_mandir}/*/*
%{perl_vendorarch}/auto/HTML/Parser
%{perl_vendorarch}/HTML/*


%changelog
* Thu Aug 21 2003 Fran�ois Pons <fpons@mandrakesoft.com> 3.31-1mdk
- 3.31.

* Thu Aug 14 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 3.28-4mdk
- rebuild for new perl
- drop Prefix tag
- drop Distribution tag
- don't use PREFIX
- use %%makeinstall_std macro
- use %%make macro

* Fri Jun 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.28-3mdk
- do not wait a reply from term for automate rebuild

* Tue May 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.28-2mdk
- rebuild for new perl provides/requires

* Fri Apr 18 2003 Fran�ois Pons <fpons@mandrakesoft.com> 3.28-1mdk
- 3.28.

* Fri Jan 24 2003 Fran�ois Pons <fpons@mandrakesoft.com> 3.27-1mdk
- 3.27.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 3.26-3mdk
- rebuild for perl thread-multi

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 3.26-2mdk
- rebuild for perl 5.8.0

* Tue Mar 26 2002 Fran�ois Pons <fpons@mandrakesoft.com> 3.26-1mdk
- 3.26.

* Thu Nov 08 2001 Fran�ois Pons <fpons@mandrakesoft.com> 3.25-3mdk
- build release.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 3.25-2mdk
- BuildRequires: perl-devel perl-HTML-Tagset

* Tue Jul 03 2001 Fran�ois Pons <fpons@mandrakesoft.com> 3.25-1mdk
- 3.25.

* Wed Jun 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.18-3mdk
- Fixed distribution tag.
- Updated Requires.
- Added an option to %makeinstall.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.18-2mdk
- Rebuild against the latest perl.

* Tue Feb 27 2001 Fran�ois Pons <fpons@mandrakesoft.com> 3.18-1mdk
- 3.18.

* Tue Jan 30 2001 Fran�ois Pons <fpons@mandrakesoft.com> 3.15-1mdk
- 3.15.

* Tue Dec 05 2000 Fran�ois Pons <fpons@mandrakesoft.com> 3.14-1mdk
- 3.14.

* Thu Oct 12 2000 Fran�ois Pons <fpons@mandrakesoft.com> 3.13-1mdk
- 3.13.

* Tue Aug 29 2000 Fran�ois Pons <fpons@mandrakesoft.com> 3.11-1mdk
- 3.11.

* Thu Aug 03 2000 Fran�ois Pons <fpons@mandrakesoft.com> 3.10-2mdk
- macroszifications.
- add doc.

* Tue Jul 18 2000 Fran�ois Pons <fpons@mandrakesoft.com> 3.10-1mdk
- removed perllocal.pod from files.
- 3.10.

* Tue Jun 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.08-1mdk
- update to 3.08

* Wed May 17 2000 David BAUDENS <baudens@mandrakesoft.com> 3.05-4mdk
- Fix build for i486
- Use %%{_tmppath} for BuildRoot

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 3.05-3mdk
- rebuild, new group, cleanup

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@netrevolution.com> 3.0.5-1mdk
- upgrade to 3.05

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
-updated to 3.02

* Sun Aug 29 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- bzip2'd sources
- updated to 2.23

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 
