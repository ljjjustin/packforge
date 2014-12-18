Name:		lotus	
Version:        0.1.2
Release:	5%{?dist}
Summary:	UnitedStack lotus

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/lotus	
Source0:	lotus-%{version}.tar.gz
Source1:	ustack-lotus-collector.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch

Requires: python-d2to1
Requires: python-pbr
Requires: python-argparse
Requires: python-keystoneclient
Requires: python-ceilometerclient
Requires: python-pecan
Requires: python-wsme
Requires: python-netaddr
Requires: python-babel
Requires: python-iso8601
Requires: python-eventlet
Requires: python-oslo-config
Requires: python-anyjson
Requires: python-migrate
Requires: python-sqlalchemy
Requires: mod_wsgi

%description
UnitedStack Monitor App Manager

%prep
%setup -q -n lotus-%{version}


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/lotus
install -d -m 755 %{buildroot}%{_localstatedir}/log/lotus

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/lotus
install -p -D -m 644 etc/lotus/lotus.conf.sample %{buildroot}%{_sysconfdir}/lotus/lotus.conf
install -p -D -m 644 etc/lotus/policy.json %{buildroot}%{_sysconfdir}/lotus/policy.json

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/lotus

# Install lotus-collector init script
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ustack-lotus-collector


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/lotus-%{version}-*.egg-info
%{python_sitelib}/lotus
%{_bindir}/lotus-api
%{_bindir}/lotus-dbsync
%{_bindir}/lotus-collector
%{_initrddir}/ustack-lotus-collector


%config(noreplace) %attr(-, root, root) %{_sysconfdir}/lotus/lotus.conf
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/lotus/policy.json

%dir %attr(0755, apache, root) %{_localstatedir}/run/lotus
%dir %attr(0755, apache, root) %{_localstatedir}/log/lotus
%doc

%changelog
* Thu Dec 31 2013 Xingchao <xingchao@unitedstack.com> - 0.1.1
- Add lotus-collector daemon
* Mon Sep 9 2013 Xingchao <xingchao@unitedstack.com> - 0.1
- Package lotus for deployment

