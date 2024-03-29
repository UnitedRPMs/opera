#
# spec file for package opera
#
# Copyright (c) 2022 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

AutoReqProv: no
%global debug_package %{nil}
%global __mangle_shebangs_exclude_from %{_bindir}
%global __mangle_shebangs_exclude_from %{_libdir}


%ifarch x86_64
%global arch amd64
%global fearch x86_64
%else
%global arch i386
%global fearch i386
%endif

%define deb_opera %{name}-stable_%{version}_%{arch}.deb

Summary: A fast and secure web browser
Name: opera
Version: 85.0.4341.47
Release: 4%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://www.opera.com/
# You can download the latest opera source with the opera-snapshot.sh
Source0: http://get.geo.opera.com.global.prod.fastly.net/pub/%{name}/desktop/%{version}/linux/%{deb_opera}
Source1: opera-snapshot.sh
Source2: opera
Source3: com.opera.opera.metainfo.xml
Patch:   widevine_fix.patch
Patch1:  ffmpeg_patch.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: systemd-libs
#Requires: libudev0
Requires: openssl1
Requires: gtk2
Requires: desktop-file-utils
Requires: shared-mime-info
Requires: libXtst
Requires: GConf2
Requires: curl
Requires: libXScrnSaver
Requires: glibc
Requires: alsa-lib
Requires: nss
Requires: freetype
#Requires: chromium-freeworld-libs-media
BuildRequires: binutils xz tar systemd-libs wget curl 
Obsoletes: opera-stable = %{version}
Conflicts: opera-beta opera-next opera-developer
Recommends: chromium-pepper-flash 
#Recommends: chromium-widevine

%description
Opera is a browser with innovative features, speed and security. 
The browser delivers a highly customizable start page (Speed Dial) 
where you can set your top sites and bookmarks, Off-road mode for 
data saving and faster browsing in slow networks such as 3G/2G and 
public Wi-Fi, a "Discover" page for getting the best of the web's 
content; and in the desktop version Stash, a tool for comparing 
pages and "read it later".

%prep

# extract data from the deb package
install -dm 755 %{_builddir}/%{name}-%{version}
ar x %{SOURCE0} 
if [ -f data.tar.xz ]; then
tar xJf data.tar.xz -C %{_builddir}/%{name}-%{version}
elif [ -f data.tar.gz ]; then 
tar xmzvf data.tar.gz -C %{_builddir}/%{name}-%{version}
fi

%setup -T -D %{name}-%{version} 

pushd usr/lib/x86_64-linux-gnu/opera/resources/
#patch -p0
%patch1 -p0
popd

%build


%install

# Make destiny directories
install -dm 755 %{buildroot}/%{_libdir} \
%{buildroot}/%{_bindir} 

# rename libdir
mv -f usr/lib/%{fearch}-linux-gnu/%{name} %{buildroot}/%{_libdir}/
mv -f usr/share %{buildroot}/%{_prefix}


cp -f %{S:2} %{buildroot}/%{_bindir}/%{name}

chmod a+x %{buildroot}/%{_bindir}/%{name} 


# delete some directories that is not needed on Fedora
rm -rf %{buildroot}/%{_datadir}/{lintian,menu}

# correct opera_sandbox permission
# FATAL:setuid_sandbox_client.cc(283)] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /usr/lib64/opera-developer/opera_sandbox is owned by root and has mode 4755.
chmod 4755 $RPM_BUILD_ROOT%{_libdir}/%{name}/opera_sandbox

# We are using a full ffmpeg in UnitedRPMs
#rm -f %{buildroot}/%{_libdir}/%{name}/libffmpeg.so
#pushd %{buildroot}/%{_libdir}/%{name}/
#ln -sf %{_libdir}/chromium/libffmpeg.so libffmpeg.so
#popd

# Install AppData
  install -Dm 0644 %{S:3} %{buildroot}/%{_metainfodir}/com.opera.opera.metainfo.xml

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/opera.desktop
%{_docdir}/opera-stable/
%{_datadir}/icons/hicolor/*/apps/opera.png
%{_datadir}/pixmaps/opera.xpm
%{_datadir}/mime/packages/opera-stable.xml
%{_metainfodir}/com.opera.opera.metainfo.xml


%changelog

* Thu Mar 31 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 85.0.4341.47-4
- Updated to 85.0.4341.47

* Thu Mar 03 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 84.0.4316.31-4
- Updated to 84.0.4316.31

* Fri Jan 14 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 82.0.4227.58-4
- Updated to 82.0.4227.58

* Wed Nov 24 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 81.0.4196.60-4
- Updated to 81.0.4196.60

* Fri Nov 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 81.0.4196.31-4
- Updated to 81.0.4196.37

* Fri Oct 22 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 80.0.4170.63-4
- Updated to 80.0.4170.63

* Sat Oct 02 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 79.0.4143.72-4
- Updated to 79.0.4143.72

* Fri Sep 24 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 79.0.4143.66-4
- Updated to 79.0.4143.66

* Tue Sep 14 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 79.0.4143.22-4
- Updated to 79.0.4143.22

* Fri Sep 03 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 78.0.4093.184-4
- Updated to 78.0.4093.184

* Thu Aug 26 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 78.0.4093.184-4
- Updated to 78.0.4093.184

* Mon Aug 16 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 78.0.4093.147-4
- Updated to 78.0.4093.147

* Wed Jul 28 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 77.0.4054.277-4
- Updated to 77.0.4054.277

* Thu Jul 01 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 77.0.4054.172-4
- Updated to 77.0.4054.172

* Fri Jun 11 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 77.0.4054.64-4
- Updated to 77.0.4054.64

* Fri May 28 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 76.0.4017.154-4
- Updated to 76.0.4017.154

* Mon Apr 26 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 75.0.3969.218-4
- Updated to 75.0.3969.218

* Sat Apr 17 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 75.0.3969.149-4
- Updated to 75.0.3969.149

* Sat Mar 27 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 75.0.3969.93-4
- Updated to 75.0.3969.93

* Sat Mar 20 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 74.0.3911.232-4
- Updated to 74.0.3911.232

* Mon Feb 15 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 74.0.3911.154-4
- Updated to 74.0.3911.154

* Mon Jan 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 73.0.3856.344-4
- Updated to 73.0.3856.344

* Wed Jan 06 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 73.0.3856.329-4
- Updated to 73.0.3856.329

* Mon Nov 30 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 72.0.3815.400-4
- Updated to 72.0.3815.400

* Fri Nov 06 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 72.0.3815.207-4
- Updated to 72.0.3815.207

* Sat Oct 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 72.0.3815.148-4
- Updated to 72.0.3815.148

* Wed Oct 14 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 71.0.3770.271-4
- Updated to 71.0.3770.271

* Mon Oct 12 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 71.0.3770.228-4
- Updated to 71.0.3770.228

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 71.0.3770.198-4
- Updated to 71.0.3770.198

* Thu Sep 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 71.0.3770.171-4
- Updated to 71.0.3770.171

* Mon Sep 14 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 71.0.3770.148-4
- Updated to 71.0.3770.148

* Fri Aug 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 70.0.3728.133-4
- Updated to 70.0.3728.133

* Mon Jul 13 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 69.0.3686.57-4
- Rebuilt

* Thu Jul 09 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 69.0.3686.57-3
- Updated to 69.0.3686.57

* Fri Jul 03 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 69.0.3686.49-3
- Updated to 69.0.3686.49

* Thu Jun 11 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 68.0.3618.165-3
- Updated to 68.0.3618.165

* Wed May 20 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 68.0.3618.125-3
- Updated to 68.0.3618.125

* Fri Feb 17 2017 David Vásquez <davidva AT tutanota DOT com> - 43.0.2442.806-1
- Updated to 43.0.2442.806-1
- Support h264

* Fri Jan 13 2017 David Vásquez <davidva AT tutanota DOT com> - 42.0.2393.94-2
- Support chromium-widevine

* Fri Nov 06 2015 David Vásquez <davidva AT tutanota DOT com> - 33.0.1990.58-2
- Recommended chromium-pepper-flash

* Sat May 23 2015 David Vásquez <davidva AT tutanota DOT com> - 29.0.1795.60-1
- Updated to - 29.0.1795.60
- Deleted bundled libraries (ssl)
- Rewrited spec, for future compatibility of Opera 32bits

* Wed Mar 18 2015 David Vásquez <davidva AT tutanota DOT com> - 28.0.1750.48-1
- Updated to - 28.0.1750.48-1

* Wed Jan 28 2015 David Vásquez <davidva AT tutanota DOT com> - 27.0.1689.54-1
- Updated to 27.0.1689.54

* Sat Jan 10 2015 David Vásquez <davidva AT tutanota DOT com> - 26.0.1656.60-1
- Upstream
- Updated to 26.0.1656.60
- replaced libudev.so.0 symlink for libudev0
- Added snapshot, it will download the current Opera deb version.

* Wed Oct 22 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1655.0-2
- delete post and postun section
- install libudev.so.0 symlink in install section
