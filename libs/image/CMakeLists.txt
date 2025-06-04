cmake_minimum_required(VERSION 3.19)
project(image)

set(TARGET image)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        include/filament/image/ColorTransform.h
        include/filament/image/ImageOps.h
        include/filament/image/ImageSampler.h
        include/filament/image/Ktx1Bundle.h
        include/filament/image/LinearImage.h
)

set(SRCS
        src/ImageOps.cpp
        src/ImageSampler.cpp
        src/Ktx1Bundle.cpp
        src/LinearImage.cpp
)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} STATIC ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

target_link_libraries(${TARGET} PUBLIC math utils)

target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/${TARGET}>
)
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)

# ==================================================================================================
# Compiler flags
# ==================================================================================================
if (MSVC)
    target_compile_options(${TARGET} PRIVATE $<$<CONFIG:Release>:/fp:fast>)
else()
    target_compile_options(${TARGET} PRIVATE $<$<CONFIG:Release>:-ffast-math -fno-finite-math-only>)
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
if (NOT ANDROID AND NOT WEBGL AND NOT IOS AND NOT FILAMENT_SKIP_SDL2)
    add_executable(test_${TARGET} tests/test_image.cpp)
    target_link_libraries(test_${TARGET} PRIVATE imageio GTest::gtest)
    set_target_properties(test_${TARGET} PROPERTIES FOLDER Tests)
endif()
