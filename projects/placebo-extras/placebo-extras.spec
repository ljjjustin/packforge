Name:		placebo_extras	
Version:        0.0.7
Release:	19%{?dist}
Summary:	UnitedStack Extra files for Dashboard

Group:		Applications/System
License:	ASL 2.0	
URL:	        http://git.ustack.com/ustack/placebo_extras	
Source0:	placebo-extras-%{version}.tar.gz	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:    noarch

%description
Collections of Extra file for placebo

%prep
%setup -q -n placebo-extras-%{version}

%build

%install
mkdir -p %{buildroot}/opt/placebo_extras
cp -dpR * %{buildroot}/opt/placebo_extras

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/placebo_extras


%changelog
* Wed Dec 31 2014 Xingchao Yu <xingchao@unitedstack.com> - 2013.1.1-1
- Package placebo_extras for deployment
