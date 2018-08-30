Name:       droplet
Version:    1.0
Release:    %(git rev-list --count HEAD)%{?dist}
Summary:    deepflow droplet

Group:      Applications/File
Vendor:     Yunshan Networks
License:    Copyright (c) 2012-2018 Yunshan Networks
URL:        http://yunshan.net
BuildArch:  x86_64
Source:     droplet.spec

BuildRequires: golang git
Requires: zeromq
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%define pwd %(echo $PWD)

%description
deepflow droplet

%prep
(cd %pwd; make clean && make)
mkdir -p $RPM_BUILD_ROOT/usr/sbin/
cp %pwd/bin/droplet $RPM_BUILD_ROOT/usr/sbin/
mkdir -p $RPM_BUILD_ROOT/usr/bin/
cp $(go env GOPATH)/bin/dlv $RPM_BUILD_ROOT/usr/bin/dlv.trident
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system/
cp %pwd/droplet.service $RPM_BUILD_ROOT/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/etc/
cp %pwd/config/droplet.yaml $RPM_BUILD_ROOT/etc/

%files
/usr/bin/dlv.trident
/usr/sbin/droplet
/lib/systemd/system/droplet.service
%config(noreplace) /etc/droplet.yaml

%preun
if [ $1 == 0 ]; then # uninstall
    systemctl stop droplet
    systemctl disable droplet
fi

%post
systemctl daemon-reload
systemctl try-restart droplet
%{_sbindir}/update-alternatives --install %{_bindir}/dlv %{name} %{_bindir}/dlv.trident 10

%postun
systemctl daemon-reload
if [ $1 == 0 ]; then # uninstall
    %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/dlv
fi

%changelog
