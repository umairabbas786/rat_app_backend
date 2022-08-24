package com.electrodragon.rat_app_admin.model.network.service

import com.electrodragon.rat_app_admin.model.network.constant.ApiRequestConstant
import com.electrodragon.rat_app_admin.model.network.response.ShowAllRatsData
import com.electrodragon.rat_app_admin.model.network.core.ElectroResponse
import retrofit2.Call
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST

interface ShowAllRatsService {
    @FormUrlEncoded
    @POST("show_all_rats.php")
    fun showAllRats(
            @Field(ApiRequestConstant.API_KEY) api_key: String,
    ): Call<ElectroResponse<ShowAllRatsData>>
}
