#
# spec file for package openstack-designate
#


%define component designate
%define groupname %{component}
%define username %{component}

Name:           openstack-%{component}
Version:        2013.2.1
Release:        3%{?dist}
Summary:        OpenStack DNS Service (Designate)
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://github.com/stackforge/designate
Source:         designate-%{version}.tar.gz
Source1:        %{name}.init
Source7:        %{name}.logrotate
BuildRequires:  openstack-utils
BuildRequires:  python-d2to1
BuildRequires:  python-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
Requires:       logrotate
Requires:       python-designate = %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(pre):  shadow-utils
Requires(pre):  chkconfig

BuildArch:      noarch

%description
Designate is an OpenStack inspired DNSaaS.

%package -n python-designate
Summary:        OpenStack DNS Service (Designate) - Python module
Group:          Development/Languages/Python
Requires:       python >= 2.6.6
Requires:       python-flask >= 0.9
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-routes >= 1.12.3
Requires:       python-sqlalchemy >= 0.7.8
Requires:       python-webob >= 1.2.3
Requires:       python-cliff >= 1.4
Requires:       python-d2to1 >= 0.2.10
Requires:       python-designateclient >= 0.2.1
Requires:       python-eventlet >= 0.13.0
Requires:       python-extras
Requires:       python-iso8601 >= 0.1.4
Requires:       python-jsonschema >= 1.3.0
Requires:       python-keystoneclient >= 0.3.0
Requires:       python-kombu >= 2.4.8
Requires:       python-netaddr
Requires:       python-oslo-config >= 1.1.0
Requires:       python-pbr >= 0.5.21
Requires:       python-pecan >= 0.2.0
Requires:       python-migrate >= 0.7.2
Requires:       python-stevedore >= 0.10

%description -n python-designate
Designate is an OpenStack inspired DNSaaS.

This package contains the core Python module of OpenStack Designate.

%package agent
Summary:        OpenStack DNS (Designate) - Agent
Group:          System/Management
Summary:        OpenStack DNS (Designate) - Agent
Group:          System/Management
Requires:       %{name} = %{version}

%description agent
This package contains the OpenStack DNS Agent.

%package api
Summary:        OpenStack DNS (Designate) - API
Group:          System/Management
Summary:        OpenStack DNS (Designate) - API
Group:          System/Management
Requires:       %{name} = %{version}

%description api
This package contains the OpenStack DNS API.

%package central
Summary:        OpenStack DNS (Designate) - Central
Group:          System/Management
Summary:        OpenStack DNS (Designate) - Central
Group:          System/Management
Requires:       %{name} = %{version}

%description central
This package contains the OpenStack DNS Central.

%package sink
Summary:        OpenStack DNS (Designate) - Sink
Group:          System/Management
Summary:        OpenStack DNS (Designate) - Sink
Group:          System/Management
Requires:       %{name} = %{version}

%description sink
This package contains the OpenStack DNS Sink.

%prep
%setup -q -n designate-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

### directories
install -d -m 755 %{buildroot}%{_localstatedir}/{lib,log,run}/designate

### configuration files
install -d -m 0755 %{buildroot}%{_sysconfdir}/designate
cp etc/designate/designate.conf.sample %{buildroot}%{_sysconfdir}/designate/designate.conf
cp etc/designate/api-paste.ini %{buildroot}%{_sysconfdir}/designate/api-paste.ini
cp etc/designate/policy.json %{buildroot}%{_sysconfdir}/designate
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

### init scripts
mkdir -p %{buildroot}%{_sbindir}
for i in api sink agent central ; do
    tmp=$(mktemp)
    cat %{SOURCE1} | sed "s/__NAME__/$i/g" > $tmp
    install -D -m 755 $tmp %{buildroot}%{_initddir}/%{name}-$i
    ln -s ../..%{_initddir}/%{name}-$i %{buildroot}%{_sbindir}/rc%{name}-$i
done

### test subpackage

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{component}

### set default configuration (mostly applies to package-only setups and quickstart, i.e. not generally crowbar)
#   %define designate_conf %{buildroot}%{_sysconfdir}/designate/designate.conf
#   openstack-config --set %{designate_conf} DEFAULT verbose True
#   openstack-config --set %{designate_conf} DEFAULT log_file designate.log

%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || useradd -r -g %{groupname} -d %{_localstatedir}/lib/designate -s /sbin/nologin -c "OpenStack designate Daemon" %{username}
exit 0

%post agent
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-agent
fi

%preun agent
if [ $1 -eq 0 ] ; then
    for svc in agent; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%postun agent
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in agent; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%post api
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-api
fi

%preun api
if [ $1 -eq 0 ] ; then
    for svc in api; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%postun api
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%post central
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-central
fi

%preun central
if [ $1 -eq 0 ] ; then
    for svc in central; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%postun central
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in central; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%post sink
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-sink
fi

%preun sink
if [ $1 -eq 0 ] ; then
    for svc in sink; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%postun sink
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in sink; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%files
%defattr(-,root,root)
%dir %attr(0755, %{username}, %{groupname}) %{_localstatedir}/lib/%{component}
%dir %attr(0755, %{username}, %{groupname}) %{_localstatedir}/log/%{component}
%ghost %dir %attr(0750, %{username}, %{groupname}) %{_localstatedir}/run/%{component}
%dir %attr(0750, root, %{groupname}) %{_sysconfdir}/%{component}
%config(noreplace) %attr(0640, root, %{groupname}) %{_sysconfdir}/%{component}/%{component}.conf
%config %{_sysconfdir}/%{component}/api-paste.ini
%config %{_sysconfdir}/%{component}/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/designate-rootwrap
%{_bindir}/designate-manage
%{_bindir}/designate-rpc-zmq-receiver


%files agent
%defattr(-,root,root)
%{_initddir}/%{name}-agent
%{_sbindir}/rc%{name}-agent
%{_bindir}/designate-agent

%files api
%defattr(-,root,root)
%{_initddir}/%{name}-api
%{_sbindir}/rc%{name}-api
%{_bindir}/designate-api

%files central
%defattr(-,root,root)
%{_initddir}/%{name}-central
%{_sbindir}/rc%{name}-central
%{_bindir}/designate-central

%files sink
%defattr(-,root,root)
%{_initddir}/%{name}-sink
%{_sbindir}/rc%{name}-sink
%{_bindir}/designate-sink

%files -n python-designate
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}


%changelog
* Tue Sep  4 2013 xuxin@unitedstack.com
- Update to version 2013.2.a266.g7308b92
