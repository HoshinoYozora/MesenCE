"""Build MesenCore.dll for Windows with MinGW-w64 (no Visual Studio required).

This is a *local* build helper: MesenCE upstream only supports MSVC on Windows.
It compiles the same translation units the MSVC solution uses (Core + Utilities +
Windows platform layer + InteropDLL + SevenZip + Lua) into a single DLL that the
Avalonia UI loads exactly like the official MesenCore.dll.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
MINGW = r"E:\Program Files\mingw-w64\bin"
GXX = os.path.join(MINGW, "g++.exe")
GCC = os.path.join(MINGW, "gcc.exe")
OBJ = os.path.join(ROOT, "obj.mingw")

SOURCES = [("Core", ".cpp"), ("Utilities", ".cpp"), ("Utilities", ".c"),
           ("Windows", ".cpp"), ("InteropDLL", ".cpp"),
           ("SevenZip", ".c"), ("Lua", ".c")]

# Unix-only sources that the MSVC Lua/SevenZip projects do not compile on Windows
EXCLUDE = {"serial.c", "unixdgram.c", "unixstream.c", "unix.c"}

INCLUDES = [".", "Core", "Utilities", "Windows", "InteropDLL", "third_party/DirectXMath"]

LIBS = ["d3d11", "dxgi", "dxguid", "d3dcompiler", "dinput8", "dsound", "xinput1_4", "winmm",
        "ole32", "oleaut32", "uuid", "wbemuuid", "ws2_32", "mmdevapi",
        "setupapi", "version", "shlwapi", "user32", "gdi32", "imm32",
        "advapi32", "shell32", "comdlg32", "dbghelp"]

DEFINES = ["NDEBUG", "WIN32", "UNICODE", "_UNICODE"]


def collect() -> list[str]:
    out = []
    for folder, ext in SOURCES:
        base = os.path.join(ROOT, folder)
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                if name.endswith(ext) and name not in EXCLUDE:
                    out.append(os.path.join(dirpath, name))
    return sorted(out)


def obj_path(src: str) -> str:
    rel = os.path.relpath(src, ROOT).replace(os.sep, "_")
    key = hashlib.md5(src.encode()).hexdigest()[:8]
    return os.path.join(OBJ, f"{rel}.{key}.o")


def compile_one(src: str, extra: list[str]) -> tuple[str, str, str]:
    out = obj_path(src)
    compiler = GCC if src.endswith(".c") else GXX
    cmd = [compiler, "-c", src, "-o", out, "-O2", "-w"]
    cmd += ["-std=c11"] if src.endswith(".c") else ["-std=c++17", "-fpermissive"]
    for d in DEFINES:
        cmd.append(f"-D{d}")
    for i in INCLUDES:
        cmd.append(f"-I{os.path.join(ROOT, i)}")
    cmd += extra
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(src):
        return "cached", src, ""
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    return ("ok" if proc.returncode == 0 else "fail"), src, proc.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--link-only", action="store_true")
    ap.add_argument("--jobs", type=int, default=min(16, (os.cpu_count() or 4)))
    ap.add_argument("--keep-going", action="store_true", default=True)
    args = ap.parse_args()

    os.makedirs(OBJ, exist_ok=True)
    srcs = collect()
    print(f"{len(srcs)} translation units")

    failures = []
    if not args.link_only:
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for state, src, err in pool.map(lambda s: compile_one(s, []), srcs):
                if state == "fail":
                    failures.append((src, err))
        print(f"compile finished in {time.time() - t0:.1f}s, {len(failures)} failures")
        if failures:
            for src, err in failures[:8]:
                rel = os.path.relpath(src, ROOT)
                lines = [ln for ln in err.splitlines() if "error" in ln][:4]
                print(f"\n--- {rel}")
                print("\n".join(lines))
            return 1

    objs = [obj_path(s) for s in srcs]
    missing = [o for o in objs if not os.path.exists(o)]
    if missing:
        print(f"{len(missing)} objects missing; run a full build first")
        return 1

    dll = os.path.join(ROOT, "bin", "mingw", "MesenCore.dll")
    os.makedirs(os.path.dirname(dll), exist_ok=True)
    rsp = os.path.join(OBJ, "link.rsp")
    with open(rsp, "w", encoding="utf-8") as fh:
        for o in objs:
            fh.write(f'"{o}"\n')
        for lib in LIBS:
            fh.write(f"-l{lib}\n")
    cmd = [GXX, "-shared", "-o", dll, "-static", "-static-libgcc", "-static-libstdc++",
           "-Wl,--out-implib," + os.path.join(ROOT, "bin", "mingw", "libMesenCore.a"),
           "@" + rsp]
    print("linking ...")
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        errs = [ln for ln in proc.stderr.splitlines() if "undefined reference" in ln or "error" in ln]
        print(f"link failed ({len(errs)} lines)")
        print("\n".join(errs[:40]))
        return 1
    print(f"wrote {dll} ({os.path.getsize(dll) / 1048576:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())




