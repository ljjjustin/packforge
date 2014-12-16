Name:		ustack-ticket	
Version:        1.2.2
Release:	1%{?dist}
Summary:	UnitedStack ticket

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/ticket	
Source0:	ticket-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires: python-d2to1
Requires: python-pbr
Requires: python-six
Requires: python-anyjson
Requires: python-iso8601
Requires: python-argparse
Requires: python-keystoneclient
Requires: python-pecan
Requires: python-wsme
Requires: python-qiniu
Requires: python-oslo-config
Requires: mod_wsgi
Requires: httpd

%description
UnitedStack Ticket System 

%prep
%setup -q -n ticket-%{version}


%build

%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/ticket
install -d -m 755 %{buildroot}%{_localstatedir}/log/ticket

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/ticket
install -p -D -m 644 etc/ticket/ticket.conf.sample %{buildroot}%{_sysconfdir}/ticket/ticket.conf
install -p -D -m 644 etc/ticket/policy.json %{buildroot}%{_sysconfdir}/ticket/policy.json


# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/ticket

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/ticket-%{version}-*.egg-info
%{python_sitelib}/ticket

%{_bindir}/ticket-api
%{_bindir}/ticket-dbsync

%config(noreplace) %attr(-, root, root) %{_sysconfdir}/ticket/ticket.conf
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/ticket/policy.json

%dir %attr(0755, root, root) %{_localstatedir}/run/ticket
%dir %attr(0755, apache, root) %{_localstatedir}/log/ticket
%doc


%pre 

%preun

%changelog
* Fri Jan 28 2014 Xingchao Yu <xingchao@unitedstack.com> - 0.1
- Package ticket for deployment
