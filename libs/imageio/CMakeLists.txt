cmake_minimum_required(VERSION 3.19)
project(imageio)

set(TARGET imageio)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        include/filament/imageio/BasisEncoder.h
        include/filament/imageio/HDRDecoder.h
        include/filament/imageio/ImageDecoder.h
        include/filament/imageio/ImageDiffer.h
        include/filament/imageio/ImageEncoder.h
)

set(SRCS
        src/BasisEncoder.cpp
        src/HDRDecoder.cpp
        src/ImageDecoder.cpp
        src/ImageDiffer.cpp
        src/ImageEncoder.cpp
)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} STATIC ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

target_include_directories(${TARGET} PUBLIC ${libpng_INCLUDE_DIRS})
target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/${TARGET}>
)

set_target_properties(${TARGET} PROPERTIES FOLDER Libs)

target_link_libraries(${TARGET} PUBLIC image math ${libpng_LIBRARIES} tinyexr::tinyexr utils z basis_encoder)
if (WIN32)
    target_link_libraries(${TARGET} PRIVATE wsock32)
endif()

# ==================================================================================================
# Compiler flags
# ==================================================================================================
if (NOT MSVC)
    target_compile_options(${TARGET} PRIVATE -Wno-deprecated-register)
endif()

install(TARGETS ${TARGET}
        EXPORT filament-targets
        PUBLIC_HEADER DESTINATION include/filament/${TARGET}
)
