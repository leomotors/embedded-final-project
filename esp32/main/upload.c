#include <string.h>
#include <stdlib.h>
#include <esp_http_client.h>
#include <esp_log.h>

#include "upload.h"

const char *UPLOAD_TAG = "UPLOAD";

void send_picture(char *picture_binary, size_t size) {
  esp_http_client_config_t config = {
    // Does not support https
    .url = UPLOAD_ENDPOINT,
    .auth_type = HTTP_AUTH_TYPE_BASIC,
    .username = UPLOAD_AUTH_USERNAME,
    .password = UPLOAD_AUTH_PASSWORD,
  };
  esp_http_client_handle_t client = esp_http_client_init(&config);

  char *prefix = "--"BOUNDARY"\r\nContent-Disposition: form-data; name=\"frame_name\"\r\n\r\ngolden_frame.png\r\n--"BOUNDARY"\r\nContent-Disposition: form-data; name=\"file\"; filename=\"image_capture\"\r\nContent-Type: image/jpeg\r\n\r\n";

  char *suffix = "\r\n\r\n--"BOUNDARY"--";

  size_t prefix_len = strlen(prefix);
  size_t suffix_len = strlen(suffix);
  size_t total_len = prefix_len + suffix_len + size;
  ESP_LOGD(UPLOAD_TAG, "Prefix len: %d", prefix_len);
  ESP_LOGD(UPLOAD_TAG, "Suffix len: %d", suffix_len);
  ESP_LOGD(UPLOAD_TAG, "Total len: %d", total_len);
  char *post_data = (char*)malloc(total_len * sizeof(char)); 
  memcpy(post_data, prefix, prefix_len);
  memcpy(post_data + prefix_len, picture_binary, size);
  memcpy(post_data + prefix_len + size, suffix, suffix_len);
  esp_http_client_set_method(client, HTTP_METHOD_POST);
  esp_http_client_set_header(client, "Content-Type", "multipart/form-data; boundary="BOUNDARY);
  esp_http_client_set_post_field(client, post_data, total_len);
  esp_err_t err = esp_http_client_perform(client);

  if (err == ESP_OK) {
    ESP_LOGI(UPLOAD_TAG, "Send message OK");
  } else {
    ESP_LOGE(UPLOAD_TAG, "Send message Failed: %s", esp_err_to_name(err));
  }

  esp_http_client_close(client);
  esp_http_client_cleanup(client);
  free(post_data);
}

