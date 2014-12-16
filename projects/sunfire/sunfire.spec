Name:		sunfire	
Version:        0.4.2
Release:	4%{?dist}
Summary:	UnitedStack sunfire for install Master Node

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/sunfire	
Source0:	sunfire-%{version}.tar.gz	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch
Requires: puppet >= 2.7.12
#Requires: rubygem-highline

%description
Collections of UnitedStack Master Node Configuration Modules

%prep
%setup -q -n sunfire-%{version}

%build

%install
rm build_modules release README.md

#mkdir -p %{buildroot}/%{_datadir}/%{name}
#cp -dpR * %{buildroot}/%{_datadir}/%{name}

mkdir -p %{buildroot}/%{_sysconfdir}/puppet/modules/production
cp -dpR * %{buildroot}/%{_sysconfdir}/puppet/modules/production
#ln -sf %{_datadir}/%{name}/*  %{buildroot}/%{_sysconfdir}/puppet/modules/

%clean
rm -rf %{buildroot}

%files
%defattr(-,puppet,root,-)
#%{_datadir}/%{name}
%{_sysconfdir}/puppet/modules/production


%changelog
* Fri Jun 12 2013 Xingchao Yu <xingchao@unitedstack.com> - 1:0.1.0
- Package sunfire for deployment
