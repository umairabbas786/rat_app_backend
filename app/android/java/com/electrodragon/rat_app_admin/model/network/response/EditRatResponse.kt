package com.electrodragon.rat_app_admin.model.network.response

import com.electrodragon.rat_app_admin.model.network.constant.ApiResponseConstant
import com.google.gson.annotations.SerializedName

data class EditRatData (
        @SerializedName(ApiResponseConstant.EXCEPTIONS) val exceptions: EditRatResponseClasses.Exceptions?,
        @SerializedName("attribute_name") val attributeName: Boolean?
)

object EditRatResponseClasses {
    data class Exceptions( // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        @SerializedName(ApiResponseConstant.MISSING_PARAM) val missingParam: String?,
        @SerializedName(ApiResponseConstant.INVALID_VALUE_OF_PARAM) val invalidValueOfParam: String?,
        @SerializedName("some_exception_name") val exceptionName: Boolean?
    ) // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
}
