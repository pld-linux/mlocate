Summary:	A locate/updatedb implementation
Name:		mlocate
Version:	0.20
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	https://fedorahosted.org/mlocate/attachment/wiki/MlocateDownloads/%{name}-%{version}.tar.bz2?format=raw
# Source0-md5:	ad5e4eb1f2aecf1a5af9fe36c6e297f4
URL:		https://fedorahosted.org/mlocate/
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mlocate is a new locate implementation. The "m" stands for "merging",
because updatedb reuses the existing database to avoid rereading most
of the file system, which makes updatedb faster and does not trash the
system caches as much. The locate(1) utility is intended to be
completely compatible to slocate. It also attempts to be compatible to
GNU locate, when it does not conflict with slocate compatibility.

%prep
%setup -q

%build

%configure
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ABOUT-NLS AUTHORS ChangeLog NEWS README

%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
