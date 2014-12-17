%global srcname amqplib

Name:           python-%{srcname}
Version:        1.0.2
Release:        3%{?dist}
Summary:        Client library for AMQP

Group:          Development/Languages
License:        LGPLv2+
URL:            http://pypi.python.org/pypi/amqplib
Source0:        http://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tgz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose


%description
Client library for AMQP (Advanced Message Queuing Protocol)

Supports the 0-8 AMQP spec, and has been tested with RabbitMQ
and Python's 2.4, 2.5, and 2.6


%prep
%setup -q -n %{srcname}-%{version}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

 
%clean
rm -rf %{buildroot}


%check
cd tests/client_0_8
nosetests run_all.py


%files
%defattr(-,root,root,-)
%doc CHANGES INSTALL LICENSE README TODO docs/ 
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info


%changelog
* Mon Nov 01 2010 Fabian Affolter <fabian@bernewireless.net> - 0.6.1-2
- Added python-nose as BR
- Remove old python stuff for Fedora 12

* Sat Jul 03 2010 Fabian Affolter <fabian@bernewireless.net> - 0.6.1-1
- Initial package
