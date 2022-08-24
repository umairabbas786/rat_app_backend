package com.electrodragon.rat_app_admin.model.network.response

import com.electrodragon.rat_app_admin.model.network.constant.ApiResponseConstant
import com.google.gson.annotations.SerializedName

data class DeleteRatData (
        @SerializedName(ApiResponseConstant.EXCEPTIONS) val exceptions: DeleteRatResponseClasses.Exceptions?,
        @SerializedName("attribute_name") val attributeName: Boolean?
)

object DeleteRatResponseClasses {
    data class Exceptions( // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        @SerializedName(ApiResponseConstant.MISSING_PARAM) val missingParam: String?,
        @SerializedName(ApiResponseConstant.INVALID_VALUE_OF_PARAM) val invalidValueOfParam: String?,
        @SerializedName("some_exception_name") val exceptionName: Boolean?
    ) // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
}
