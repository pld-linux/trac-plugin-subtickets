%define		trac_ver	0.12
%define		plugin		subtickets
Summary:	Subtickets support for Trac tickets
Name:		trac-plugin-%{plugin}
Version:	0.1.0
Release:	1
License:	BSD
Group:		Applications/WWW
Source0:	http://trac-hacks.org/attachment/wiki/SubticketsPlugin/TracSubTicketsPlugin-%{version}.zip?format=raw
# Source0-md5:	4a541b176f0793d2bbc6f5a3fd95a028
URL:		http://trac-hacks.org/wiki/SubticketsPlugin
BuildRequires:	python-devel
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin offers sub-ticket feature for managing tickets.

%prep
%setup -q -n TracSubTicketsPlugin-%{version}

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin "tracsubtickets.*"
if [ "$1" -eq 1 ]; then
	echo "Do not forget to upgrade env: trac-admin ENV upgrade"
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/check-trac-subtickets
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/*-*.egg-info
