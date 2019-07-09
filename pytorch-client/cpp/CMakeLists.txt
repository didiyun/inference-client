cmake_minimum_required(VERSION 2.8.10)
project(client-demo C CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -std=c++11 -DNDEBUG -W")

include(FindProtobuf)
find_package(Protobuf REQUIRED)

include_directories("/usr/local/include/")

FILE(GLOB CAFFE2_PROTOS "../protos/*.proto")

EXECUTE_PROCESS(
    COMMAND bash -c "mkdir ./protos" 
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

FOREACH(FIL ${CAFFE2_PROTOS})
  GET_FILENAME_COMPONENT(ABS_FIL ${FIL} ABSOLUTE)
  GET_FILENAME_COMPONENT(FIL_WE ${FIL} NAME_WE)
  message(${FIL})

  LIST(APPEND BAR_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/protos/${FIL_WE}.pb.cc")
  LIST(APPEND BAR_HDRS "${CMAKE_CURRENT_SOURCE_DIR}/protos/${FIL_WE}.pb.h")

  EXECUTE_PROCESS(
      COMMAND ${PROTOBUF_PROTOC_EXECUTABLE} -I${CMAKE_CURRENT_SOURCE_DIR}/../protos --cpp_out=${CMAKE_CURRENT_SOURCE_DIR}/protos ${FIL}
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
ENDFOREACH()


add_executable(pytorch_serving_client pytorch_serving_client.cc ${BAR_SRCS})
target_link_libraries(pytorch_serving_client curl ${PROTOBUF_LIBRARIES})

