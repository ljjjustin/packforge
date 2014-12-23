# Created by pyp2rpm-1.0.1
%global pypi_name oslo.serialization
%global pkg_name oslo-serialization

Name:           python-oslo-serialization
Version:        0.3.0
Release:        2%{?dist}
Summary:        OpenStack oslo.serialization library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
Requires:       python-babel
Requires:       python-iso8601
Requires:       python-oslo-utils
Requires:       python-six

%description
An OpenStack library for representing objects in transmittable and
storable formats.

%package doc
Summary:    Documentation for the Oslo serialization library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the Oslo serialization library.

%prep
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -f requirements.txt
# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py


%build
%{__python} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python} setup.py install --skip-build --root %{buildroot}

#delete tests
rm -fr %{buildroot}%{python_sitelib}/%{pypi_name}/tests/

%files
%doc README.rst LICENSE
%{python_sitelib}/oslo
%{python_sitelib}/*.egg-info
%{python_sitelib}/*-nspkg.pth

%files doc
%doc html LICENSE


%changelog
* Wed Sep 17 2014 Nejc Saje <nsaje@redhat.com> - 0.3.0-1
- Initial package (#1142753)
