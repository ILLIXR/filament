cmake_minimum_required(VERSION 3.19)
project(smol-v)

set(TARGET smol-v)

set(PUBLIC_HDR_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../source)
set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../source)

set(SRCS
    ${SRC_DIR}/smolv.cpp
)

add_library(${TARGET} STATIC ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDR_DIR}/smolv.h")
target_compile_options(${TARGET} PRIVATE
        $<$<PLATFORM_ID:Linux>:-fPIC>
)

if (NOT MSVC)
    target_compile_options(${TARGET} PRIVATE -Wno-tautological-unsigned-enum-zero-compare)
endif()

target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/${TARGET}>
)
set_target_properties(${TARGET} PROPERTIES FOLDER ThirdParty)
set(SMOLV_BUILD_INCLUDE_PATH ${PUBLIC_HDR_DIR} PARENT_SCOPE)
install(TARGETS ${TARGET}
        EXPORT filament-targets
        ARCHIVE DESTINATION lib/${DIST_DIR}
        PUBLIC_HEADER DESTINATION include/${TARGET}
)
