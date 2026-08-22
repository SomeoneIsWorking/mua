cmake_minimum_required(VERSION 3.25)

project(mua VERSION 0.1.0 LANGUAGES CXX)

if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    message(FATAL_ERROR "MUA requires clang++; configured compiler is ${CMAKE_CXX_COMPILER_ID}")
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_program(CLANG_FORMAT_EXECUTABLE NAMES clang-format REQUIRED)
find_program(CLANG_TIDY_EXECUTABLE NAMES clang-tidy REQUIRED)
find_program(RUFF_EXECUTABLE NAMES ruff REQUIRED)

set(_XENON_HOST_DEFAULT "${CMAKE_CURRENT_SOURCE_DIR}/../../shared/xenon-host")
if(DEFINED ENV{XENON_HOST_REPO} AND NOT "$ENV{XENON_HOST_REPO}" STREQUAL "")
    set(_XENON_HOST_DEFAULT "$ENV{XENON_HOST_REPO}")
endif()
set(XENON_HOST_SOURCE_DIR "${_XENON_HOST_DEFAULT}"
    CACHE PATH "Path to the title-neutral xenon-host checkout")
unset(_XENON_HOST_DEFAULT)
if(NOT EXISTS "${XENON_HOST_SOURCE_DIR}/CMakeLists.txt")
    message(FATAL_ERROR
            "xenon-host is required; set XENON_HOST_SOURCE_DIR (tried ${XENON_HOST_SOURCE_DIR})")
endif()
add_subdirectory("${XENON_HOST_SOURCE_DIR}" "${CMAKE_BINARY_DIR}/xenon-host"
                 EXCLUDE_FROM_ALL)

set(MUA_GENERATED_DIR "${CMAKE_BINARY_DIR}/generated")
set(MUA_PROFILE_HEADER "${MUA_GENERATED_DIR}/mua_profile_data.hpp")
add_custom_command(
    OUTPUT "${MUA_PROFILE_HEADER}"
    COMMAND ${CMAKE_COMMAND} -E make_directory "${MUA_GENERATED_DIR}"
    COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/generate_profile.py"
            "${CMAKE_CURRENT_SOURCE_DIR}/config/mua.toml" "${MUA_PROFILE_HEADER}"
    DEPENDS config/mua.toml tools/generate_profile.py
    VERBATIM
)

set(MUA_TITLE_SOURCES src/title/title_profile.cpp)
set(MUA_TITLE_HEADERS include/mua/title_profile.hpp)
add_library(mua_title STATIC ${MUA_TITLE_SOURCES} ${MUA_TITLE_HEADERS} "${MUA_PROFILE_HEADER}")
target_include_directories(mua_title PUBLIC include PRIVATE "${MUA_GENERATED_DIR}")
target_link_libraries(mua_title PUBLIC xenon_host)
target_compile_options(mua_title PRIVATE -Wall -Wextra -Wpedantic -Werror)

enable_testing()
add_executable(mua_title_contract_tests tests/title_profile_tests.cpp)
target_link_libraries(mua_title_contract_tests PRIVATE mua_title)
target_compile_options(mua_title_contract_tests PRIVATE -Wall -Wextra -Wpedantic -Werror)
add_test(NAME title_profile COMMAND mua_title_contract_tests)
add_test(NAME profile_generator
         COMMAND ${Python3_EXECUTABLE} tools/generate_profile.py --selftest)
set_tests_properties(profile_generator PROPERTIES WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

set(MUA_FORMAT_FILES ${MUA_TITLE_SOURCES} ${MUA_TITLE_HEADERS} tests/title_profile_tests.cpp)
add_test(NAME mua_format
         COMMAND ${CLANG_FORMAT_EXECUTABLE} --dry-run --Werror ${MUA_FORMAT_FILES}
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME mua_clang_tidy
         COMMAND ${CLANG_TIDY_EXECUTABLE} -p=${CMAKE_BINARY_DIR} --warnings-as-errors=*
                 ${MUA_TITLE_SOURCES} tests/title_profile_tests.cpp
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME mua_structure
         COMMAND ${Python3_EXECUTABLE} tools/check_structure.py
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME mua_structure_selftest
         COMMAND ${Python3_EXECUTABLE} tools/check_structure.py --selftest
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME mua_python_lint
         COMMAND ${RUFF_EXECUTABLE} check tools tests
         WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
