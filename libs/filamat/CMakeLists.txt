cmake_minimum_required(VERSION 3.19)
project(filamat)

set(TARGET         filamat)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(HDRS
        include/filamat/Enums.h
        include/filamat/IncludeCallback.h
        include/filamat/MaterialBuilder.h
        include/filamat/Package.h)

set(COMMON_PRIVATE_HDRS
        src/eiff/Chunk.h
        src/eiff/ChunkContainer.h
        src/eiff/DictionaryTextChunk.h
        src/eiff/Flattener.h
        src/eiff/LineDictionary.h
        src/eiff/MaterialTextChunk.h
        src/eiff/MaterialInterfaceBlockChunk.h
        src/eiff/ShaderEntry.h
        src/eiff/SimpleFieldChunk.h
        src/Includes.h
        src/PushConstantDefinitions.h)

set(COMMON_SRCS
        src/eiff/Chunk.cpp
        src/eiff/ChunkContainer.cpp
        src/eiff/DictionaryTextChunk.cpp
        src/eiff/LineDictionary.cpp
        src/eiff/MaterialTextChunk.cpp
        src/eiff/MaterialInterfaceBlockChunk.cpp
        src/eiff/SimpleFieldChunk.cpp
        src/shaders/CodeGenerator.cpp
        src/shaders/ShaderGenerator.cpp
        src/shaders/SibGenerator.cpp
        src/shaders/UibGenerator.cpp
        src/Enums.cpp
        src/Includes.cpp
        src/MaterialBuilder.cpp
        src/MaterialVariants.cpp
)

# Sources and headers for filamat

set(PRIVATE_HDRS
        ${COMMON_PRIVATE_HDRS}
        src/eiff/BlobDictionary.h
        src/eiff/DictionarySpirvChunk.h
        src/eiff/DictionaryMetalLibraryChunk.h
        src/eiff/MaterialBinaryChunk.h
        src/GLSLPostProcessor.h
        src/MetalArgumentBuffer.h
        src/ShaderMinifier.h
        src/SpirvFixup.h
        src/sca/ASTHelpers.h
        src/sca/GLSLTools.h
        src/sca/builtinResource.h)

set(SRCS
        ${COMMON_SRCS}
        src/eiff/BlobDictionary.cpp
        src/eiff/DictionarySpirvChunk.cpp
        src/eiff/DictionaryMetalLibraryChunk.cpp
        src/eiff/MaterialBinaryChunk.cpp
        src/MetalArgumentBuffer.cpp
        src/sca/ASTHelpers.cpp
        src/sca/GLSLTools.cpp
        src/GLSLPostProcessor.cpp
        src/ShaderMinifier.cpp
        src/SpirvFixup.cpp)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})
include_directories(${CMAKE_BINARY_DIR})

# Filamat
add_library(${TARGET} STATIC ${HDRS} ${PRIVATE_HDRS} ${SRCS})
target_include_directories(${TARGET} PUBLIC ${PUBLIC_HDR_DIR})
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)
target_link_libraries(${TARGET} backend_headers shaders filabridge utils smol-v)

if (FILAMENT_SUPPORTS_WEBGPU)
    target_link_libraries(${TARGET} libtint)
endif ()

# We are being naughty and accessing private headers here
# For spirv-tools, we're just following glslang's example
target_include_directories(${TARGET} PRIVATE ${spirv-tools_SOURCE_DIR}/include)

# glslang libraries have circular dependencies. To make sure the proper object are part of the link
# we need to force archive re-scan on new symbol dependencies via start/end-group.
# Read more about this here https://eli.thegreenplace.net/2013/07/09/library-order-in-static-linking
if (APPLE OR MSVC)
    target_link_libraries(${TARGET} glslang::glslang glslang::SPIRV SPIRV-Tools-opt spirv-cross-glsl)
else()
    target_link_libraries(${TARGET}
            -Wl,--start-group glslang::glslang glslang::SPIRV spirv-cross-glsl spirv-cross-msl glslang::SPVRemapper -Wl,--end-group)
endif()

# ==================================================================================================
# Compiler flags
# ==================================================================================================
# this must match options enabled in glslang's CMakeLists.txt
target_compile_options(${TARGET} PRIVATE -DAMD_EXTENSIONS -DNV_EXTENSIONS )

if (MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W0 /Zc:__cplusplus")
endif()

if (FILAMENT_ENABLE_MATDBG)
    add_definitions(-DFILAMENT_ENABLE_MATDBG)
endif()

# ==================================================================================================
# Installation
# ==================================================================================================

# Filamat has dependencies on a bunch of SPIRV-related libraries. To make things simpler, we bundle
# them together into a single shared library and copy this into the installation folder. This
# requires us to explicitly list the dependencies below, as CMake doesn't have a way to recursively
# query dependencies.
set(FILAMAT_DEPS
        OSDependent
        SPIRV
        SPIRV-Tools
        SPIRV-Tools-opt
        filamat
        glslang
        spirv-cross-core
        spirv-cross-glsl
        spirv-cross-msl
        )

set(FILAMAT_COMBINED_OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/libfilamat_combined.a")
combine_static_libs(filamat "${FILAMAT_COMBINED_OUTPUT}" "${FILAMAT_DEPS}")

set(FILAMAT_LIB_NAME ${CMAKE_STATIC_LIBRARY_PREFIX}filamat${CMAKE_STATIC_LIBRARY_SUFFIX})
install(FILES "${FILAMAT_COMBINED_OUTPUT}" DESTINATION lib/${DIST_DIR} RENAME ${FILAMAT_LIB_NAME})
install(DIRECTORY ${PUBLIC_HDR_DIR}/filamat DESTINATION include)

# Need to install libtint for filamat on Android.
# See libs/filamat/CMakeLists.txt and android/filamat-android/CMakeLists.txt.
if (ANDROID)
   target_link_libraries(${TARGET} libtint_combined)
endif()

# ==================================================================================================
# Tests
# ==================================================================================================
if (IS_HOST_PLATFORM)
    project(test_filamat)
    set(TARGET test_filamat)
    set(SRCS
            tests/test_filamat.cpp
            tests/test_argBufferFixup.cpp
            tests/test_clipDistanceFixup.cpp
            tests/test_includes.cpp)

    add_executable(${TARGET} ${SRCS})
    target_include_directories(${TARGET} PRIVATE src)
    target_link_libraries(${TARGET} filamat GTest::gtest SPIRV-Tools-opt)
    set_target_properties(${TARGET} PROPERTIES FOLDER Tests)
endif()
