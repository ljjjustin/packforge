# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-eventlet
Version:        0.13.0
Release:        3%{?dist}
Summary:        Highly concurrent networking library
Group:          Development/Libraries
License:        MIT
URL:            http://eventlet.net
Source0:        http://pypi.python.org/packages/source/e/eventlet/eventlet-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx10
BuildRequires:  python-greenlet
Requires:       python-greenlet

%description
Eventlet is a networking library written in Python. It achieves high
scalability by using non-blocking io while at the same time retaining
high programmer usability by using coroutines to make the non-blocking
io operations appear blocking at the source code level.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for the python-eventlet package.

%prep
%setup -q -n eventlet-%{version}
find -name '.*' -type f -exec rm {} \;
sed -i -e 's///g' tests/mock.py
sed -i -e '1d' eventlet/support/greendns.py

%build
%{__python} setup.py build
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
rm _build/html/.buildinfo
popd
chmod a-x tests/mock.py

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE NEWS README README.twisted
%{python_sitelib}/eventlet
%{python_sitelib}/eventlet*.egg-info

%files doc
%defattr(-,root,root,-)
%doc doc/_build/html examples tests

%changelog
* Mon Nov 12 2012 Pádraig Brady <P@draigBrady.com - 0.9.17-2
- fix waitpid() override to not return immediately

* Fri Aug 03 2012 Pádraig Brady <P@draigBrady.com - 0.9.17-1
- Update to 0.9.17

* Tue Mar 27 2012 Pádraig Brady <P@draigBrady.com - 0.9.16-5
- Update patch to avoid leak of _DummyThread objects

* Wed Feb 29 2012 Pádraig Brady <P@draigBrady.com - 0.9.16-4
- Apply a patch to avoid leak of _DummyThread objects

* Wed Nov 09 2011 Pádraig Brady <P@draigBrady.com - 0.9.16-3
- Apply a patch to support subprocess.Popen implementations
  that accept the timeout parameter, which is the case on RHEL >= 6.1

* Fri Oct 21 2011 Pádraig Brady <P@draigBrady.com> - 0.9.16-2
- Changed python-sphinx build dependency to python-sphinx10

* Sat Aug 27 2011 Kevin Fenzi <kevin@scrye.com> - 0.9.16-1
- Update to 0.9.16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Lev Shamardin <shamardin@gmail.com> - 0.9.12-1
- Updated to version 0.9.12.

* Wed Jul 28 2010 Lev Shamardin <shamardin@gmail.com> - 0.9.9-1
- Updated to version 0.9.9.

* Wed Apr 14 2010 Lev Shamardin <shamardin@gmail.com> - 0.9.7-1
- Initial package version.
