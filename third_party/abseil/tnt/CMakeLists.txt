find_package(absl REQUIRED CONFIG)

# To make Abseil easy for clients to link against, we create a dummy target just for installation
# purposes and combine all of Abseil's libraries into a single, easy to link against static library.
add_library(filament-abseil STATIC ${CMAKE_SOURCE_DIR}/third_party/abseil/tnt/dummy.c)

set(ABSEIL_DEPS
    # This is a full list of static library targets that Abseil exports, generated with the
    # following commands:
    # cd out/cmake-debug
    # ninja -t targets | grep libabsl | sed 's/^lib//; s/\.a: phony$//'
    absl::bad_any_cast_impl
    absl::bad_optional_access
    absl::bad_variant_access
    absl::base
    absl::city
    absl::civil_time
    absl::cord
    absl::cord_internal
    absl::cordz_functions
    absl::cordz_handle
    absl::cordz_info
    absl::cordz_sample_token
    absl::crc32c
    absl::crc_cord_state
    absl::crc_cpu_detect
    absl::crc_internal
    absl::debugging_internal
    absl::decode_rust_punycode
    absl::demangle_internal
    absl::demangle_rust
    absl::die_if_null
    absl::examine_stack
    absl::exponential_biased
    absl::failure_signal_handler
    absl::flags_commandlineflag
    absl::flags_commandlineflag_internal
    absl::flags_config
    absl::flags_internal
    absl::flags_marshalling
    absl::flags_parse
    absl::flags_private_handle_accessor
    absl::flags_program_name
    absl::flags_reflection
    absl::flags_usage
    absl::flags_usage_internal
    absl::graphcycles_internal
    absl::hash
    absl::hashtablez_sampler
    absl::int128
    absl::kernel_timeout_internal
    absl::leak_check
    absl::log_entry
    absl::log_flags
    absl::log_globals
    absl::log_initialize
    absl::log_internal_check_op
    absl::log_internal_conditions
    absl::log_internal_fnmatch
    absl::log_internal_format
    absl::log_internal_globals
    absl::log_internal_log_sink_set
    absl::log_internal_message
    absl::log_internal_nullguard
    absl::log_internal_proto
    absl::log_internal_structured_proto
    absl::log_severity
    absl::log_sink
    absl::low_level_hash
    absl::malloc_internal
    absl::periodic_sampler
    absl::poison
    absl::random_distributions
    absl::random_internal_distribution_test_util
    absl::random_internal_platform
    absl::random_internal_pool_urbg
    absl::random_internal_randen
    absl::random_internal_randen_hwaes
    absl::random_internal_randen_hwaes_impl
    absl::random_internal_randen_slow
    absl::random_internal_seed_material
    absl::random_seed_gen_exception
    absl::random_seed_sequences
    absl::raw_hash_set
    absl::raw_logging_internal
    absl::scoped_set_env
    absl::spinlock_wait
    absl::stacktrace
    absl::status
    absl::statusor
    absl::str_format_internal
    absl::strerror
    absl::string_view
    absl::strings
    absl::strings_internal
    absl::symbolize
    absl::synchronization
    absl::throw_delegate
    absl::time
    absl::time_zone
    absl::tracing_internal
    absl::utf8_for_code_point
    absl::vlog_config_internal
)
set(ABSEIL_COMBINED_OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/libabseil_combined.a")
combine_static_libs(filament-abseil "${ABSEIL_COMBINED_OUTPUT}" "${ABSEIL_DEPS}")

set(ABSEIL_LIB_NAME ${CMAKE_STATIC_LIBRARY_PREFIX}abseil${CMAKE_STATIC_LIBRARY_SUFFIX})
install(FILES "${ABSEIL_COMBINED_OUTPUT}" DESTINATION lib/${DIST_DIR} RENAME ${ABSEIL_LIB_NAME})
