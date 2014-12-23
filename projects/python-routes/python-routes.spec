Name:		python-routes
Version:	1.13
Release:	6%{?dist}
Summary:	Rails-like routes for Python
Group:		Development/Languages
License:	BSD
URL:		http://routes.groovie.org/
Source0:	http://pypi.python.org/packages/source/R/Routes/Routes-%{version}.tar.gz

BuildArch: noarch

BuildRequires: python-setuptools-devel
BuildRequires: python-nose1.1
BuildRequires: python-coverage
BuildRequires: python-webtest
BuildRequires: python-paste

Requires: python-repoze-lru >= 0.3


%description
Routes is a Python re-implementation of the Rails routes system for mapping
URLs to Controllers/Actions and generating URLs. Routes makes it easy to
create pretty and concise URLs that are RESTful with little effort.


%prep
%setup -q -n Routes-%{version}

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
#PYTHONPATH=$(pwd) nosetests


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README docs
%{python_sitelib}/*


%changelog
* Tue Apr 24 2012 Pádraig Brady <P@draigBrady.com> 1.12.3-4
- Built parallel installable version for EPEL 6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Luke Macken <lmacken@redhat.com> - 1.12.3-1
- Update to 1.12.3

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 05 2010 Luke Macken <lmacken@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 1.10.3-1
- Update to 1.10.3

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 1.10.1-2
- Update to 1.10.1
- Run the test suite

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.8-3
- Rebuild for Python 2.6

* Sun May 11 2008 Kyle VanderBeek <kylev@kylev.com> - 1.8-2
- Fix rpmlint warning.
- Add documentation files.

* Wed Apr  9 2008 Kyle VanderBeek <kylev@kylev.com> - 1.8-1
- Initial version.

