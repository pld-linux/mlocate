# TODO:
# - Add
#	nodevs=$(awk '$1 == "nodev" && $2 != "rootfs" { print $2 }' /proc/filesystems)
#	exec /usr/bin/updatedb -f "$nodevs"
#   to ExecStart=/usr/bin/updatedb

Summary:	A locate/updatedb implementation
Summary(pl.UTF-8):	Implementacja locate/updatedb
Name:		mlocate
Version:	0.26
Release:	5
License:	GPL v2
Group:		Applications/System
Source0:	https://releases.pagure.org/mlocate/%{name}-%{version}.tar.xz
# Source0-md5:	539e6f86bf387358aa2b14d5f880e49a
Source1:	updatedb.conf
Source2:	%{name}.cron
Source3:	cronjob-%{name}.timer
Source4:	cronjob-%{name}.service
URL:		https://pagure.io/mlocate
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	awk
Requires:	rc-scripts >= 0.4.2.4-2
Requires:	systemd-units >= 38
Suggests:	cronjobs
Provides:	group(mlocate)
Provides:	locate-utility
Obsoletes:	locate-utility
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mlocate is a new locate implementation. The "m" stands for "merging",
because updatedb reuses the existing database to avoid rereading most
of the file system, which makes updatedb faster and does not trash the
system caches as much. The locate(1) utility is intended to be
completely compatible to slocate. It also attempts to be compatible to
GNU locate, when it does not conflict with slocate compatibility.

%description -l pl.UTF-8
mlocate to nowa implementacja locate. "m" oznacza "merging" (łącząca),
ponieważ updatedb wykorzystuje istniejącą bazę aby zapobiec ponownemu
odczytywaniu większości systemu plików, dzięki czemu updatedb działa
szybciej i nie czyści tak bardzo buforów systemowych. Narzędzie
locate(1) powinno być w pełni kompatybilne z slocate. Próbuje być
kompatybilne także z GNU locate, o ile nie jest to w konflikcie z
kompatybilnością z slocate.

%prep
%setup -q

%build
%configure \
	--localstatedir=/var/lib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL='install -p' \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.daily}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/updatedb.conf
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/%{name}
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/%{name}.db

install -d  $RPM_BUILD_ROOT%{systemdunitdir}
install -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/cronjob-%{name}.timer
install -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/cronjob-%{name}.service

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 196 %{name}

%post
if [ ! -f %{_localstatedir}/lib/%{name}/%{name}.db ]; then
	echo 'Run "%{_bindir}/updatedb" if you want to make %{name} database immediately.'
fi
%systemd_post cronjob-%{name}.timer

%preun
%systemd_preun cronjob-%{name}.timer

%postun
if [ "$1" = "0" ]; then
	%groupremove %{name}
fi
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) /etc/cron.daily/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/updatedb.conf
%attr(2755,root,mlocate) %{_bindir}/locate
%attr(755,root,root) %{_bindir}/updatedb
%{_mandir}/man1/locate.1*
%{_mandir}/man5/%{name}.db.5*
%{_mandir}/man5/updatedb.conf.5*
%{_mandir}/man8/updatedb.8*
%dir %attr(750,root,mlocate) /var/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}/%{name}.db
%{systemdunitdir}/cronjob-%{name}.service
%{systemdunitdir}/cronjob-%{name}.timer
