#
# Conditional build:
%bcond_with	apidocs		# build and package API docs (withdrawn in 1.5)
%bcond_with	fortran		# Fortran interface (removed from 1.5 sources)
%bcond_without	hdf5		# HDF5-based MAT v7.3 files support
#
Summary:	MATIO - Matlab MAT file I/O library
Summary(pl.UTF-8):	MATIO - biblioteka wejścia/wyjścia do plików MAT (Matlaba)
Name:		matio
Version:	1.5.27
Release:	3
License:	BSD
Group:		Libraries
Source0:	https://downloads.sourceforge.net/matio/%{name}-%{version}.tar.gz
# Source0-md5:	d9e55f091cbecbe988d4579a51c08776
Patch0:		%{name}-hdf5.patch
URL:		https://matio.sourceforge.net/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.8
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_fortran:BuildRequires:	gcc-fortran}
%{?with_hdf5:BuildRequires:	hdf5-devel >= 1.10}
BuildRequires:	libtool >= 2:2
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-makeindex
%endif
Obsoletes:	matio-apidocs < 1.5
Obsoletes:	matio-fortran < 1.5
Obsoletes:	matio-fortran-devel < 1.5
Obsoletes:	matio-fortran-static < 1.5
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
%{?with_hdf5:Requires:	hdf5-devel >= 1.10}
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

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_fortran:--enable-fortran} \
	%{!?with_hdf5:--disable-mat73}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmatio.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/matdump
%attr(755,root,root) %{_libdir}/libmatio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatio.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatio.so
%{_includedir}/matio*.h
%{_pkgconfigdir}/matio.pc
%{_mandir}/man3/Mat_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmatio.a

%if %{with fortran}
%files fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatio-fortran.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatio-fortran.so.2

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
