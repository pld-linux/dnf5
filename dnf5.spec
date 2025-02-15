#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	docs		# build html documentation
#
%bcond_without	dnf5daemon_client
%bcond_without	dnf5daemon_server
%bcond_without	libdnf_cli
%bcond_without	dnf5
%bcond_without	dnf5_plugins
# libdnf5 plugins
%bcond_without	plugin_actions
%bcond_without	plugin_appstream
%bcond_without	plugin_expired_pgp_keys
%bcond_without	python_plugins_loader

%bcond_without	comps
%bcond_without	modulemd
%bcond_without	zchunk
%bcond_without	systemd

%bcond_with	go
%bcond_without	perl
%bcond_without	python3
%bcond_with	ruby

%define		libmodulemd_version	2.5.0
%define		librepo_version		1.18.0
%define		libsolv_version		0.7.31
%define		sqlite_version		3.35.0
%define		zchunk_version		0.9.11

Summary:	Command-line package manager
Name:		dnf5
Version:	5.2.10.0
Release:	1
License:	GPL v2+
Source0:	https://github.com/rpm-software-management/dnf5/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	118b176708e1c463ce56f371725c8905
Patch0:		systemdunitdir.patch
Patch1:		perl-long-long.patch
# sdbus-cpp 2.x
Patch100:	0001-cmake-Move-sdbus-c-check-to-one-place.patch
Patch101:	0002-dnfdaemon-sdbus-cpp-v.-2-requires-strong-types.patch
Patch102:	0003-dnfdaemon-sdbus-Variant-constructor-is-explicit.patch
Patch103:	0004-dnfdaemon-Explicit-sdbus-Variant-conversion.patch
Patch104:	0005-dnfdaemon-Make-signal-handlers-compatible.patch
Patch105:	0006-dnfdaemon-Register-interface-methods-for-sdbus-cpp-2.patch
Patch106:	0007-dnfdaemon-client-Use-correct-data-type-for-callbacks.patch
Patch107:	0008-dnfdaemon-Properly-leave-event-loop.patch
Patch108:	0009-daemon-client-Separate-context-and-callbacks.patch
URL:		https://github.com/rpm-software-management/dnf5
BuildRequires:	AppStream-devel >= 0.16
BuildRequires:	bash-completion-devel
BuildRequires:	check-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	json-c-devel
BuildRequires:	libfmt-devel
BuildRequires:	librepo-devel >= %{librepo_version}
BuildRequires:	libsolv-devel >= %{libsolv_version}
BuildRequires:	openssl-devel
BuildRequires:	rpm-devel >= 4.17.0
BuildRequires:	sqlite3-devel >= %{sqlite_version}
BuildRequires:	toml11
%if %{with tests}
BuildRequires:	cppunit-devel
BuildRequires:	createrepo_c
%endif
%{?with_comps:BuildRequires:	libcomps-devel}
%{?with_modulemd:BuildRequires:	libmodulemd-devel >= %{libmodulemd_version}}
%{?with_zchunk:BuildRequires:	zchunk-devel >= %{zchunk_version}}
%if %{with systemd}
BuildRequires:	sdbus-cpp-devel >= 0.8.1
BuildRequires:	systemd-devel
%endif
%if %{with docs}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
%endif
%if %{with libdnf_cli}
BuildRequires:	libsmartcols-devel
%endif
%if %{with dnf5_plugins}
BuildRequires:	curl-devel >= 7.62.0
%endif
%if %{with dnf5daemon_server}
BuildRequires:	sdbus-cpp-devel >= 0.9.0
%endif
%if %{with perl} || %{with ruby} || %{with python3}
BuildRequires:	swig
%endif
%if %{with perl}
BuildRequires:	perl-devel
%if %{with tests}
BuildRequires:	perl-Test-Exception
BuildRequires:	perl-base
BuildRequires:	perl-modules
%endif
%endif
%if %{with ruby}
BuildRequires:	ruby-devel
%if %{with tests}
BuildRequires:	rubygem-test-unit
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
%endif
Requires:	coreutils
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}
Provides:	dnf = %{version}-%{release}
Provides:	yum = %{version}-%{release}
Obsoletes:	dnf < 5
Obsoletes:	yum < 5
Conflicts:	python3-dnf-plugins-core < 4.7.0

%description
DNF5 is a command-line package manager that automates the process of
installing, upgrading, configuring, and removing computer programs in
a consistent manner. It supports RPM packages, modulemd modules, and
comps groups & environments.

%package -n libdnf5
Summary:	Package management library
License:	LGPL v2.1+
#Requires:	libmodulemd{?_isa} >= {libmodulemd_version}
Requires:	librepo%{?_isa} >= %{librepo_version}
Requires:	libsolv%{?_isa} >= %{libsolv_version}
Requires:	sqlite-libs%{?_isa} >= %{sqlite_version}
Conflicts:	dnf-data < 4.20.0

%description -n libdnf5
Package management library.

%package -n libdnf5-cli
Summary:	Library for working with a terminal in a command-line package manager
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli
Library for working with a terminal in a command-line package manager.

%package -n dnf5-devel
Summary:	Development files for dnf5
License:	LGPL v2.1+
Requires:	dnf5%{?_isa} = %{version}-%{release}
Requires:	libdnf5-cli-devel%{?_isa} = %{version}-%{release}
Requires:	libdnf5-devel%{?_isa} = %{version}-%{release}

%description -n dnf5-devel
Development files for dnf5.

%package -n libdnf5-devel
Summary:	Development files for libdnf
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	libsolv-devel%{?_isa} >= %{libsolv_version}

%description -n libdnf5-devel
Development files for libdnf.

%package -n libdnf5-cli-devel
Summary:	Development files for libdnf5-cli
License:	LGPL v2.1+
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli-devel
Development files for libdnf5-cli.

%package -n perl-libdnf5
Summary:	Perl 5 bindings for the libdnf library
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}

%description -n perl-libdnf5
Perl 5 bindings for the libdnf library.

%package -n perl-libdnf5-cli
Summary:	Perl 5 bindings for the libdnf5-cli library
License:	LGPL v2.1+
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n perl-libdnf5-cli
Perl 5 bindings for the libdnf5-cli library.

%package -n python3-libdnf5
Summary:	Python 3 bindings for the libdnf5 library
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5
Python 3 bindings for the libdnf library.

%package -n python3-libdnf5-cli
Summary:	Python 3 bindings for the libdnf5-cli library
License:	LGPL v2.1+
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-cli
Python 3 bindings for the libdnf5-cli library.

%package -n ruby-libdnf5
Summary:	Ruby bindings for the libdnf library
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	ruby(release)
Provides:	ruby(libdnf) = %{version}-%{release}

%description -n ruby-libdnf5
Ruby bindings for the libdnf library.

%package -n ruby-libdnf5-cli
Summary:	Ruby bindings for the libdnf5-cli library
License:	LGPL v2.1+
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:	ruby(release)
Provides:	ruby(libdnf_cli) = %{version}-%{release}

%description -n ruby-libdnf5-cli
Ruby bindings for the libdnf5-cli library.

%package -n libdnf5-plugin-actions
Summary:	Libdnf5 plugin that allows to run actions (external executables) on hooks
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-actions
Libdnf5 plugin that allows to run actions (external executables) on
hooks.

%package -n libdnf5-plugin-appstream
Summary:	Libdnf5 plugin to install repo Appstream data
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-appstream
Libdnf5 plugin that installs repository's Appstream data, for
repositories which provide them.

%package -n libdnf5-plugin-expired-pgp-keys
Summary:	Libdnf5 plugin for detecting and removing expired PGP keys
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-expired-pgp-keys
Libdnf5 plugin for detecting and removing expired PGP keys.

%package -n python3-libdnf5-python-plugins-loader
Summary:	Libdnf5 plugin that allows loading Python plugins
License:	LGPL v2.1+
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	python3-libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-python-plugins-loader
Libdnf5 plugin that allows loading Python plugins.

%package -n dnf5daemon-client
Summary:	Command-line interface for dnf5daemon-server
License:	GPL v2+
Requires:	dnf5daemon-server
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n dnf5daemon-client
Command-line interface for dnf5daemon-server.

%package -n dnf5daemon-server
Summary:	Package management service with a DBus interface
License:	GPL v2+
Requires:	dbus
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:	polkit

%description -n dnf5daemon-server
Package management service with a DBus interface.

%package -n dnf5-plugins
Summary:	Plugins for dnf5
License:	LGPL v2.1+
Requires:	dnf5%{?_isa} = %{version}-%{release}
Requires:	libcurl%{?_isa} >= 7.62.0
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n dnf5-plugins
Core DNF5 plugins that enhance dnf5 with builddep, changelog,
config-manager, copr, repoclosure, and reposync commands.

%package plugin-automatic
Summary:	Package manager - automated upgrades
License:	LGPL v2.1+
Requires:	dnf5%{?_isa} = %{version}-%{release}
Requires:	libcurl-full%{?_isa}
Requires:	libdnf5%{?_isa} = %{version}-%{release}
Requires:	libdnf5-cli%{?_isa} = %{version}-%{release}
Provides:	dnf-automatic = %{version}-%{release}
Obsoletes:	dnf-automatic < 5

%description plugin-automatic
Alternative command-line interface "dnf upgrade" suitable to be
executed automatically and regularly from systemd timers, cron jobs or
similar.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 100 -p1
%patch -P 101 -p1
%patch -P 102 -p1
%patch -P 103 -p1
%patch -P 104 -p1
%patch -P 105 -p1
%patch -P 106 -p1
%patch -P 107 -p1
%patch -P 108 -p1

%{__mv} dnf5-plugins/automatic_plugin/config/{usr/,}lib

%build
mkdir build
cd build
%cmake ../ \
	-DPERL_INSTALLDIRS=vendor \
	-DENABLE_SOLV_FOCUSNEW=ON \
	-DWITH_DNF5DAEMON_CLIENT=%{?with_dnf5daemon_client:ON}%{!?with_dnf5daemon_client:OFF} \
	-DWITH_DNF5DAEMON_SERVER=%{?with_dnf5daemon_server:ON}%{!?with_dnf5daemon_server:OFF} \
	-DWITH_LIBDNF5_CLI=%{?with_libdnf_cli:ON}%{!?with_libdnf_cli:OFF} \
	-DWITH_DNF5=%{?with_dnf5:ON}%{!?with_dnf5:OFF} \
	-DWITH_PLUGIN_ACTIONS=%{?with_plugin_actions:ON}%{!?with_plugin_actions:OFF} \
	-DWITH_PLUGIN_APPSTREAM=%{?with_plugin_appstream:ON}%{!?with_plugin_appstream:OFF} \
	-DWITH_PLUGIN_RHSM=OFF \
	-DWITH_PYTHON_PLUGINS_LOADER=%{?with_python_plugins_loader:ON}%{!?with_python_plugins_loader:OFF} \
	\
	%{cmake_on_off comps WITH_COMPS} \
	%{cmake_on_off modulemd WITH_MODULEMD} \
	%{cmake_on_off zchunk WITH_ZCHUNK} \
	%{cmake_on_off systemd WITH_SYSTEMD} \
	%{cmake_on_off docs WITH_HTML} \
	%{cmake_on_off go WITH_GO} \
	%{cmake_on_off perl WITH_PERL5} \
	%{cmake_on_off python3 WITH_PYTHON3} \
	%{cmake_on_off ruby WITH_RUBY} \
	%{cmake_on_off tests WITH_TESTS}

%{__make}
%if %{with docs}
%{__make} -j1 doc
%endif

%if %{with tests}
TMPDIR=/tmp /usr/bin/ctest --force-new-ctest-process --output-on-failure
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/{cache/libdnf5,lib/dnf}
install -d $RPM_BUILD_ROOT%{_prefix}/lib/sysimage/libdnf5/{comps_groups,offline}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sr $RPM_BUILD_ROOT%{_bindir}/dnf5 $RPM_BUILD_ROOT%{_bindir}/dnf
ln -sr $RPM_BUILD_ROOT%{_bindir}/dnf5 $RPM_BUILD_ROOT%{_bindir}/yum
ln -sr $RPM_BUILD_ROOT%{bash_compdir}/dnf5 $RPM_BUILD_ROOT%{bash_compdir}/dnf
(cd $RPM_BUILD_ROOT%{_mandir}
for file in man[578]/dnf5[-.]*; do
	echo ".so $file" > "$(dirname $file)/dnf${file##*/dnf5}"
done)

# own dirs and files that dnf5 creates on runtime
for file in \
    environments.toml groups.toml modules.toml nevras.toml packages.toml \
    system.toml \
    transaction_history.sqlite transaction_history.sqlite-shm \
    transaction_history.sqlite-wal
do
    touch $RPM_BUILD_ROOT%{_prefix}/lib/sysimage/libdnf5/$file
done
touch $RPM_BUILD_ROOT%{_sysconfdir}/dnf/versionlock.toml
touch $RPM_BUILD_ROOT%{_sysconfdir}/dnf/dnf5-plugins/automatic.conf

%if %{with systemd}
install -d $RPM_BUILD_ROOT%{systemdunitdir}/system-update.target.wants
ln -sr $RPM_BUILD_ROOT%{systemdunitdir}{,/system-update.target.wants}/dnf5-offline-transaction.service
%endif

%find_lang dnf5
%find_lang dnf5-plugin-builddep
%find_lang dnf5-plugin-changelog
%find_lang dnf5-plugin-config-manager
%find_lang dnf5-plugin-copr
%find_lang dnf5-plugin-needs-restarting
%find_lang dnf5-plugin-repoclosure
%find_lang dnf5daemon-client
%find_lang dnf5daemon-server
%find_lang libdnf5
%find_lang libdnf5-cli
%find_lang libdnf5-plugin-actions

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post dnf5-makecache.timer

%preun
%systemd_preun dnf5-makecache.timer

%postun
%systemd_postun_with_restart dnf5-makecache.timer

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%post -n libdnf5 -p /sbin/ldconfig
%postun -n libdnf5 -p /sbin/ldconfig
%post -n libdnf5-cli -p /sbin/ldconfig
%postun -n libdnf5-cli -p /sbin/ldconfig

%files -f dnf5.lang
%defattr(644,root,root,755)
%doc COPYING.md
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dnf5
%attr(755,root,root) %{_bindir}/dnf
%attr(755,root,root) %{_bindir}/yum
%{systemdunitdir}/dnf5-makecache.service
%{systemdunitdir}/dnf5-makecache.timer

%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_datadir}/dnf5
%dir %{_datadir}/dnf5/aliases.d
%{_datadir}/dnf5/aliases.d/compatibility.conf
%dir %{_libdir}/dnf5
%dir %{_libdir}/dnf5/plugins
%dir %{_datadir}/dnf5/dnf5-plugins
%dir %{_sysconfdir}/dnf/dnf5-plugins
%doc %{_libdir}/dnf5/plugins/README
%dir %{_libdir}/libdnf5/plugins
%dir %{_datadir}/bash-completion/
%dir %{bash_compdir}/
%{bash_compdir}/dnf*
%dir %{_prefix}/lib/sysimage/libdnf5
%dir %{_prefix}/lib/sysimage/libdnf5/comps_groups
%dir %{_prefix}/lib/sysimage/libdnf5/offline
%ghost %verify(not md5 mtime size) %{_prefix}/lib/sysimage/libdnf5/*.toml
%ghost %verify(not md5 mtime size) %{_prefix}/lib/sysimage/libdnf5/transaction_history.sqlite*
%{_mandir}/man8/dnf.8*
%{_mandir}/man8/dnf5.8*
%{_mandir}/man8/dnf*-advisory.8*
%{_mandir}/man8/dnf*-autoremove.8*
%{_mandir}/man8/dnf*-check.8*
%{_mandir}/man8/dnf*-clean.8*
%{_mandir}/man8/dnf*-distro-sync.8*
%{_mandir}/man8/dnf*-downgrade.8*
%{_mandir}/man8/dnf*-download.8*
%{_mandir}/man8/dnf*-environment.8*
%{_mandir}/man8/dnf*-group.8*
%{_mandir}/man8/dnf*-history.8*
%{_mandir}/man8/dnf*-info.8*
%{_mandir}/man8/dnf*-install.8*
%{_mandir}/man8/dnf*-leaves.8*
%{_mandir}/man8/dnf*-list.8*
%{_mandir}/man8/dnf*-makecache.8*
%{_mandir}/man8/dnf*-mark.8*
%{_mandir}/man8/dnf*-module.8*
%{_mandir}/man8/dnf*-offline.8*
%{_mandir}/man8/dnf*-provides.8*
%{_mandir}/man8/dnf*-reinstall.8*
%{_mandir}/man8/dnf*-remove.8*
%{_mandir}/man8/dnf*-replay.8*
%{_mandir}/man8/dnf*-repo.8*
%{_mandir}/man8/dnf*-repoquery.8*
%{_mandir}/man8/dnf*-search.8*
%{_mandir}/man8/dnf*-swap.8*
%{_mandir}/man8/dnf*-upgrade.8*
%{_mandir}/man8/dnf*-versionlock.8*
%{_mandir}/man7/dnf*-aliases.7*
%{_mandir}/man7/dnf*-caching.7*
%{_mandir}/man7/dnf*-comps.7*
%{_mandir}/man7/dnf*-filtering.7*
%{_mandir}/man7/dnf*-forcearch.7*
%{_mandir}/man7/dnf*-installroot.7*
%{_mandir}/man7/dnf*-modularity.7*
%{_mandir}/man7/dnf*-specs.7*
%{_mandir}/man7/dnf*-system-state.7*
%{_mandir}/man7/dnf*-changes-from-dnf4.7*
%{_mandir}/man5/dnf*.conf.5*
%{_mandir}/man5/dnf*.conf-todo.5*
%{_mandir}/man5/dnf*.conf-deprecated.5*

%if %{with systemd}
%{systemdunitdir}/dnf5-offline-transaction.service
%{systemdunitdir}/dnf5-offline-transaction-cleanup.service
%{systemdunitdir}/system-update.target.wants/dnf5-offline-transaction.service
%endif

%files -n libdnf5 -f libdnf5.lang
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnf/dnf.conf
%dir %{_sysconfdir}/dnf/vars
%dir %{_sysconfdir}/dnf/protected.d
%ghost %{_sysconfdir}/dnf/versionlock.toml
%dir %{_datadir}/dnf5/libdnf.conf.d
%dir %{_sysconfdir}/dnf/libdnf5.conf.d
%dir %{_datadir}/dnf5/repos.override.d
%dir %{_sysconfdir}/dnf/repos.override.d
%dir %{_sysconfdir}/dnf/libdnf5-plugins
%dir %{_datadir}/dnf5/repos.d
%dir %{_datadir}/dnf5/vars.d
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so.2*
%dir %{_var}/cache/libdnf5
%dir %{_sharedstatedir}/dnf

%files -n libdnf5-cli -f libdnf5-cli.lang
%defattr(644,root,root,755)
%{_libdir}/libdnf5-cli.so.2*

%files -n dnf5-devel
%defattr(644,root,root,755)
%{_includedir}/dnf5/

%files -n libdnf5-devel
%defattr(644,root,root,755)
%{_includedir}/libdnf5/
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so
%{_pkgconfigdir}/libdnf5.pc

%files -n libdnf5-cli-devel
%defattr(644,root,root,755)
%{_includedir}/libdnf5-cli/
%{_libdir}/libdnf5-cli.so
%{_pkgconfigdir}/libdnf5-cli.pc

%if %{with perl}
%files -n perl-libdnf5
%defattr(644,root,root,755)
%{perl_vendorarch}/libdnf5
%{perl_vendorarch}/auto/libdnf5
%endif

%if %{with perl} && %{with libdnf_cli}
%files -n perl-libdnf5-cli
%defattr(644,root,root,755)
%{perl_vendorarch}/libdnf5_cli
%{perl_vendorarch}/auto/libdnf5_cli
%endif

%if %{with python3}
%files -n python3-libdnf5
%defattr(644,root,root,755)
%{py3_sitedir}/libdnf5
%{py3_sitedir}/libdnf5-*.dist-info
%endif

%if %{with python3} && %{with libdnf_cli}
%files -n python3-libdnf5-cli
%defattr(644,root,root,755)
%{py3_sitedir}/libdnf5_cli
%{py3_sitedir}/libdnf5_cli-*.dist-info
%endif

%if %{with ruby}
%files -n ruby-libdnf5
%defattr(644,root,root,755)
%{ruby_vendorarchdir}/libdnf5
%endif

%if %{with ruby} && %{with libdnf_cli}
%files -n ruby-libdnf5-cli
%defattr(644,root,root,755)
%{ruby_vendorarchdir}/libdnf5_cli
%endif

%if %{with plugin_actions}
%files -n libdnf5-plugin-actions -f libdnf5-plugin-actions.lang
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnf/libdnf5-plugins/actions.conf
%dir %{_sysconfdir}/dnf/libdnf5-plugins/actions.d
%{_libdir}/libdnf5/plugins/actions.*
%{_mandir}/man8/libdnf5-actions.8*
%endif

%if %{with plugin_appstream}
%files -n libdnf5-plugin-appstream
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnf/libdnf5-plugins/appstream.conf
%{_libdir}/libdnf5/plugins/appstream.so
%endif

%if %{with plugin_expired_pgp_keys}
%files -n libdnf5-plugin-expired-pgp-keys
%defattr(644,root,root,755)
%{_sysconfdir}/dnf/libdnf5-plugins/expired-pgp-keys.conf
%{_libdir}/libdnf5/plugins/expired-pgp-keys.so
%{_mandir}/man8/libdnf5-expired-pgp-keys.8*
%endif

%if %{with python_plugins_loader}
%files -n python3-libdnf5-python-plugins-loader
%defattr(644,root,root,755)
%{_libdir}/libdnf5/plugins/python_plugins_loader.*
%dir %{py3_sitescriptdir}/libdnf_plugins/
%doc %{py3_sitescriptdir}/libdnf_plugins/README
%endif

%if %{with dnf5daemon_client}
%files -n dnf5daemon-client -f dnf5daemon-client.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dnf5daemon-client
%{_mandir}/man8/dnf5daemon-client.8*
%endif

%if %{with dnf5daemon_server}
%files -n dnf5daemon-server -f dnf5daemon-server.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dnf5daemon-server
%{systemdunitdir}/dnf5daemon-server.service
%{_datadir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.*.xml
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%{_mandir}/man8/dnf5daemon-server.8*
%{_mandir}/man8/dnf5daemon-dbus-api.8*
%endif

%if %{with dnf5_plugins}
%files -n dnf5-plugins -f dnf5-plugin-builddep.lang -f dnf5-plugin-changelog.lang -f dnf5-plugin-config-manager.lang -f dnf5-plugin-copr.lang -f dnf5-plugin-needs-restarting.lang -f dnf5-plugin-repoclosure.lang
%defattr(644,root,root,755)
%{_libdir}/dnf5/plugins/builddep_cmd_plugin.so
%{_libdir}/dnf5/plugins/changelog_cmd_plugin.so
%{_libdir}/dnf5/plugins/config-manager_cmd_plugin.so
%{_libdir}/dnf5/plugins/copr_cmd_plugin.so
%{_libdir}/dnf5/plugins/needs_restarting_cmd_plugin.so
%{_libdir}/dnf5/plugins/repoclosure_cmd_plugin.so
%{_libdir}/dnf5/plugins/reposync_cmd_plugin.so
%{_mandir}/man8/dnf*-builddep.8*
%{_mandir}/man8/dnf*-changelog.8*
%{_mandir}/man8/dnf*-config-manager.8*
%{_mandir}/man8/dnf*-copr.8*
%{_mandir}/man8/dnf*-needs-restarting.8*
%{_mandir}/man8/dnf*-repoclosure.8*
%{_mandir}/man8/dnf*-reposync.8*
%{_datadir}/dnf5/aliases.d/compatibility-plugins.conf
%{_datadir}/dnf5/aliases.d/compatibility-reposync.conf

%files plugin-automatic
%defattr(644,root,root,755)
#%ghost %{_sysconfdir}/motd.d/dnf5-automatic
%{_libdir}/dnf5/plugins/automatic_cmd_plugin.so
%{_datadir}/dnf5/dnf5-plugins/automatic.conf
%ghost %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnf/dnf5-plugins/automatic.conf
%{_mandir}/man8/dnf*-automatic.8*
%{systemdunitdir}/dnf5-automatic.service
%{systemdunitdir}/dnf5-automatic.timer
%{systemdunitdir}/dnf-automatic.service
%{systemdunitdir}/dnf-automatic.timer
%attr(755,root,root) %{_bindir}/dnf-automatic
%endif
