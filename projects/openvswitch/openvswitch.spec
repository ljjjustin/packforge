Name:           openvswitch
Version:        2.1.2
Release:        3%{?dist}
Summary:        Open vSwitch daemon/database/utilities

# Nearly all of openvswitch is ASL 2.0.  The bugtool is LGPLv2+, and the
# lib/sflow*.[ch] files are SISSL
# datapath/ is GPLv2 (although not built into any of the binary packages)
# python/compat is Python (although not built into any of the binary packages)

# This provides a way for distros that doesn't provide
# python-twisted-conch to disable building of ovsdbmonitor
# by default. You can override by passing --with ovsdbmonitor
# or --without ovsdbmonitor while building the RPM.
%define _pkg_ovsdbmonitor 0

%if %{?_with_ovsdbmonitor: 1}%{!?_with_ovsdbmonitor: 0}
%define with_ovsdbmonitor 1
%else
%define with_ovsdbmonitor %{?_without_ovsdbmonitor: 0}%{!?_without_ovsdbmonitor: %{_pkg_ovsdbmonitor}}
%endif

License:        ASL 2.0 and LGPLv2+ and SISSL
URL:            http://openvswitch.org
Source0:        http://openvswitch.org/releases/%{name}-%{version}.tar.gz
Source2:        openvswitch.init
Source3:        openvswitch.logrotate
Source4:        ifup-ovs
Source5:        ifdown-ovs
#Source6:        ovsdbmonitor.desktop

BuildRequires:  initscripts openssl openssl-devel
BuildRequires:  python python-twisted-core python-twisted-conch python-zope-interface PyQt4
BuildRequires:  desktop-file-utils
BuildRequires:  groff graphviz

Requires:       openssl iproute module-init-tools
Requires:       kernel >= 2.6.32-343

Requires(post):  initscripts
Requires(preun): initscripts
Requires(postun): initscripts

Obsoletes: openvswitch-controller <= 0:2.1.0-1

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package -n python-openvswitch
Summary:        Open vSwitch python bindings
License:        ASL 2.0
BuildArch:      noarch
Requires:       python

%description -n python-openvswitch
Python bindings for the Open vSwitch database

%if %{with_ovsdbmonitor}
%package -n ovsdbmonitor
Summary:        Open vSwitch graphical monitoring tool
License:        ASL 2.0
BuildArch:      noarch
Requires:       python-openvswitch = %{version}-%{release}
Requires:       python python-twisted-core python-twisted-conch python-zope-interface PyQt4

%description -n ovsdbmonitor
A GUI tool for monitoring and troubleshooting local or remote Open
vSwitch installations.  It presents GUI tables that graphically represent
an Open vSwitch kernel flow table (similar to "ovs-dpctl dump-flows")
and Open vSwitch database contents (similar to "ovs-vsctl list <table>").
%endif


%package test
Summary:        Open vSwitch testing utilities
License:        ASL 2.0
BuildArch:      noarch
Requires:       python-openvswitch = %{version}-%{release}
Requires:       python python-twisted-core python-twisted-web
# python-2.6 does not have argparse included yet
Requires:       python-argparse

%description test
Utilities that are useful to diagnose performance and connectivity
issues in Open vSwitch setup.

%package devel
Summary:        Open vSwitch OpenFlow development package (library, headers)
License:        ASL 2.0
Provides:       openvswitch-static = %{version}-%{release}

%description devel
This provides static library, libopenswitch.a and the openvswtich header
files needed to build an external application.

%prep
%setup -q

%build
%configure --enable-ssl --with-pkidir=%{_sharedstatedir}/openvswitch/pki
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch

src=rhel/usr_share_openvswitch_scripts_sysconfig.template
dst=$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/openvswitch
install -p -D -m 0644 $src $dst

install -p -D -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/openvswitch
install -p -D -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/openvswitch

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
install -p -m 0755 %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/

install -d -m 0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/openvswitch

install -d -m 0755 $RPM_BUILD_ROOT%{python_sitelib}
mv $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/* $RPM_BUILD_ROOT%{python_sitelib}
rmdir $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/

install -d -m 0755 $RPM_BUILD_ROOT%{_includedir}/openvswitch
install -p -D -m 0644 include/openvswitch/*.h \
        -t $RPM_BUILD_ROOT%{_includedir}/openvswitch
install -p -D -m 0644 config.h -t $RPM_BUILD_ROOT%{_includedir}/openvswitch

install -d -m 0755 $RPM_BUILD_ROOT%{_includedir}/openvswitch/lib
install -p -D -m 0644 lib/*.h \
        -t $RPM_BUILD_ROOT%{_includedir}/openvswitch/lib

install -d -m 0755 $RPM_BUILD_ROOT%{_includedir}/openflow
install -p -D -m 0644 include/openflow/*.h \
        -t $RPM_BUILD_ROOT%{_includedir}/openflow

# Get rid of stuff we don't want to make RPM happy.
rm -f \
    $RPM_BUILD_ROOT%{_sbindir}/ovs-vlan-bug-workaround \
    $RPM_BUILD_ROOT%{_mandir}/man8/ovs-vlan-bug-workaround.8 \
    $RPM_BUILD_ROOT%{_sbindir}/ovs-brcompatd \
    $RPM_BUILD_ROOT%{_mandir}/man8/ovs-brcompatd.8

#desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE6}

%preun
if [ "$1" = "0" ]; then
    # Package removal, not upgrade
    /sbin/chkconfig openvswitch off > /dev/null 2>&1 || :
    /sbin/service openvswitch stop > /dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service openvswitch restart >/dev/null 2>&1 || :
fi

%files
%{_sysconfdir}/openvswitch/
%config(noreplace) %{_sysconfdir}/logrotate.d/openvswitch
%config(noreplace) %{_sysconfdir}/sysconfig/openvswitch
%{_sysconfdir}/sysconfig/network-scripts/ifup-ovs
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ovs
%{_sysconfdir}/rc.d/init.d/openvswitch
%{_bindir}/ovs-appctl
%{_bindir}/ovs-benchmark
%{_bindir}/ovs-dpctl
%{_bindir}/ovs-dpctl-top
%{_bindir}/ovs-ofctl
%{_bindir}/ovs-pcap
%{_bindir}/ovs-pki
%{_bindir}/ovs-tcpundump
%{_bindir}/ovs-vsctl
%{_bindir}/ovsdb-client
%{_bindir}/ovsdb-tool
%{_bindir}/ovs-parse-backtrace
%{_bindir}/vtep-ctl
# ovs-bugtool is LGPLv2+
%{_sbindir}/ovs-bugtool
%{_sbindir}/ovs-vswitchd
%{_sbindir}/ovsdb-server
%{_mandir}/man1/ovs-benchmark.1*
%{_mandir}/man1/ovs-pcap.1*
%{_mandir}/man1/ovs-tcpundump.1*
%{_mandir}/man1/ovsdb-client.1*
%{_mandir}/man1/ovsdb-server.1*
%{_mandir}/man1/ovsdb-tool.1*
%{_mandir}/man5/ovs-vswitchd.conf.db.5*
%{_mandir}/man5/vtep.5*
%{_mandir}/man8/vtep-ctl.8*
%{_mandir}/man8/ovs-appctl.8*
%{_mandir}/man8/ovs-bugtool.8*
%{_mandir}/man8/ovs-ctl.8*
%{_mandir}/man8/ovs-dpctl.8*
%{_mandir}/man8/ovs-dpctl-top.8*
%{_mandir}/man8/ovs-ofctl.8*
%{_mandir}/man8/ovs-pki.8*
%{_mandir}/man8/ovs-vsctl.8*
%{_mandir}/man8/ovs-vswitchd.8*
%{_mandir}/man8/ovs-parse-backtrace.8*
# /usr/share/openvswitch/bugtool-plugins and
# /usr/share/openvswitch/scripts/ovs-bugtool* are LGPLv2+
%{_datadir}/openvswitch/
%{_sharedstatedir}/openvswitch
#%{_docdir}/%{name}-%{version}/README.RHEL
# see COPYING for full licensing details
%doc COPYING DESIGN INSTALL.SSL NOTICE README WHY-OVS

%files -n python-openvswitch
%{python_sitelib}/ovs
%doc COPYING


%if %{with_ovsdbmonitor}
%files -n ovsdbmonitor
%{_bindir}/ovsdbmonitor
%{_mandir}/man1/ovsdbmonitor.1*
%{_datadir}/ovsdbmonitor
%{_datadir}/applications/ovsdbmonitor.desktop
%doc ovsdb/ovsdbmonitor/COPYING
%endif

%files test
%{_bindir}/ovs-test
%{_bindir}/ovs-vlan-test
%{_bindir}/ovs-l3ping
%{_mandir}/man8/ovs-test.8*
%{_mandir}/man8/ovs-vlan-test.8*
%{_mandir}/man8/ovs-l3ping.8*
%{python_sitelib}/ovstest

%files devel
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/openvswitch/*
%{_includedir}/openflow/*


%changelog
* Tue May 02 2013 Thomas Graf <tgraf@redhat.com> - 1.10.0-1
- Update to 1.10.0 (#958814)

* Thu Mar 07 2013 Thomas Graf <tgraf@redhat.com> - 1.9.0-2
- Update to 1.9.0 (#916655)

* Thu Nov 29 2012 Thomas Graf <tgraf@redhat.com> - 1.7.1-7
- Require kernel >= 2.6.32-343 (#881704)

* Tue Nov 20 2012 Thomas Graf <tgraf@redhat.com> - 1.7.1-6
- Don't create world writable pki/*/incomming directory (#845351)

* Tue Nov 20 2012 Thomas Graf <tgraf@redhat.com> 1.7.1-5
- Increase max fd limit to support 256 bridges (#873072)

* Tue Oct 25 2012 Thomas Graf <tgraf@redhat.com> - 1.7.1-4
- Don't add iptables accept rule for -p GRE as GRE tunneling is unsupported

* Wed Oct 10 2012 Thomas Graf <tgraf@redhat.com> 1.7.1-3
- Automatically start openvswitch service in ifup/ifdown-ovs
- Don't add iptables accept rule for -p GRE as GRE tunneling is unsupported
- openvswitch-test requires python-argparse

* Tue Oct 09 2012 Thomas Graf <tgraf@redhat.com> 1.7.1-2
- Fix ovs-ifup and ovs-ifdown to timeout if ovs daemon can't be reached

* Mon Sep 10 2012 Thomas Graf <tgraf@redhat.com> 1.7.1-1
- Update to 1.7.1

* Fri Aug 30 2012 Thomas Graf <tgraf@redhat.com> 1.7.0-1
- Initial rhel package
