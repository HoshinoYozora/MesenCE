# Modifications to Mesen Community Edition

Fork: https://github.com/HoshinoYozora/MesenCE (based on nesdev-org/MesenCE `master`, 4b8a196e)

This fork is distributed under the same license as upstream, **GNU GPL v3**
(see `LICENSE`). All upstream copyright notices are left untouched, and every
file that was changed carries a notice with the date of the change (GPLv3 §5a).

## 1. VRC7-Wide — NES mapper 85 submapper 2 (2026-10-27)

The stock VRC7 keeps 6 bits in its three switchable PRG bank registers
(`page = value & 0x3F`), so the board can only address 64 × 8 KiB = 512 KiB of
PRG ROM. ROM hacks that store engine/text/font data above 512 KiB select banks
with plain byte writes (e.g. `LDA #$41` / `STA $9000`) and therefore need 7-bit
bank registers.

Mapper 85 submapper 2 ("VRC7-Wide") keeps 7 bits, allowing 128 × 8 KiB = 1 MiB.
Everything else (OPLL audio, IRQ, CHR banking, mirroring, WRAM control, fixed
last page) is unchanged, and submapper 0 ROMs keep the stock behaviour.

Files: `Core/NES/Mappers/Konami/VRC7.h`, `Core/NES/MapperFactory.cpp`

## 2. MinGW-w64 build support (2026-10-27, local convenience only)

Not needed for the official MSVC build. Adds `build-mingw.py` (compiles
Core + Utilities + Windows + InteropDLL + SevenZip + Lua into `MesenCore.dll`)
and the portability fixes it requires:

* `Utilities/UTF8Util.h`, `Utilities/UTF8Util.cpp` — `utf8::decode` implemented
  for any `_WIN32` compiler, fstreams constructed from
  `std::filesystem::path` (libstdc++ has no `std::wstring` overload).
* `Utilities/UPnPPortMapper.cpp` — use the existing stub when `natupnp.h` is
  unavailable (no UPnP port mapping in MinGW builds).
* `third_party/DirectXMath/` — unmodified upstream headers plus a MIT note
  (the MinGW-w64 `directxmath.h` lacks the definitions the Windows renderer
  needs).

## Building

* Windows, Visual Studio 2022/2026: `Mesen.sln`, Release/x64 (upstream path).
* Windows, no Visual Studio: `python build-mingw.py`, then publish the UI with
  `dotnet publish UI\UI.csproj -c Release -r win-x64 -p:OptimizeUi=true
  -p:PublishAot=false -p:SelfContained=false -p:PublishSingleFile=true
  -p:SolutionDir=<repo>\`.
