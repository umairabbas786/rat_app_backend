package com.electrodragon.rat_app.provider

class ElectroLibAccessProvider {
    external fun getMasterKey(): String
    external fun getSecretKey(): String
    external fun getServerBaseUrl(): String
    external fun getServerApiKey(): String

    companion object {
        init {
            System.loadLibrary("electro_lib")
        }
    }
}
