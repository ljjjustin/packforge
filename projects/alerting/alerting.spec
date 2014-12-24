Name:           alerting
Version:        0.2.0
Release:        1%{?dist}
Summary:        Ops Plantform alerting

Group:          Applications/System
License:        ASL 2.0
URL:            http://git.ustack.com/ustack/alerting
Source0:        alerting-%{version}.tar.gz
Source1:        ops-alert-api.init
Source2:        ops-alert-api.upstart
Source3:        ops-alert-worker.init
Source4:        ops-alert-worker.upstart
Source5:        ops-alert-flusher.init
Source6:        ops-alert-flusher.upstart
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch

Requires: python-sqlalchemy
Requires: python-migrate
Requires: python-anyjson
Requires: python-iso8601
Requires: python-netaddr
Requires: python-eventlet
Requires: python-argparse
Requires: python-greenlet
Requires: python-pecan
Requires: python-wsme
Requires: python-extras
Requires: python-oslo-config
Requires: python-babel
Requires: python-memcached
Requires: python-ordereddict
Requires: python-requests
Requires: python-msgpack
Requires: ssdb 
Requires: memcached
Requires: mod_wsgi

%description
UnitedStack Alerting Manager

%prep
%setup -q -n alerting-%{version}


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/alerting
install -d -m 755 %{buildroot}%{_localstatedir}/log/alerting

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/alerting
install -p -D -m 644 etc/alerting/alerting.conf %{buildroot}%{_sysconfdir}/alerting/alerting.conf
install -p -D -m 644 etc/alerting/channel.json %{buildroot}%{_sysconfdir}/alerting/channel.json
install -p -D -m 644 etc/alerting/person.json %{buildroot}%{_sysconfdir}/alerting/person.json
install -p -D -m 644 etc/alerting/priority.json %{buildroot}%{_sysconfdir}/alerting/priority.json

# Install initscripts for Mimic services
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ops-alert-api

install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/ops-alert-worker

install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/ops-alert-flusher

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/alerting

# Install upstart jobs examples
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/alerting/
install -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/alerting/
install -p -m 644 %{SOURCE6} %{buildroot}%{_datadir}/alerting/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/alerting-%{version}-*.egg-info
%{python_sitelib}/alerting

%{_bindir}/alert-api
%{_bindir}/alert-worker
%{_bindir}/alert-flusher

%{_initrddir}/ops-alert-api
%{_initrddir}/ops-alert-worker
%{_initrddir}/ops-alert-flusher
%{_datarootdir}/alerting/ops-alert-api.upstart
%{_datarootdir}/alerting/ops-alert-worker.upstart
%{_datarootdir}/alerting/ops-alert-flusher.upstart

%config(noreplace) %attr(-, root, alerting) %{_sysconfdir}/alerting/alerting.conf
%config(noreplace) %attr(-, root, alerting) %{_sysconfdir}/alerting/channel.json
%config(noreplace) %attr(-, root, alerting) %{_sysconfdir}/alerting/person.json
%config(noreplace) %attr(-, root, alerting) %{_sysconfdir}/alerting/priority.json

%dir %attr(0755, alerting, root) %{_localstatedir}/run/alerting
%dir %attr(0755, alerting, root) %{_localstatedir}/log/alerting
%doc


%pre 
getent group alerting >/dev/null || groupadd -r alerting --gid 199
if ! getent passwd alerting >/dev/null; then
  useradd -u 298 -r -g alerting -G alerting,nobody -d %{_sharedstatedir}/alerting -s /sbin/nologin -c "Ops Plantform Alerting" alerting
fi
exit 0

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service ops-alerting-api stop >/dev/null 2>&1
    /sbin/chkconfig --del ops-alerting-api
fi

%changelog
* Wed Feb 19 2014 wentian <wentian@unitedstack.com> - 0.1
- First version of alerting
