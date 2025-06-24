# File: CMakeLists.txt
cmake_minimum_required(VERSION 3.16)
project(SpallationSim)

find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})

include_directories(include)
file(GLOB sources src/*.cc)

add_executable(SpallationSim main.cc ${sources})
target_link_libraries(SpallationSim ${Geant4_LIBRARIES})
