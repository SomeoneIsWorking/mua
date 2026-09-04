cmake_minimum_required(VERSION 3.25)

project(mua VERSION 0.1.0 LANGUAGES NONE)

set(X360PORT_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../../shared/x360port"
    CACHE PATH "Path to the title-neutral x360port checkout")

if(EXISTS "${X360PORT_SOURCE_DIR}/CMakeLists.txt")
    set(MUA_PRODUCT_UNAVAILABLE_REASON
        "the MUA title adapter over x360port has not been implemented")
else()
    set(MUA_PRODUCT_UNAVAILABLE_REASON
        "x360port is missing at ${X360PORT_SOURCE_DIR}")
endif()

add_custom_target(
    mua_product ALL
    COMMAND ${CMAKE_COMMAND} -E echo
            "MUA gameplay product unavailable: ${MUA_PRODUCT_UNAVAILABLE_REASON}"
    COMMAND ${CMAKE_COMMAND} -E false
    VERBATIM
)
