INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_LACROSSE lacrosse)

FIND_PATH(
    LACROSSE_INCLUDE_DIRS
    NAMES lacrosse/api.h
    HINTS $ENV{LACROSSE_DIR}/include
        ${PC_LACROSSE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    LACROSSE_LIBRARIES
    NAMES gnuradio-lacrosse
    HINTS $ENV{LACROSSE_DIR}/lib
        ${PC_LACROSSE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(LACROSSE DEFAULT_MSG LACROSSE_LIBRARIES LACROSSE_INCLUDE_DIRS)
MARK_AS_ADVANCED(LACROSSE_LIBRARIES LACROSSE_INCLUDE_DIRS)

