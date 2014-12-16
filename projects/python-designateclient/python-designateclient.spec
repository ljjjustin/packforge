#
# spec file for package python-designateclient
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define component designateclient

Name:           python-%{component}
Version:        1.0.3
Release:        3%{?dist}
Summary:        Openstack DNS (Designate) API Client
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            http://launchpad.net/python-designateclient
Source:         python-designateclient-%{version}.tar.gz
BuildRequires:  python-d2to1 >= 0.2.10
BuildRequires:  python-devel
BuildRequires:  python-pbr >= 0.5.21
BuildRequires:  python-setuptools

# Documentation requirements:
#BuildRequires:  python-sphinx >= 1.1.2
Requires:       python >= 2.6.6
Requires:       python-cliff >= 1.4
Requires:       python-jsonschema >= 1.0.0
Requires:       python-keyring
Requires:       python-keystoneclient >= 0.2
Requires:       python-pbr >= 0.5.21
Requires:       python-requests >= 1.1
Requires:       python-stevedore >= 0.9
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
This is a client for the OpenStack Designate API. There's a Python API
(the designateclient module), and a command-line tool (designate).

%package doc
Summary:        Openstack DNS (Designate) API Client - Documentation
Group:          Documentation/HTML
Requires:       %{name} = %{version}

%description doc
This package contains documentation files for %{name}.


%prep
%setup -q -n python-designateclient-%{version}

%build
python setup.py build
#python setup.py build_sphinx

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-data=%{python_sitelib}

#rm doc/build/html/.buildinfo


%files
%defattr(-,root,root,-)
%doc README.rst
%{_bindir}/designate
%{python_sitelib}/%{component}/
%{python_sitelib}/python_%{component}-*.egg-info

#%files doc
#%defattr(-,root,root,-)
#%doc doc/build/html


%changelog
* Thu Sep 19 2013 opensuse-cloud@opensuse.org
- Update to version 2013.1.a4:
  + Ensure we only list sphinx as a dep once
  + Add a --insecure arg to ignore invalid SSL certs
  + Ensure beta versions are not downloaded from pypi
* Wed Sep  4 2013 opensuse-cloud@opensuse.org
- Update to version 2013.1.a1:
  + Use Python 3.x compatible except construct.
* Tue Sep  3 2013 dmueller@suse.com
- fix requires
- remove unneeded requires
* Tue Sep  3 2013 opensuse-cloud@opensuse.org
- Update to version 2013.1.a15:
  + Update to PBR 0.5.21+
  + Allow auth using a pre-fetched token
* Wed Jul 17 2013 speilicke@suse.com
- Drop LICENSE, run disabled source service
* Wed Jul 17 2013 speilicke@suse.com
- Initial version
