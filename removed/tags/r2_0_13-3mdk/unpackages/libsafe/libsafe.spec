%define version 2.0.13
%define release 3mdk

Summary:	Stack Overflow protection
Name:		libsafe
Version:	%{version}
Release:	%{release}
Source:		libsafe-2.0-13.tar.bz2
License:	LGPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/libsafe
ExclusiveArch:	%ix86
URL: http://www.research.avayalabs.com/project/libsafe/

%description
The libsafe library is designed to overwrite dangerous
library C function like strcpy / snprintf and perform
bound checking on the destination buffer address in order
to detect an eventual Stack Overflow attempt.

The libsafe library protects a process against the exploitation of buffer
overflow vulnerabilities in process stacks. Libsafe works with any
existing pre-compiled executable and can be used transparently, even on a
system-wide basis. The method intercepts all calls to library functions
that are known to be vulnerable. A substitute version of the corresponding
function implements the original functionality, but in a manner that
ensures that any buffer overflows are contained within the current stack
frame. Libsafe has been shown to detect several known attacks and can
potentially prevent yet unknown attacks. Experiments indicate that the
performance overhead of libsafe is negligible.

%prep 
%setup -q -n %{name}-2.0-13

%build
# Do not use the Mandrake compilation flags,
# this library must not be compiled without any optimizations flags...
make libsafe

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
#problem with ldconfig in makefile cannot make install without patch
#make install LIBDIR=$RPM_BUILD_ROOT/lib LIBDIR=$RPM_BUILD_ROOT/%{_mandir} 
rm -f exploits/xlock

install -d $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 doc/libsafe.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -d $RPM_BUILD_ROOT/lib
install -m 644 src/libsafe.so.%{version} $RPM_BUILD_ROOT/lib
cd $RPM_BUILD_ROOT/lib
ln -s libsafe.so.%{version} libsafe.so.`echo %{version} | cut -d. -f1`

%post
tmpfile=`mktemp /tmp/libsafe.XXXXXX`
cp /etc/sysconfig/system $tmpfile
grep -v LIBSAFE $tmpfile > /etc/sysconfig/system
echo "LIBSAFE=yes" >> /etc/sysconfig/system

if [ -f /etc/ld.so.preload ]; then
  if grep -q libsafe /etc/ld.so.preload 2>/dev/null; then

	echo "Updating path to libsafe in /etc/ld.so.preload"
	cp /etc/ld.so.preload $tmpfile
	grep -v libsafe < $tmpfile > /etc/ld.so.preload
	echo /lib/libsafe.so.2 >> /etc/ld.so.preload

  fi
fi

rm -f $tmpfile

%preun
tmpfile=`mktemp /tmp/libsafe.XXXXXX`
cp /etc/sysconfig/system $tmpfile
grep -v LIBSAFE $tmpfile > /etc/sysconfig/system

if [ -f /etc/ld.so.preload ]; then
  if grep -q libsafe /etc/ld.so.preload 2>/dev/null; then

    echo "Removing libsafe from /etc/ld.so.preload"
	cp /etc/ld.so.preload $tmpfile
	grep -v libsafe < $tmpfile > /etc/ld.so.preload
  fi
fi

rm -f $tmpfile



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/* exploits
/lib/*
%{_mandir}/*/*


%changelog
* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.0.13-3mdk
- quiet setup
- rebuild

* Fri Apr 12 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.13-2mdk
- make scripts silent if ld.so.preload doesn't exist

* Wed Mar 27 2002 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.13-1mdk
- update to newer version.
- no need for glibc related patch anymore.

* Tue Sep 25 2001 Warly <warly@mandrakesoft.com> 2.0.5-5mdk
- removing libsafe from ld.so.preload in postun and not in preun
is nonsense.

* Mon Sep 24 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.5-4mdk
- On installation, update link to libsafe in /etc/ld.so.preload if it already exist.
- On removal, remove link to libsafe in /etc/ld.so.preload if present.

* Fri Sep 21 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.5-3mdk
- Do not compile the content of the exploits directory. 
  Just install it under doc.
- Patch to fix breakage due to recent GLIBC API change.
- use mktemp to avoid tmp race.
- correct wrong path to the "system" file.

* Fri Aug 31 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.5-2mdk
- Enable libsafe for server if installed. Disable it on uninstall.

* Fri Aug 31 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.5-1mdk
- Update libsafe version. This release fix the clash with newer glibc.
- Do not put libsafe in ld.so.preload.
- No need to call ldconfig. This library is not to be linked.

* Sat Apr 21 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0-3mdk
- ExclusiveArch: %%ix86.

* Wed Apr  4 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0-2mdk
- Remove reference on libsafe old version if upgrade 

* Mon Apr  2 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0-1mdk
- Up to 2.0
- Adding more description
- use more maccro

* Thu Aug 31 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3-8mdk
- ExcludeArch: sparc, sparc64 
- use %{_mandir} %{_docdir}

* Fri Jul 14 2000 David BAUDENS <baudens@mandrakesoft.com> 1.3-7mdk
- ExludeArch: alpha (Geoffrey Lee <snailtalk@linux-mandrake.com>)

* Wed Jul 12 2000 David BAUDENS <baudens@mandrakesoft.com> 1.3-6mdk
- ExcludeArch: ppc (thanks to Yoann Vandoorselaere)

* Wed May 17 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3-5mdk
- libsafe in /lib instead of /usr/lib .

* Tue Apr 25 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3-4mdk
- fix a problem with getwd replacement

* Fri Apr 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3-3mdk
- util.c : __builtin_frame_address take a depth of 2.
- util.c : (fp <= stack_start).

* Fri Mar 31 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3-2mdk
- Fix group
- First libsafe package.
