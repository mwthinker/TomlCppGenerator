cmake_minimum_required(VERSION 3.24)
project(TomlCppGenerator
	DESCRIPTION
		"A lib for tetris board rules and ai logic"
	LANGUAGES
		CXX
)

set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT TomlCppGenerator)

include(${CMAKE_CURRENT_SOURCE_DIR}/toml_generate_cpp.cmake)

toml_generate_cpp(GENERATED_HEADERS FILES "${CMAKE_CURRENT_SOURCE_DIR}/tetris.toml" OUT_DIR "src/")

message(STATUS "Generated config header: ${GENERATED_HEADERS}")

add_executable(TomlCppGenerator
	tetris.toml
	${GENERATED_HEADERS}
	main.cpp
)

find_package(toml11 CONFIG REQUIRED)

target_include_directories(TomlCppGenerator
	PUBLIC
		${CMAKE_CURRENT_BINARY_DIR}/src
)

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
