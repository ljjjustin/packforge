Name:		gringotts	
Version:        0.3.4
Release:	1%{?dist}
Summary:	UnitedStack Gringotts

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/gringotts	
Source0:	gringotts-%{version}.tar.gz
Source1:	ustack-gring-api.init
Source2:	ustack-gring-waiter.init		
Source3:	ustack-gring-master.init
Source4:	ustack-gring-checker.init
Source5:	gringotts.logrotate
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch


%description
UnitedStack Billing System


%package api
Summary:          Ustack Billing API service
Group:            Applications/System

Requires:         python-gringotts = %{version}-%{release}

%description api
This package coantains Gringotts api service.

%package waiter
Summary:          Ustack Billing Waiter service
Group:            Applications/System

Requires:         python-gringotts = %{version}-%{release}

%description waiter
This package coantains Gringotts waiter service.

%package master
Summary:          Ustack Billing Master service
Group:            Applications/System

Requires:         python-gringotts = %{version}-%{release}

%description master
This package coantains Gringotts master service.

%package checker
Summary:          Ustack Billing Checker service
Group:            Applications/System

Requires:         python-gringotts = %{version}-%{release}

%description checker
This package coantains Gringotts checker service.

%package -n python-gringotts
Summary:          Ustack Billing Master service
Group:            Applications/System

Requires: python-d2to1
Requires: python-pbr
Requires: python-apscheduler
Requires: MySQL-python
Requires: python-alembic
Requires: python-httplib2
Requires: python-greenlet
Requires: python-iso8601
Requires: python-anyjson
Requires: python-argparse
Requires: python-keystoneclient
Requires: python-ceilometerclient
Requires: python-novaclient
Requires: python-glanceclient
Requires: python-cinderclient
Requires: python-neutronclient
Requires: python-dateutil
Requires: python-sqlalchemy
Requires: python-eventlet
Requires: python-extras
Requires: python-netaddr
Requires: python-pecan
Requires: python-wsme
Requires: python-oslo-config
Requires: python-migrate
Requires: python-memcached
Requires: python-stevedore
Requires: python-kombu

%description -n python-gringotts
This package coantains Gringotts Python lib.
Requires:    gringotts = %{version}-%{release}

%prep
%setup -q -n gringotts-%{version}

find . \( -name .gitignore -o -name .placeholder \) -delete

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/gringotts
install -d -m 755 %{buildroot}%{_localstatedir}/log/gringotts

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/gringotts
install -p -D -m 644 etc/gringotts/gringotts.conf.sample %{buildroot}%{_sysconfdir}/gringotts/gringotts.conf
install -p -D -m 644 etc/gringotts/rootwrap.conf %{buildroot}%{_sysconfdir}/gringotts/rootwrap.conf
install -p -D -m 644 etc/gringotts/policy.json %{buildroot}%{_sysconfdir}/gringotts/policy.json

# Install initscripts for gring services
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ustack-gring-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/ustack-gring-waiter
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/ustack-gring-master
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/ustack-gring-checker

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/gringotts

# Install logrotate
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/gringotts

%clean
rm -rf %{buildroot}

%files


%files api
%{_bindir}/gring-api
%{_initrddir}/ustack-gring-api
%files waiter
%{_bindir}/gring-waiter
%{_initrddir}/ustack-gring-waiter
%files master
%{_bindir}/gring-worker
%{_bindir}/gring-master
%{_initrddir}/ustack-gring-master
%files checker
%{_bindir}/gring-checker
%{_initrddir}/ustack-gring-checker

%files -n python-gringotts
%{_bindir}/gring-dbsync
%defattr(-,root,root,-)
%{python_sitelib}/gringotts-%{version}-*.egg-info
%{python_sitelib}/gringotts

%config(noreplace) %attr(-, root, gringotts) %{_sysconfdir}/gringotts/gringotts.conf
%config %attr(-, root, gringotts) %{_sysconfdir}/gringotts/policy.json
%config(noreplace) %attr(-, root, gringotts) %{_sysconfdir}/gringotts/rootwrap.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/gringotts

%dir %attr(0755, root, root) %{_localstatedir}/run/gringotts
%dir %attr(0755, root, root) %{_localstatedir}/log/gringotts

%pre 

%preun api
if [ $1 -eq 0 ] ; then
    /sbin/service ustack-gring-api stop >/dev/null 2>&1
    /sbin/chkconfig --del ustack-gring-api
fi
%preun waiter
if [ $1 -eq 0 ] ; then
    /sbin/service ustack-gring-waiter stop >/dev/null 2>&1
    /sbin/chkconfig --del ustack-gring-waiter
fi
%preun master
if [ $1 -eq 0 ] ; then
    /sbin/service ustack-gring-master stop >/dev/null 2>&1
    /sbin/chkconfig --del ustack-gring-master
fi
%preun checker
if [ $1 -eq 0 ] ; then
    /sbin/service ustack-gring-checker stop >/dev/null 2>&1
    /sbin/chkconfig --del ustack-gring-checker
fi

%changelog
* Tue Mar 11 2014 Xingchao Yu <xingchao@unitedstack.com> - 0.1
- Package gringotts for deployment
