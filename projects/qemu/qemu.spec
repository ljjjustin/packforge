%global kvm_target    x86_64
%global pkgname       qemu-kvm

#%define buildid %{nil}.test
%define buildid %{nil}.ustack
%define rpmversion 2.1.2
%define pkgrelease 18

#%define full_release %{pkgrelease}%{?dist}%{?buildid}
%define full_release %{pkgrelease}%{?dist}
%define qemudocdir %{_docdir}/%{pkgname}

Summary: QEMU is a FAST! processor emulator
Name: %{pkgname}
Version: 2.1.2
Release: 1%{full_release}
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 10
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/

ExclusiveArch: x86_64

Requires: seabios-bin >= 1.7.5-1
Requires: sgabios-bin
Requires: seavgabios-bin
Requires: ipxe-roms-qemu
Requires: libseccomp >= 1.0.0
# For compressed guest memory dumps
Requires: lzo snappy

Requires: %{pkgname}-common = %{epoch}:%{version}-%{release}
Requires: qemu-img = %{epoch}:%{version}-%{release}

#Source0: http://wiki.qemu.org/download/qemu-%{version}.tar.bz2
Source0: qemu-%{version}.tar.gz

Source1: qemu.binfmt
# Creates /dev/kvm
Source2: 80-kvm.rules
# KSM control scripts
Source3: ksm.service
Source4: ksm.sysconfig
Source5: ksmctl.c
Source6: ksmtuned.service
Source7: ksmtuned
Source8: ksmtuned.conf
Source9: qemu-guest-agent.service
Source10: 99-qemu-guest-agent.rules
Source11: bridge.conf
Source12: qemu-ga.sysconfig

# custom for ustack
Source101: qemu.init
Source102: ksm.init
Source103: ksmtuned.init
Source104: qemu-ga.init
Source105: pxe-virtio-qemu-kvm-1.2.rom

Patch0002: 0002-Fixes-for-changing-qemu-to-qemu-kvm.patch
Patch0003: 0003-Rename-man-page-qemu-1-to-qemu-kvm-1.patch
Patch0004: 0004-Use-kvm-by-default.patch
#Patch0005: 0005-Remove-unsupported-usb-devices.patch
#Patch0006: 0006-Disable-unsupported-emulated-SCSI-devices.patch
#Patch0007: 0007-Disable-unsupported-audio-devices.patch
#Patch0008: 0008-Remove-unsupported-network-devices.patch
#Patch0009: 0009-Disable-HPET-device.patch
#Patch0010: 0010-Disable-various-devices.patch
Patch0011: 0011-rbd-link-and-load-librbd-dynamically.patch

# we don't need Patch0012
#Patch0012: 0012-rbd-Only-look-for-qemu-specific-copy-of-librbd.so.1.patch
#Patch0013: 0013-Disable-EFI-enabled-roms.patch
# we nee all machine type
#Patch0014: 0014-Enable-only-2.1-machine-type.patch

BuildRequires: zlib-devel
BuildRequires: SDL-devel
BuildRequires: which
BuildRequires: texi2html
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: python
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libiscsi-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: libusbx-devel
BuildRequires: usbredir-devel >= 0.6
BuildRequires: texinfo
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
BuildRequires: libseccomp-devel >= 1.0.0
# For network block driver
BuildRequires: libcurl-devel
# For gluster block driver
BuildRequires: glusterfs-api-devel
BuildRequires: glusterfs-devel
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For smartcard NSS support
BuildRequires: nss-devel
# For XFS discard support in raw-posix.c
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For Braille device support
BuildRequires: brlapi-devel
# For test suite
BuildRequires: check-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# Documentation requirement
BuildRequires: perl-podlators
BuildRequires: texinfo
# For rdma
BuildRequires: librdmacm-devel
# iasl and cpp for acpi generation (not a hard requirement as we can use
# pre-compiled files, but it's better to use this)
BuildRequires: iasl
BuildRequires: cpp
# For compressed guest memory dumps
BuildRequires: lzo-devel snappy-devel

%description
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor. qemu-kvm acts as a virtual machine monitor together with
the KVM kernel modules, and emulates the hardware for a full system such as
a PC and its assocated peripherals.

As qemu-kvm requires no host kernel patches to run, it is safe and easy to use.

%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%description -n qemu-img
This package provides a command line tool for manipulating disk images.

%package -n qemu-kvm-common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
%if %{with systemd}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

%description -n qemu-kvm-common
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor. 

This package provides documentation and auxiliary programs used with qemu-kvm.

%package -n qemu-guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
%if %{with systemd}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

%description -n qemu-guest-agent
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor. 

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post -n qemu-guest-agent
if [ $1 -eq 1 ]; then
    # Initial installation.
%if %{with systemd}
%systemd_post qemu-guest-agent.service
%else
    /sbin/chkconfig --add qemu-ga
%endif
fi

%preun -n qemu-guest-agent
if [ $1 -eq 0 ]; then
    # Package removeal, not upgrade.
%if %{with systemd}
%systemd_preun qemu-guest-agent.service
%else
    /sbin/chkconfig --del qemu-ga
%endif
fi

%postun -n qemu-guest-agent
if [ $1 -eq 1 ]; then
    # Package upgrade, not uninstall.
%if %{with systemd}
%systemd_postun_with_restart qemu-guest-agent.service
%else
    /sbin/service qemu-ga condrestart
%endif
fi

%package -n qemu-kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description -n qemu-kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.

%package -n libcacard
Summary:        Common Access Card (CAC) Emulation
Group:          Development/Libraries

%description -n libcacard
Common Access Card (CAC) emulation library.

%package -n libcacard-tools
Summary:        CAC Emulation tools
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}

%description -n libcacard-tools%{?pkgsuffix}
CAC emulation tools.

%package -n libcacard-devel
Summary:        CAC Emulation devel
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}

%description -n libcacard-devel
CAC emulation development files.

%prep
%setup -q -n qemu-%{version}

# if patch fuzzy patch applying will be forbidden
%define with_fuzzy_patches 0
%if %{with_fuzzy_patches}
    patch_command='patch -p1 -s'
%else
    patch_command='patch -p1 -F1 -s'
%endif

ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
#%patch0005 -p1
#%patch0006 -p1
#%patch0007 -p1
#%patch0008 -p1
#%patch0009 -p1
#%patch0010 -p1
%patch0011 -p1
#%patch0012 -p1
#%patch0013 -p1
#%patch0014 -p1

%build
buildarch="%{kvm_target}-softmmu"

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

dobuild() {
    ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,alsa \
        --with-confsuffix=/%{pkgname} \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --with-pkgversion=%{name}-%{version}-%{release} \
        --disable-strip \
        --disable-qom-cast-debug \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE" \
        --enable-trace-backend=dtrace \
        --enable-werror \
        --disable-xen \
        --disable-virtfs \
        --enable-kvm \
        --enable-libusb \
        --enable-spice \
        --enable-seccomp \
        --disable-fdt \
        --enable-docs \
        --disable-sdl \
        --disable-debug-tcg \
        --disable-sparse \
        --disable-brlapi \
        --disable-bluez \
        --disable-vde \
        --disable-curses \
        --disable-curl \
        --enable-vnc-tls \
        --enable-vnc-sasl \
        --enable-linux-aio \
        --enable-smartcard-nss \
        --enable-lzo \
        --enable-snappy \
        --enable-usb-redir \
        --enable-vnc-png \
        --disable-vnc-jpeg \
        --enable-vnc-ws \
        --enable-uuid \
        --disable-vhost-scsi \
        --enable-guest-agent \
        --disable-tpm \
        --enable-glusterfs \
        --disable-xfsctl \
        --disable-quorum \
        --block-drv-rw-whitelist=qcow2,raw,file,host_device,nbd,iscsi,gluster,rbd \
        --block-drv-ro-whitelist=vmdk,vhdx,vpc \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    make V=1 %{?_smp_mflags} $buildldflags
}

dobuild --target-list="$buildarch"

# Setup back compat qemu-kvm binary
./scripts/tracetool.py --backend dtrace --format stap \
  --binary %{_libexecdir}/qemu-kvm --target-name %{kvm_target} \
  --target-type system --probe-prefix \
  qemu.kvm < ./trace-events > qemu-kvm.stp

cp -a %{kvm_target}-softmmu/qemu-system-%{kvm_target} qemu-kvm


gcc %{SOURCE5} -O2 -g -o ksmctl


%install
%define _udevdir %(pkg-config --variable=udevdir udev)/rules.d

install -D -p -m 0755 %{SOURCE104} $RPM_BUILD_ROOT%{_initddir}/qemu-ga

install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
%if %{with systemd}
install -D -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/ksm.service
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT%{_libexecdir}/ksmctl
%else
install -D -p -m 0755 %{SOURCE102} $RPM_BUILD_ROOT%{_initddir}/ksm
%endif

install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf
%if %{with systemd}
install -D -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/ksmtuned.service
%else
install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0755 %{SOURCE103} $RPM_BUILD_ROOT%{_initddir}/ksmtuned
%endif

mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_udevdir}

install -m 0755 scripts/kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_udevdir}

make DESTDIR=$RPM_BUILD_ROOT \
  sharedir="%{_datadir}/%{pkgname}" \
  datadir="%{_datadir}/%{pkgname}" \
  install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset

install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_libexecdir}/

# add in /usr/bin/qemu-kvm for me..
install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/

install -m 0644 qemu-kvm.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/

rm $RPM_BUILD_ROOT%{_bindir}/qemu-system-%{kvm_target}
rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}.stp

mkdir -p $RPM_BUILD_ROOT%{qemudocdir}
install -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE
mv ${RPM_BUILD_ROOT}%{_docdir}/qemu/qemu-doc.html $RPM_BUILD_ROOT%{qemudocdir}
mv ${RPM_BUILD_ROOT}%{_docdir}/qemu/qemu-tech.html $RPM_BUILD_ROOT%{qemudocdir}
mv ${RPM_BUILD_ROOT}%{_docdir}/qemu/qmp-commands.txt $RPM_BUILD_ROOT%{qemudocdir}
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man8/*

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu-kvm.conf

# Remove unpackaged files.
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/palcode-clipper
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/petalogix*.dtb
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/bamboo.dtb
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/ppc_rom.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/s390-zipl.rom
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/s390-ccw.img

# Remove unpackaged locale files.
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/locale

# Remove ppc stuff
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/spapr-rtas.bin
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/u-boot.e500
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/slof.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/openbios-ppc

# Remove sparc files
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/QEMU,tcx.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/QEMU,cgthree.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/openbios-sparc64

# Remove efi roms
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/efi*.rom

# Provided by package ipxe
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/pxe*rom

# Provided by package vgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/vgabios*bin
# Provided by package seabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/bios*.bin
# Provided by package sgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/sgabios.bin

# the pxe ipxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
    ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{pkgname}/pxe-$1.rom
    ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139

# we add pxe-virtio.rom from qemu-kvm 1.2 for compatibility ...
#pxe_link virtio 1af41000
install -D -p -m 0644 %{SOURCE105} $RPM_BUILD_ROOT%{_datadir}/%{name}/pxe-virtio.rom
ln -s ../ipxe.efi/1af41000.rom %{buildroot}%{_datadir}/%{name}/efi-virtio.rom

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{pkgname}/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin

rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../sgabios/sgabios.bin sgabios.bin

# For the qemu-guest-agent subpackage, install:
# - the systemd service file and the udev rules:
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_udevdir}
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_udevdir}

# - the environment file for the systemd service:
install -D -p -m 0644 %{SOURCE12} \
  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/qemu-ga

# - the fsfreeze hook script:
install -D --preserve-timestamps \
  scripts/qemu-guest-agent/fsfreeze-hook \
  $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook

# - the directory for user scripts:
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook.d

# - and the fsfreeze script samples:
mkdir --parents $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
install --preserve-timestamps --mode=0644 \
  scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/

# - Install dedicated log directory:
mkdir -p -v $RPM_BUILD_ROOT%{_localstatedir}/log/qemu-ga/

# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/%{pkgname}

make %{?_smp_mflags} $buildldflags DESTDIR=$RPM_BUILD_ROOT install-libcacard
find $RPM_BUILD_ROOT -name "libcacard.so*" -exec chmod +x \{\} \;

find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -c -m 0755  qemu-ga ${RPM_BUILD_ROOT}%{_bindir}/qemu-ga

%post -n qemu-kvm-common
%if %{with systemd}
%systemd_post ksm.service
%systemd_post ksmtuned.service
%else
    /sbin/chkconfig --add ksm
    /sbin/chkconfig --add ksmtuned
%endif

getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
   useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
   -c "qemu user" qemu

%preun -n qemu-kvm-common
%if %{with systemd}
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%else
    /sbin/service ksm stop &>/dev/null || :
    /sbin/chkconfig --del ksm
    /sbin/service ksmtuned stop &>/dev/null || :
    /sbin/chkconfig --del ksmtuned
%endif

%postun -n qemu-kvm-common
%if %{with systemd}
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service
%else
    /sbin/service ksm condrestart &>/dev/null || :
    /sbin/service ksmtuned condrestart &>/dev/null || :
%endif

%global kvm_files \
%{_udevdir}/80-kvm.rules

%global qemu_kvm_files \
%{_libexecdir}/qemu-kvm \
%{_bindir}/qemu-kvm \
%{_datadir}/systemtap/tapset/qemu-kvm.stp

%files -n qemu-kvm-common
%defattr(-,root,root)
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/qmp-commands.txt
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{pkgname}/
%{_datadir}/%{pkgname}/keymaps/
%{_mandir}/man1/qemu-kvm.1*
%attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/%{pkgname}.conf
%if %{with systemd}
%{_unitdir}/ksm.service
%{_libexecdir}/ksmctl
%else
%{_initddir}/ksm
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%if %{with systemd}
%{_unitdir}/ksmtuned.service
%else
%{_initddir}/ksmtuned
%endif
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%dir %{_sysconfdir}/%{pkgname}
%config(noreplace) %{_sysconfdir}/%{pkgname}/bridge.conf

%files -n qemu-guest-agent
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/qemu-ga
%if %{with systemd}
%{_unitdir}/qemu-guest-agent.service
%else
%{_initddir}/qemu-ga
%endif
%{_udevdir}/99-qemu-guest-agent.rules
%{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%{_datadir}/%{name}/qemu-ga
%dir %{_localstatedir}/log/qemu-ga

%files
%defattr(-,root,root)
%{_datadir}/%{pkgname}/acpi-dsdt.aml
%{_datadir}/%{pkgname}/q35-acpi-dsdt.aml
%{_datadir}/%{pkgname}/bios.bin
%{_datadir}/%{pkgname}/bios-256k.bin
%{_datadir}/%{pkgname}/linuxboot.bin
%{_datadir}/%{pkgname}/multiboot.bin
%{_datadir}/%{pkgname}/kvmvapic.bin
%{_datadir}/%{pkgname}/sgabios.bin
%{_datadir}/%{pkgname}/vgabios.bin
%{_datadir}/%{pkgname}/vgabios-cirrus.bin
%{_datadir}/%{pkgname}/vgabios-qxl.bin
%{_datadir}/%{pkgname}/vgabios-stdvga.bin
%{_datadir}/%{pkgname}/vgabios-vmware.bin
%{_datadir}/%{pkgname}/pxe-e1000.rom
%{_datadir}/%{pkgname}/pxe-virtio.rom
%{_datadir}/%{pkgname}/pxe-pcnet.rom
%{_datadir}/%{pkgname}/pxe-rtl8139.rom
%{_datadir}/%{pkgname}/pxe-ne2k_pci.rom
%{_datadir}/%{pkgname}/efi-e1000.rom
%{_datadir}/%{pkgname}/efi-virtio.rom
%{_datadir}/%{pkgname}/efi-pcnet.rom
%{_datadir}/%{pkgname}/efi-rtl8139.rom
%{_datadir}/%{pkgname}/efi-ne2k_pci.rom
%{_datadir}/%{pkgname}/qemu-icon.bmp
%{_datadir}/%{pkgname}/qemu_logo_no_text.svg
%config(noreplace) %{_sysconfdir}/%{pkgname}/target-x86_64.conf
%{?kvm_files:}
%{?qemu_kvm_files:}

%files -n qemu-kvm-tools
%defattr(-,root,root,-)
%{_bindir}/kvm_stat

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*

%files -n libcacard
%defattr(-,root,root,-)
%{_libdir}/libcacard.so.*

%files -n libcacard-tools
%defattr(-,root,root,-)
%{_bindir}/vscclient

%files -n libcacard-devel
%defattr(-,root,root,-)
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc

