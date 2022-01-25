cmake_minimum_required(VERSION 3.10)
project(crossworlds)

set(CMAKE_CXX_STANDARD 11)

include_directories(src)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)
FetchContent_MakeAvailable(googletest)

include(CTest)

add_subdirectory(src)
add_subdirectory(tests)
