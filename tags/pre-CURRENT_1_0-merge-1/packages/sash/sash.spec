Summary:	A statically linked shell, including some built-in basic commands
Name:		sash
Version:	3.5
Release:	6mdk
License:	GPL
Group:		Shells
Url:        http://www.canb.auug.org.au/~dbell/
Source0:	http://www.canb.auug.org.au/~dbell/programs/sash-%{version}.tar.bz2
Patch0:		sash-3.5-optflags.patch.bz2
Patch1:		sash-3.4-scriptarg.patch.bz2
Patch2: 	sash-3.4-losetup.patch.bz2
Patch3: 	sash-3.4-fix-loop__remove_it_when_kernel_headers_are_fixed.patch.bz2
Patch4: 	sash-3.4-ignore-args.patch.bz2

BuildRequires:	zlib-devel glibc-static-devel
Buildroot:	%_tmppath/%name-%version-%release-root
Prereq:	 grep

%description
Sash is a simple, standalone, statically linked shell which includes
simplified versions of built-in commands like ls, dd and gzip.  Sash
is statically linked so that it can work without shared libraries, so
it is particularly useful for recovering from certain types of system
failures.  Sash can also be used to safely upgrade to new versions of
shared libraries.

%prep
%setup -q
%patch0 -p1 -b ".misc"
%patch1 -p1 -b ".scriptarg"
%patch2 -p1 -b ".losetup"
%patch3 -p1
%patch4 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%_mandir/man8

install -s -m755 sash $RPM_BUILD_ROOT/sbin
install -m644 sash.1 $RPM_BUILD_ROOT%_mandir/man8/sash.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/sash
%_mandir/*/*

%changelog
* Mon May  5 2003 Pixel <pixel@mandrakesoft.com> 3.5-6mdk
- add "BuildRequires: glibc-static-devel"

* Mon Jan 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5-5mdk
- remove rpm-helper usage for drakx

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5-4mdk
- Prereq:  grep, rpm-helper >= 0.7
- use new shell helpers

* Tue Aug 20 2002 Pixel <pixel@mandrakesoft.com> 3.5-3mdk
- make rpmlint happy

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed Mar 20 2002 Pixel <pixel@mandrakesoft.com> 3.5-1mdk
- new release

* Sat Feb  2 2002 Pixel <pixel@mandrakesoft.com> 3.4-10mdk
- add Url

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 3.4-9mdk
- rebuild

* Wed Jun 27 2001 Stefan van der Eijk <stefan@eijk.nu> 3.4-8mdk
- BuildRequires:	zlib-devel

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 3.4-7mdk
- Use %%_tmppath for BuildRoot

* Thu Nov 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.4-6mdk
- ignore extra command line arguments.

* Thu Nov  2 2000 Pixel <pixel@mandrakesoft.com> 3.4-5mdk
- fix build (fix-loop__remove_it_when_kernel_headers_are_fixed)

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 3.4-4mdk
- cleanup, BM, macroization

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 3.4-3mdk
- new group

* Mon Mar 13 2000 Pixel <pixel@mandrakesoft.com> 3.4-2mdk
- new version

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- rebuild against new glibc in the sparc tree

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 3.3 (#4301).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build
