Name:           placebo
Version:        1.3.4
Release:        5%{?dist}
Summary:        uStack Dashboard

Group:          Development/Libraries

License:        ASL 2.0 and BSD
URL:            http://git.ustack.com/ustack/placebo
BuildArch:      noarch

Source0:        placebo-%{version}.tar.gz
#Source1:        placebo.conf
#Source2:        placebo-httpd-2.4.conf
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%if 0%{?rhel}<7 || 0%{?fedora} < 18

# epel6 has a separate Django14 package
%if 0%{?rhel}==6
Requires:   Django14
%else
Requires:   Django
%endif

%else
Requires:   python-django
%endif

Requires: python-pbr
Requires: python-keystoneclient
Requires: python-django-openstack-auth
Requires: MySQL-python
Requires: python-memcached
Requires: python-lockfile
Requires: python-mako
Requires: mod_wsgi
Requires: httpd
Requires: python-django-south
Requires: django-simple-captcha
Requires: placebo_extras


BuildRequires: django-simple-captcha
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: nodejs-less
BuildRequires: python-django-south
BuildRequires: python-requests
BuildRequires: python-keystoneclient

# for checks:
#BuildRequires:   python-django-nose
#BuildRequires:   python-cinderclient
#BuildRequires:   python-django-appconf
#BuildRequires:   python-django-openstack-auth
#BuildRequires:   python-django-compressor

%description
UnitedStack Placebo

%prep
%setup -q -n %{name}-%{version}

# remove unnecessary .po files
#find . -name "django*.po" -exec rm -f '{}' \;

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# drop httpd-conf snippet
#%if 0%{?rhel} || 0%{?fedora} <18
#install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
#%else
## httpd-2.4 changed the syntax
#install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
#%endif


# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/placebo
install -d -m 755 %{buildroot}%{_localstatedir}/log/placebo

# Copy everything to /usr/share
mv manage.py %{buildroot}%{_datadir}/%{name}

# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{python_sitelib}/%{name}/local/local_settings.py.example %{buildroot}%{_sysconfdir}/%{name}/local_settings
test -h %{buildroot}%{python_sitelib}/%{name}/local/local_settings.py && rm -rf %{buildroot}%{python_sitelib}/%{name}/local/local_settings.py
ln -s %{_sysconfdir}/%{name}/local_settings %{buildroot}%{python_sitelib}/%{name}/local/local_settings.py

%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
%find_lang django
%find_lang djangojs
%else
# Handling locale files
# This is adapted from the %%find_lang macro, which cannot be directly
# used since Django locale files are not located in %%{_datadir}
#
# The rest of the packaging guideline still apply -- do not list
# locale files by hand!
(cd $RPM_BUILD_ROOT && find . -name 'django*.po') | %{__sed} -e 's|^.||' |
%{__sed} -e \
   's:\(.*/locale/\)\([^/_]\+\)\(.*\.po$\):%lang(\2) \1\2\3:' \
      >> django.lang
%endif

%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
cat djangojs.lang >> placebo.lang
%endif

touch placebo.lang

# finally put compressed js, css to the right place, and also manifest.json
(cd %{buildroot}%{python_sitelib} && export PYTHONPATH="$( pwd ):$PYTHONPATH" && %{buildroot}%{_datadir}/%{name}/manage.py less)

%files -f placebo.lang
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*.py*

%dir %{python_sitelib}/%name
%{python_sitelib}/%{name}/*
%{python_sitelib}/*.egg-info
#%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/%{name}/local_settings

%dir %attr(0750, apache, root) %{_sysconfdir}/%{name}
%dir %attr(0750, apache, root) %{_localstatedir}/run/placebo
%dir %attr(0755, apache, root) %{_localstatedir}/log/placebo

%changelog
* Thu Jan 09 2014 Xin Xu <xuxin@unitedstack.com> - 0.1.0.a85.g4b6474b-1
- Initial Package
