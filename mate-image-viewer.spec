Summary:	MATE image viewer
Name:		mate-image-viewer
Version:	1.6.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/sources/mate-image-viewer/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	de728693721f1b35166f7687bba1f70d
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	exempi-devel
BuildRequires:	gettext-devel
BuildRequires:	mate-desktop-devel
BuildRequires:	intltool
BuildRequires:	lcms-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eye of MATE is a tool for viewing/cataloging images.

%package devel
Summary:	Development files
Group:		Development/Libraries

%description devel
Eye of the MATE Development files.

%package apidocs
Summary:	Eye of the MATE API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Eye of the MATE API documentation.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
mate-doc-prepare --copy --force
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-python		\
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/eom.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*/*/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang eom --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%files -f eom.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/eom
%dir %{_libdir}/eom
%dir %{_libdir}/eom/plugins
%attr(755,root,root) %{_libdir}/eom/plugins/*.so
%{_libdir}/eom/plugins/*-plugin
%{_datadir}/mate-image-viewer
%{_datadir}/glib-2.0/schemas/org.mate.eom.gschema.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/eom.*
%{_mandir}//man1/eom.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/eom-2.20
%{_pkgconfigdir}/*.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/eom

