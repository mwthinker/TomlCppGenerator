cmake_minimum_required(VERSION 3.24)
project(TomlCppGenerator
	DESCRIPTION
		"Helper functions for generated C++ code from TOML files"
	LANGUAGES
		CXX
)

find_package(toml11 CONFIG REQUIRED)

add_library(TomlCppGenerator INTERFACE)

target_include_directories(TomlCppGenerator
	INTERFACE
		include/
)

target_compile_features(TomlCppGenerator INTERFACE cxx_std_23)

message(STATUS "TomlCppGenerator_Example is available to add: -DTomlCppGenerator_Example=1")
option(TomlCppGenerator_Example "Add TomlCppGenerator_Example project." OFF)
if (TomlCppGenerator_Example)
	include(toml_generate_cpp.cmake)
	add_subdirectory(TomlCppGenerator_Example)
endif ()
