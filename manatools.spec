%define upstream_name    ManaTools
%define upstream_version 1.1.7
%define yui_major   7
%define internal_ver 0

%global debug_package %{nil}

Name:          manatools
Version:       %perl_convert_version %{upstream_version}
Release:       2%{?dist}

Summary:       ManaTools is a collection of user-friendly system configuration tools
License:       GPLv2+
Group:         System/Configuration
# TODO fix url when git is moved accordingly
Url:           http://gitweb.mageia.org/software/manatools/
Source0:       http://gitweb.mageia.org/software/manatools/snapshot/%{name}-master.tar.xz

Obsoletes:     adminpanel < 1.0.0-1

BuildRequires: gettext
BuildRequires: itstool
BuildRequires: perl(ExtUtils::CBuilder) >= 0.270.0
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.520.0
BuildRequires: perl(File::ShareDir::Install)
BuildRequires: perl(Test::More) >= 0.820.0
BuildRequires: perl-devel

Requires:      bash-completion
Requires:      perl-MDK-Common >= 1.1.18-2
Requires:      perl-MooseX-Getopt
Requires:      perl-URPM >= 3.07-2
Requires:      perl-USER
Requires:      perl-yui
Requires:      polkit
Requires:      urpmi >= 7.30
Requires:      %{_lib}yui%{yui_major}-ncurses
Requires:      %{_lib}yui%{yui_major}-mga-ncurses
Recommends:    manatools-gui

%description
ManaTools is a collection of configuration tools that allows
users to configure most of their system components in a very simple,
intuitive and attractive interface. It consists of some modules
that can be also run as autonomous applications.

Its entry point is 'mpan', which acts as an overview for all the
distinct Manatools.

ManaTools started as a porting of MCC (Mageia/Mandriva Control Center)
to libYui (Suse widget abstraction library), but its aim is to give
an easy and common interface to developer to add new modules based
on libYui. Every modules as well as ManaTools itself can be run
using Qt, GTK+ or ncurses interface.

%package qt
Summary:        ManaTools for Qt
Group:          System/Configuration
Provides:       manatools-gui
Requires:       manatools
Requires:       manatools-common
Requires:       %{_lib}yui%{yui_major}-qt
Requires:       %{_lib}yui%{yui_major}-mga-qt
Obsoletes:      adminpanel-qt < 1.0.0-1

%description qt
manatools-qt is a meta-package containing Qt dependency for manatools.
It allows the use of the Qt graphical interface.

%package gtk
Summary:        ManaTools for GTK+
Group:          System/Configuration
Provides:       manatools-gui
Requires:       manatools
Requires:       manatools-common
Requires:       %{_lib}yui%{yui_major}-gtk
Requires:       %{_lib}yui%{yui_major}-mga-gtk
Obsoletes:      adminpanel-gtk < 1.0.0-1

%description gtk
manatools-gtk is a meta-package containing GTK+ dependency for manatools.
It allows the use of the GKT+ graphical interface.

%package common
Summary:        Shared files for Qt and GTK+ flavours of ManaTools
Group:          System/Configuration

%description common
This package contains shared files used by both the Qt and GTK+ flavours of
ManaTools, which are however not strictly necessary for the ncurses flavour
in the main manatools package.

%package extra
Summary:        ManaTools extra modules
Group:          System/Configuration
Requires:       manatools
Obsoletes:      adminpanel-extra < 1.0.0-1
Requires:       python-yui

%description extra
manatools-extra contains some extra modules written in python.

%prep
%setup -q -n %{name}-master
%autopatch -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor INSTALLSITEBIN=%{_bindir}
%make_build CFLAGS="%{optflags}"

%install
%make_install PREFIX=%{buildroot}%{_prefix} install_locales

%find_lang %{name}

# NOTE removing files needed to localize configurations
find extras -name "*.in" -type f -delete
find extras -name "*.its" -type f -delete

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -R extras/conf/* %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
cp -R extras/polkit/* %{buildroot}%{_datadir}/polkit-1/actions

mkdir -p %{buildroot}%{_datadir}/applications
cp -R extras/desktop/* %{buildroot}%{_datadir}/applications

#icons TODO fixing
install -d %{buildroot}%{_iconsdir}
install -m644 share/images/mana*.png %{buildroot}%{_iconsdir}
install -m644 share/images/mpan.png %{buildroot}%{_iconsdir}

#bash completions
install -d -m755 %{buildroot}%{_datadir}/bash-completion/completions
install -m644 extras/bash_completion/mana %{buildroot}%{_datadir}/bash-completion/completions/mana

%check
#make test

%files qt

%files gtk

%files common
%{_datadir}/applications/*.desktop
%{_iconsdir}/*.png

%files extra
%{_bindir}/contribfinder.py

%files -f manatools.lang
%doc Changes README.md MODULE_HACKING COPYING.GPLv2
%{perl_vendorlib}/%{upstream_name}
%{perl_vendorlib}/auto/share/dist/%{name}
%{_bindir}/mana*
%{_bindir}/*dragora*
%{_bindir}/mpan
%{_datadir}/bash-completion/completions/mana
%{_datadir}/polkit-1/actions/org.mageia.*.policy
%{_mandir}/man1/*.1*
%{_mandir}/man3/ManaTools*.3*
%dir %{_sysconfdir}/%{name}/
%config %{_sysconfdir}/%{name}/mpan/categories.conf.d/*
%config(noreplace) %{_sysconfdir}/%{name}/mpan/settings.conf
%config(noreplace) %{_sysconfdir}/%{name}/mpan/categories.conf
%config(noreplace) %{_sysconfdir}/%{name}/manauser/manauser
%config(noreplace) %{_sysconfdir}/%{name}/manawall/spec.conf
