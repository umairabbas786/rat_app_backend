package com.electrodragon.rat_app_admin.model.network.core

import com.electrodragon.rat_app_admin.model.network.constant.ApiResponseConstant
import com.google.gson.annotations.SerializedName

data class ElectroResponse<T>(
    @SerializedName(ApiResponseConstant.RESPONSE_STATE) val responseState: String,
    @SerializedName(ApiResponseConstant.DATA) val data: T?
)
