%global release_prefix          1000

Name:                           gzdoom
Version:                        4.7.1
Release:                        %{release_prefix}%{?dist}
Summary:                        An OpenGL DOOM source port with graphic and modding extensions
License:                        GPLv3
URL:                            https://zdoom.org

Source0:                        %{name}-g%{version}.tar.xz

Patch1:                         %{name}-waddir.patch
Patch2:                         %{name}-asmjit.patch

BuildRoot:                      %{_tmppath}/%{name}-%{version}-build
BuildRequires:                  gcc-c++
BuildRequires:                  make
BuildRequires:                  cmake
BuildRequires:                  tar
BuildRequires:                  git
BuildRequires:                  nasm
BuildRequires:                  glew-devel

# Todo: Patch.
# BuildRequires:  glslang-devel

# pkgconfig.
BuildRequires:                  pkgconfig(flac)
BuildRequires:                  pkgconfig(bzip2)
BuildRequires:                  pkgconfig(zlib)
BuildRequires:                  pkgconfig(liblzma)
BuildRequires:                  pkgconfig(gl)
BuildRequires:                  pkgconfig(fluidsynth)
BuildRequires:                  pkgconfig(gtk+-3.0)
BuildRequires:                  pkgconfig(sdl)
BuildRequires:                  pkgconfig(sdl2)
BuildRequires:                  pkgconfig(sndfile)
BuildRequires:                  pkgconfig(libgme)
BuildRequires:                  pkgconfig(openal)
BuildRequires:                  pkgconfig(libmpg123)
BuildRequires:                  pkgconfig(vulkan)

BuildRequires:                  timidity++
BuildRequires:                  pkgconfig(libjpeg)
BuildRequires:                  pkgconfig(wildmidi)
Requires:                       wildmidi
Requires:                       openal-soft
Requires:                       fluidsynth
Requires:                       SDL2

# ZMusic requirement.
BuildRequires:                  zmusic-devel
Requires:                       zmusic

Recommends:                     freedoom

%description
ZDoom is a family of enhanced ports (modifications) of the Doom engine for
running on modern operating systems. It runs on Windows, Linux, and OS X, and
adds new features not found in the games as originally published by id Software.

ZDoom features the following that is not found in the original Doom:

  - Runs on all modern versions of Windows, Mac, and Linux distributions.
  - Can play all Doom engine games, including Ultimate Doom, Doom II, Heretic, Hexen, Strife, and more.
  - Supports all editing features of Hexen.
  - Supports most of the Boom editing features.
  - Supports new features such as colored lighting, 3D floors, and much more.
  - All Doom limits are gone.
  - Several softsynths for MUS and MIDI playback, including OPL softsynth for an authentitc "oldschool" flavor.
  - High resolutions.
  - Quake-style console and key bindings.
  - Crosshairs.
  - Free look.
  - Jumping, crouching, swimming, and flying.
  - Up to 8 player network games using UDP/IP, including team-based gameplay.
  - Support for the Bloodbath announcer from the classic Monolith game Blood.
  - Walk over/under monsters and other things.

GZDoom provides an OpenGL renderer and HQnX rescaling.

# -------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------------< SCRIPT >----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

%prep
%setup -qn %{name}-g%{version}
%patch -P 1 -P 2 -p1

perl -i -pe 's{__DATE__}{""}g' \
  src/common/platform/posix/sdl/i_main.cpp
perl -i -pe 's{<unknown version>}{%version}g' \
  tools/updaterevision/UpdateRevision.cmake


%build
%define _lto_cflags %nil
%{cmake}                                    \
  -B builddir                               \
  -DNO_STRIP=1                              \
  -DCMAKE_SHARED_LINKER_FLAGS=""            \
  -DCMAKE_EXE_LINKER_FLAGS=""               \
  -DCMAKE_MODULE_LINKER_FLAGS=""            \
  -DBUILD_SHARED_LIBS="OFF"                 \
  -DINSTALL_DOCS_PATH="%{_docdir}/%{name}"  \
  -DINSTALL_PK3_PATH="%{_datadir}/doom"     \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo

# make_build -C builddir
%{__make} %{?_smp_mflags} -C builddir


%install
%{__rm} -rf %{buildroot}

# Install GZDoom.
%{make_install} -C builddir

%{__mkdir} -p %{buildroot}%{_datadir}/applications

# Don't know why but the XPM isn't put anywhere.
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
%{__cp} %{_builddir}/%{name}-g%{version}/src/posix/zdoom.xpm \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/gzdoom.xpm

# Fallback soundfont - Symlinking instead of copying
# as a test for now. It's not clear if the binary will look here
# or look in /usr/share/games/doom yet.
pushd %{buildroot}%{_datadir}/doom
  %{__ln_s} %{_datadir}/games/doom/soundfounts soundfonts
  %{__ln_s} %{_datadir}/games/doom/fm_banks fm_banks
popd


%post
echo "INFO: %{name}: The global IWAD directory is %{_datadir}/doom."


%files
%defattr(-, root, root, -)
%doc docs/console.css docs/console.html docs/rh-log.txt docs/licenses/* docs/skins.txt
%{_bindir}/%{name}
%{_datadir}/doom/*
%{_docdir}/%{name}/*
%{_datadir}/icons/hicolor/256x256/apps/gzdoom.xpm
%{_datadir}/games/doom/*


%changelog
* Fri Apr 01 2022 Package Store <pkgstore@mail.ru> - 4.7.1-1000
- NEW: GZDoom v4.7.1.
- UPD: Rebuild by Package Store.
- UPD: File "gzdoom.spec".

* Wed Aug 11 2021 Package Store <pkgstore@mail.ru> - 4.6.1-100
- NEW: v4.6.1.

* Fri Jun 18 2021 Package Store <pkgstore@mail.ru> - 4.6.0-102
- UPD: Add "Vendor" & "Packager" fields.

* Fri Jun 18 2021 Package Store <pkgstore@mail.ru> - 4.6.0-101
- UPD: New build for latest changes.

* Thu Jun 17 2021 Package Store <pkgstore@mail.ru> - 4.6.0-100
- NEW: v4.6.0.
- UPD: Move to GitHub.
- UPD: License.

* Tue Mar 31 2020 Package Store <pkgstore@mail.ru> - 4.3.3-101
- FIX: Delete freedoom recommends.

* Fri Mar 13 2020 Package Store <pkgstore@mail.ru> - 4.3.3-100
- NEW: v4.3.3.

* Thu Oct 03 2019 Package Store <pkgstore@mail.ru> - 4.2.1-100
- NEW: v4.2.1.

* Mon Jul 08 2019 Package Store <pkgstore@mail.ru> - 4.1.3-101
- UPD: SPEC-file.

* Mon Jul 08 2019 Package Store <pkgstore@mail.ru> - 4.1.3-100
- UPD: MARKETPLACE.

* Mon Jun 10 2019 Louis Abel <tucklesepk@gmail.com> - 4.1.3-1
- Update to 4.1.3
- Removed static patches

* Fri May 31 2019 Louis Abel <tucklesepk@gmail.com> - 4.1.2-6
- Added AARCH64 to builds
- Added i386 back to builds

* Wed May 22 2019 Louis Abel <tucklesepk@gmail.com> - 4.1.2-5
- Update to 4.1.2
- Modified patches

* Wed May 15 2019 Louis Abel <tucklesepk@gmail.com> - 4.1.1-5
- Update to 4.1.1

* Sun Apr 28 2019 Louis Abel <tucklesepk@gmail.com> - 4.0.0-5
- Added more static libraries in patches

* Tue Apr 16 2019 Louis Abel <tucklesepk@gmail.com> - 4.0.0-4
- Rebase to 4.0.0
- Fixed, removed, redid patches as needed
- 32 bit builds are no longer supported

* Tue Apr 09 2019 Louis Abel <tucklesepk@gmail.com> - 3.7.2-4
- Adding Fedora 30 to build
- Added OpenSUSE Tumbleweed as a distribution
- Some BuildRequires converted to pkgconfig based on fedora spec

* Mon Feb 25 2019 Louis Abel <tucklesepk@gmail.com> - 3.7.2-3
- Added application file for games menu
- Updated description
- Removed timidity++ as a weak dependency
- Removed Group section as it is not required
- Added fallback soundfont from the sources

* Mon Feb 25 2019 Louis Abel <tucklesepk@gmail.com> - 3.7.2-2
- Added back qzdoom provides
- Added patch to allow build to work with fluidsynth 2
  for when Fedora decides to rebase

* Mon Feb 25 2019 Tommy Nguyen <remyabel@gmail.com> - 3.7.2-2
- Added patch for libasmjit.so

* Mon Feb 25 2019 Louis Abel <tucklesepk@gmail.com> - 3.7.2-1
- Rebased to 3.7.2
- Removed provides of qzdoom
- Automated webhook build from git

* Fri Oct 12 2018 Louis Abel <tucklesepk@gmail.com> - 3.6.0-1
- Rebuild spec according to Fedora guidelines
- Removed timidity dependency as timidity is built-in to gzdoom
- Rebased to 3.6.0
