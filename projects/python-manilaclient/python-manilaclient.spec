Name:             python-manilaclient
Epoch:            1
Version:          2014.10.0
Release:          2%{?dist}
Summary:          Python API and CLI for OpenStack Nova

Group:            Development/Languages
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/%{name}
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-d2to1
BuildRequires:    python-pbr

Requires:         python-argparse
Requires:         python-iso8601
Requires:         python-oslo-utils
Requires:         python-oslo-config
Requires:         python-oslo-serialization >= 1.0.0
Requires:         python-crypto
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-simplejson
Requires:         python-six
Requires:         python-babel
Requires:         python-keystoneclient
Requires:         python-keyring
Requires:         python-setuptools

%description
This is a client for the OpenStack Nova API. There's a Python API (the
manilaclient module), and a command-line script (manila). Each implements 100% of
the OpenStack Nova API.

%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
manilaclient module), and a command-line script (manila). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%prep
%setup -q

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATNOVACLIENTVERSION/%{version}/ manilaclient/__init__.py

# Remove bundled egg-info
rm -rf python_manilaclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/manila.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/manila

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/manilaclient/tests
export PYTHONPATH="$( pwd ):$PYTHONPATH"
#sphinx-build -b html doc/source html
#sphinx-build -b man doc/source man

#install -p -D -m 644 man/manila.1 %{buildroot}%{_mandir}/man1/manila.1

# Fix hidden-file-or-dir warnings
#rm -fr html/.doctrees html/.buildinfo

%files
%doc README.rst
%doc LICENSE
%{_bindir}/manila
%{python_sitelib}/manilaclient
%{python_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
#%{_mandir}/man1/manila.1.gz

#%files doc
#%doc html

%changelog
* Mon Dec 15 2014 Xingchao Yu <xingchao@unitedstack.com> 1:0.10.0-1
- First commit
