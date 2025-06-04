cmake_minimum_required(VERSION 3.19)
project(math)

set(TARGET mathio)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        include/filament/mathio/ostream.h
)

set(SRCS src/ostream.cpp)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} STATIC ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")
target_compile_options(${TARGET} PRIVATE ${OPTIMIZATION_FLAGS})
target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/mathio>
)
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)
target_link_libraries(${TARGET} PRIVATE math)

# ==================================================================================================
# Installation
# ==================================================================================================
install(TARGETS ${TARGET}
        EXPORT filament-targets
        PUBLIC_HEADER DESTINATION include/filament/mathio
)
