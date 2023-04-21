cmake_minimum_required(VERSION 3.24)
project(GNL)

set(CMAKE_CXX_STANDARD 23)

add_executable(GNL main.cpp main.h argread.h argread.cpp libraries.cpp libraries.h pvtools.cpp pvtools.h combine.cpp delay.cpp delay.h modules.cpp modules.h debug.h write.cpp parameters.cpp)
