#
# spec file for package gettext
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gettext
%define version 	0.14.6
%define release 	%_revrel

%define major		3
%define libname		%mklibname intl %{major}

Summary:	GNU libraries and utilities for producing multi-lingual messages
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gettext/
Source:		ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz.sig
# (gb) some tests try to link non-pic static libs into a dso (XXX patch as XFAIL?)
Patch0:		gettext-0.14.6-mdv-pic.patch
Patch1:		gettext-0.14.2-charsets.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	bison
BuildRequires:	texinfo
BuildRequires:	automake1.8
BuildRequires:	flex

Requires:	%{name}-base = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%mklibname expat 0
Requires(post):	info-install
Requires(preun): info-install

%description
The GNU gettext package provides a set of tools and documentation for producing
multi-lingual messages in programs. Tools include a set of conventions about
how programs should be written to support message catalogs, a directory and
file naming organization for the message catalogs, a runtime library which
supports the retrieval of translated messages, and stand-alone programs for
handling the translatable and the already translated strings. Gettext provides
an easy to use library and tools for creating, using, and modifying natural
language catalogs and is a powerful and simple method for internationalizing
programs.


%package -n %{libname}
Summary:	The dynamic libintl library for the gettext package
Group:		System/Libraries
Provides:	libintl
Provides:	libintl2
Obsoletes:	libintl2

%description -n %{libname}
This package contains the libintl library for the gettext package.


%package devel
Summary:	GNU libraries and utilities for producing multi-lingual messages
Group:		Development/Other
Requires:	%{name} = %{version}
Requires(post):	info-install
Requires(preun): info-install

%description devel
Header files, used when the libc does not provide code of handling
multi-lingual messages.


%package base
Summary:	GNU libraries and utilities for producing multi-lingual messages
Group:		Development/Other
Requires:	%{libname} = %{version}

%description base
The base package which includes the gettext binary.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .pic
%patch1 -p1 -b .more_charsets

# (Abel) disable lang-java test, java bytecode failed to run
sed -i -e 's/lang-java//' gettext-tools/tests/Makefile.in


%build
%configure2_5x \
    --enable-shared \
    --with-included-gettext \
    --disable-csharp

make


%check
LC_ALL=C make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# remove unwanted files
rm -f %{buildroot}%{_includedir}/libintl.h \
      %{buildroot}%{_datadir}/locale/locale.alias \
      %{buildroot}%{_libdir}/GNU.Gettext.dll \
      %{buildroot}%{_libdir}/%{name}/gnu.gettext.* \
      %{buildroot}%{_datadir}/%{name}/*.jar
rm -f gettext-runtime/intl-java/javadoc2/package-list

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf %{buildroot}/%{_datadir}/locale/$i; done

# move installed doc back to %%doc
rm -rf htmldoc examples
mkdir htmldoc
for i in gettext-runtime/man/*.html; do
    rm -f %{buildroot}%{_datadir}/doc/gettext/`basename $i`
done
rm -rf %{buildroot}%{_datadir}/gettext/javadoc*
mv %{buildroot}%{_datadir}/doc/gettext/* %{buildroot}%{_datadir}/doc/libasprintf/* htmldoc

# move crucial stuff to /lib and /bin
pushd %{buildroot}
    mkdir -p bin
    mkdir -p ./%{_lib}
    mv usr/bin/gettext bin/
    ln -s ../../bin/gettext usr/bin/gettext
    mv .%{_libdir}/libintl.so.* ./%{_lib}/
    rm -f .%{_libdir}/libintl.so
    ln -s ../../%{_lib}/libintl.so.%{major} .%{_libdir}/libintl.so
popd

%kill_lang %{name}
%find_lang %{name} --all-name


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info gettext.info


%post devel
%_install_info autosprintf.info


%post -n %{libname} -p /sbin/ldconfig


%preun
%_remove_install_info gettext.info


%preun devel
%_remove_install_info autosprintf.info


%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/msg*
%{_bindir}/xgettext
%{_bindir}/envsubst
%{_bindir}/gettext.sh
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/hostname
%{_libdir}/%{name}/project-id
%{_libdir}/%{name}/urlget
%{_libdir}/%{name}/user-email
%{_infodir}/gettext*
%{_mandir}/man1/msg*
%{_mandir}/man1/xgettext*
%{_mandir}/man1/envsubst*
%{_mandir}/man3/*

%files base -f gettext.lang
%defattr(-,root,root)
/bin/gettext
%{_bindir}/gettext
%{_bindir}/ngettext
%{_mandir}/man1/gettext*
%{_mandir}/man1/ngettext*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*
%{_libdir}/lib*-*.*.so
%{_libdir}/lib*.so*

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.la
# "lib*.so" cannot be used (it should be 'lib[^\.]*\.so' regexp in fact
# but using regexp is not possible here; so we list all files manually
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextsrc.so
%{_libdir}/libintl.so
%{_libdir}/libasprintf.so
%{_libdir}/libgettextpo.so
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_datadir}/gettext
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/autosprintf*
%{_mandir}/man1/autopoint.1*
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc README COPYING AUTHORS NEWS THANKS


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14.6
- spec cleanups
- remove locales

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14.6
- 0.14.6
- put autopoint in the devel package
- move man3 manpages to devel package
- put back make check
- updated P0 from Mandriva
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14.5
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14.5
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq
- install autosprintf.info

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.5-1avx
- 1.14.5
- build --disabled-shared autoconf-lib-link tests --with-pic (gbeauchesne)
- BuildRequires: automake1.8 not automake1.7
- don't use parallel make

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-5avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-3avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-2avx
- Annvix build

* Fri Apr 30 2004 Vincent Danen <vdanen@opensls.org> 0.14.1-1sls
- 0.14.1
- rename P5 to P1
- sorta sync with cooker (0.14.1-4mdk):
  - P0: fix libtool 1.5 DESTDIR issue (abel)
  - parallel make works now (abel)
  - bump major to 3 (peroyvind)
  - Provides: devel(libintl) on -devel pkg (charles)
  - fix %%{_libdir}/libintl.so link (tvignaud)
- fix amd64 compile (thanks gwenole)
- Requires: lib64expat0 ifarch is amd64
- hack to make it build with automake 1.7 (we don't ship 1.8)
- NOTE: should Provides/Obsoletes: libintl2 for smooth upgrade before
  1.0-RELEASE

- remove P7; LSB is going to accomodate current gettext behaviour

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.11.5-9sls
- remove %%build_opensls macro
- remove %%prefix
- minor spec cleanups
- remove htmldoc
- README and COPYING files should not be duplicated in each package

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.11.5-8sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not require or build emacs-specific stuff
