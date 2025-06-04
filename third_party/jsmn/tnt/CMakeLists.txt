cmake_minimum_required(VERSION 3.19)

find_path(PUBLIC_HDR_DIR jsmn.h)
if(NOT PUBLIC_HDR_DIR)
    message(STATUS "Using bundled jsmn.h")
    set(PUBLIC_HDR_DIR ${CMAKE_CURRENT_SOURCE_DIR}/..)
    install(FILES ${PUBLIC_HEADER_DIR}/jsmn.h TYPE INCLUDE DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
else()
    message(STATUS "Found jsmn.h")
endif()
set(jsmn_INCLUDE_DIRS ${PUBLIC_HDR_DIR} CACHE PATH "")


#add_library(${TARGET} INTERFACE)
#set_target_properties(${TARGET} PROPERTIES PUBLIC_HEADER "${PUBLIC_HDRS}")

#target_include_directories(${TARGET} INTERFACE
#                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${PUBLIC_HDR_DIR}>
#)
#set_target_properties(${TARGET} PROPERTIES FOLDER ThirdParty)
