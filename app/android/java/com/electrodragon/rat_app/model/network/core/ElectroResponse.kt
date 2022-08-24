package com.electrodragon.rat_app.model.network.core

import com.electrodragon.rat_app.model.network.constant.ApiResponseConstant
import com.google.gson.annotations.SerializedName

data class ElectroResponse<T>(
    @SerializedName(ApiResponseConstant.RESPONSE_STATE) val responseState: String,
    @SerializedName(ApiResponseConstant.DATA) val data: T?
)
