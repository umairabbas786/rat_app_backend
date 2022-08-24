package com.electrodragon.rat_app_admin.model.network.validator

import com.electrodragon.rat_app_admin.model.network.constant.ElectroResponseState
import com.electrodragon.rat_app_admin.model.network.response.DeleteRatData
import com.electrodragon.rat_app_admin.model.network.core.ElectroResponse
import com.electrodragon.rat_app_admin.model.network.core.BadRequest
import retrofit2.Response

interface DeleteRatValidatorCallbacks {
    fun onResponseUnsuccessful() // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
    fun onUnderMaintenance() // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
    fun onBadRequest(badRequest: BadRequest) // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
    fun onUnauthorized() // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
//    fun onDeleteRatMilestoneCompleted(thing: SomeType, thing2: SomeType)
}
class DeleteRatValidator {
    companion object {
        fun validate(
            response: Response<ElectroResponse<DeleteRatData>>,
            callbacks: DeleteRatValidatorCallbacks
        ) {
            when {
                response.isSuccessful -> {
                    response.body()?.let { electroResponse ->
                        when (electroResponse.responseState) {
                            ElectroResponseState.UNDER_MAINTENANCE -> callbacks.onUnderMaintenance()
                            ElectroResponseState.BAD_REQUEST -> {
                                val badRequest = BadRequest()
                                electroResponse.data?.exceptions?.let { exceptions ->
                                    exceptions.missingParam?.let { missingParam ->
                                        badRequest.missingParam = missingParam
                                    }
                                     exceptions.invalidValueOfParam?.let { invalidValueOfParam ->
                                         badRequest.invalidValueOfParam = invalidValueOfParam
                                     }
                                }
                                callbacks.onBadRequest(badRequest)
                            }
                            ElectroResponseState.UNAUTHORIZED -> {
                                callbacks.onUnauthorized()
                            }
//                            ElectroResponseState.COMPROMISED -> {
//                                callbacks.onDataGotCompromised()
//                            }
                            ElectroResponseState.FAILURE -> {
//                                electroResponse.data?.exceptions?.let { exceptions ->
//                                    exceptions.failedToDoSo?.let {
//                                        callbacks.onFailedToDoSo()
//                                    }
//                                }
                            }
                            else -> { // OK
                                electroResponse.data?.let { data ->
//                                    data.areThingsWorked?.let {
//                                        callbacks.onDeleteRatMilestoneCompleted(thing1, thing2)
//                                    }
                                }
                            }
                        }
                    }
                }
                else -> callbacks.onResponseUnsuccessful()
            }
        }
    }
}
