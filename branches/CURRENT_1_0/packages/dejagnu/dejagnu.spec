%define name	dejagnu
%define version 1.4.2
%define release 7sls

Summary:	A front end for testing other programs.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		20010912
Group:		Development/Other
License:	GPL
URL:		http://sourceware.cygnus.com
Source:		%{name}-%{version}.tar.bz2 
Patch2:		dejagnu-1.4.2-mkargs.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	autoconf automake libtool
BuildArch:	noarch

Requires:	common-licenses, tcl >= 8.0, expect >= 5.21

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q
%patch2 -p1

%build
%configure
%make
# all tests must pass (use runtest that was just built)
(
export PATH=$PWD:$PATH
make check
)

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 contrib/bluegnu2.0.3/doc/dejagnu.1 %{buildroot}%{_mandir}/man1

# Nuke unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/config.guess
rm -f $RPM_BUILD_ROOT%{_includedir}/dejagnu.h

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README TODO
%dir %{_datadir}/dejagnu
%{_datadir}/dejagnu/*
%{_bindir}/runtest
%{_mandir}/man1/dejagnu.1*
%{_mandir}/man1/runtest.1*

%changelog
* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.4.2-7sls
- remove %%build_opensls macros
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.4.2-6sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build any doc stuff

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-5mdk
- Add new runtest to PATH for make check

* Sat Aug 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-4mdk
- Make check with itself
- Ship with the right README file
- BuildRequires: docbook-utils for docs
- Remove unapplied/obsolete? Patch0 (moredocs)
- Remove conflictual Patch1 (libtool)

* Fri Oct  5 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-3mdk
- Patch2: don't fail at processing/skipping of Makefile style args
  (e.g. CC=gcc) in the second command line parsing pass.

* Thu Sep 27 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.4.2-2mdk
- add infopages

* Thu Sep 13 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.4.2-1mdk
- 1.4.2

* Wed Sep 12 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.1-2mdk
- Sanitize specfile (s/Copyright/License/, Epoch: 20010912)
- Patch2: lib/target.exp (prune_warnings): fix typo when calling regsub

* Mon Jul 02 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.4.1-1mdk
- updated to 1.4.1

* Fri Mar  9 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 20010308-1mdk
- spec cleanup
- new snapshot from cvs
- Regenerate autoconf/automake/libtool stuff for every build
- Add BuildRequires: autoconf automake libtool
- Use configure, make, makeinstall macros
- Install man and info pages too
- Create PostScript and HTML docs

* Tue May 09 2000 Lenny Cartier <lenny@mandrakesoft.com> 20000303-1mdk
- fix group
- bzip2 patches

* Tue Nov 30 1999 Jakub Jelinek <jakub@redhat.com>
- made noarch.

* Mon Nov 8 1999 Tim Powers <timp@redhat.com>
- updated to 19991101

* Mon Jul 12 1999 Tim Powers <timp@redhat.com>
- updated to 19990628
- updated patches as needed
- added %defattr in files section

* Wed Mar 10 1999 Jeff Johnson <jbj@redhat.com>
- add alpha expect patch (#989)
- use %configure

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- Update to 19981215.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-10-29.

* Wed Jul  8 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-05-28.

* Sun Feb  1 1998 Jeff Johnson <jbj@jbj.org>
- Create.
