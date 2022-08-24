package com.electrodragon.rat_app.model.network.service

import com.electrodragon.rat_app.model.network.constant.ApiRequestConstant
import com.electrodragon.rat_app.model.network.response.EditRatData
import com.electrodragon.rat_app.model.network.core.ElectroResponse
import retrofit2.Call
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST

interface EditRatService {
    @FormUrlEncoded
    @POST("edit_rat.php")
    fun editRat(
            @Field(ApiRequestConstant.API_KEY) api_key: String,
    ): Call<ElectroResponse<EditRatData>>
}
