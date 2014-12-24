%define USE_LIBNSS 1
%define USE_FIPSCHECK 1
%define USE_LIBCAP_NG 1
%define USE_NM 1
%define USE_LABELED_IPSEC 1
%define nss_version 3.14.3
%define fipscheck_version 1.2.0-7
#737975, 693432
%define USE_CRL_FECTCHING 1

Summary: IPSEC implementation with IKEv1 and IKEv2 keying protocols
Name: openswan
Version: 2.6.32
Release: 28%{?dist}

License: GPLv2+
Url: http://www.openswan.org/
Source: https://download.openswan.org/openswan/old/openswan-2.6/openswan-%{version}.tar.gz
Source2: ipsec.conf
Source3: README.x509
# rhbz#1002633 blacklist for FIPS mode
Source4: openswan-prelink.conf

Patch1: openswan-2.6-relpath.patch
Patch2: openswan-ipsec-help-524146-509318.patch
Patch3: openswan-658253-658121-2.patch
Patch4: openswan-668785.patch
Patch5: openswan-658253-658121-3.patch
Patch6: openswan-621790.patch
Patch7: openswan-658253-658121.patch
Patch8: openswan-labeled-ipsec.patch
Patch9: openswan-681974-683604.patch
Patch10: openswan-703473.patch
Patch11: openswan-703985.patch
Patch12: openswan-704548.patch
Patch13: openswan-711975.patch
Patch14: openswan-cisco-738385.patch
Patch15: openswan-592265-737973.patch
Patch16: openswan-742632.patch 
Patch17: openswan-742070.patch
Patch18: openswan-cve-2011-4073.patch
Patch19: openswan-749605-609343.patch
Patch20: openswan-768162.patch
Patch21: openswan-771470.patch
Patch22: openswan-ikev2-fixes.patch
Patch23: openswan-ikev2-additional-fixes.patch
Patch24: openswan-ikev2-795842-795850.patch
Patch25: openswan-ikev2-ts.patch
Patch26: openswan-768442.patch
Patch27: openswan-771467.patch
#Patch28: openswan-831669.patch
Patch28: openswan-831669-mb_zig.patch
Patch29: openswan-831676.patch
Patch30: openswan-831676-loopback.patch
Patch31: openswan-846797.patch

Patch33: openswan-880004-libreswan-ikefrag-backport.patch
Patch34: openswan-libreswan-backport-nat_keepalive.patch
Patch35: openswan-libreswan-backport-initial-contact.patch
Patch36: openswan-libreswan-backport-ikeping.patch
Patch37: openswan-771612.patch
Patch38: openswan-libreswan-backport-916743.patch
Patch39: openswan-libreswan-backport-960235-atodn.patch
Patch40: openswan-libreswan-backport-960235-no_oe.patch
Patch41: openswan-libreswan-backport-963833-do_aes.patch
Patch42: openswan-libreswan-backport-963833-do_3des.patch
Patch43: openswan-841325.patch
Patch44: openswan-957400.patch
Patch45: openswan-libreswan-backport-960235-asn1_cleanup.patch
Patch46: openswan-libreswan-backport-963833-get_rnd_bytes.patch
Patch47: openswan-libreswan-backport-960235-x509dn.patch
Patch48: openswan-libreswan-backport-960171.patch
Patch49: openswan-libreswan-backport-958969.patch
Patch50: openswan-848132.patch
Patch51: openswan-868986.patch
Patch52: openswan-747966.patch
Patch53: openswan-libreswan-backport-954249.patch
Patch54: openswan-libreswan-backport-881914.patch
Patch55: openswan-libreswan-backport-985596.patch
Patch56: openswan-libreswan-backport-975550.patch
Patch57: openswan-libreswan-backport-994240.patch
Patch58: openswan-libreswan-backport-1002312.patch
Patch59: openswan-libreswan-backport-fips.patch
Patch60: openstack_unitedstack.patch

Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gmp-devel bison flex xmlto bind-devel
%if %{USE_LIBNSS}
BuildRequires: nss-devel >= %{nss_version}
%endif
%if %{USE_LABELED_IPSEC}
BuildRequires: libselinux-devel
%endif
Requires(post): coreutils bash
Requires(preun): initscripts chkconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%if %{USE_FIPSCHECK}
BuildRequires: fipscheck-devel >= %{fipscheck_version}
%endif

%if %{USE_LIBCAP_NG}
BuildRequires: libcap-ng-devel
%endif

%if %{USE_CRL_FECTCHING}
BuildRequires: openldap-devel curl-devel
Requires: curl openldap
%endif

Provides: ipsec-userland = %{version}-%{release}
#unless kernel with NETKEY supplies this capability we cannot do this
#Requires: ipsec-kernel

%package doc
Summary: Full documentation of Openswan IPSEC implementation
Group: System Environment/Daemons

%description
Openswan is a free implementation of IPsec & IKE for Linux.  IPsec is
the Internet Protocol Security and uses strong cryptography to provide
both authentication and encryption services.  These services allow you
to build secure tunnels through untrusted networks.  Everything passing
through the untrusted net is encrypted by the ipsec gateway machine and
decrypted by the gateway at the other end of the tunnel.  The resulting
tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
Openswan. It supports the NETKEY/XFRM IPsec kernel stack that exists
in the default Linux kernel.

Openswan 2.6.x also supports IKEv2 (RFC4306)

%description doc
This package contains extensive documentation of the Openswan IPSEC
system.

%prep
%setup -q -n openswan-%{version}
install -m 644 %{SOURCE3} doc/README.x509
find doc/examples -type f -print0 | xargs -0 chmod a-x
find doc -name .gitignore -print0 | xargs -0 rm -v

%patch1 -p1 -b .relpath
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1

# pwouters backpors from libreswan
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60
%build
%{__make} \
  USERCOMPILE="-g -DGCC_LINT %{optflags} -fPIE -pie -fno-strict-aliasing -Wformat -Wformat-nonliteral -Wformat-security -Wunused-variable" \
  USERLINK="-g -pie -Wl,-z,relro -Wl,-z,now" \
  INC_USRLOCAL=%{_prefix} \
  FINALLIBDIR=%{_libexecdir}/ipsec \
  IPSEC_LIBDIR="${IPSEC_LIBDIR-/usr/libexec/ipsec}" \
  MANTREE=%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
%if %{USE_LIBNSS}
  USE_LIBNSS=true \
%endif
%if %{USE_FIPSCHECK}
  USE_FIPSCHECK=true \
  FIPSPRODUCTCHECK=/etc/system-fips \
%endif
%if %{USE_LIBCAP_NG}
  USE_LIBCAP_NG=true \
%endif
%if %{USE_NM}
  USE_NM=true \
%endif
%if %{USE_LABELED_IPSEC}
  USE_LABELED_IPSEC=true \
%endif
%if %{USE_CRL_FECTCHING}
  USE_LDAP=true \
  USE_LIBCURL=true \
  HAVE_THREADS=true \
%endif
  programs
FS=$(pwd)

%if %{USE_FIPSCHECK}
# Add generation of HMAC checksums of the final stripped binaries
%define swanexec $RPM_BUILD_ROOT%{_libexecdir}/ipsec
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
  fipshmac $RPM_BUILD_ROOT%{_libexecdir}/ipsec/* \
  fipshmac $RPM_BUILD_ROOT%{_sbindir}/ipsec \
%{nil}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} \
  DESTDIR=$RPM_BUILD_ROOT \
  INC_USRLOCAL=%{_prefix} \
  FINALLIBDIR=%{_libexecdir}/ipsec \
  IPSEC_LIBDIR="${IPSEC_LIBDIR-/usr/libexec/ipsec}" \
  MANTREE=$RPM_BUILD_ROOT%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
  install
FS=$(pwd)
rm -rf $RPM_BUILD_ROOT/usr/share/doc/openswan

# ipsec and setup both installed by default - they are identical
rm -f $RPM_BUILD_ROOT/etc/rc.d/init.d/setup
rm -f $RPM_BUILD_ROOT/usr/share/man/man3/*
install -d -m 0700 $RPM_BUILD_ROOT%{_localstatedir}/run/pluto
%if %{USE_FIPSCHECK}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/
install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/openswan-fips.conf
%endif
install -d $RPM_BUILD_ROOT%{_sbindir}
find $RPM_BUILD_ROOT/etc/ipsec.d -type f -exec chmod 644 {} \;

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 600 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/ipsec.conf

sed -i -e 's#/usr/lib/#%{_libexecdir}/#g' $RPM_BUILD_ROOT%{_initrddir}/ipsec

echo "include /etc/ipsec.d/*.secrets" > $RPM_BUILD_ROOT%{_sysconfdir}/ipsec.secrets

chmod a-x $RPM_BUILD_ROOT%{_mandir}/*/*

# nuke duplicate docs to save space.  this leaves html and ps
rm -f doc/HOWTO.pdf doc/HOWTO.txt

rm -fr $RPM_BUILD_ROOT/etc/rc.d/rc*

rm -fr $RPM_BUILD_ROOT%{_sysconfdir}/ipsec.d/examples

# only used with KLIPS/MAST, and plutomain.c does not check its .hmac
# in FIPS mode
rm -rf $RPM_BUILD_ROOT%{_libexecdir}/ipsec/policy


%clean
rm -rf $RPM_BUILD_ROOT

%files doc
%defattr(-,root,root)
%doc doc/README.* doc/CHANGES.* doc/CREDITS.* doc/2.6.known-issues
%doc doc/examples doc/std doc/quickstarts doc/*.html

%files 
%defattr(-,root,root)
%doc BUGS CHANGES COPYING CREDITS README LICENSE
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ipsec.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ipsec.secrets
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ipsec.d/policies/*
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/policies
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d
%{_initrddir}/ipsec
%{_sbindir}/ipsec
%dir %{_libexecdir}/ipsec
%{_libexecdir}/ipsec/*
%{_mandir}/*/*.gz
%{_localstatedir}/run/pluto
%if %{USE_FIPSCHECK}
%{_sbindir}/.ipsec.hmac
%{_libexecdir}/ipsec/.*.hmac
%endif

%if %{USE_FIPSCHECK}
# We own the directory so we don't have to require prelink
%attr(0755,root,root) %dir %{_sysconfdir}/prelink.conf.d/
%{_sysconfdir}/prelink.conf.d/openswan-fips.conf
%endif

%preun
if [ $1 = 0 ]; then
	/sbin/service ipsec stop || :
	/sbin/chkconfig --del ipsec
fi

%postun
if [ $1 -ge 1 ] ; then
	/sbin/service ipsec condrestart 2>&1 > /dev/null || :
fi

%post
chkconfig --add ipsec || :

%changelog
* Thu Oct 17 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-27
- Resolves: rhbz#1020322 openswan cannot start if FIPS misconfigured

* Wed Oct 09 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-26
- Resolves: rhbz#1017371  Verification of openswan package fails

* Wed Oct 02 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-25
- Resolves: rhbz#841325 [proxy id for_1_0_0_2_6_3_3]
  Modified to use dracut-fips now

* Thu Sep 12 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-24
- Resolves: rhbz#1002633 API change for versioned FIPS hmac files

* Tue Sep 03 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-23
- Resolves: rhbz#998587 underspecific build requires (of nss)
- Resolves: rhbz#1002312 IKEv2 skeyseed calculation only succeeds because of unspecified compiler behaviour
- Resolves: rhbz#1002633 openswan needs -fips subpackage that would provide the FIPS hmac files

* Fri Aug 23 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-22
- Resolves: rhbz#994240  NAT-T transport bug affects Openswan+L2TP connections with NATed clients

* Wed Aug 14 2013 Paul Wouters <pwouters@redhat.com> - 2.6.32-21
- Resolves: rhbz#975550 ikev2 md5 hash results in incorrect policy
- Resolves: rhbz#985596 openswan does not allow SHA2 auth algorithms under FIPS mode 
- Resolves: rhbz#881914 openswan doesn't support SHA2 certificates
- Resolves: rhbz#954249 barf and look should not cause loading of kernel modules
- Resolves: rhbz#954249 barf and look should not cause loading of kernel modules
- Resolves: rhbz#960235 CVE-2013-2053: remote buffer overflow in atodn()
- Resolves: rhbz#963833 Abort pluto on crypto failure to prevent plaintext / nonce leak
- Resolves: rhbz#771612 ipsec barf should not grep sparse file
- Resolves: rhbz#841325 leftmodecfgclient=no causes rekey failure [Avesh]
- Resolves: rhbz#848132 dpdaction=restart can cause full phase1 timeout after DPD [Avesh]
- Resolves: rhbz#880004 Backported libreswan IKE fragmentation support 
- Resolves: rhbz#908476 Backported libreswan INITIAL-CONTACT Notify support
- Resolves: rhbz#796683 Backported libreswan USERCOMPILE with -fno-strict-aliasing
- Resolves: rhbz#959568 Backported libreswan nat_keepalive=yes|no (default yes) option
- Resolves: rhbz#916743 Backported libreswan control transmission delay timing
- Resolves: rhbz#959566 Backported libreswan ikeping compile warnings
- Resolves: rhbz#957400 Openswan did not load aesni_intel kernel module
- Resolves: rhbz#960171 Initial loading of CRL always fails on pluto startup [Matt Rogers]
- Resolves: rhbz#958969 Crl signature verification failure in when input signature is stripped of all leading zeros
- Resolves: rhbz#868986 Fix for RDN values containing a comma [Matt Rogers]
- Resolves: rhbz#747966 Missing else keyword

*Fri Aug 24 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-19
Resolves: #846797

*Fri Jul 6 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-18
Resolves: #831676 : fixing loopback issue regression

*Fri Jun 22 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-17
Resolves: #831669
Resolves: #831676

*Mon Apr 30 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-16
Resolves: #771467

*Fri Apr 20 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-15
Resolves: #768442

*Wed Apr 11 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-14
Resolves: #771461
Resolves: #771472

* Fri Mar 2 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-13
Resolves: #795842
Resolves: #795850

* Thu Feb 16 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-12
Resolves: #771457
Resolves: #771460
Resolves: #771463

* Tue Feb 14 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-11
Resolves: #771464
Resolves: #771465
Resolves: #771466
Resolves: #771467
Resolves: #771473
Resolves: #771475

* Tue Jan 31 2012 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-10
Resolves: #768162
Resolves: #771470

* Fri Oct 28 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-9
Resolves: #748970 cve-2011-4073 updated upstream patch
Resolves: #749605

* Tue Oct 25 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-8
Resolves: #748970 cve-2011-4073

* Mon Oct 3 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-7
Resolves: #737973
Resolves: #737975
Resolves: #737976
Resolves: #738385
Resolves: #742632
Resolves: #742070

* Fri Jun 17 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-6
Resolves: #711975

* Fri Jun 3 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-5
Resolves: #703985
Resolves: #703473
Resolves: #704548

* Thu Mar 17 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-4
Resolves: #681974 
Resolves: #683604

* Wed Mar 2 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-3
Resolves: 235720

* Mon Feb 21 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-2
Resolves: 235720

* Wed Jan 12 2011 Avesh Agarwal <avagarwa@redhat.com> - 2.6.32-1
Resolves: 642722
Resolves: 642724
Resolves: 646718
Resolves: 628879
Resolves: 621790
Resolves: 668785
Resolves: 658253
Resolves: 658121
 
* Wed Oct 6 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-9
Resolves: #635060 CVE-2010-3302 CVE-2010-3308 
                  CVE-2010-2752 CVE-2010-3753

* Wed Jul 21 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-8
Resolves: #616910

* Wed Jun 30 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-7
Resolves: #614250

* Wed Jun 30 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-6
Resolves: #600174
Resolves: #600167

* Fri Jun 18 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-5
Resolves: #529260

* Mon Jun 14 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-4
Resolves: #579629
Resolves: #584224
Resolves: #586420
Resolves: #592630
Resolves: #594767
Resolves: #579747
Resolves: #587669

* Tue Mar 23 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-3
Resolves: #568355 Implementation of new Diffie-Hellman groups 
                  described in RFC 5114
Resolves: #568493 Pluto's child process can not add routes
Resolves: #568648 some subcommand doesn't work
Resolves: #568652 the transport mode doesn't work
Resolves: #574833 Openswan client can not interop with 
                  Cisco VPN servers
Resolves: #574839 ImplicitDSOLinking
Resolves: #574841 Openswan Implementation issue related to 
                  hardcoded length of hash algorithms

* Mon Feb 8 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-2
- Modified summary in spec file
- Replaced buildroot with RPM_BUILD_ROOT in spec file
- Included html files in the doc package
- Patch for disabling openswan startup at the system
  boot by default

* Fri Jan 15 2010 Avesh Agarwal <avagarwa@redhat.com> - 2.6.24-1
- New upstream release
- Cisco interop patches
- Improved init script
- Fix to allow ";" in the ike/esp parameters
- Fix to unset IKEv2 Critical flag for payloads defined in RFC 4306
- Fix to Zeroize ISAKMP and IPsec SA's when in FIPS mode
- Fix to the issue where Some programs were installed
  twice causing .old files
- lwdns.req.log moved from /var/tmp/ to /var/run/pluto/ .
  This is to avoid an SElinux AVC Denial
- Fix for the issueo where ipsec help shows the list twice
- Fix for compile time warnings

* Wed Sep 09 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.23-1
- New upstream release
- Supports smartcards now
- Supports PSK with NSS
- Supports libcap-ng for lowering capabilities of pluto process 
- Updated README.nss

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.22-1
- New upstream release
- Added support for using PSK with NSS
- Fixed several warnings and undid unnecessary debug messages
- Updated README.nss with an example configuration
- Moved README.nss to openswan/doc/
- Improved FIPS integrity check functionality

* Mon Jul 06 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.21-5
- Added support for using PSK with NSS
- Fixed several warnings and undid unnecessary comments
- Updated README.nss with an example configuration
- Fixed Openswan ASN.1 parser vulnerability (CVE-2009-2185)

* Tue Apr 14 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.21-4
- Updated the Openswan-NSS porting to enable nss and fipscheck by default
- fipscheck requires fipscheck-devel library

* Tue Apr 14 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.21-3
- Updated the Openswan-NSS porting to enable nss by default
- The patch includes README.nss for information about NSS usage

* Mon Apr 13 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.21-2
- Applied patch to support NSS, currently disabled due to
  dependency on rh bz #491693
- The patch also supports fips check integrity 
   (requires fipscheck-devel library)

* Mon Mar 30 2009 Avesh Agarwal <avagarwa@redhat.com> - 2.6.21-1
- new upstream release
- Fix for CVE-2009-0790 DPD crasher
- Fix remaining SADB_EXT_MAX -> K_SADB_EXT_MAX entries
- Fix ipsec setup --status not showing amount of tunnels with netkey

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 25 2008 Avesh Agarwal <avagarwa@redhat.com> - 2.6.19-1
- new upstream release

* Mon Oct 13 2008 Avesh Agarwal <avagarwa@redhat.com> - 2.6.18-2
- Addressed some issues related to buzilla 447419
- Added xmlto and bind-devel to BuildRequires 
- Removed the patch openswan-2.6-noxmlto.patch
- Removed the command "rm -rf programs/readwriteconf" from the spec file
  as readwriteconf is used with "make check" for debugging purposes.
- Removed USE_LWRES=false from the spec file as it has been 
  obsolete in upstream (using bind-devel instead)	

* Mon Oct 06 2008 Avesh Agarwal <avagarwa@redhat.com> - 2.6.18-1
- new upstream release
- modified default ipsec.conf to address rhbz#463931

* Fri Sep 12 2008 Avesh Agarwal <avagarwa@redhat.com> - 2.6.16-2
- added initscript patch to prevent openswan service start by default

* Tue Sep 09 2008 Avesh Agarwal <avagarwa@redhat.com> - 2.6.16-1
- new upstream release

* Sat Jul 05 2008 Steve Grubb <sgrubb@redhat.com> - 2.6.15-1
- new upstream release

* Fri Jun 06 2008 Steve Grubb <sgrubb@redhat.com> - 2.6.14-1
- new upstream release

* Tue Mar 18 2008 Steve Conklin <sconklin@redhat.com> - 2.6.09-2
- removing patch - using upstream init script as is

* Wed Mar 12 2008 Steve Conklin <sconklin@redhat.com> - 2.6.08-1
- Moved to latest upstream
- Replaced the init script source file with a patch to the upstream one
-    (no functional changes to the init script)
- Added protostack=netkey to ipsec.conf
- New patch to include definition of HOST_NAME_MAX

* Mon Feb 11 2008 Steve Conklin <sconklin@redhat.com> - 2.6.07-1
- Moved to latest upstream

* Thu Feb  7 2008 Steve Conklin <sconklin@redhat.com> - 2.6.05-1
- Removed check for selinux enforcing mode in verify script
- Moved to latest upstream

* Mon Jan 28 2008 Steve Conklin <sconklin@redhat.com> - 2.6.04-1
- Move to new upstream source

* Thu Jan 24 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-9
- Added af_key module load to init script
- Removed spurious warning about interfaces=

* Mon Jan 21 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-8
Related: rhbz#235224
- rpmdiff spotted these:
- Cleaned out unused man page
- patch error in barf script

* Fri Jan 18 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-7
- Addressed the last set of small changes for package review

* Thu Jan 17 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-6
- Moved everything else out of /usr/lib
- Added tmraz's patch to remove extra slashes in makefile
- Removed macros from changelog entries

* Thu Jan 17 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-5
- Removed userland macros from spec file

* Thu Jan 17 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-4
- Removed use of xmlto and the BuildRequires
- moved scripts from /usr/lib to /usr/libexec
- removed man3 pages for libopenswan functions (we don't deliver)

* Wed Jan 16 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-3
- Removed _smp_mflags macro from from the spec file build section
- Added BuildRequires for xmlto
- Changed License from GPL to GPL+
- removed klips ifdefs from spec file
- Added patch to move example configs to doc dir
- Added a patch to make the link to init script relative, 
  for chroot environments

* Fri Jan 11 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-2
- Removed copy of file that no longer exists

* Fri Jan 11 2008 Steve Conklin <sconklin@redhat.com> - 2.6.03-1
- Latest upstream tarball, includes fixes

* Thu Jan 10 2008 Steve Conklin <sconklin@redhat.com> - 2.6.02-2
- Rebase to 2.6.02, add initial ikev2 support

* Mon Sep 17 2007 Steve Conklin <sconklin@redhat.com> - 2.4.9-2
- Forgot changelog on last entry

* Mon Sep 17 2007 Steve Conklin <sconklin@redhat.com> - 2.4.9-1
- sync to upstream latest

* Tue Mar 20 2007 Florian La Roche <laroche@redhat.com> - 2.4.7-3
- do not use epoch macro, it is unset

* Wed Feb 28 2007 Harald Hoyer <harald@redhat.com> - 2.4.7-2
- specfile review

* Fri Jan 26 2007 Harald Hoyer <harald@redhat.com> - 2.4.7-1
- removed key generation from install phase
- version 2.4.7

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4.5-2.1
- rebuild

* Wed May 17 2006 Harald Hoyer <harald@redhat.com> - 2.4.5-2
- fixed typo (bug #191930)

* Fri May 05 2006 Harald Hoyer <harald@redhat.com> - 2.4.5-1
- version 2.4.5

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.4-1.1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.4-1.1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Harald Hoyer <harald@redhat.com> - 2.4.4-1.1
- version 2.4.4
- fixes NISCC Vulnerability Advisory 273756/NISCC/ISAKMP
- fixes NISCC Advisory 3756/NISCC/ISAKMP

* Wed Nov 02 2005 Harald Hoyer <harald@redhat.com> - 2.4.2-0.dr5.1
- version 2.4.2dr5

* Tue Oct 25 2005 Harald Hoyer <harald@redhat.com> - 2.4.2-0.dr1.1
- version 2.4.2dr1

* Tue Sep 13 2005 Harald Hoyer <harald@redhat.com> - 2.4.0-1
- version 2.4.0

* Wed Aug 31 2005 Harald Hoyer <harald@redhat.com> - 2.4.0-0.rc4.1
- new version

* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- remove sysv startup links to build with current rpm

* Thu May 12 2005 Harald Hoyer <harald@redhat.com> - 2.3.1-3
- added openswan-2.3.1-nat_t_aggr.patch
- added openswan-2.3.1-iproute2.patch
- added openswan-2.3.1-cisco.patch
- NAT-T/XAUTH/AGGR-MODE is now possible with a Cisco VPN 3000

* Wed Apr 27 2005 Harald Hoyer <harald@redhat.com> - 2.3.1-2
- added Requires(post) of coreutils bash (bug 155699)
- added Requires(preun) initscripts chkconfig

* Wed Apr 13 2005 Harald Hoyer <harald@redhat.com> - 2.3.1-1
- version 2.3.1

* Mon Apr  4 2005 Jeremy Katz <katzj@redhat.com> - 2.3.0-6
- remove some duplicate copies of the docs

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Mon Feb 21 2005 Harald Hoyer <harald@redhat.com> - 2.3.0-4
- fixed bug rh#149164

* Fri Feb 18 2005 Harald Hoyer <harald@redhat.com> - 2.3.0-3
- patched code to compile with gcc4

* Fri Jan 14 2005 Harald Hoyer <harald@redhat.com> - 2.3.0-2
- Do not enable the initscript per default

* Tue Jan 11 2005 Harald Hoyer <harald@redhat.com> - 2.3.0-1
- version 2.3.0
- reimported specfile
- PIEd openswan
- cleaned up initial config files and added include directives
  for easy config drop in

* Wed Jan  5 2005 Paul Wouters <paul@xelerance.com>
- Updated for x86_64 and klips on 2.6

* Tue Nov 2 2004 Dan Walsh <dwalsh@redhat.com> - 2.1.5-3
- Apply selinux patch

* Thu Oct 21 2004 Bill Nottingham <notting@redhat.com> - 2.1.5-2
- don't run by default. again.

* Wed Oct 13 2004 Harald Hoyer <harald@redhat.com> - 2.1.5-1
- added selinux patch from Daniel Walsh
- initscript now uses translated strings
- version 2.1.5 with minor fixes

* Tue Sep 21 2004 Harald Hoyer <harald@redhat.com> - 2.1.4-7
- added more build reqs (bug #132877)

* Thu Sep  9 2004 Bill Nottingham <notting@redhat.com> - 2.1.4-6
- don't run by default
- don't create/chmod directories in %%post, just include them with the
  right perms
- fix debuginfo
- fix docs

* Mon Aug 23 2004 Jason Vas Dias <jvdias@redhat.com> - 2.1.4-5
- Added debuginfo package

* Mon Aug 23 2004 Jason Vas Dias <jvdias@redhat.com> - 2.1.4-4
- Install man-pages
- Fix initscript 'fail()' func to write newline before failure()
  
* Thu Aug 19 2004 Jason Vas Dias <jvdias@redhat.com> - 2.1.4-3
- Fix 'service ipsec status' output

* Wed Aug 18 2004 Jason Vas Dias <jvdias@redhat.com> - 2.1.4-2
- Normalize initscripts for Red Hat and add translation string support

* Tue Aug 17 2004 Harald Hoyer <harald@redhat.com> - 2.1.4-1
- initial import

* Tue May 25 2004 Ken Bantoft <ken@xelerance.com>
- Initial version, based on FreeS/WAN .spec
