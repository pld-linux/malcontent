#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	gui		# UI library and app (disable for flatpak bootstrap)
#
Summary:	Library providing access to parental control settings
Summary(pl.UTF-8):	Biblioteka zapewniająca dostęp do ustawień kontroli rodzicielskiej
Name:		malcontent
Version:	0.12.0
Release:	1
License:	LGPL v2.1+ (library), CC-AS-SA v3.0 (docs)
Group:		Applications
#Source0Download: https://gitlab.freedesktop.org/pwithnall/malcontent/-/tags
Source0:	https://gitlab.freedesktop.org/pwithnall/malcontent/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	481685ce3cf72f3e8ef1affe06dd1f6c
Patch0:		no-cache-update.patch
URL:		https://gitlab.freedesktop.org/pwithnall/malcontent
%{?with_gui:BuildRequires:	AppStream-devel >= 0.12.10}
%{?with_gui:BuildRequires:	accountsservice-devel >= 0.6.39}
# appstream-util in malcontent-control/meson.build
BuildRequires:	appstream-glib >= 0.7.15
BuildRequires:	dbus-devel
BuildRequires:	flatpak-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.60.1
BuildRequires:	gobject-introspection-devel
%{?with_gui:BuildRequires:	gtk4-devel >= 4.12}
%{?with_gui:BuildRequires:	libadwaita-devel >= 1.1}
BuildRequires:	libglib-testing-devel
BuildRequires:	meson >= 1.2.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
%if %{with gui}
Requires:	accountsservice >= 0.6.39
Requires:	libmalcontent-ui = %{version}-%{release}
%endif
Requires:	python3-pygobject3 >= 3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
malcontent implements support for restricting the type of content
accessible to non-administrator accounts on a Linux system. Typically,
when this is used, a non-administrator account will be for a child
using the system; and the administrator accounts will be for the
parents; and the content being filtered will be apps which are not
suitable for the child to use, due to (for example) being too violent.

%description -l pl.UTF-8
malcontent implementuje obsługę ograniczania rodzaju treści dostępnych
dla kont innych niż administrator w systemie Linux. W typowym
przypadku użycia konto nie-administratora będzie dla dziecka
korzystającego z systemu, a konta administratora dla rodziców; treścią
filtrowaną będą aplikacje niewłaściwe dla dzieci ze względu np. na
przemoc.

%package -n libmalcontent
Summary:	Library providing access to parental control settings
Summary(pl.UTF-8):	Biblioteka zapewniająca dostęp do ustawień kontroli rodzicielskiej
Group:		Libraries
Requires:	glib2 >= 1:2.60.1

%description -n libmalcontent
Library providing access to parental control settings.

%description -n libmalcontent -l pl.UTF-8
Biblioteka zapewniająca dostęp do ustawień kontroli rodzicielskiej.

%package -n libmalcontent-devel
Summary:	Header files for libmalcontent library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmalcontent
Group:		Development/Libraries
Requires:	libmalcontent = %{version}-%{release}
Requires:	glib2-devel >= 1:2.60.1

%description -n libmalcontent-devel
Header files for libmalcontent library.

%description -n libmalcontent-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmalcontent.

%package -n libmalcontent-static
Summary:	Static libmalcontent library
Summary(pl.UTF-8):	Statyczna biblioteka libmalcontent
Group:		Development/Libraries
Requires:	libmalcontent-devel = %{version}-%{release}

%description -n libmalcontent-static
Static libmalcontent library.

%description -n libmalcontent-static -l pl.UTF-8
Statyczna biblioteka libmalcontent.

%package -n libmalcontent-ui
Summary:	Library providing widgets for parental control settings
Summary(pl.UTF-8):	Biblioteka zapewniająca kontrolki do ustawień kontroli rodzicielskiej
Group:		Libraries
Requires:	AppStream >= 0.12.10
Requires:	accountsservice-libs >= 0.6.39
Requires:	gtk4 >= 4.12
Requires:	libadwaita >= 1.1
Requires:	libmalcontent = %{version}-%{release}

%description -n libmalcontent-ui
Library providing widgets for parental control settings.

%description -n libmalcontent-ui -l pl.UTF-8
Biblioteka zapewniająca kontrolki do ustawień kontroli rodzicielskiej.

%package -n libmalcontent-ui-devel
Summary:	Header files for libmalcontent-ui library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmalcontent-ui
Group:		Development/Libraries
Requires:	AppStream-devel >= 0.12.10
Requires:	libmalcontent-devel = %{version}-%{release}
Requires:	libmalcontent-ui = %{version}-%{release}
Requires:	accountsservice-devel >= 0.6.39
Requires:	flatpak-devel
Requires:	gtk4-devel >= 4.12
Requires:	libadwaita-devel >= 1.1

%description -n libmalcontent-ui-devel
Header files for libmalcontent-ui library.

%description -n libmalcontent-ui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmalcontent-ui.

%package -n libmalcontent-ui-static
Summary:	Static libmalcontent-ui library
Summary(pl.UTF-8):	Statyczna biblioteka libmalcontent-ui
Group:		Development/Libraries
Requires:	libmalcontent-ui-devel = %{version}-%{release}

%description -n libmalcontent-ui-static
Static libmalcontent-ui library.

%description -n libmalcontent-ui-static -l pl.UTF-8
Statyczna biblioteka libmalcontent-ui.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' malcontent-client/malcontent-client.py

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Dpamlibdir=/%{_lib}/security \
	-Dui=%{__enabled_disabled gui}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{without gui}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{accountsservice,help,polkit-1}
%endif

%find_lang %{name} %{?with_gui:--with-gnome}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libmalcontent -p /sbin/ldconfig
%postun	-n libmalcontent -p /sbin/ldconfig

%post	-n libmalcontent-ui -p /sbin/ldconfig
%postun	-n libmalcontent-ui -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/malcontent-client
%attr(755,root,root) /%{_lib}/security/pam_malcontent.so
%{_datadir}/dbus-1/interfaces/com.endlessm.ParentalControls.*.xml
%{_mandir}/man8/malcontent-client.8*

%if %{with gui}
%attr(755,root,root) %{_bindir}/malcontent-control
%{_datadir}/accountsservice/interfaces/com.endlessm.ParentalControls.*.xml
%{_datadir}/metainfo/org.freedesktop.MalcontentControl.appdata.xml
%{_datadir}/polkit-1/actions/com.endlessm.ParentalControls.policy
%{_datadir}/polkit-1/actions/org.freedesktop.MalcontentControl.policy
%{_datadir}/polkit-1/rules.d/com.endlessm.ParentalControls.rules
%{_desktopdir}/org.freedesktop.MalcontentControl.desktop
%{_iconsdir}/hicolor/scalable/apps/org.freedesktop.MalcontentControl.svg
%{_iconsdir}/hicolor/symbolic/apps/org.freedesktop.MalcontentControl-symbolic.svg
%endif

%files -n libmalcontent
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmalcontent-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmalcontent-0.so.0
%{_libdir}/girepository-1.0/Malcontent-0.typelib

%files -n libmalcontent-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmalcontent-0.so
%{_includedir}/malcontent-0
%{_datadir}/gir-1.0/Malcontent-0.gir
%{_pkgconfigdir}/malcontent-0.pc

%if %{with static_libs}
%files -n libmalcontent-static
%defattr(644,root,root,755)
%{_libdir}/libmalcontent-0.a
%endif

%if %{with gui}
%files -n libmalcontent-ui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmalcontent-ui-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmalcontent-ui-1.so.1
%{_libdir}/girepository-1.0/MalcontentUi-1.typelib

%files -n libmalcontent-ui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmalcontent-ui-1.so
%{_includedir}/malcontent-ui-1
%{_datadir}/gir-1.0/MalcontentUi-1.gir
%{_pkgconfigdir}/malcontent-ui-1.pc

%if %{with static_libs}
%files -n libmalcontent-ui-static
%defattr(644,root,root,755)
%{_libdir}/libmalcontent-ui-1.a
%endif
%endif
