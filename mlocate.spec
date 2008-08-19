Summary:	A locate/updatedb implementation
Summary(pl.UTF-8):	Implementacja locate/updatedb
Name:		mlocate
Version:	0.21
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	https://fedorahosted.org/releases/m/l/mlocate/%{name}-%{version}.tar.bz2
# Source0-md5:	51c8e6a40079542923c0a1411512c57d
URL:		https://fedorahosted.org/mlocate/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
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
install -d $RPM_BUILD_ROOT/var/lib/mlocate

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 196 mlocate

%post
if [ ! -f /var/lib/mlocate/mlocate.db ]; then
	echo 'Run "%{_bindir}/updatedb" if you want to make mlocate database immediately.'
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove mlocate
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(2755,root,mlocate) %{_bindir}/locate
%attr(755,root,root) %{_bindir}/updatedb
%{_mandir}/man1/locate.1*
%{_mandir}/man5/mlocate.db.5*
%{_mandir}/man5/updatedb.conf.5*
%{_mandir}/man8/updatedb.8*
%dir %attr(750,root,mlocate) /var/lib/mlocate
