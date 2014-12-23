Name:           python-jsonrpclib
Version:        0.1.3
Release:        2%{?dist}
License:        Apache-2.0
Summary:        Implementation of the JSON-RPC v2.0 specification as a client library
Group:          Development/Languages/Python
Url:            http://github.com/joshmarshall/jsonrpclib/
Source:         https://pypi.python.org/packages/source/j/jsonrpclib/jsonrpclib-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
This project is an implementation of the JSON-RPC v2.0 specification
(backwards-compatible) as a client library.

%prep
%setup -q -n jsonrpclib-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python_sitelib}/jsonrpclib
%{python_sitelib}/*.egg-info

%changelog
* Wed Sep 17 2014 Jiajun Liu <jiajun@unitedstack.com>
- Initial version
