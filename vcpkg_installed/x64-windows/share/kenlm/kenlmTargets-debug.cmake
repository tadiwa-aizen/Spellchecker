#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "kenlm::kenlm_util" for configuration "Debug"
set_property(TARGET kenlm::kenlm_util APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(kenlm::kenlm_util PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "C;CXX"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/lib/kenlm_util.lib"
  )

list(APPEND _cmake_import_check_targets kenlm::kenlm_util )
list(APPEND _cmake_import_check_files_for_kenlm::kenlm_util "${_IMPORT_PREFIX}/debug/lib/kenlm_util.lib" )

# Import target "kenlm::kenlm_builder" for configuration "Debug"
set_property(TARGET kenlm::kenlm_builder APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(kenlm::kenlm_builder PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "CXX"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/lib/kenlm_builder.lib"
  )

list(APPEND _cmake_import_check_targets kenlm::kenlm_builder )
list(APPEND _cmake_import_check_files_for_kenlm::kenlm_builder "${_IMPORT_PREFIX}/debug/lib/kenlm_builder.lib" )

# Import target "kenlm::kenlm_filter" for configuration "Debug"
set_property(TARGET kenlm::kenlm_filter APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(kenlm::kenlm_filter PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "CXX"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/lib/kenlm_filter.lib"
  )

list(APPEND _cmake_import_check_targets kenlm::kenlm_filter )
list(APPEND _cmake_import_check_files_for_kenlm::kenlm_filter "${_IMPORT_PREFIX}/debug/lib/kenlm_filter.lib" )

# Import target "kenlm::kenlm" for configuration "Debug"
set_property(TARGET kenlm::kenlm APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(kenlm::kenlm PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "CXX"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/lib/kenlm.lib"
  )

list(APPEND _cmake_import_check_targets kenlm::kenlm )
list(APPEND _cmake_import_check_files_for_kenlm::kenlm "${_IMPORT_PREFIX}/debug/lib/kenlm.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
