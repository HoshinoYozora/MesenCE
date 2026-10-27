DirectXMath — https://github.com/microsoft/DirectXMath
=====================================================

The headers under `official/` are an unmodified copy of `Inc/` from
microsoft/DirectXMath, used only for the local MinGW-w64 build of the Windows
core (the MinGW-w64 runtime ships an incomplete `directxmath.h` that lacks the
`XMGLOBALCONST`/DirectXColors definitions Mesen relies on).

`directxmath.h` and `directxcolors.h` at this level are one-line shims that map
the lowercase include names used by Mesen's Windows layer onto the upstream
files (Windows file systems are case-insensitive, so the shims and the upstream
files cannot live in the same directory).

License: MIT

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
