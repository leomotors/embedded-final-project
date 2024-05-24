#include <esp_log.h>
#include <esp_psram.h>
#include <esp_system.h>
#include <nvs_flash.h>
#include <string.h>
#include <sys/param.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#include <esp_camera.h>

#include <driver/gpio.h>

#include "camera.h"
#include "wifi.h"
#include "upload.h"

#define GPIO_PIN GPIO_NUM_12

const char *MAIN_TAG = "MAIN";

void app_main(void) {
    printf("will init camera\n");

    gpio_set_direction(GPIO_PIN, GPIO_MODE_INPUT);

    size_t psram_size = esp_psram_get_size();
    printf("PSRAM size: %d bytes\n", psram_size);

    if (ESP_OK != init_camera()) {
        printf("init failed :sob:\n");
        return;
    }

    printf("init wifi\n");
    init_wifi();
    printf("init wifi finished\n");

    while (!wifi_ready) {
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }

    ESP_LOGI(MAIN_TAG, "Wifi ready, start accepting gpio input");

    while (1) {
        while (1) {
            if (gpio_get_level(GPIO_PIN) == 1) {
                break;
            }
            ESP_LOGI(MAIN_TAG, "Meh");
            vTaskDelay(5000 / portTICK_PERIOD_MS);
        }
        ESP_LOGI(MAIN_TAG, "Taking picture...");
        camera_fb_t *pic = esp_camera_fb_get();

        // use pic->buf to access the image
        ESP_LOGI(MAIN_TAG, "Picture taken! Its size was: %zu bytes\nwidth: %zu height: %zu", pic->len, pic->width, pic->height);
        send_picture((char*)pic->buf, pic->len);
        ESP_LOGI(MAIN_TAG, "Message sent");

        esp_camera_fb_return(pic);
        vTaskDelay(10000 / portTICK_PERIOD_MS);
    }
}

