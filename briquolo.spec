%define name	briquolo
%define version 0.5.7
%define release %mkrel 2
%define Summary	An OpenGL breakout

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
Source0:	http://briquolo.free.fr/download/%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.5.6-desktop-install.patch
Patch1:		%{name}-0.5.5-desktop-remove-double-category.patch
Patch2:		briquolo-0.5.7-gcc43.patch
Patch3:		briquolo-0.5.6-fix-icon-install.patch
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}-48.png
BuildRequires:	SDL-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	SDL_mixer1.2-devel
BuildRequires:	dos2unix
BuildRequires:	png-devel
BuildRequires:	mesaglut-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
Group:		Games/Arcade
License:	GPLv2+
URL:		http://briquolo.free.fr/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Briquolo is a 3D brick game using OpenGL

%prep
%setup -q
dos2unix data/tableau/old/{001,002,003,006}.tab
%patch0 -p1 -b .desktop
%patch1 -p1 -b .remove_category
%patch2 -p0 -b .gcc
%patch3 -p0 -b .icon

%build
autoreconf -fi
%configure2_5x --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#this empty file makes rpmlint shouting otherwise...
echo %{version} > %{buildroot}%{_gamesdatadir}/%{name}/%{version}

mv %buildroot%_gamesdatadir/locale %buildroot%_datadir
mv %buildroot%_gamesdatadir/pixmaps %buildroot%_datadir

%find_lang %{name}

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

desktop-file-install --vendor="" --delete-original \
	--add-category="X-MandrivaLinux-MoreApplications-Games-Arcade" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_gamesdatadir}/applications/*

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS ChangeLog DejaVuSans.ttf-LICENSE README.fr
%attr(0755,root,games) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/briquolo.desktop
%{_datadir}/pixmaps/briquolo.svg
