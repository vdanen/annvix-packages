#
# spec file for package perl-CGI
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		CGI
%define revision	$Rev$
%define name		perl-%{module}
%define version		3.05
%define release		%_revrel
%define epoch		1

Summary:        Simple Common Gateway Interface class for Perl
Name:           %{name}
Version:        %{version}
Release:        %{release}
Epoch:		%{epoch}
License:        GPL or Artistic
Group:          Development/Perl
URL:            http://stein.cshl.org/WWW/software/CGI/
Source:         CGI.pm-%{version}.tar.bz2

BuildRoot:      %{_buildroot}/%{name}-%{version}
BuildArch:      noarch
BuildRequires:  perl-devel

Requires:       perl >= 0:5.004
Conflicts:      perl < 0:5.600-28mdk

%description
This perl library uses perl5 objects to make it easy to create
Web fill-out forms and parse their contents.  This package
defines CGI objects, entities that contain the values of the
current query string and other state variables.  Using a CGI
object's methods, you can examine keywords and parameters
passed to your script, and create forms whose initial values
are taken from the current query (thereby preserving state
information).


%package Fast
Group:		Development/Perl
Summary: 	CGI Interface for Fast CGI
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description Fast
CGI::Fast is a subclass of the CGI object created by CGI.pm. It is
specialized to work well with the Open Market FastCGI standard, which
greatly speeds up CGI scripts by turning them into persistently running
server processes.  Scripts that perform time-consuming initialization
processes, such as loading large modules or opening persistent database
connections, will see large performance improvements.


%prep
%setup -q -n %{module}.pm-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make
%{__make} test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc Changes README *.html examples
%{perl_vendorlib}/CGI
%exclude %{perl_vendorlib}/CGI/Fast.pm
%{perl_vendorlib}/*.pm
%{_mandir}/man3/*
%exclude %{_mandir}/man3/CGI::Fast.3pm.*

%files Fast
%defattr(-,root,root)
%{perl_vendorlib}/CGI/Fast.pm
%{_mandir}/man3/CGI::Fast.3pm.*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-6avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-4avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-3avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.05-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 3.05-1sls
- 3.0.5

* Mon Apr 12 2004 Vincent Danen <vdanen@opensls.org> 3.00-4sls
- fix epoch in requires

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 3.00-3sls
- rebuild for new perl
- small spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 3.00-2sls
- OpenSLS build
- tidy spec

* Tue Aug 19 2003 Ben Reser <ben@reser.org> 3.00-1mdk
- 3.00

* Fri Aug 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.99-2mdk
- rebuild

* Wed Aug 06 2003 Ben Reser <breser@mandrakesecure.net> 2.99-1mdk
- 2.99 security issues with cross site scripting (CAN-2003-0615)
  http://eyeonsecurity.org/advisories/CGI.pm/adv.html
- Include Fast subpackage again
- Switch to new perl make macros/remove PREFIX
- Man path

* Tue Aug 05 2003 Ben Reser <breser@mandrakesecure.net> 2.99-0.2mdk
- 2.99 security issues with cross site scripting (CAN-2003-0615)
  http://eyeonsecurity.org/advisories/CGI.pm/adv.html
- Switch back to vendorlib and man3pm for 9.0 and 9.1 builds

* Tue Aug 05 2003 Ben Reser <breser@mandrakesecure.net> 2.99-0.1mdk
- 2.99 security issues with cross site scripting (CAN-2003-0615)
  http://eyeonsecurity.org/advisories/CGI.pm/adv.html
- Remove explicit packager tag
- Use macros for rm
- Temporarily back out subpackage for security update builds
  (older distros didn't have the subpackage and it may break depdencies)
- Temporarily roll back to installing in vendorlib and man3pm for 8.2

* Tue May 27 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.93-2mdk
- Fast subpackage to leverage dependencies

* Fri May 23 2003 François Pons <fpons@mandrakesoft.com> 2.93-1mdk
- 2.93.

* Sun May 18 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.91-3mdk
- fix autoprov

* Thu May 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.91-2mdk
- rebuild for autoprov

* Thu Apr 24 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.91-1mdk
- 2.91
- used Epoch to fix this version mess
- remove prefix tag

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 2.810-3mdk
- drop Patch0 (unused)
- fix requires perl

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 2.810-2mdk
- rebuild for perl 5.8.0

* Tue Jun 25 2002 Pixel <pixel@mandrakesoft.com> 2.810-1mdk
- 2.81

* Sat Feb  2 2002 Pixel <pixel@mandrakesoft.com> 2.790-1mdk
- add "make test"
- 2.79

* Fri Aug 31 2001 François Pons <fpons@mandrakesoft.com> 2.753-1mdk
- 2.753.

* Wed Apr 25 2001 Pixel <pixel@mandrakesoft.com> 2.752-2mdk
- rebuild with new perl

* Sat Mar  3 2001 Pixel <pixel@mandrakesoft.com> 2.752-1mdk
- cleanup
(made by Alexander Skwar <ASkwar@Linux-Mandrake.com>)
- First seperate Mandrake version
- Added Upload Tmpdir patch from perl
- Requires perl *WITHOUT* CGI.pm!
