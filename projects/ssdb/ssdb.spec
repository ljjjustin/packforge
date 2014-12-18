%global  ssdb_confdir       %{_sysconfdir}/%{name}
%global  ssdb_builddir       %{_builddir}/%{name}-%{version}

Name:           ssdb
License:        GPL-2.0+
Group:          System/Base
Version:        1.700.0.2
Release:        27%{?dist}
Summary:        A LevelDB Wrapper
Source0:        ssdb-%{version}.tar.gz
Source1:        %{name}.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
ssdb is a LevelDB Wrapper

Authors:
--------
    Xin Xu <xuxin@unitedstack.com>

%prep
%setup -n ssdb-%{version}

%build
#sed -i s#r\ tools/\\*\ \${PREFIX}#a\ tools/\ \${PREFIX}/tools# Makefile
./build.sh
make all

%install
#make install PREFIX=${_topdir}/build

install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-server

install -p -d -m 0755 %{buildroot}%{ssdb_confdir}
install -p -d -m 0755 %{buildroot}%{_sbindir}
install -p -d -m 0755 %{buildroot}%{_datadir}/%{name}/api
install -p -d -m 0755 %{buildroot}%{_datadir}/%{name}/tools
install -p -d -m 0755 %{buildroot}%{_datadir}/%{name}/deps
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}
install -p -d -m 0755 %{buildroot}%{python_sitelib}

install -m 644 %{ssdb_builddir}/ssdb.conf %{buildroot}%{ssdb_confdir}/
install -m 644 %{ssdb_builddir}/ssdb_slave.conf %{buildroot}%{ssdb_confdir}/
install -m 755 %{ssdb_builddir}/ssdb-server %{buildroot}%{_sbindir}/
install -m 755 %{ssdb_builddir}/tools/ssdb-repair %{buildroot}%{_sbindir}/
install -m 755 %{ssdb_builddir}/tools/ssdb-cli %{buildroot}%{_sbindir}/
install -m 755 %{ssdb_builddir}/tools/ssdb-bench %{buildroot}%{_sbindir}/
install -m 755 %{ssdb_builddir}/tools/ssdb-dump %{buildroot}%{_sbindir}/

cp -a %{ssdb_builddir}/api %{buildroot}%{_datadir}/%{name}
cp -a %{ssdb_builddir}/tools %{buildroot}%{_datadir}/%{name}
cp -a %{ssdb_builddir}/deps  %{buildroot}%{_datadir}/%{name}
cp -a %{ssdb_builddir}/api/python/* %{buildroot}%{python_sitelib}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%config %{ssdb_confdir}/ssdb.conf
%config %{ssdb_confdir}/ssdb_slave.conf
%{_sbindir}/ssdb-server
%{_sbindir}/ssdb-repair
%{_sbindir}/ssdb-cli
%{_sbindir}/ssdb-bench
%{_sbindir}/ssdb-dump
%{python_sitelib}/SSDB.py*
%{python_sitelib}/demo.py*
%dir %{_sharedstatedir}/%{name}
/usr/share/%{name}/*
%{_initrddir}/%{name}-server

%changelog
* Tue Aug 13 2014 xingchao@unitedstack.com
- Initial Package
* Tue Dec 17 2013 xuxin@unitedstack.com
- Initial Package
