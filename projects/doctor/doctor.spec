Name:		doctor	
Version:        1.0.21
Release:	2%{?dist}
Summary:	UnitedStack Doctor

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/doctor	
Source0:	doctor-%{version}.tar.gz
Source1:	ustack-doctor.init
Source2:	ustack-doctor.logrotate
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch

Requires: MySQL-python
Requires: python-alembic
Requires: python-argparse
Requires: python-babel
Requires: python-cinderclient
Requires: python-crypto
Requires: python-eventlet
Requires: python-glanceclient
Requires: python-iso8601
Requires: python-keystoneclient
Requires: python-netaddr
Requires: python-neutronclient
Requires: python-nose
Requires: python-novaclient
Requires: python-oslo-config
Requires: python-paramiko
Requires: python-pbr
Requires: python-pecan
Requires: python-sqlalchemy
Requires: python-testresources
Requires: python-wsme
Requires: python-ceilometerclient
Requires: python-gringotts

%description
UnitedStack Doctor Service

%prep
%setup -q -n doctor-%{version}


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/doctor
install -d -m 755 %{buildroot}%{_localstatedir}/log/doctor

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/doctor
install -p -D -m 640 etc/doctor/doctor.conf.sample %{buildroot}%{_sysconfdir}/doctor/doctor.conf.sample
install -p -D -m 640 etc/doctor/logging.conf.sample %{buildroot}%{_sysconfdir}/doctor/logging.conf.sample

# Install initscripts for doctor services
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ustack-doctor

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/ustack-doctor

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/doctor

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/doctor-%{version}-*.egg-info
%{python_sitelib}/doctor

%{_initrddir}/ustack-doctor

%{_bindir}/doctor-api
%{_bindir}/doctor-manage

%config(noreplace) %attr(-, root, doctor) %{_sysconfdir}/doctor/doctor.conf.sample
%config(noreplace) %attr(-, root, doctor) %{_sysconfdir}/doctor/logging.conf.sample

%config(noreplace) %{_sysconfdir}/logrotate.d/ustack-doctor

%dir %attr(0755, doctor, root) %{_localstatedir}/run/doctor
%dir %attr(0755, doctor, root) %{_localstatedir}/log/doctor
%doc

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service ustack-doctor stop >/dev/null 2>&1
    /sbin/chkconfig --del ustack-doctor
fi

%changelog
* Mon Apr 07 2014 Jiajun Liu <jiajun@unitedstack.com> - 2014.1.1.dev18.gbe539e6-2
- Initial RPM release
