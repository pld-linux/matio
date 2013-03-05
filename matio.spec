#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	fortran		# Fortran interface
#
Summary:	MATIO - Matlab MAT file I/O library
Summary(pl.UTF-8):	MATIO - biblioteka wejścia/wyjścia do plików MAT (Matlaba)
Name:		matio
Version:	1.3.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/matio/%{name}-%{version}.tar.gz
# Source0-md5:	a91208cf18f2456a5855bc1a9fdb90fd
Patch0:		%{name}-link.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-separate-fortran.patch
URL:		http://matio.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_fortran:BuildRequires:	gcc-fortran}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-makeindex
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmatio is an open-source library for reading/writing Matlab MAT
files. This library is designed for use by programs/libraries that do
not have access or do not want to rely on Matlab's libmat shared
library.

%description -l pl.UTF-8
libmatio to mająca otwarte źródłą biblioteka do odczytu i zapisu
plików MAT (z programu Matlab). Jest przeznaczona dla programów i
bibliotek nie mających dostępu albo nie chcących polegać na bibliotece
współdzielonej libmat z Matlaba.

%package devel
Summary:	Header files for MATIO library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MATIO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
Header files for MATIO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MATIO.

%package static
Summary:	Static MATIO library
Summary(pl.UTF-8):	Statyczna biblioteka MATIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MATIO library.

%description static -l pl.UTF-8
Statyczna biblioteka MATIO.

%package fortran
Summary:	Fortran interface for MATIO library
Summary(pl.UTF-8):	Interfejs Fortranu do biblioteki MATIO
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description fortran
Fortran interface for MATIO library.

%description fortran -l pl.UTF-8
Interfejs Fortranu do biblioteki MATIO.

%package fortran-devel
Summary:	Header file for Fortran interface for MATIO library
Summary(pl.UTF-8):	Plik nagłówkowy interfejsu Fortranu do biblioteki MATIO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-fortran = %{version}-%{release}

%description fortran-devel
Header file for Fortran interface for MATIO library.

%description fortran-devel -l pl.UTF-8
Plik nagłówkowy interfejsu Fortranu do biblioteki MATIO.

%package fortran-static
Summary:	Fortran interface for MATIO library - static library
Summary(pl.UTF-8):	Interfejs Fortranu do biblioteki MATIO - biblioteka statyczna
Group:		Development/Libraries
Requires:	%{name}-fortran-devel = %{version}-%{release}

%description fortran-static
Fortran interface for MATIO library - static library.

%description fortran-static -l pl.UTF-8
Interfejs Fortranu do biblioteki MATIO - biblioteka statyczna.

%package apidocs
Summary:	MATIO API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki MATIO
Group:		Documentation

%description apidocs
API and internal documentation for MATIO library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki MATIO.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__automake}
%configure \
	%{?with_apidocs:--enable-docs} \
	%{?with_fortran:--enable-fortran} \
	--enable-shared

# parallel build is broken (matio.mod, docs)
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# keep .la - needed for -fortran

# packaged in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/matio

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libmatio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatio.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatio.so
%{_libdir}/libmatio.la
%{_includedir}/matio*.h
%{_pkgconfigdir}/matio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmatio.a

%if %{with fortran}
%files fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatio-fortran.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatio-fortran.so.0

%files fortran-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatio-fortran.so
%{_libdir}/libmatio-fortran.la
%{_includedir}/matio.mod

%files fortran-static
%defattr(644,root,root,755)
%{_libdir}/libmatio-fortran.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/latex/libmatio.pdf
%endif
