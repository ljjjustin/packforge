# Created by pyp2rpm-1.0.1
%global pypi_name tooz

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        0.3
Release:        1%{?dist}
Summary:        Coordination library for distributed systems

License:        ASL 2.0
URL:            https://tooz.readthedocs.org
Source0:        https://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
# For building documentation
BuildRequires:  python-sphinx
Requires:       python-babel
Requires:       python-stevedore
Requires:       python-six
Requires:       python-iso8601
Requires:       python-kazoo
Requires:       python-oslo-config
Requires:       python-pymemcache
Requires:       python-posix_ipc
Requires:       python-msgpack
Requires:       python-retrying

%description
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Coordination library for distributed systems
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# For building documentation
BuildRequires:  python3-sphinx
Requires:       python3-babel
Requires:       python3-stevedore
Requires:       python3-six
Requires:       python3-iso8601
Requires:       python3-kazoo
Requires:       python3-oslo-config
Requires:       python3-pymemcache
Requires:       python3-posix_ipc
Requires:       python3-msgpack
Requires:       python3-retrying

%description -n python3-%{pypi_name}
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.
%endif

%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0

%description doc
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.

This package contains documentation in HTML format.


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
# generate html docs
sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

#delete tests
rm -fr %{buildroot}%{python_sitelib}/%{pypi_name}/tests/
%if 0%{?with_python3}
rm -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/
%endif


%files
%doc README.rst LICENSE
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files doc
%doc html

%changelog
* Tue Sep 09 2014 Nejc Saje <nsaje@redhat.com> - 0.3-1
- Initial package.

