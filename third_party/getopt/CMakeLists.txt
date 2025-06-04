cmake_minimum_required(VERSION 3.10)
project(getopt)

set(TARGET getopt)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS include/getopt/getopt.h)
set(PRIVATE_HDRS include/getopt/getopt.h)

set(SRCS
        src/getopt.c
        src/getopt_long.c)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} STATIC ${PRIVATE_HDRS} ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

target_include_directories (${TARGET} PUBLIC
                            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                            $<INSTALL_INTERFACE:include>
)

set_target_properties(${TARGET} PROPERTIES FOLDER ThirdParty)
install(TARGETS ${TARGET}
        EXPORT filament-targets
        ARCHIVE DESTINATION lib
        PUBLIC_HEADER DESTINATION include
)
