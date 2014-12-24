Name:           accounting
Version:        2013.2.a4.g42ea8fb
Release:        1%{?dist}
Summary:        Ops Plantform Accounting

Group:          Applications/System
License:        ASL 2.0
URL:            http://git.ustack.com/ustack/accounting
Source0:        accounting-%{version}.tar.gz
Source1:        ops-account-api.init
Source2:        ops-account-api.upstart
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
Requires: python-ordereddict
Requires: python-requests
Requires: mod_wsgi

%description
UnitedStack Accounting Manager

%prep
%setup -q -n accounting-%{version}


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/accounting
install -d -m 755 %{buildroot}%{_localstatedir}/log/accounting

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/accounting
install -p -D -m 644 etc/accounting/accounting.conf %{buildroot}%{_sysconfdir}/accounting/accounting.conf

# Install initscripts for accounting services
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ops-account-api

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/accounting

# Install upstart jobs examples
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/accounting/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/accounting-%{version}-*.egg-info
%{python_sitelib}/accounting

%{_bindir}/account-api

%{_initrddir}/ops-account-api
%{_datarootdir}/accounting/ops-account-api.upstart

%config(noreplace) %attr(-, root, accounting) %{_sysconfdir}/accounting/accounting.conf

%dir %attr(0755, accounting, root) %{_localstatedir}/run/accounting
%dir %attr(0755, accounting, root) %{_localstatedir}/log/accounting
%doc


%pre 
getent group accounting >/dev/null || groupadd -r accounting --gid 199
if ! getent passwd accounting >/dev/null; then
  useradd -u 298 -r -g accounting -G accounting,nobody -d %{_sharedstatedir}/accounting -s /sbin/nologin -c "Ops Plantform Accounting" accounting
fi
exit 0

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service ops-accounting-api stop >/dev/null 2>&1
    /sbin/chkconfig --del ops-accounting-api
fi

%changelog
* Wed Feb 19 2014 wentian <wentian@unitedstack.com> - 0.1
- First version of accounting
