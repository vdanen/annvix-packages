%define name	gzip
%define version	1.2.4a
%define release 13sls

Summary:	The GNU data compression program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving/Compression
URL:		http://www.gzip.org/
Source:		ftp://ftp.gnu.org/pub/gnu/gzip/gzip-1.2.4a.tar.bz2
Patch:		gzip-1.2.4-basename.patch.bz2
Patch1:		gzip-1.2.4-gzexe.patch.bz2
Patch2:		gzip-1.2.4a-mktemp.patch.bz2
Patch3:		gzip-1.2.4-zforce.patch.bz2
Patch4:		gzip-1.2.4-4g.patch.bz2
Patch5:		gzip-1.2.4a-fixinfo.patch.bz2
Patch6:		gzip-64bit.patch.bz2
Patch7:		gzip-better-output-when-segfaults.patch.bz2
Patch8:		gzip-security-fix-filenames-too-long.patch.bz2
Patch9:		gzip-1.2.4a-znew.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	texinfo

Requires:	mktemp less
Prereq:		/sbin/install-info

%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.  

Gzip should be installed on your Mandrake Linux system, because it is a
very commonly used data compression program.

%prep
%setup -q
%patch -p1
%patch1 -p1
%patch2 -p1 -b .mktemp
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1 -b .64bit
%patch7 -p0
%patch8 -p1
%patch9 -p1 -b .znew

%build
export DEFS="-DNO_ASM"
%configure
%make all gzip.info
make test

%install
install -d $RPM_BUILD_ROOT/%{_mandir}

%makeinstall mandir=$RPM_BUILD_ROOT/%{_mandir}/man1

install -d $RPM_BUILD_ROOT/bin

mv -f $RPM_BUILD_ROOT/%{_bindir}/gzip $RPM_BUILD_ROOT/bin/gzip

rm -f $RPM_BUILD_ROOT/%{_bindir}/gunzip
rm -f $RPM_BUILD_ROOT/%{_bindir}/zcat

ln -f $RPM_BUILD_ROOT/bin/gzip $RPM_BUILD_ROOT/bin/gunzip
ln -f $RPM_BUILD_ROOT/bin/gzip $RPM_BUILD_ROOT/bin/zcat
ln -sf ../../bin/gzip $RPM_BUILD_ROOT/%{_bindir}/gzip
ln -sf ../../bin/gunzip $RPM_BUILD_ROOT/%{_bindir}/gunzip

for i in zcmp zdiff zforce zgrep zmore znew ; do
	sed -e "s|$RPM_BUILD_ROOT||g" < $RPM_BUILD_ROOT/%{_bindir}/$i > $RPM_BUILD_ROOT/%{_bindir}/.$i
	rm -f $RPM_BUILD_ROOT/%{_bindir}/$i
	mv $RPM_BUILD_ROOT/%{_bindir}/.$i $RPM_BUILD_ROOT/%{_bindir}/$i
	chmod 755 $RPM_BUILD_ROOT/%{_bindir}/$i
done

cat > $RPM_BUILD_ROOT/%{_bindir}/zless <<EOF
#!/bin/sh
export LESSOPEN="|lesspipe.sh %s"
less "\$@"
EOF
chmod 755 $RPM_BUILD_ROOT/%{_bindir}/zless

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.2.4a-13sls
- OpenSLS build
- tidy spec

* Mon Jun 16 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.4a-12mdk
- security fixes (CAN-2003-0367)

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.4a-11mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.4a-10mdk
- Automated rebuild in gcc3.1 environment

* Fri Jan 25 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.4a-9mdk
- have Jean-Loup's fix to get better output when sigsegv/sigbus
  [Patch #7]
- discover on gzip.org that we don't ship our gzip with a known security
  fix !? have it in our package [Patch #8]

* Mon Oct 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.4a-8mdk
- s!Linux Mandrake!Mandrake Linux!g

* Wed Sep 12 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.4a-7mdk
- packager tag
- undadouize

* Fri Apr 04 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.2.4a-6mdk
- added 64bit support (for files larger than 2GB).
- added make test.

* Fri Jan 05 2001 David BAUDENS <baudens@mandrakesoft.com> 1.2.4a-5mdk
- BuildRequires: texinfo
- Spec clean up

* Sun Aug 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.4a-4mdk
- Fix info file.

* Sat Aug 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.4a-3mdk
- More macros for install-info.
- Remove lesspipe.sh (moved to less package).

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.4a-2mdk
- BM
- use new macros

* Sun Apr 02 2000 Jerome Martin <jerome@mandrakesoft.com> 1.2.4a-1mdk
- Updated sources to 1.2.4a (minor doc changes)
- Updated rpm group
- Cleanup to conform to spec-helper 

* Wed Mar 08 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.2.4-19mdk
- added lesspipe.sh (allowing zless to handle arbitrary compressions
  methods, but also allows to use less command line parameters on zless,
  and use arrows keys to navigate between various files; that is a nice
  and useful zless not one only limited to "zcat $* | less" )

* Thu Dec 16 1999 Maurizio De Cecco <maurizio@mandrakesoft.com>
- Added 4g patch, from www.gzip.org

* Thu Dec 16 1999 Maurizio De Cecco <maurizio@mandrakesoft.com>
- Fixed zforce.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix building as user.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- built against glibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- added %{_bindir}/gzip and %{_bindir}/gunzip symlinks as some programs are too
  brain dead to figure out they should be at least trying to use $PATH
- added BuildRoot

* Wed Jan 28 1998 Erik Troan <ewt@redhat.com>
- fix /tmp races

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info
- applied patch for gzexe

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Marc Ewing <marc@redhat.com>
- (Entry added for Marc by Erik) fixed gzexe to use /bin/gzip
