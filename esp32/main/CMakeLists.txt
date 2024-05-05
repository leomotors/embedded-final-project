idf_component_register(SRCS "camera.c" "main.c" "wifi.c"
  PRIV_INCLUDE_DIRS .
  PRIV_REQUIRES nvs_flash esp_psram esp_wifi)
