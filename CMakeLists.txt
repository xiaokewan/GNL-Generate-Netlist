cmake_minimum_required(VERSION 3.24)
project(gnl)

set(CMAKE_CXX_STANDARD 23)

# add_executable(gnl main.cpp main.h argread.h argread.cpp libraries.cpp libraries.h pvtools.cpp pvtools.h combine.cpp delay.cpp delay.h modules.cpp modules.h debug.h write.cpp parameters.cpp)
set(SOURCE_FILES
    src/main.cpp
    src/argread.cpp
    src/libraries.cpp
    src/pvtools.cpp
    src/combine.cpp
    src/delay.cpp
    src/modules.cpp
    src/write.cpp
    src/parameters.cpp
)

set(HEADER_FILES
    src/main.h
    src/argread.h
    src/libraries.h
    src/pvtools.h
    src/delay.h
    src/modules.h
    src/debug.h
)
add_executable(gnl ${SOURCE_FILES} ${HEADER_FILES})