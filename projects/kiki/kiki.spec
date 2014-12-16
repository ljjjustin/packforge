Name:		kiki	
Version:        2.0.3
Release:	2%{?dist}
Summary:	UnitedStack kiki

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/kiki	
Source0:	kiki-%{version}.tar.gz
Source1:	ustack-kiki-ws.init
Source2:	ustack-kiki-api.init
Source3:	ustack-kiki-mq-consumer.init
Source4:	ustack-kiki-websocket-server.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires: python-d2to1
Requires: python-pbr
Requires: python-migrate
Requires: python-sqlalchemy
Requires: python-anyjson
Requires: python-iso8601
Requires: python-netaddr
Requires: python-argparse
Requires: python-eventlet
Requires: python-stevedore
Requires: python-mako
Requires: python-crypto2.6
Requires: python-memcached
Requires: python-ordereddict
Requires: python-keystoneclient
Requires: python-pecan
Requires: python-wsme
Requires: python-sockjs-tornado >= 1.0.0
Requires: python-oslo-config
Requires: python-twilio >= 3.6.6
Requires: python-kombu >= 2.4.8
Requires: python-amqp  >= 1.4.5
Requires: python-oslo-messaging >= 1.4.0.1
Requires: mod_wsgi

%description
UnitedStack Message Notifier

%prep
%setup -q -n kiki-%{version}


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/kiki
install -d -m 755 %{buildroot}%{_localstatedir}/log/kiki

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/kiki
install -p -D -m 640 etc/kiki/kiki.conf.sample %{buildroot}%{_sysconfdir}/kiki/kiki.conf
install -p -D -m 640 etc/kiki/policy.json %{buildroot}%{_sysconfdir}/kiki/policy.json

# Install initscripts for Kiki services
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ustack-kiki-ws
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/ustack-kiki-api
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/ustack-kiki-mq-consumer
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/ustack-kiki-websocket-server

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/kiki

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/kiki-%{version}-*.egg-info
%{python_sitelib}/kiki

%{_initrddir}/ustack-kiki-ws
%{_initrddir}/ustack-kiki-api
%{_initrddir}/ustack-kiki-mq-consumer
%{_initrddir}/ustack-kiki-websocket-server

%{_bindir}/kiki-api
%{_bindir}/kiki-dbsync
%{_bindir}/kiki-db-version
%{_bindir}/kiki-ws
%{_bindir}/kiki-mq-consumer
%{_bindir}/kiki-websocket-server
%{_bindir}/kiki-tpl-test

%config(noreplace) %attr(-, root, root) %{_sysconfdir}/kiki/kiki.conf
%config %attr(-, root, root) %{_sysconfdir}/kiki/policy.json

%dir %attr(0755, root, root) %{_localstatedir}/run/kiki
%dir %attr(0755, root, root) %{_localstatedir}/log/kiki
%doc


%pre 

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service ustack-kiki-ws stop >/dev/null 2>&1
    /sbin/chkconfig --del ustack-kiki-ws
fi

%changelog
* Mon Dec 28 2013 Xingchao Yu <xingchao@unitedstack.com> - 0.1
- Package kiki for deployment

