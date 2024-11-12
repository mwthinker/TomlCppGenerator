find_package(Python3 REQUIRED COMPONENTS Interpreter)

message(STATUS "11111111111111111111111111111111111111111111111")

# Function to process TOML files and generate C++ headers in the specified output directory
function(toml_generate_cpp TOML_HDRS_VAR)
    # Parse the arguments: "OUT_DIR" is optional, "FILES" are positional arguments
    cmake_parse_arguments(TOML_GEN_CPP "" "OUT_DIR" "FILES" ${ARGN})

    message(STATUS "TOML_GEN_CPP_OUT_DIR " "${TOML_GEN_CPP_OUT_DIR}")
    message(STATUS "TOML_GEN_CPP_FILES " "${TOML_GEN_CPP_FILES}")

    if (NOT TOML_GEN_CPP_FILES)
        message(FATAL_ERROR "No TOML files specified")
    endif()

    # Convert relative OUT_DIR to absolute based on CMAKE_CURRENT_BINARY_DIR
    if (NOT IS_ABSOLUTE "${TOML_GEN_CPP_OUT_DIR}")
        set(TOML_GEN_CPP_OUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/${TOML_GEN_CPP_OUT_DIR}")
    endif()

    set(generated_headers)

    foreach(TOML_FILE IN LISTS TOML_GEN_CPP_FILES)
        # Get the base name of the TOML file (without extension)
        get_filename_component(BASE_NAME "${TOML_FILE}" NAME_WE)

        # Define the output header file in the resolved OUT_DIR
        set(TOML_HDR "${TOML_GEN_CPP_OUT_DIR}/${BASE_NAME}_config.h")
        message(STATUS "MMMMMMMMM " "COMMAND Python3::Interpreter " "${CMAKE_CURRENT_FUNCTION_LIST_DIR}/toml_cpp_generator.py " "${TOML_FILE} " "${TOML_GEN_CPP_OUT_DIR} ")

        # Call the Python script with the input TOML file and output header file
        add_custom_command(
            OUTPUT "${TOML_HDR}"
            COMMAND Python3::Interpreter "${CMAKE_CURRENT_FUNCTION_LIST_DIR}/toml_cpp_generator.py" "${TOML_FILE}" "${TOML_GEN_CPP_OUT_DIR}"
            DEPENDS "${TOML_FILE}"
            COMMENT "Generating config header from ${TOML_FILE} in ${TOML_GEN_CPP_OUT_DIR}"
            VERBATIM
        )

        # Append the generated header to the list
        list(APPEND generated_headers "${TOML_HDR}")

        # Create a custom target to ensure the file is generated before the build
        add_custom_target("generate_${BASE_NAME}_header" ALL DEPENDS "${TOML_HDR}")
    endforeach()

    # Set the output variable with the list of generated headers
    set(${TOML_HDRS_VAR} ${generated_headers} PARENT_SCOPE)

    message(STATUS "Generated config headers: ${generated_headers}")
endfunction()
