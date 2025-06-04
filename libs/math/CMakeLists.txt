cmake_minimum_required(VERSION 3.19)
project(math)

set(TARGET math)
set(PUBLIC_HDR_DIR include)

if (MSVC)
    set(OPTIMIZATION_FLAGS /fp:fast)
else()
    set(OPTIMIZATION_FLAGS -ffast-math -fno-finite-math-only -ffp-contract=fast)
endif()

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        include/filament/math/TMatHelpers.h
        include/filament/math/TQuatHelpers.h
        include/filament/math/TVecHelpers.h
        include/filament/math/compiler.h
        include/filament/math/fast.h
        include/filament/math/half.h
        include/filament/math/mathfwd.h
        include/filament/math/mat2.h
        include/filament/math/mat3.h
        include/filament/math/mat4.h
        include/filament/math/norm.h
        include/filament/math/quat.h
        include/filament/math/scalar.h
        include/filament/math/vec2.h
        include/filament/math/vec3.h
        include/filament/math/vec4.h
)

set(SRCS src/dummy.cpp)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
include_directories(${PUBLIC_HDR_DIR})

add_library(${TARGET} STATIC ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")
target_compile_options(${TARGET} PRIVATE ${OPTIMIZATION_FLAGS})
target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/math>
)
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)

# ==================================================================================================
# Installation
# ==================================================================================================
install(TARGETS ${TARGET}
        EXPORT filament-targets
        PUBLIC_HEADER DESTINATION include/filament/math
)

# ==================================================================================================
# Tests
# ==================================================================================================
add_executable(test_${TARGET}
        tests/test_fast.cpp
        tests/test_half.cpp
        tests/test_mat.cpp
        tests/test_vec.cpp
        tests/test_quat.cpp
)
target_link_libraries(test_${TARGET} PRIVATE math GTest::gtest)
set_target_properties(test_${TARGET} PROPERTIES FOLDER Tests)

# ==================================================================================================
# Benchmarks
# ==================================================================================================

set(BENCHMARK_SRCS
        benchmarks/benchmark_fast.cpp include/filament/math/mathfwd.h)

add_executable(benchmark_${TARGET} ${BENCHMARK_SRCS})

target_compile_options(benchmark_${TARGET} PRIVATE ${OPTIMIZATION_FLAGS})

target_link_libraries(benchmark_${TARGET} PRIVATE benchmark::benchmark_main utils math)

set_target_properties(benchmark_${TARGET} PROPERTIES FOLDER Benchmarks)
