target "dl_control_api" {
  pull     = false
  contexts = {
    bake_ctx_base_img = "target:base_jammy_db"
    bake_ctx_src_lib  = "target:dl_src_lib"
    bake_ctx_metapkg  = "target:dl_src_metapkg"
  }
  context    = "${DL_B_PROJECT_ROOT}/app/dl_control_api"
  dockerfile = "Dockerfile"
}

target "dl_data_api" {
  pull     = false
  contexts = {
    bake_ctx_base_img = "target:base_jammy_db"
    bake_ctx_src_lib  = "target:dl_src_lib"
    bake_ctx_metapkg  = "target:dl_src_metapkg"
  }
  context    = "${DL_B_PROJECT_ROOT}/app/dl_data_api"
  dockerfile = "Dockerfile"
}

target "base_jammy_db" {
  context  = "target_base_jammy_db"
  contexts = {
    bake_ctx_base_img = "target:base_jammy"
  }
  platforms = PLATFORMS
}

target "base_jammy" {
  context = "target_base_jammy"
  platforms = PLATFORMS
}

target "dloveryt_control_api" {
  pull     = false
  contexts = {
    bake_ctx_base_img = "target:base_jammy_db"
    bake_ctx_src_lib  = "target:dl_src_lib"
    bake_ctx_metapkg  = "target:dl_src_metapkg"
  }
  context    = "${DL_B_PROJECT_ROOT}/app/dloveryt_control_api"
  dockerfile = "Dockerfile"
  platforms = PLATFORMS
}

target "dloveryt_data_api" {
  pull     = false
  contexts = {
    bake_ctx_base_img = "target:base_jammy_db"
    bake_ctx_src_lib  = "target:dl_src_lib"
    bake_ctx_metapkg  = "target:dl_src_metapkg"
  }
  context    = "${DL_B_PROJECT_ROOT}/app/dloveryt_data_api"
  dockerfile = "Dockerfile"
  platforms = PLATFORMS
}
