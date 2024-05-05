idf_component_register(SRCS "main.c" "wifi.c"
  PRIV_INCLUDE_DIRS .
  PRIV_REQUIRES nvs_flash REQUIRES esp_psram esp_wifi)
