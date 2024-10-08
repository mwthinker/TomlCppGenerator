cmake_minimum_required(VERSION 3.24)
project(TomlCppGenerator
	DESCRIPTION
		"A lib for tetris board rules and ai logic"
	LANGUAGES
		CXX
)

include(${CMAKE_CURRENT_SOURCE_DIR}/toml_generate_cpp.cmake)
toml_generate_cpp(TOML_HDRS "${CMAKE_CURRENT_SOURCE_DIR}/tetris.toml" ${CMAKE_CURRENT_SOURCE_DIR})

message(STATUS "Generated config header: ${TOML_HDRS}")

add_library(TomlCppGenerator
	tetris.toml
	${TOML_HDRS}
	main.cpp
)

find_package(toml11 CONFIG REQUIRED)

target_link_libraries(TomlCppGenerator
	PUBLIC
		toml11::toml11
)

set_target_properties(TomlCppGenerator
	PROPERTIES
		CXX_STANDARD 23
		CXX_STANDARD_REQUIRED YES
		CXX_EXTENSIONS NO
)
