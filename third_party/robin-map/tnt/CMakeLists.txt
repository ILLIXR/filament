cmake_minimum_required(VERSION 3.19)
project(tsl)

set(TARGET tsl)
find_package(tsl-robin-map QUIET CONFIG)
if(tsl-robin-map_FOUND)
    message(STATUS "Using robin-map: ${tsl-robin-map_VERSION}")
    set(OUR_DIR "${tsl-robin-map_INCLUDE_DIRS}")
else()
    message(STATUS "Using bundled robin-map")
    set(OUR_DIR ${CMAKE_CURRENT_SOURCE_DIR}/..)
endif()

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        ${OUR_DIR}/tsl/robin_growth_policy.h
        ${OUR_DIR}/tsl/robin_hash.h
        ${OUR_DIR}/tsl/robin_map.h
        ${OUR_DIR}/tsl/robin_set.h
)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${OUR_DIR}/tsl)

add_library(${TARGET} INTERFACE)
target_sources(${TARGET} INTERFACE ${PUBLIC_HDRS})
target_include_directories(${TARGET} INTERFACE ${OUR_DIR})
set_target_properties(${TARGET} PROPERTIES FOLDER ThirdParty)

# ==================================================================================================
# Installation
# ==================================================================================================
if(NOT tsl-robin-map_FOUND)
    install(FILES ${PUBLIC_HDRS} DESTINATION include/${TARGET})
endif()
