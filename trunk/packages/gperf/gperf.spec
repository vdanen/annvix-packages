%define name	gperf
%define version	3.0.1
%define release	3sls

Summary:	A perfect hash function generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/gperf/
Source:		ftp://ftp.gnu.org/gnu/gperf/%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root

PreReq:		/sbin/install-info

%description
Gperf is a perfect hash function generator written in C++.  Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.

Install gperf if you need a program that generates perfect hash
functions.

%prep
%setup -q

%build
%configure2_5x
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/gperf/gperf.html

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc README NEWS doc/gperf.html
%{_bindir}/gperf
%{_mandir}/man1/gperf.1*
%{_infodir}/gperf.info*

%changelog
* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 3.0.1-3sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.0.1-2sls
- OpenSLS build
- tidy spec

* Wed Aug 20 2003 Giuseppe Ghib� <ghibo@mandrakesoft.com> 3.0.1-1mdk
- Release: 3.0.1.

* Fri Jul 25 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 2.7.2-8mdk
- rebuild

* Wed Feb 19 2003 Giuseppe Ghib� <ghibo@mandrakesoft.coM> 2.7.2-7mdk
- Rebuilt.

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.7.2-6mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.7.2-5mdk
- Automated rebuild with gcc3.2

* Tue May 28 2002 Giuseppe Ghib� <ghibo@mandrakesoft.com> 2.7.2-4mdk
- Rebuilt.

* Sat Jan 19 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.7.2-3mdk
- Add URL tag, update source URL
- s/Copyright/License/
- Use %%make, %%configure2_5x, %%makeinstall_std macros

* Fri Nov 17 2000 David BAUDENS <baudens@mandrakesoft.com> 2.7.2-2mdk
- Rebuild with gcc-2.96 & glibc-2.2

* Fri Oct 20 2000 Fran�ois Pons <fpons@mandrakesoft.com> 2.7.2-1mdk
- removed patch and simplified a bit install step.
- 2.7.2.

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-13mdk
- fix bad scripts

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-12mdk
- major spec cleaning
- BM

* Wed Apr 05 2000 John Buswell <johnb@mandrakesoft.com> 2.7-11mdk
- fixed vendor tag

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 2.7-10mdk
- fixed groups
- uses spec-helper

* Tue Nov 23 1999 Fran�ois PONS <fpons@mandrakesoft.com>
- Build release.

* Thu Jun  3 1999 Bernhard Rosenkr�nzer <bero@mandrakesoft.com>
- REALLY bzip2 info files rather than just renaming them ;)
  seems I'm not the only one around here who should stop working after
  4 am ;)
- replace the egcs patch with the REAL egcs patch (from the egcs server)

* Wed May 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- bzip2 info files.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Wed Mar 24 1999 Cristian Gafton <gafton@redhat.com>
- added patches for egcs from UP

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- patch for latest egcs

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binary

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- create.
