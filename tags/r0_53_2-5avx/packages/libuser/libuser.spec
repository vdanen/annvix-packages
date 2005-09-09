#
# spec file for package libuser
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		libuser
%define version		0.53.2
%define release		5avx

%define major		1
%define libname		%mklibname user %{major}

Summary:	A user and group account administration library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Configuration/Other
URL:		http://qa.mandriva.com
Source:		libuser-%{version}.tar.bz2
Patch1:	libuser-0.53.2-nosgml.patch	

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext, glib2-devel, openldap-devel
BuildRequires:	pam-devel, popt-devel, python-devel

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts.  The library uses pluggable
back-ends to interface to its data sources.

Sample applications modeled after those included with the shadow password
suite are included.


%package -n %{name}-python
Summary:	Library bindings for python
Group:		Development/Python

%description -n %{name}-python
this package contains the python library for python applications that 
use libuser


%package -n %{name}-ldap
Summary:	Libuser ldap library 
Group:		System/Libraries

%description -n %{name}-ldap
this package contains the libuser ldap library


%package -n %{libname}
Summary:	The actual libraries for libuser
Group:		System/Libraries

%description -n %{libname}
This is the actual library for the libuser library.


%package -n %{libname}-devel
Summary:	Files needed for developing applications which use libuser
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
The libuser-devel package contains header files, static libraries, and other
files useful for developing applications with libuser.


%prep
%setup -q
%patch1 -p0 -b .nosgml


%build
export CFLAGS="%{optflags} -DG_DISABLE_ASSERT -I/usr/include/sasl -DLDAP_DEPRECATED"
%configure2_5x \
    --with-ldap \
    --with-python-version=%{pyver} \
    --with-python-path=%{_includedir}/python%{pyver} \
    --enable-gtk-doc=no
%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

LD_LIBRARY_PATH=%{buildroot}%{_libdir}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

# Verify that all python modules load, just in case.
pushd %{buildroot}%{_libdir}/python%{pyver}/site-packages/
    python -c "import libuser"
popd

# RH cruft.
# too disgusting to watch.
set -x
pushd po
    rm -rf %{buildroot}%_datadir/locale
    for i in *.po; do
        msgfmt $i -o $(basename $i .po).mo
        p=%{buildroot}%_datadir/locale/$(basename $i .po)/LC_MESSAGES
        mkdir -p $p
        install -m 0644 $(basename $i .po).mo $p/libuser.mo
    done
popd
rm -rf %{buildroot}%_datadir/locale/zh_TW.Big5
set +x

%find_lang %{name}

# Remove unpackaged files
rm -rf %{buildroot}/usr/share/man/man3/userquota.3
rm -rf %{buildroot}%{_libdir}/python%{pyver}/site-packages/*a


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README TODO docs/*.txt python/modules.txt
%config(noreplace) %{_sysconfdir}/libuser.conf
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%attr(0755,root,root) %{_libdir}/%{name}/libuser_files.so
%attr(0755,root,root) %{_libdir}/%{name}/libuser_shadow.so
%{_mandir}/man1/*

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{name}-python
%attr(0755,root,root) %{_libdir}/python%{pyver}/site-packages/*.so

%files -n %{name}-ldap
%attr(0755,root,root) %{_libdir}/%{name}/libuser_ldap.so

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_includedir}/libuser
%attr(0644,root,root) %{_includedir}/libuser/*
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_libdir}/*.la
%attr(0755,root,root) %{_libdir}/*.so
#%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*


%changelog
* Fri Sep 09 2005 Vincent Danen <vdanen@annvix.org> 0.53.2-5avx
- pass -DLDAP_DEPRECATED to CFLAGS (oden)
- BuildRequires: openldap-devel, not libldap-devel
- libuser_ldap module is in it's own package now

* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 0.53.2-4avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen@annvix.org> 0.53.2-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.53.2-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen@annvix.org> 0.53.2-1avx
- 0.53.2
- remove redundant BuildRequires (stefan)
- move non-versioned-file from library package to main package (stefan)
- remove useless files from -devel package (gotz)
- drop unneeded patches
- use pyver macro
- spec cosmetics
- mklibname (gbeauchesne)

* Thu Jan 06 2005 Vincent Danen <vdanen@annvix.org> 0.51.7-13avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen@annvix.org> 0.51.7-12avx
- rebuild against latest openssl

* Wed Jun 22 2004 Vincent Danen <vdanen@annvix.org> 0.51.7-11avx
- Annvix build

* Mon May 17 2004 Vincent Danen <vdanen@opensls.org> 0.51.7-10sls
- security fixes from Steve Grubb

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.51.7-9sls
- remove %%build_opensls macro
- minor spec cleanups

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 0.51.7-8sls
- OpenSLS build
- tidy spec
- use %%build_opensls to apply P3; don't build sgml junk

* Thu Aug  7 2003 Daouda LO <daouda@mandrakesoft.com> 0.51.7-7mdk
- rebuild against latest python

* Mon Jul 28 2003 Daouda LO <daouda@mandrakesoft.com> 0.51.7-6mdk
- add an extra package to prevent python from linking to libuser library. 

* Fri Jul 18 2003 Daouda LO <daouda@mandrakesoft.com> 0.51.7-5mdk
- libuser1 should not provide libuser

* Fri Jul 18 2003 G�tz Waschk <waschk@linux-mandrake.com> 0.51.7-4mdk
- add sasl include dir to the cflags

* Wed Jul 16 2003 G�tz Waschk <waschk@linux-mandrake.com> 0.51.7-3mdk
- fix gtk-doc option (no spaces allowed)
- configure2_5x macro

* Mon Jun 23 2003 Daouda LO <daouda@mandrakesoft.com> 0.51.7-2mdk
- define G_DISABLE_ASSERT (don't die on assertion issue warning instead)

* Thu Apr 03 2003 Nicolas Planel <nplanel@mandrakesoft.com> 0.51.7-1mdk
- 0.51.7.

* Sun Jan 19 2003 Stefan van der Eijk <stefan@eijk.nu> 0.51-6mdk
- Undo BuildRequires: db3-devel --> db4-devel (db4 is in contrib)

* Sun Jan 19 2003 Stefan van der Eijk <stefan@eijk.nu> 0.51-5mdk
- Remove unpackaged files
- BuildRequires: db3-devel --> db4-devel

* Mon Sep 30 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.51-4mdk
- Patch[0-2]: Build all needed modules with PIC.

* Sun Aug 18 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.51-3mdk
- Spelling for locale fix.

* Thu Aug  8 2002 Stefan van der Eijk <stefan@eijk.nu> 0.51-2mdk
- BuildRequires

* Sun Jul 07 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.51-1mdk
- Mandrake-ize.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51-1
- files: ignore blank lines in files
- libuser: disallow creation of accounts with names containing whitespace,
  control characters, or non-ASCII characters

* Tue Apr 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.50.2-1
- refresh translations
- fix a heap-corruption bug in the python bindings

* Mon Apr 15 2002 Nalin Dahyabhai <nalin@redhat.com> 0.50-1
- bump version
- refresh translations

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.102-1
- ldap: cache an entity's dn in the entity structure to try to speed things up

* Mon Mar 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-3
- rebuild in new environment

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-2
- add missing buildreqs on cyrus-sasl-devel and openldap-devel (#59456)
- translation refresh

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-1
- fix python bindings of enumerateFull functions
- adjust prompter wrapping to not error out on successful returns

* Thu Feb 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.100-1
- be more careful about printing error messages
- fix refreshing after adding of accounts
- ldap: try to use a search to convert names to DNs, and only fall back to
  guessing if it turns up nothing
- files: fix an off-by-one in removal of entries

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.99-1
- refresh translations
- fix admin() constructor comments in the python module

* Thu Feb 21 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.98-1
- automatically refresh entities after add, modify, setpass, removepass,
  lock, and unlock operations
- remove debug spewage when creating and removing mail spools
- files: fix saving of multi-valued attributes
- rename MEMBERUID attribute for groups to MEMBERNAME

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.97-1
- files: fix bug in removals
- ldap: revert attempts at being smart at startup time, because it makes UIs
  very messy (up the three whole dialogs just to start the ldap stuff!)

* Sun Feb 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.96-1
- fix thinko in dispatch routines

* Wed Feb 13 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.95-1
- lgroupmod: fix thinko

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.94-2
- rebuild in new environment

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.93-1
- move shadow initialization for groups to the proper callback
- rework locking in the files module to not require that files be writable

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com>
- expose lu_strerror()
- add various typedefs for types used by the library

* Mon Jan 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.92-1
- add removepass() functions

* Thu Jan 24 2002 Nalin Dahyabhai <nalin@redhat.com>
- lchfn,lchsh,lpasswd - reorder PAM authentication calls
- include API docs in the package

* Thu Jan 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.91-1
- ldap: finish port to new API
- sasl: finish port to new API (needs test)
- libuser: don't commit object changes before passing data to service
  functions which might need differing data sets to figure out what to
  change (for example, ldap)

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.90-1
- bind the internal mail spool creation/removal functions for python

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com>
- renamed the python module
- revamped internals to use gobject's gvalues and gvaluearrays instead of
  glists of cached strings
- add enumeration-with-data functions to the C library

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- require linuxdoc-tools instead of sgml-tools for rawhide

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- fixup build files to allow building for arbitrary versions of python

* Wed Aug 29 2001 Nalin Dahyabhai <nalin@redhat.com> 0.32-1
- link the python module against libpam
- attempt to import the python modules at build-time to verify dependencies

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 0.31-1
- fix a file-parsing bug that popped up in 0.29's mmap modifications

* Mon Aug 27 2001 Nalin Dahyabhai <nalin@redhat.com> 0.30-1
- quotaq: fix argument order when reading quota information
- user_quota: set quota grace periods correctly
- luseradd: never create home directories for system accounts

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- add da translation files
- update translations

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 0.29-1
- add an explicit build dependency on jade (for the docs)

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- HUP nscd on modifications
- userutil.c: mmap files we're reading for probable speed gain
- userutil.c: be conservative with the amount of random data we read
- docs fixes

* Wed Aug 15 2001 Nalin Dahyabhai <nalin@redhat.com> 0.28-1
- apps: print usage on errors
- lnewusers.c: initialize groups as groups, not users
- lnewusers.c: set passwords for new accounts
- luseradd.c: accept group names in addition to IDs for the -g flag
- luseradd.c: allow the primary GID to be a preexisting group

* Tue Aug 14 2001 Nalin Dahyabhai <nalin@redhat.com> 0.27-1
- add ko translation files
- files.c: fix a heap corruption bug in lock/unlock (#51750)
- files.c: close a memory leak in reading of files

* Mon Aug 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- files.c: remove implementation limits on lengths of lines

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com> 0.26-1
- lusermod: change user name in groups the user is a member of during renames
- lgroupmod: change primary GID for users who are in the group during renumbers
- ldap.c: handle new attributes more gracefully if possible
- add ru translation files

* Tue Aug  7 2001 Nalin Dahyabhai <nalin@redhat.com> 0.25.1-1
- rename the quota source files to match the library, which clears up a
  file conflict with older quota packages
- add ja translation files

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- add lu_ent_clear_all() function

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.25-1
- close up some memory leaks
- add the ability to include resident versions of modules in the library

* Wed Aug  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.24-4
- fix incorrect Py_BuildValue invocation in python module

* Tue Jul 31 2001 Nalin Dahyabhai <nalin@redhat.com> 0.24-3
- stop leaking descriptors in the files module
- speed up user creation by reordering some checks for IDs being in use
- update the shadowLastChanged attribute when we set a password
- adjust usage of getXXXXX_r where needed
- fix assorted bugs in python binding which break prompting

* Mon Jul 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.23-1
- install sv translation
- make lpasswd prompt for passwords when none are given on the command line
- make sure all user-visible strings are marked for translation
- clean up some user-visible strings
- require PAM authentication in lchsh, lchfn, and lpasswd for non-networked modules

* Fri Jul 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- print uids and gids of users and names in lid app
- fix tree traversal in users_enumerate_by_group and groups_enumerate_by_users
- implement enumerate_by_group and enumerate_by_user in ldap module
- fix id-based lookups in the ldap module
- implement islocked() method in ldap module
- implement setpass() method in ldap module
- add lchfn and lchsh apps
- add %%d substitution to libuser.conf

* Thu Jul 26 2001 Nalin Dahyabhai <nalin@redhat.com> 0.21-1
- finish adding a sasldb module which manipulates a sasldb file
- add users_enumerate_by_group and groups_enumerate_by_users

* Wed Jul 25 2001 Nalin Dahyabhai <nalin@redhat.com> 
- luserdel: remove the user's primary group if it has the same name as
  the user and has no members configured (-G disables)
- fixup some configure stuff to make libuser.conf get generated correctly
  even when execprefix isn't specified

* Tue Jul 24 2001 Nalin Dahyabhai <nalin@redhat.com> 0.20-1
- only call the auth module when setting passwords (oops)
- use GTrees instead of GHashTables for most internal tables
- files: complain properly about unset attributes
- files: group passwords are single-valued, not multiple-valued
- add lpasswd app, make sure all apps start up popt with the right names

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.18-1
- actually make the new optional arguments optional
- fix lu_error_new() to actually report errors right
- fix part of the python bindings
- include tools in the binary package again
- fixup modules so that password-changing works right again
- add a "key" field to prompt structures for use by apps which like to
  cache these things
- add an optional "mvhomedir" argument to userModify (python)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com> 0.16.1-1
- finish home directory population
- implement home directory moving
- change entity get semantics in the python bindings to allow default values for .get()
- add lu_ent_has(), and a python has_key() method to Entity types
- don't include tools in the binary package
- add translated strings

* Thu Jul 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- lib/user.c: catch and ignore errors when running stacks
- lusermod: fix slightly bogus help messages
- luseradd: when adding a user and group, use the gid of the group
  instead of the user's uid as the primary group
- properly set the password field in user accounts created using
  auth-only auth modules (shadow needs "x" instead of "!!")
- implement home directory removal, start on population

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix group password setting in the files module
- setpass affects both auth and info, so run both stacks

* Tue Jul 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- make the testbed apps noinst

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix errors due to uninitialized fields in the python bindings
- add kwargs support to all python wrappers
- add a mechanism for passing arguments to python callbacks

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- stub out the krb5 and ldap modules so that they'll at least compile again
 
* Tue Jul 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't bail when writing empty fields to colon-delimited files
- use permissions of the original file when making backup files instead of 0600

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish implementing is_locked methods in files/shadow module
- finish cleanup of the python bindings
- allow conditional builds of modules so that we can build without
  all of the prereqs for all of the modules

* Thu Jun 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- add error reporting facilities
- split public header into pieces by function
- backend cleanups

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- make %%{name}-devel require %%{name} and not %%{name}-devel

* Fri Jun 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- clean up quota bindings some more
- finish most of the ldap bindings
- fix a subtle bug in the files module that would show up when renaming accounts
- fix mapping methods for entity structures in python

* Thu Jun 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- get bindings for prompts to work correctly
- clean up some of the add/remove semantics (set source on add)
- ldap: implement enumeration
- samples/enum: fix the argument order

* Wed Jun 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- clean up python bindings for quota

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com> 0.11
- finish up python bindings for quota support

* Sun Jun 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish up quota support libs

* Fri Jun  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- start quota support library to get some type safety

* Thu Jun  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- start looking at quota manipulation

* Wed Jun  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add functions for enumerating users and groups, optionally per-module
- lusermod.c: -s should specify the shell, not the home directory

* Fri Jun  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.10
- finish the python bindings and verify that the file backend works again

* Wed May 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove a redundant check which was breaking modifications

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish adding setpass methods

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9
- get a start on some Python bindings

* Tue May  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8.2
- make binary-incompatible change in headers

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8.1
- add doxygen docs and a "doc" target for them

* Sat Jan 20 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8
- add a "quiet" prompter
- add --interactive flag to sample apps and default to using quiet prompter
- ldap: attempt a "self" bind if other attempts fail
- krb5: connect to the password-changing service if the user principal has
  the NULL instance

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- the great adding-of-the-copyright-statements
- take more care when creating backup files in the files module

* Wed Jan  3 2001 Nalin Dahyabhai <nalin@redhat.com> 0.7
- add openldap-devel as a buildprereq
- krb5: use a continuous connection
- krb5: add "realm" config directive
- ldap: use a continuous connection
- ldap: add "server", "basedn", "binddn", "user", "authuser" config directives
- ldap: actually finish the account deletion function
- ldap: don't send cleartext passwords to the directory
- fix naming attribute for users (should be uid, not gid)
- refine the search-by-id,convert-to-name,search-by-name logic
- fix handling of defaults when the config file is read in but contains no value
- implement an LDAP information store
- try to clean up module naming with libtool
- luseradd: pass plaintext passwords along
- luseradd: use symbolic attribute names instead of hard-coded
- lusermod: pass plaintext passwords along
- lgroupadd: pass plaintext passwords along
- lgroupmod: pass plaintext passwords along
- add libuser as a dependency of libuser-devel

* Tue Jan  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.6
- initial packaging
