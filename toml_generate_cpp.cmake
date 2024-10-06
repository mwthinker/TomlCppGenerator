function(toml_generate_cpp OUT_VAR)
    set(options)
    set(oneValueArgs)
    set(multiValueArgs INPUT_FILES)
    cmake_parse_arguments(TOML_GEN_CPP "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if(NOT TOML_GEN_CPP_INPUT_FILES)
        message(FATAL_ERROR "No input files specified for toml_generate_cpp()")
    endif()

    set(output_files)
    foreach(input_file IN LISTS TOML_GEN_CPP_INPUT_FILES)
        get_filename_component(filename ${input_file} NAME_WE)
        set(output_file "${CMAKE_CURRENT_BINARY_DIR}/${filename}.cpp")
        add_custom_command(
            OUTPUT ${output_file}
            COMMAND ${CMAKE_COMMAND} -E env python toml_cpp_generator.py ${input_file} > ${output_file}
            DEPENDS ${input_file} toml_cpp_generator.py
            COMMENT "Generating C++ source file from ${input_file}"
        )
        list(APPEND output_files ${output_file})
    endforeach()

    set(${OUT_VAR} ${output_files} PARENT_SCOPE)
endfunction()
