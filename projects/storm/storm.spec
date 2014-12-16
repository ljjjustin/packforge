Name:		storm	
Version:        0.2.4
Release:	1%{?dist}
Summary:	UnitedStack storm for install Master Node

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/storm	
Source0:	storm-%{version}.tar.gz	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch
Requires: puppet >= 2.7.12
Requires: sunfire

%description
Collections of UnitedStack Master Node Configuration Modules

%prep
%setup -q -n storm-%{version}

%build

%install
rm README.md
mkdir -p %{buildroot}/%{_sysconfdir}/puppet/modules/production
cp -dpR * %{buildroot}/%{_sysconfdir}/puppet/modules/production

%clean
rm -rf %{buildroot}

%files
%defattr(-,puppet,root,-)
%{_sysconfdir}/puppet/modules/production


%changelog
* Wed Jul 31 2013 Xingchao Yu <xingchao@unitedstack.com> - 2013.1.1-1
- Package storm for deployment
