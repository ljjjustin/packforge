Name:		nginx-lua-dispatcher	
Version:        0.2.0
Release:        16%{?dist}
Summary:	Placebo dispatcher for nginx
Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/dispatcher	
Source0:	dispatcher-%{version}.tar.gz	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch
Requires:  openresty

%description
Nginx placebo distpatcher

%prep
%setup -q -n dispatcher-%{version}

%build

%install
mkdir -p %{buildroot}/%{_sysconfdir}/nginx/conf.d/lua
cp -dpR dispatcher/lua/* %{buildroot}/%{_sysconfdir}/nginx/conf.d/lua

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/nginx/conf.d/lua


%changelog
* Mon Feb 10 2014 Xingchao Yu <xingchao@unitedstack.com> - 1:0.1.0
- Package dispatcher for deployment
