Name:		zabbix_plugin
Version:        0.0.26
Release:	138%{?dist}
Summary:	UnitedStack zabbix plugin for install Master Node

Group:		Applications/System
License:	ASL 2.0
URL:	        http://git.ustack.com/ustack/sunfire
Source0:	zabbix-plugin-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch
Requires: puppet >= 2.7.12
#Requires: rubygem-highline

%description
Zabbix plugin to get information from system

%prep
%setup -q -n zabbix-plugin-%{version}

%build

%install
mkdir -p %{buildroot}/%{_sysconfdir}/zabbix/zabbix_agentd.d/
mkdir -p %{buildroot}/%{_bindir}/
cp -dpR plugin/* %{buildroot}%{_sysconfdir}/zabbix/zabbix_agentd.d/
cp -dpR scripts/* %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,zabbix_agent,root,-)
%{_sysconfdir}/zabbix/zabbix_agentd.d
%{_bindir}/zabbix-*


%changelog
* Wed Apr 23 2014 Wentian Jiang <wentian@unitedstack.com> - 1:0.1.0
- Package zabbix_agent for deployment
