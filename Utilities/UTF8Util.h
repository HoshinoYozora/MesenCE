#pragma once

#include <filesystem>
#include <fstream>

namespace utf8
{
	class utf8
	{
	public:
		static std::wstring decode(const std::string& str);
		static std::string encode(const std::wstring& wstr);
		static std::string encode(const std::u16string& wstr);
	};

#ifdef _WIN32
	//MinGW-w64 (libstdc++) has no std::ifstream(const std::wstring&) overload; a
	//std::filesystem::path built from the wide name works on both toolchains.
	class ifstream : public std::ifstream
	{
	public:
		ifstream(const std::string& _Str, ios_base::openmode _Mode = ios_base::in) : std::ifstream(std::filesystem::path(utf8::decode(_Str)), _Mode) {}
		ifstream() : std::ifstream() {}
		void open(const std::string& _Str, ios_base::openmode _Mode = ios_base::in) { std::ifstream::open(std::filesystem::path(utf8::decode(_Str)), _Mode); }
	};

	class ofstream : public std::ofstream
	{
	public:
		ofstream(const std::string& _Str, ios_base::openmode _Mode = ios_base::in) : std::ofstream(std::filesystem::path(utf8::decode(_Str)), _Mode) {}
		ofstream() : std::ofstream() {}
		void open(const std::string& _Str, ios_base::openmode _Mode = ios_base::in) { std::ofstream::open(std::filesystem::path(utf8::decode(_Str)), _Mode); }
	};
#else
	using std::ifstream;
	using std::ofstream;
#endif
}