cmake_minimum_required(VERSION 3.19)
project(camutils)

set(TARGET camutils)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        include/filament/camutils/Bookmark.h
        include/filament/camutils/compiler.h
        include/filament/camutils/Manipulator.h
)

set(SRCS
        src/Bookmark.cpp
        src/FreeFlightManipulator.h
        src/Manipulator.cpp
        src/MapManipulator.h
        src/OrbitManipulator.h
)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} STATIC ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

target_link_libraries(${TARGET} PUBLIC math)

target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/${TARGET}>
)
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)

# ==================================================================================================
# Compiler flags
# ==================================================================================================
if (MSVC)
else()
    target_compile_options(${TARGET} PRIVATE -Wno-deprecated-register)
endif()

# ==================================================================================================
# Installation
# ==================================================================================================
install(TARGETS ${TARGET}
        EXPORT filament-targets
        ARCHIVE DESTINATION lib/${DIST_DIR}
        PUBLIC_HEADER DESTINATION include/filament/${TARGET}
)

# ==================================================================================================
# Tests
# ==================================================================================================
if (NOT ANDROID AND NOT WEBGL AND NOT IOS)
    add_executable(test_${TARGET} tests/test_camutils.cpp)
    target_link_libraries(test_${TARGET} PRIVATE camutils GTest::gtest)
    set_target_properties(test_${TARGET} PROPERTIES FOLDER Tests)
endif()
