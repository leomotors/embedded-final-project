#include <esp_log.h>
#include <esp_psram.h>
#include <esp_system.h>
#include <nvs_flash.h>
#include <string.h>
#include <sys/param.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#include <esp_camera.h>

#include "camera.h"
#include "wifi.h"
#include "upload.h"

const char *MAIN_TAG = "MAIN";

void app_main(void) {
    printf("will init camera\n");

    size_t psram_size = esp_psram_get_size();
    printf("PSRAM size: %d bytes\n", psram_size);

    if (ESP_OK != init_camera()) {
        printf("init failed :sob:\n");
        return;
    }

    printf("init wifi\n");
    init_wifi();
    printf("init wifi finished\n");

    while (1) {
        ESP_LOGI(MAIN_TAG, "Taking picture...");
        camera_fb_t *pic = esp_camera_fb_get();

        // use pic->buf to access the image
        ESP_LOGI(MAIN_TAG, "Picture taken! Its size was: %zu bytes\nwidth: %zu height: %zu", pic->len, pic->width, pic->height);
        if (wifi_ready) {
          ESP_LOGI(MAIN_TAG, "Sending message");
          send_picture((char*)pic->buf, pic->len);
          // send_picture("hello", 5);
        } else {
          ESP_LOGI(MAIN_TAG, "Wifi is not ready for sending message");
        }

        esp_camera_fb_return(pic);
        vTaskDelay(10000 / portTICK_PERIOD_MS);
    }
}

