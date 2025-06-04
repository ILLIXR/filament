cmake_minimum_required(VERSION 3.19)
project(viewer)

set(TARGET viewer)
set(PUBLIC_HDR_DIR include)

# ==================================================================================================
# Sources and headers
# ==================================================================================================
set(PUBLIC_HDRS
        include/filament/viewer/AutomationEngine.h
        include/filament/viewer/AutomationSpec.h
        include/filament/viewer/RemoteServer.h
        include/filament/viewer/Settings.h
        include/filament/viewer/ViewerGui.h
)

set(SRCS
        src/jsonParseUtils.h
        src/AutomationEngine.cpp
        src/AutomationSpec.cpp
        src/RemoteServer.cpp
        src/Settings.cpp
        src/Settings_generated.cpp
        src/Settings_generated.h
        src/TIFFExport.cpp
        src/TIFFExport.h
        src/ViewerGui.cpp
)

# ==================================================================================================
# Include and target definitions
# ==================================================================================================
add_library(${TARGET} STATIC ${PUBLIC_HDRS} ${SRCS})
set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")
target_link_libraries(${TARGET} PUBLIC ${imgui_LIBRARIES} filament gltfio_core filagui civetweb::civetweb-cpp)
target_include_directories(${TARGET} PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
                           $<INSTALL_INTERFACE:include/filament/${TARGET}>
)
target_include_directories(${TARGET} PUBLIC ${imgui_INCLUDE_DIRS} ${jsmn_INCLUDE_DIRS})
set_target_properties(${TARGET} PROPERTIES FOLDER Libs)

if (FILAMENT_SAMPLES_STEREO_TYPE STREQUAL "instanced")
    add_definitions(-DFILAMENT_SAMPLES_STEREO_TYPE_INSTANCED)
elseif (FILAMENT_SAMPLES_STEREO_TYPE STREQUAL "multiview")
    add_definitions(-DFILAMENT_SAMPLES_STEREO_TYPE_MULTIVIEW)
endif ()

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
#install(DIRECTORY ${PUBLIC_HDR_DIR}/viewer DESTINATION include)

# ==================================================================================================
# Tests
# ==================================================================================================
if (NOT ANDROID AND NOT WEBGL AND NOT IOS)
    add_executable(test_settings tests/test_settings.cpp)
    target_link_libraries(test_settings PRIVATE ${TARGET} GTest::gtest)
    set_target_properties(test_settings PROPERTIES FOLDER Tests)
endif()
