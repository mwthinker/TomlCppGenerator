find_package(Python3 REQUIRED COMPONENTS Interpreter)

# Function to process TOML files and generate a C++ header
function(toml_generate_cpp TOML_HDRS TOML_FILE OUT_DIR)
    # Get the base name of the TOML file (without extension)
    get_filename_component(BASE_NAME "${TOML_FILE}" NAME_WE)
    #cmake_path(GET "${TOML_FILE}" STEM BASE_NAME)

    # Define the output file based on the TOML file
    set(TOML_HDRS "${CMAKE_BINARY_DIR}/${BASE_NAME}_config.h")

    # Call the Python script with the input TOML file and output header file
    add_custom_command(
        OUTPUT "${TOML_HDRS}"
        DEPENDS "${TOML_FILE}"
        DEPENDS "${TOML_HDRS}"
        COMMAND Python3::Interpreter ${CMAKE_CURRENT_SOURCE_DIR}/toml_cpp_generator.py "${TOML_FILE}" "$OUT_DIR"
        COMMENT "Generating config header from ${TOML_FILE}"
        VERBATIM
        COMMAND_EXPAND_LISTS
    )

    message(STATUS "MWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW Generated config header: ${TOML_HDRS}")

    # If the Python script fails, CMake will stop the build
    add_custom_target(check_python_script ALL DEPENDS "${TOML_HDRS}")

    # Set the generated output file in the caller's scope
    set(${OUTPUT_FILE} "${TOML_HDRS}" PARENT_SCOPE)

    # Make sure that the output is known to CMake
    set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${TOML_HDRS}")
endfunction()
