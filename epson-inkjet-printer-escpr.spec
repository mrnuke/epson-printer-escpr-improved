# The lsb release used in the tarball name
%global lsb 1lsb3.2

Name:           epson-inkjet-printer-escpr
Summary:        Drivers for Epson inkjet printers
Group:          Applications/System
Version:        1.6.18
Release:        1
License:        GPLv2+
URL:            http://download.ebz.epson.net/dsc/search/01/search/?OSC=LX
# Download address is garbled on web page
Source0:        %{name}-%{version}.tar.gz
# PPD files extracted from escpr2 tarball, but tested and compatible with escpr
Source1:        Epson-ET-3700_Series-epson-escpr-en.ppd

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  chrpath
BuildRequires:  cups-devel
BuildRequires:  libjpeg-devel

# For automatic detection of printer drivers
BuildRequires:  python3-cups
# For dir ownership
Requires:       cups-filesystem
# So that automatic printer driver installation works
BuildRequires:  python-cups

%description
This package contains drivers for Epson Inkjet printers that use 
the New Generation Epson Printer Control Language.

For a detailed list of supported printers, please refer to
http://avasys.jp/english/linux_e/

%prep
%setup -q

# Fix permissions
find . -name \*.h -exec chmod 644 {} \;
find . -name \*.c -exec chmod 644 {} \;
for f in README README.ja COPYING AUTHORS NEWS; do
 chmod 644 $f
done

%build
autoconf
%configure --disable-static --enable-shared --disable-rpath
# SMP make doesn't work
#make %{?_smp_mflags}
make

%install
make install DESTDIR=%{buildroot} CUPS_PPD_DIR=%{_datadir}/ppd/Epson
# Get rid of .la files
rm -f %{buildroot}%{_libdir}/*.la
# Copy extra PPD files
cp Epson-ET-3700_Series-epson-escpr-en.ppd %{buildroot}%{_datadir}/ppd/Epson/epson-inkjet-printer-escpr
# Compress ppd files
for ppd in %{buildroot}%{_datadir}/ppd/Epson/epson-inkjet-printer-escpr/*.ppd; do
 gzip $ppd
done
# Get rid of rpath
chrpath --delete %{buildroot}%{_cups_serverbin}/filter/epson-escpr
# Copy documentation
cp -a README README.ja COPYING AUTHORS NEWS ..

# Get rid of .so file, since no headers are installed.
rm %{buildroot}%{_libdir}/libescpr.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README README.ja COPYING AUTHORS NEWS
%{_cups_serverbin}/filter/epson-*
%{_datadir}/ppd/Epson/
%{_libdir}/libescpr.so.*
