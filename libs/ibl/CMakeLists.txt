cmake_minimum_required(VERSION 3.19)
project(cmgen)

set(TARGET ibl)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
    ${PUBLIC_HDR_DIR}/filament/ibl/Cubemap.h
    ${PUBLIC_HDR_DIR}/filament/ibl/CubemapIBL.h
    ${PUBLIC_HDR_DIR}/filament/ibl/CubemapSH.h
    ${PUBLIC_HDR_DIR}/filament/ibl/CubemapUtils.h
    ${PUBLIC_HDR_DIR}/filament/ibl/Image.h
    ${PUBLIC_HDR_DIR}/filament/ibl/utilities.h
)

set(PRIVATE_HDRS
    src/CubemapUtilsImpl.h
)

set(SRCS
    src/Cubemap.cpp
    src/CubemapIBL.cpp
    src/CubemapSH.cpp
    src/CubemapUtils.cpp
    src/Image.cpp
)

# ==================================================================================================
# Target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} ${PUBLIC_HDRS} ${PRIVATE_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/${TARGET}>
)
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)
target_link_libraries(${TARGET} math utils)

add_library(${TARGET}-lite ${PUBLIC_HDRS} ${PRIVATE_HDRS} ${SRCS})
set_target_properties(${TARGET}-lite PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

target_compile_definitions(${TARGET}-lite PUBLIC -DFILAMENT_IBL_LITE=1)
target_include_directories(${TARGET}-lite PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/${TARGET}-lite>
)
set_target_properties(${TARGET}-lite PROPERTIES FOLDER Libs)
target_link_libraries(${TARGET}-lite math utils)

# ==================================================================================================
# Compile options and optimizations
# ==================================================================================================
if (MSVC)
    target_compile_options(${TARGET} PRIVATE /fp:fast)
    target_compile_options(${TARGET}-lite PRIVATE /fp:fast)
else()
    target_compile_options(${TARGET} PRIVATE -ffast-math -fno-finite-math-only)
    target_compile_options(${TARGET}-lite PRIVATE -ffast-math -fno-finite-math-only)
endif()


# ==================================================================================================
# Installation
# ==================================================================================================
install(TARGETS ${TARGET}
        EXPORT filament-targets
        ARCHIVE DESTINATION lib/${DIST_DIR}
        PUBLIC_HEADER DESTINATION include/filament/ibl
)
install(TARGETS ${TARGET}-lite
        EXPORT filament-targets
        ARCHIVE DESTINATION lib/${DIST_DIR}
        PUBLIC_HEADER DESTINATION include/filament/ibl-lite
)
