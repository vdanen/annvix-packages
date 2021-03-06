%define name	quota
%define version 3.09
%define release 3avx

Summary:	System administration tools for monitoring users' disk usage
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Configuration/Other
URL:		http://sourceforge.net/projects/linuxquota
Source:		http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.bz2
Patch1:		quota-tools-man-pages-path.patch.bz2
Patch2:		quota-tools-no-stripping.patch.bz2
Patch3:		quota-tools-warnquota.patch.bz2
Patch4:		quota-tools-default-conf.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	e2fsprogs-devel, gettext

Requires:	kernel >= 2.4, initscripts >= 6.38

%description
The quota package contains system administration tools for monitoring
and limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk
usage.

%prep
%setup -q -n quota-tools
%patch1 -p1 -b .man-pages
%patch2 -p1 -b .no-stripping
%patch3 -p1 -b .warnquota
%patch4 -p1 -b .default-conf

%build
%configure \
	--with-ext2direct=no
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,%{_sysconfdir},%{_sbindir},%{_bindir},%{_mandir}/{man1,man2,man3,man8}}

make install ROOTDIR=%{buildroot}

for i in convertquota quotacheck quotaoff quotaon;do
	mv %{buildroot}/%{_sbindir}/$i %{buildroot}/sbin/$i 
done

install -m 644 warnquota.conf %{buildroot}%{_sysconfdir}

%find_lang %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/warnquota.conf
%config(noreplace) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %{_sysconfdir}/quotatab
%attr(0755,root,root) /sbin/*
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%{_includedir}/rpcsvc/*
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man2/*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_mandir}/man8/*

%changelog
* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 3.09-3avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 3.09-2sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Juan Quintela <quintela@mandrakesoft.com> 3.09-1mdk
- 3.09.

* Thu Jul 24 2003 Per ?yvind Karlsen <peroyvind@sintrax.net> 3.08-2mdk
- rebuild
- use %%make macro

* Sat Feb  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.08-1mdk
- Bump to version 3.08 (not updated for more than 1 year and half woo).

* Mon Jun  3 2002 Stefan van der Eijk <stefan@eijk.nu> 3.01-0.6mdk
- BuildRequires

* Wed Jan 16 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.01-0.5mdk
- Really make sure to build again the right libcomerr (and that's the
  ugly part 8-().

* Wed Jan 16 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.01-0.4mdk
- Make sure to build again the right libcomerr.

* Thu Dec 20 2001 Stew Benedict <sbenedict@mandrakesoft.com> 3.01-0.3mdk
- patch to allow PPC build (__swab64), rpmlint fixes (URL, License)

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.01-0.2mdk
- Merge rh patches.
- 3.01pre9.

* Fri Aug 24 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.01-0.1mdk
- 3.01pre8.
- Clean up and rh patches merges.

* Fri May 11 2001 Stew Benedict <sbenedict@mandrakesoft.com> 3.00-2mdk
- patches for PPC build

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.00-1mdk
- RedHat package merge..
- quota 3.00 is required by recent kernel 2.4 changes.
- no warnquota included this time, not yet ported.
- quite a bit of work on quotacheck to make is backwards compatible (rh)

* Sat Jan 13 2001 Geoff <snailtalk@mandrakesoft.com> 2.00-2mdk
- remove the conflicts with the glibc headers.

* Sat Jan 13 2001 Geoff <snailtalk@mandrakesoft.com> 2.00-1mdk
- new and shiny source.
- port spec file to 2.00 release.
- replace the source url with a correct one.

* Wed Oct 19 2000 Daouda Lo <daouda@mandrakesoft.com> 1.70-4mdk
- add quota binary to package (who Sux?)

* Fri Jul 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.70-3mdk
- Remove also rquotad.8 manpages to fix conflicts.


* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.70-2mdk
- BM, macros


* Mon Jun 26 2000 Francis Galiegue <fg@mandrakesoft.com> 1.70-1mdk

- Removed docs.tar.gz, it was just dead weight
- Spec file cleanup
- Patches cleanup

* Sun Jun 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.66-12mdk
- don't install rpc.rquotad - we will use the one from the knfsd package
  instead

* Thu Mar 16 2000 Francis Galiegue <francis@mandrakesoft.com>
- Some spec file fixes
- Changed group according to 7.1 specs
- Let spec helper do its job

* Tue Jan 11 2000 Pixel <pixel@linux-mandrake.com>
- fix build as non-root

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- rh merge.
- fix man page FUD.(r)
- changes to allow non-root users to build too (Makefile patch, %attr).(r)

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Tue Apr 13 1999 Jeff Johnson <jbj@redhat.com>
- fix for sparc64 quotas (#2147)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Mon Dec 28 1998 Cristian Gafton <gafton@redhat.com>
- don't install rpc.rquotad - we will use the one from the knfsd package
  instead

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- merge ultrapenguin 1.1.9 changes.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- removed patch for mntent

* Fri Mar 27 1998 Jakub Jelinek <jj@ultra.linux.cz>
- updated to quota 1.66

* Tue Jan 13 1998 Erik Troan <ewt@redhat.com>
- builds rquotad
- installs rpc.rquotad.8 symlink

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- removed /usr/include/rpcsvc/* from filelist
- uses a buildroot and %attr

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Moved /usr/sbin/quota to /usr/bin/quota
