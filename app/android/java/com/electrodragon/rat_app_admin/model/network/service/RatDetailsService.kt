package com.electrodragon.rat_app_admin.model.network.service

import com.electrodragon.rat_app_admin.model.network.constant.ApiRequestConstant
import com.electrodragon.rat_app_admin.model.network.response.RatDetailsData
import com.electrodragon.rat_app_admin.model.network.core.ElectroResponse
import retrofit2.Call
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST

interface RatDetailsService {
    @FormUrlEncoded
    @POST("rat_details.php")
    fun ratDetails(
            @Field(ApiRequestConstant.API_KEY) api_key: String,
    ): Call<ElectroResponse<RatDetailsData>>
}
