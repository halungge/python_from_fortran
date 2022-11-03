
        project(field_copy)
        cmake_minimum_required(VERSION 3.20.0)

        # Languages
        enable_language(CXX)

        # Paths
        list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
        list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

        set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
        set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
        set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

        # Find dependencies
        include(FetchContent)

        FetchContent_Declare(GridTools
    GIT_REPOSITORY https://github.com/GridTools/gridtools.git
    GIT_TAG        master
)
FetchContent_MakeAvailable(GridTools)                    

        # Targets
        add_library(field_copy)

        target_compile_features(field_copy PRIVATE cxx_std_17)
        set_target_properties(field_copy PROPERTIES PREFIX "lib" SUFFIX ".x86_64-linux-gnu.a")

        target_sources(field_copy
            PRIVATE
                field_copy.h field_copy.cpp field_copy.cpp.inc
        )

        # Link dependencies
        target_link_libraries(field_copy PUBLIC GridTools::fn_naive)
