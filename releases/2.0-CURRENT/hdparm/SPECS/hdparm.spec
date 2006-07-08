#
# spec file for package hdparm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		hdparm
%define version 	6.6
%define release 	%_revrel

Summary:	A utility for displaying and/or setting hard disk parameters
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Kernel and hardware
URL:		http://sourceforge.net/projects/hdparm/
Source:		ftp://sunsite.unc.edu/pub/Linux/system/hardware/%{name}-%{version}.tar.gz
Source1:	hdparm-sysconfig

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Hdparm is a useful system utility for setting (E)IDE hard drive
parameters.  For example, hdparm can be used to tweak hard drive
performance and to spin down hard drives for power conservation.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
perl -pi -e "s/-O2/%{optflags}/" Makefile
make clean
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/sbin
install -D -m 0755 hdparm %{buildroot}/sbin/hdparm
install -D -m 0644 hdparm.8 %{buildroot}%{_mandir}/man8/hdparm.8
install -D -m 0644 %{_sourcedir}/hdparm-sysconfig %{buildroot}/etc/sysconfig/harddisks


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/hdparm
%{_mandir}/man8/hdparm.8*
%config(noreplace) /etc/sysconfig/harddisks

%files doc
%defattr(-,root,root)
%doc hdparm.lsm Changelog contrib/README README.acoustic


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.6
- 6.6
- use the real source
- use %%_sourcdir/file instead of %%{SOURCEx}
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.1
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1-2avx
- put back our hdparm-sysconfig file; accidentally replaced it
  with the less-complete Mandriva one

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1-1avx
- 6.1
- update url

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.6-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.6-2avx
- rebuild

* Wed Aug 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.6-1avx
- 5.6
- update /etc/sysconfig/harddisks with more info

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.4-6avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 5.4-5sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 5.4-4sls
- OpenSLS build
- tidy spec

* Mon Aug 25 2003 Abel Cheung <deaddog@deaddog.org> 5.4-3mdk
- Move ThinkPad contrib stuff to tpctl

* Tue Jul 08 2003 Nicolas Planel <nplanel@mandrakesoft.com> 5.4-2mdk
- fix contrib idectl stuff.

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.4-1mdk
- new release

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.3-2mdk
- build release

* Wed Nov 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.3-1mdk
- new release
- fix build

* Sat Jul 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.2-1mdk
- new release

* Tue May 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.1-1mdk
- new release

* Tue May 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.9-1mdk
- new release

* Mon Apr 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.8-1mdk
- new release

* Sun Jan 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.6-1mdk
- new release

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.3-1mdk
- new release

* Tue Oct 16 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.2-1mdk
- new release

* Tue Oct 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-5mdk
- qa-ize()

* Mon Jul 23 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-4mdk
- fix build whith glibc-2.2 which macroize printf when using gcc-2.97 or
  more so that gcc can optimize special cases

* Mon Jul 23 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-3mdk
- fi

* Tue Jun 19 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-3mdk
- spec cleaning : macros, s!copyright!license, config files,
 license is bsd, ...

* Sun Apr  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1-2mdk
- Add /etc/sysconfig/harddisks file example.

* Mon Mar 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-1mdk
- Version 4.1 bumped into cooker.
- Remove the kernel-2.4 patch as it is no longer needed.
- Add stuff from the contrib directory as well.

* Wed Dec 06 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9-6mdk
- fix build on PPC
- fix build with kernel-2.4


* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9-5mdk
- use new macrso
- BM

* Tue May 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.9-4mdk
- Make clean before running make (or we get an x86 hdparm for all arch)

* Tue Apr 18 2000 Warly <warly@mandrakesoft.com> 3.9-3mdk 
- new group: System/Kernel and hardware

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- use spechelp & converted to the NNSS (New Naming Scheme Standard)
- remove old comented patches

* Sun Feb 06 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 3.9-1mdk
- 3.9

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix building as non-root.
- Fix wrong patch.

* Mon May 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 3.5 (UltraDMA at last...)

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- handle RPM_OPT_FLAGS

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.3
- build rooted

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- fixed spelling error in summary

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

