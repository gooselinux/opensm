Name: opensm
Version: 3.3.5
Release: 1%{?dist}
Summary: OpenIB InfiniBand Subnet Manager and management utilities
Group: System Environment/Daemons
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source0: http://www.openfabrics.org/downloads/management/%{name}-%{version}.tar.gz
Source1: opensm.conf
Source2: opensm.logrotate
Source3: opensm.initd
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibmad-devel = 1.3.4, libtool, bison, flex, byacc
Requires: %{name}-libs = %{version}-%{release}, logrotate, rdma
ExcludeArch: s390 s390x

%description
OpenSM is the OpenIB project's Subnet Manager for Infiniband networks.
The subnet manager is run as a system daemon on one of the machines in
the infiniband fabric to manage the fabric's routing state.  This package
also contains various tools for diagnosing and testing Infiniband networks
that can be used from any machine and do not need to be run on a machine
running the opensm daemon.

%package libs
Summary: Libraries used by opensm and included utilities
Group: System Environment/Libraries

%description libs
Shared libraries for Infiniband user space access

%package devel
Summary: Development files for the opensm-libs libraries
Group: Development/System
Requires: %{name}-libs = %{version}-%{release}

%description devel
Development environment for the opensm libraries

%package static
Summary: Static version of the opensm libraries
Group: Development/System
Requires: %{name}-devel = %{version}-%{release}
%description static
Static version of opensm libraries

%prep
%setup -q

%build
%configure --with-opensm-conf-sub-dir=rdma
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -fr $RPM_BUILD_ROOT%{_sysconfdir}/init.d
install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rdma/opensm.conf
install -D -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/opensm
install -D -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_initddir}/opensm
mkdir -p ${RPM_BUILD_ROOT}/var/cache/opensm

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
	/sbin/chkconfig --add opensm
else
	/sbin/service opensm condrestart
fi

%preun
if [ $1 = 0 ]; then
	/sbin/service opensm stop
	/sbin/chkconfig --del opensm
	rm -f /var/cache/opensm/*
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir /var/cache/opensm
%{_sbindir}/*
%{_initddir}/opensm
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/logrotate.d/opensm
%config(noreplace) %{_sysconfdir}/rdma/opensm.conf
%doc AUTHORS COPYING ChangeLog INSTALL README NEWS

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/infiniband

%files static
%defattr(-,root,root,-)
%{_libdir}/lib*.a

%changelog
* Mon Mar 08 2010 Doug Ledford <dledford@redhat.com> - 3.3.5-1
- Update to latest upstream release.  We need various defines in ib_types.h
  for the latest ibutils package to build properly, and the latest ibutils
  package is needed because we found licensing problems in the older
  tarballs during review.

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 3.3.3-2
- ExcludeArch s390(x) as there's no hardware support there

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 3.3.3-1
- Update to latest upstream release
- Minor tweaks to init script for LSB compliance

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Doug Ledford <dledford@redhat.com> - 3.3.2-1
- Update to latest upstream version

* Wed Apr 22 2009 Doug Ledford <dledford@redhat.com> - 3.3.1-1
- Update to latest upstream version

* Fri Mar 06 2009 Caolán McNamara <caolanm@redhat.com> - 3.2.1-3
- fix bare elifs to rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 3.2.1-1
- Initial package for Fedora review process

