cmake_minimum_required(VERSION 3.19)
project(vkmemalloc)

set(TARGET vkmemalloc)

set(PUBLIC_HDR_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../include)

set(PUBLIC_HDRS ${PUBLIC_HDR_DIR}/vk_mem_alloc.h)


add_library(${TARGET} INTERFACE)
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")
target_include_directories(${TARGET} INTERFACE
                           $<BUILD_INTERFACE:${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/${TARGET}>
)
set_target_properties(${TARGET} PROPERTIES FOLDER ThirdParty)

install(TARGETS ${TARGET}
        EXPORT filament-targets
        PUBLIC_HEADER DESTINATION include/${TARGET}
)
