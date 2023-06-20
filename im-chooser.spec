%if 0%{!?_with_xfce:1} && 0%{!?_without_xfce:1}
#%if 0%{?rhel}
%global _with_xfce 0
#%else
#%global _with_xfce 1
#%endif
%endif

Name:		im-chooser
Version:	1.7.1
Release:	10
License:	GPLv2+ and LGPLv2+
URL:		http://pagure.io/im-chooser/
%{?_with_gtk2:BuildRequires:	gtk2-devel}
%{!?_with_gtk2:BuildRequires:	gtk3-devel}
BuildRequires:	libSM-devel imsettings-devel >= 1.3.0
%if 0%{?_with_xfce}
BuildRequires:	libxfce4util-devel
%endif
BuildRequires:	desktop-file-utils intltool gettext
BuildRequires:	gcc
BuildRequires:	libxfce4util-devel

Source0:	http://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2

Summary:	Desktop Input Method configuration tool
Obsoletes:	im-chooser-gnome3 < 1.4.2-2
Provides:	im-chooser-gnome3 = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}

%description
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

%package	common
Summary:	Common files for im-chooser subpackages
Requires:	imsettings >= 1.3.0
Obsoletes:	im-chooser < 1.5.0.1
## https://fedorahosted.org/fpc/ticket/174
Provides:	bundled(egglib)

%description	common
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

This package contains the common libraries/files to be used in
im-chooser subpackages.

%if 0%{?_with_xfce}
%package	xfce
Summary:	XFCE settings panel for im-chooser
Requires:	%{name}-common = %{version}-%{release}
Obsoletes:	im-chooser < 1.5.0.1

%description	xfce
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

This package contains the XFCE settings panel for im-chooser.
%endif


%prep
%autosetup

%build
%if "%toolchain" == "clang"
	export CFLAGS="$CFLAGS -Wno-error=format-nonliteral"
	export CXXFLAGS="$CXXFLAGS -Wno-error=format-nonliteral"
%endif
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
	--vendor=fedora				\
%endif
	--add-category=X-GNOME-PersonalSettings			\
	--delete-original					\
	--dir=$RPM_BUILD_ROOT%{_datadir}/applications		\
	$RPM_BUILD_ROOT%{_datadir}/applications/im-chooser.desktop
%if 0%{?_with_xfce}
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/xfce4-im-chooser.desktop
%endif
#%%{!?_with_gtk2:desktop-file-validate $RPM_BUILD_ROOT%%{_datadir}/applications/im-chooser-panel.desktop}

rm -rf $RPM_BUILD_ROOT%{_libdir}/libimchooseui.{so,la,a}
#%%{!?_with_gtk2:rm -rf $RPM_BUILD_ROOT%%{_libdir}/control-center-1/panels/libim-chooser.{a,la}}

# disable panel so far
rm -rf $RPM_BUILD_ROOT%{_libdir}/control-center-1/panels/libim-chooser.so
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications/im-chooser-panel.desktop

%find_lang %{name}


%ldconfig_scriptlets	common

%files
%{_bindir}/im-chooser
%if 0%{?fedora} && 0%{?fedora} < 19
%{_datadir}/applications/fedora-im-chooser.desktop
%else
%{_datadir}/applications/im-chooser.desktop
%endif
%{_mandir}/man1/im-chooser.1*

%files	common -f %{name}.lang
%doc AUTHORS ChangeLog README
%license COPYING
%{_libdir}/libimchooseui.so.*
%{_datadir}/icons/hicolor/*/apps/im-chooser.png
%dir %{_datadir}/imchooseui
%{_datadir}/imchooseui/imchoose.ui

%if 0%{?_with_xfce}
%files	xfce
%{_bindir}/xfce4-im-chooser
%{_datadir}/applications/xfce4-im-chooser.desktop
#/usr/lib/debug/usr/bin/xfce4-im-chooser-1.7.1-7.isoft.aarch64.debug
%endif

%changelog
* Tue Jun 20 2023 yoo <sunyuechi@iscas.ac.cn> - 1.7.1-10
- fix clang build error

* Mon Dec 13 2021 zhangshaoning <zhangshaoning@uniontech.com> - 1.7.1-9
- delete %dist.

* Mon May 26 2021 isoft <isoft@isoft-linux.com> - 1.7.1-7
- Rebuilt for iSoft
* Fri Feb 01 2019 isoft <isoft@isoft-linux.com> - 1.7.1-7
- Rebuilt for iSoft

