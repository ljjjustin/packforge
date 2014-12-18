Name:	        zabbix	
Version:	    2.4.1.0
Release:	    1%{?dist}
Summary:	    zabbix monitor
Vendor:         wentian@unitedstack.com

Group:	        System Environment/Daemons	
License:	    GPL
URL:	     	http://www.zabbix.com
Source0:	    zabbix-%{version}.tar.gz

BuildRoot:    	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      x86_64 

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	libssh2-devel
BuildRequires:	net-snmp-devel
BuildRequires:	curl-devel
BuildRequires:	unixODBC-devel
BuildRequires:	OpenIPMI-devel
BuildRequires:	java-devel >= 1.6.0

Requires(pre):  gcc
Requires(post): chkconfig	
Provides: Monitor

%description
 Zabbix is the ultimate open source availability and performance monitoring solution. Zabbix offers advanced monitoring, alerting, and visualization features today which are missing in other monitoring systems, even some of the best commercial ones

%package server
Summary:server version of zabbix
Group: System Environment/Daemons
#Requires:            libssh-devel 
Requires:            libssh2-devel 
Requires:            net-snmp-devel
Requires:            curl-devel
Requires:            fping
Requires:            unixODBC-devel 
Requires:            OpenIPMI-devel 
Requires:            libdbi-dbd-mysql      
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service

%description server
Zabbix server common files

%package agent
Summary:             Zabbix Agent
Group:               Applications/Internet
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service

%description agent
The Zabbix client agent, to be installed on monitored systems.


%package proxy
Summary:             Zabbix Proxy
Group:               Applications/Internet
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
Requires:            fping

%description proxy
The Zabbix proxy


%package web-apache
Summary:             Zabbix Web for apache
Group:               Applications/Internet
Requires(pre):       shadow-utils
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
Requires:            httpd
Requires:            php
Requires:            php-mysql
Requires:            php-gd
Requires:            php-xml
Requires:            php-mbstring
Requires:            php-xmlrpc
Requires:            php-bcmath

%description web-apache
The Zabbix web-apache

%package mysql
Summary         : Zabbix server mysql
Group           : Applications/Internet
%description mysql
The Zabbix mysql


%prep
%setup -q

%build
common_flags="
     --enable-dependency-tracking
     --enable-server
     --enable-proxy  
     --enable-agent 
     --enable-ipv6
     --with-net-snmp
     --with-libcurl
     --with-openipmi
     --with-unixodbc
     --with-ldap
     --with-ssh2
     --with-libcurl
     --with-libxml2
     --sysconfdir=%{_sysconfdir}/zabbix
     --datadir=%{_sharedstatedir}
     "
%configure $common_flags --enable-server --with-mysql  --with-cc-opt="%{optflags} $(pcre-config --cflags)"
make %{?_smp_mflags}



%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/scripts
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/zabbix_agentd.d
%{__install} -d %{buildroot}%{_mandir}/man1/
%{__install} -d %{buildroot}%{_mandir}/man8/
%{__install} -d %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -d %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/externalscripts
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/alertscripts
%{__install} -d %{buildroot}%{_datadir}/%{name}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__install} -m 755 misc/init.d/fedora/core/zabbix_agentd   $RPM_BUILD_ROOT%{_initrddir}/zabbix-agent
%{__install} -m 755 misc/init.d/fedora/core/zabbix_server   $RPM_BUILD_ROOT%{_initrddir}/zabbix-server
%{__install} -m 755 misc/init.d/fedora/core/zabbix_server   $RPM_BUILD_ROOT%{_initrddir}/zabbix-proxy
%{__install} -d -m  755      $RPM_BUILD_ROOT%{_datadir}/%{name}-database/mysql/
%{__mv} database/mysql/*     $RPM_BUILD_ROOT%{_datadir}/%{name}-database/mysql/
%{__mv} frontends/php/*      $RPM_BUILD_ROOT%{_datadir}/%{name}


install -m 0755 -p src/zabbix_server/zabbix_server $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_proxy/zabbix_proxy   $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_get/zabbix_get       $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_sender/zabbix_sender $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_agent/zabbix_agent   $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_agent/zabbix_agentd  $RPM_BUILD_ROOT%{_sbindir}/
install -m 0644 -p conf/zabbix_server.conf         $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p conf/zabbix_agent.conf          $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p conf/zabbix_agentd.conf         $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p conf/zabbix_proxy.conf          $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 -p man/zabbix_agentd.man           $RPM_BUILD_ROOT%{_mandir}/man8/zabbix_agentd.8
install -m 0644 -p man/zabbix_server.man           $RPM_BUILD_ROOT%{_mandir}//man8/zabbix_server.8
install -m 0644 -p man/zabbix_proxy.man            $RPM_BUILD_ROOT%{_mandir}/man8/zabbix_proxy.8
install -m 0644 -p man/zabbix_get.man              $RPM_BUILD_ROOT%{_mandir}/man1/zabbix_get.1
install -m 0644 -p man/zabbix_sender.man           $RPM_BUILD_ROOT%{_mandir}/man1/zabbix_sender.1
#cp -ar frontends/php                               $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__rm} -rf $RPM_BUILD_ROOT/usr/bin

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%files server
%defattr(-,root,root,-)
%doc
%attr(0755,zabbixsrv,zabbixsrv) %dir %{_localstatedir}/log/%{name}
%attr(0775,root,zabbixsrv)   %dir %{_localstatedir}/run/%{name}
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_server.conf
%{_sbindir}/zabbix_sender
%{_sbindir}/zabbix_server
%{_sbindir}/zabbix_get

%{_initrddir}/zabbix-server

%config(noreplace) %{_sysconfdir}/%{name}/externalscripts
%config(noreplace) %{_sysconfdir}/%{name}/alertscripts

%{_mandir}/man8/zabbix_server.8*
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*

%files agent
%defattr(-,root,root,-)
%doc
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/%{name}
%attr(0775,root,zabbix) %dir %{_localstatedir}/run/%{name}
%attr(0775,root,zabbix) %dir %{_sysconfdir}/%{name}/zabbix_agentd.d
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_agent.conf
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_agentd.conf
%{_sbindir}/zabbix_sender
%{_sbindir}/zabbix_agent
%{_sbindir}/zabbix_agentd
%{_sbindir}/zabbix_get

%{_initrddir}/zabbix-agent

%{_mandir}/man8/zabbix_agentd.8*
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*


%files proxy
%defattr(-,root,root,-)
%doc
%attr(0755,zabbixsrv,zabbixsrv) %dir %{_localstatedir}/log/%{name}
%attr(0775,root,zabbixsrv)   %dir %{_localstatedir}/run/%{name}
%config(noreplace)  %{_sysconfdir}/%{name}/zabbix_proxy.conf
%{_sbindir}/zabbix_proxy
%{_initrddir}/zabbix-proxy

%{_mandir}/man8/zabbix_proxy.8*
%config(noreplace) %{_sysconfdir}/%{name}/externalscripts
%config(noreplace) %{_sysconfdir}/%{name}/alertscripts

%files web-apache
%defattr(-,root,root,-)
%config(noreplace) %{_datadir}/%{name}/*

%files mysql
%defattr(-,root,root,-)
%config(noreplace) %{_datadir}/%{name}-database/mysql/schema.sql
%config(noreplace) %{_datadir}/%{name}-database/mysql/images.sql
%config(noreplace) %{_datadir}/%{name}-database/mysql/data.sql


%post server
if [ $1 -eq 1 ]; then
/sbin/chkconfig zabbix-server on
/sbin/service zabbix-server start
fi
chown root:zabbix /bin/netstat
chmod 4755 /bin/netstat
chown root:zabbix $(which fping)
chmod 4755 $(which fping)

%post agent
if [ $1 -eq 1 ]; then
sed -i "s@Hostname=Zabbix server@Hostname=$HOSTNAME@g" /etc/zabbix/zabbix_agentd.conf
getent group zabbix >/dev/null || groupadd -r  zabbix
getent passwd zabbix >/dev/null || useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s   /sbin/nologin  -c "zabbix user" zabbix
/sbin/chkconfig zabbix-agent on
/sbin/service zabbix-agent start
chown root:zabbix /bin/netstat
chmod 4755 /bin/netstat
fi

%post proxy
if [ $1 -eq 1 ]; then
/sbin/chkconfig zabbix-proxy on
fi


%post web-apache
chown -R apache.apache  /usr/share/zabbix/zabbix
sed -i "s/;date.timezone =/date.timezone = Asia\/Shanghai/g"        /etc/php.ini
sed -i "s#max_execution_time = 30#max_execution_time = 300#g"       /etc/php.ini
sed -i "s#post_max_size = 8M#post_max_size = 32M#g"                 /etc/php.ini
sed -i "s#max_input_time = 60#max_input_time = 300#g"               /etc/php.ini
sed -i "s#memory_limit = 128M#memory_limit = 128M#g"                /etc/php.ini
sed -i "/;mbstring.func_overload = 0/ambstring.func_overload = 2\n" /etc/php.ini
#config apache
sed -i "s/DirectoryIndex index.html index.html.var/DirectoryIndex index.php index.html index.html.var/g" /etc/httpd/conf/httpd.conf
sed -i "s/ServerTokens OS/ServerTokens Prod/g"  /etc/httpd/conf/httpd.conf


%pre server
#add zabbix to services
grep zabbix /etc/services
[ "$?" != 0 ] && cat >> /etc/services <<EOF
zabbix-agent    10050/tcp               #Zabbix Agent
zabbix-agent    10050/udp               #Zabbix Agent 
zabbix-trapper  10051/tcp               #Zabbix Trapper 
zabbix-trapper  10051/udp               #Zabbix Trapper
EOF
# Add the "zabbix" user
getent group zabbixsrv >/dev/null || groupadd -r  zabbixsrv
getent passwd zabbixsrv >/dev/null || useradd -r -g zabbixsrv -d %{_sharedstatedir}/zabbixsrv -s   /sbin/nologin  -c "zabbix user" zabbixsrv

%pre agent
#add zabbix to services
grep zabbix /etc/services
[ "$?" != 0 ] && cat >> /etc/services <<EOF
zabbix-agent    10050/tcp               #Zabbix Agent
zabbix-agent    10050/udp               #Zabbix Agent 
zabbix-trapper  10051/tcp               #Zabbix Trapper 
zabbix-trapper  10051/udp               #Zabbix Trapper
EOF
# Add the "zabbix" user
getent group zabbix >/dev/null || groupadd -r  zabbix
getent passwd zabbix >/dev/null || useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s   /sbin/nologin  -c "zabbix user" zabbix


%preun server
if [ "$1" = 0 ]
then
  /sbin/service zabbix_server stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix_server
fi

%preun proxy
if [ "$1" = 0 ]
then
  /sbin/service zabbix_proxy stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix_proxy
fi

%preun agent
if [ "$1" = 0 ]
then
  /sbin/service zabbix_agentd stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix_agentd
fi


%changelog
* Mon Oct 07 2013 Wentian <wentian@gmail.com> 2.4.1 
- update to 2.4.1
