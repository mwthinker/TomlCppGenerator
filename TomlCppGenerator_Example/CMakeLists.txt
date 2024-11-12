project(TomlCppGenerator_Example
	DESCRIPTION
		"A lib for tetris board rules and ai logic"
	LANGUAGES
		CXX
)

toml_generate_cpp(GENERATED_HEADERS FILES "${CMAKE_CURRENT_SOURCE_DIR}/tetris.toml" OUT_DIR "src/")

message(STATUS "Generated config header: ${GENERATED_HEADERS}")

add_executable(TomlCppGenerator_Example
	tetris.toml
	${GENERATED_HEADERS}
	src/main.cpp
)

find_package(toml11 CONFIG REQUIRED)
find_package(fmt CONFIG REQUIRED)

target_include_directories(TomlCppGenerator_Example
	PUBLIC
		${CMAKE_CURRENT_BINARY_DIR}/src
		src/
)

target_link_libraries(TomlCppGenerator_Example
	PRIVATE
		toml11::toml11
		fmt::fmt
		TomlCppGenerator
)

set_target_properties(TomlCppGenerator_Example
	PROPERTIES
		CXX_STANDARD 23
		CXX_STANDARD_REQUIRED YES
		CXX_EXTENSIONS NO
)

if (MSVC)
	target_compile_options(TomlCppGenerator_Example
		PRIVATE
			"/permissive-"
	)
endif ()
