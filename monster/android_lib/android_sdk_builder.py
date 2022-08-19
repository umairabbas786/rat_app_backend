import os
import sys
from ..route_creator import RouteCreator
from ..iterable_file_writer import write_from_iterable
from ..case_converters import pascal_to_camel
from ..case_converters import snake_to_pascal
from ..case_converters import snake_to_camel


class AndroidSdkBuilder:

    def __init__(self, eevee_config, project_root, android_app_pkg_name):
        self.start_tag = '<***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>'
        self.end_tag = '</***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>'
        self.eevee_config = eevee_config
        self.project_root = project_root
        self.pkg_name = android_app_pkg_name
        self.cpp_route = f'{self.project_root}/app/android/cpp'
        self.java_route = f'{self.project_root}/app/android/java/{self.pkg_name.replace(".", "/")}'
        self.di_route = f'{self.java_route}/di'
        self.api_client_di_route = f'{self.di_route}/api_client'
        self.network_route = f'{self.java_route}/model/network'
        self.network_client_route = f'{self.network_route}/client'
        self.network_core_route = f'{self.network_route}/core'
        self.network_constant_route = f'{self.network_route}/constant'
        self.network_response_route = f'{self.network_route}/response'
        self.network_service_route = f'{self.network_route}/service'
        self.network_validator_route = f'{self.network_route}/validator'
        self.provider_route = f'{self.java_route}/provider'
        self.magician_route = f'{self.java_route}/utils/magician'

    def create_core(self):
        android_bundle_dirs = [
            self.cpp_route,
            self.java_route,
            self.di_route,
            self.api_client_di_route,
            self.network_route,
            self.network_client_route,
            self.network_core_route,
            self.network_constant_route,
            self.network_response_route,
            self.network_service_route,
            self.network_validator_route,
            self.provider_route,
            self.magician_route
        ]
        for _android_bundle_dir in android_bundle_dirs:
            if not os.path.exists(_android_bundle_dir):
                os.system(f'mkdir -p "{_android_bundle_dir}"')
            os.system(f'mkdir -p "{self.java_route}"')
            os.system(f'mkdir -p "{self.di_route}"')
            os.system(f'mkdir -p "{self.api_client_di_route}"')
            os.system(f'mkdir -p "{self.network_route}"')
            os.system(f'mkdir -p "{self.network_client_route}"')
            os.system(f'mkdir -p "{self.network_core_route}"')
            os.system(f'mkdir -p "{self.network_constant_route}"')
            os.system(f'mkdir -p "{self.network_response_route}"')
            os.system(f'mkdir -p "{self.network_service_route}"')
            os.system(f'mkdir -p "{self.network_validator_route}"')
            os.system(f'mkdir -p "{self.provider_route}"')
            os.system(f'mkdir -p "{self.magician_route}"')

        with open(f'{self.network_core_route}/ElectroResponse.kt', 'w+') as electro_response_file:
            write_from_iterable(electro_response_file, [
                f'package {self.pkg_name}.model.network.core\n',
                f'import {self.pkg_name}.model.network.constant.ApiResponseConstant',
                f'import com.google.gson.annotations.SerializedName\n',
                f'data class ElectroResponse<T>(',
                f'    @SerializedName(ApiResponseConstant.RESPONSE_STATE) val responseState: String,',
                f'    @SerializedName(ApiResponseConstant.DATA) val data: T?',
                f')'
            ], suffix='\n')

        with open(f'{self.network_core_route}/MultipartHelper.java', 'w+') as multipart_helper_file:
            write_from_iterable(multipart_helper_file, [
                f'package {self.pkg_name}.model.network.core;\n',

                'import java.io.File;',
                'import okhttp3.MediaType;',
                'import okhttp3.MultipartBody;',
                'import okhttp3.RequestBody;\n',

                'public class MultipartHelper {',
                '    public static RequestBody createRequestBody(String payload) {',
                '        return RequestBody.create(payload, MediaType.parse("multipart/form-data"));',
                '    }\n',

                '    /**',
                '     * @param partKey: server identifier for its file.',
                '     * @param imageName: original name of image.',
                '     * @param image: file pointing to real image',
                '     */',
                '    public static MultipartBody.Part createMultipartBodyPartImage(String partKey, String imageName, File image) {',
                '        RequestBody requestBody = RequestBody.create(image, MediaType.parse("image/*"));',
                '        return MultipartBody.Part.createFormData(partKey, imageName, requestBody);',
                '    }',
                '}',
            ], suffix='\n')

        with open(f'{self.network_constant_route}/ApiResponseConstant.kt', 'w+') as api_res_const_file:
            write_from_iterable(api_res_const_file, [
                f'package {self.pkg_name}.model.network.constant\n',
                f'object ApiResponseConstant {{',
                f'    const val RESPONSE_STATE = "state"',
                f'    const val DATA = "data"',
                f'    const val EXCEPTIONS = "exceptions"',
                f'    const val MISSING_PARAM = "missing_param"',
                f'    const val INVALID_VALUE_OF_PARAM = "invalid_value_of_param"',
                f'    const val ID = "id"',
                f'    const val UID = "uid"',
                f'    const val CREATED_AT = "created_at"',
                f'    const val UPDATED_AT = "updated_at"',
                f'}}'
            ], suffix='\n')

        with open(f'{self.network_constant_route}/ApiRequestConstant.kt', 'w+') as api_req_const_file:
            write_from_iterable(api_req_const_file, [
                f'package {self.pkg_name}.model.network.constant\n',
                f'object ApiRequestConstant {{',
                f'    const val API_KEY = "__api_key__"',
                f'}}'
            ], suffix='\n')

        with open(f'{self.network_constant_route}/ElectroResponseState.kt', 'w+') as electro_res_state_file:
            write_from_iterable(electro_res_state_file, [
                f'package {self.pkg_name}.model.network.constant\n',
                f'object ElectroResponseState {{',
                f'    const val OK = "OK"',
                f'    const val UNDER_MAINTENANCE = "UNDER_MAINTENANCE"',
                f'    const val UNAUTHORIZED = "UNAUTHORIZED"',
                f'    const val COMPROMISED = "COMPROMISED"',
                f'    const val BAD_REQUEST = "BAD_REQUEST"',
                f'    const val FAILURE = "FAILURE"',
                f'}}'
            ], suffix='\n')

        api_agents = os.listdir(f'{self.project_root}/app/agents')
        api_agents.sort()

        with open(f'{self.network_client_route}/ApiClient.kt', 'w+') as api_client_file:
            api_client_file.write(f'package {self.pkg_name}.model.network.client\n\n')
            api_client_file.write(f'import {self.pkg_name}.model.network.service.*\n\n')
            api_client_file.write(f'class ApiClient(\n')
            for api_agent in api_agents:
                comma_prefix = ',' if api_agent != api_agents[-1] else ''
                agent_name = api_agent.split('.php')[0]
                api_client_file.write(f'    val {pascal_to_camel(agent_name)}Service: {agent_name}Service{comma_prefix}\n')
            api_client_file.write(f')\n')

        with open(f'{self.api_client_di_route}/ApiClientModule.kt', 'w+') as api_client_module_file:
            write_from_iterable(api_client_module_file, [
                f'package {self.pkg_name}.di.api_client\n',
                f'import {self.pkg_name}.model.network.client.ApiClient',
                f'import {self.pkg_name}.model.network.service.*',
                f'import dagger.Module',
                f'import dagger.Provides',
                f'import dagger.hilt.InstallIn',
                f'import dagger.hilt.components.SingletonComponent',
                f'import retrofit2.Retrofit',
                f'import javax.inject.Singleton\n',
                f'@Module',
                f'@InstallIn(SingletonComponent::class)',
                f'class ApiClientModule {{',
                f'    @Provides',
                f'    @Singleton',
                f'    fun provideApiClient(retrofit: Retrofit): ApiClient {{',
                f'        return ApiClient(',
            ], suffix='\n')
            for api_agent in api_agents:
                comma_prefix = ',' if api_agent != api_agents[-1] else ''
                api_client_module_file.write(f'            retrofit.create({api_agent[:-4]}Service::class.java){comma_prefix}\n')
            api_client_module_file.write(f'        )\n')
            api_client_module_file.write(f'    }}\n')
            api_client_module_file.write(f'}}\n')

        with open(f'{self.api_client_di_route}/OkHttpClientModule.kt', 'w+') as ok_http_client_module_file:
            write_from_iterable(ok_http_client_module_file, [
                f'package {self.pkg_name}.di.api_client\n',
                f'import dagger.Module',
                f'import dagger.Provides',
                f'import dagger.hilt.InstallIn',
                f'import dagger.hilt.components.SingletonComponent',
                f'import okhttp3.OkHttpClient',
                f'import okhttp3.logging.HttpLoggingInterceptor',
                f'import java.util.concurrent.TimeUnit',
                f'import javax.inject.Singleton\n',
                f'@Module',
                f'@InstallIn(SingletonComponent::class)',
                f'class OkHttpClientModule {{',
                f'    @Provides',
                f'    @Singleton',
                f'    fun provideOkHttpClient(): OkHttpClient {{',
                f'        val logging = HttpLoggingInterceptor()',
                f'        logging.setLevel(HttpLoggingInterceptor.Level.HEADERS)\n',
                f'        return OkHttpClient.Builder()',
                f'            .readTimeout(5, TimeUnit.MINUTES)',
                f'            .connectTimeout(5, TimeUnit.MINUTES)',
                f'            .addInterceptor(logging)',
                f'            .build()',
                f'    }}',
                f'}}',
            ], suffix='\n')

        with open(f'{self.cpp_route}/electro_lib_{self.pkg_name.replace(".", "_")}.cpp', 'w+') as electro_lib_file:
            electro_lib_file_content = [
                '#include <jni.h>',
                '#include <string>',
                '',
                'extern "C" JNIEXPORT jstring JNICALL',
                f'Java_{self.pkg_name.replace("_", "_1").replace(".", "_")}_provider_ElectroLibAccessProvider_getMasterKey(JNIEnv* env, jobject _j) {{',
                '{}std::string s = "{}";'.format(' ' * 4, self.eevee_config.get_tink_master_key()),
                '{}return env->NewStringUTF(s.c_str());'.format(' ' * 4),
                '}',
                '',
                'extern "C" JNIEXPORT jstring JNICALL',
                f'Java_{self.pkg_name.replace("_", "_1").replace(".", "_")}_provider_ElectroLibAccessProvider_getSecretKey(JNIEnv* env, jobject _j) {{',
                '{}std::string s = "{}";'.format(' ' * 4, self.eevee_config.get_android_tink_secret_key()),
                '{}return env->NewStringUTF(s.c_str());'.format(' ' * 4),
                '}',
                '',
                'extern "C" JNIEXPORT jstring JNICALL',
                f'Java_{self.pkg_name.replace("_", "_1").replace(".", "_")}_provider_ElectroLibAccessProvider_getServerBaseUrl(JNIEnv* env, jobject _j) {{',
                '{}std::string s = "{}";'.format(' ' * 4, self.eevee_config.get_server_base_url()),
                '{}return env->NewStringUTF(s.c_str());'.format(' ' * 4),
                '}'
            ]

            for env_key in self.eevee_config.get_env_list():
                if env_key[0] == '__api_key__':
                    electro_lib_file_content.append('\nextern "C" JNIEXPORT jstring JNICALL'),
                    electro_lib_file_content.append(f'Java_{self.pkg_name.replace("_", "_1").replace(".", "_")}_provider_ElectroLibAccessProvider_getServerApiKey(JNIEnv* env, jobject _j) {{'),
                    electro_lib_file_content.append('{}std::string s = "{}";'.format(' ' * 4, env_key[1])),
                    electro_lib_file_content.append('{}return env->NewStringUTF(s.c_str());'.format(' ' * 4)),
                    electro_lib_file_content.append('}')
                    break

            for lin in electro_lib_file_content:
                electro_lib_file.write(f'{lin}\n')

        with open(f'{self.provider_route}/ElectroLibAccessProvider.kt', 'w+') as electro_lib_provider_file:
            write_from_iterable(electro_lib_provider_file, [
                f'package {self.pkg_name}.provider\n',
                f'class ElectroLibAccessProvider {{',
                f'    external fun getMasterKey(): String',
                f'    external fun getSecretKey(): String',
                f'    external fun getServerBaseUrl(): String',
            ], suffix='\n')

            if len(list(filter(lambda x: x[0] == '__api_key__', self.eevee_config.get_env_list()))) == 1:
                electro_lib_provider_file.write(f'    external fun getServerApiKey(): String\n')

            write_from_iterable(electro_lib_provider_file, [
                f'\n    companion object {{',
                f'        init {{',
                f'            System.loadLibrary("electro_lib")',
                f'        }}',
                f'    }}',
                f'}}'
            ], suffix='\n')

        with open(f'{self.di_route}/ElectroLibAccessProviderModule.kt', 'w+') as electro_lib_access_provider_module:
            write_from_iterable(electro_lib_access_provider_module, [
                f'package {self.pkg_name}.di\n',
                f'import {self.pkg_name}.provider.ElectroLibAccessProvider',
                f'import dagger.Module',
                f'import dagger.Provides',
                f'import dagger.hilt.InstallIn',
                f'import dagger.hilt.components.SingletonComponent',
                f'import javax.inject.Singleton\n',
                f'@Module',
                f'@InstallIn(SingletonComponent::class)',
                f'class ElectroLibAccessProviderModule {{',
                f'    @Provides',
                f'    @Singleton',
                f'    fun provideElectroLibAccessProviderModule(): ElectroLibAccessProvider {{',
                f'        return ElectroLibAccessProvider()',
                f'    }}',
                f'}}'
            ], suffix='\n')

        with open(f'{self.provider_route}/ElectroLibAccessProvider.kt', 'w+') as electro_lib_provider_file:
            write_from_iterable(electro_lib_provider_file, [
                f'package {self.pkg_name}.provider\n',
                f'class ElectroLibAccessProvider {{',
                f'    external fun getMasterKey(): String',
                f'    external fun getSecretKey(): String',
                f'    external fun getServerBaseUrl(): String',
            ], suffix='\n')

            if len(list(filter(lambda x: x[0] == '__api_key__', self.eevee_config.get_env_list()))) == 1:
                electro_lib_provider_file.write(f'    external fun getServerApiKey(): String\n')

            write_from_iterable(electro_lib_provider_file, [
                f'\n    companion object {{',
                f'        init {{',
                f'            System.loadLibrary("electro_lib")',
                f'        }}',
                f'    }}',
                f'}}',
            ], suffix='\n')

        with open(f'{self.api_client_di_route}/RetrofitModule.kt', 'w+') as retrofit_module_file:
            write_from_iterable(retrofit_module_file, [
                f'package {self.pkg_name}.di.api_client\n',
                f'import {self.pkg_name}.provider.ElectroLibAccessProvider',
                f'import dagger.Module',
                f'import dagger.Provides',
                f'import dagger.hilt.InstallIn',
                f'import dagger.hilt.components.SingletonComponent',
                f'import okhttp3.OkHttpClient',
                f'import retrofit2.Retrofit',
                f'import retrofit2.converter.gson.GsonConverterFactory',
                f'import javax.inject.Singleton\n',
                f'@Module',
                f'@InstallIn(SingletonComponent::class)',
                f'class RetrofitModule {{',
                f'    @Provides',
                f'    @Singleton',
                f'    fun provideRetrofit(',
                f'        electroLibAccessProvider: ElectroLibAccessProvider,',
                f'        okHttpClient: OkHttpClient',
                f'    ): Retrofit {{',
                f'        return Retrofit.Builder()',
                f'            .baseUrl(electroLibAccessProvider.getServerBaseUrl())',
                f'            .addConverterFactory(GsonConverterFactory.create())',
                f'            .client(okHttpClient)',
                f'            .build()',
                f'    }}',
                f'}}'
            ], suffix='\n')

        with open(f'{self.magician_route}/Magician.kt', 'w+') as magician_file:
            write_from_iterable(magician_file, [
                f'package {self.pkg_name}.utils.magician\n',
                'import com.google.crypto.tink.Aead',
                'import com.google.crypto.tink.subtle.Base64\n',
                'class Magician(',
                '    private val aead: Aead,',
                '    private val secret: ByteArray',
                ') {',
                '    fun encrypt(content: String, secretKey: String): String {',
                '        return encrypt(content, secretKey.toByteArray())',
                '    }\n',
                '    private fun encrypt(content: String, secretKey: ByteArray): String {',
                '        return Base64.encode(aead.encrypt(content.toByteArray(), secretKey))',
                '    }\n',
                '    fun encrypt(content: String): String {',
                '        return encrypt(content, secret)',
                '    }\n',
                '    fun decrypt(cipherText: String): String {',
                '        return decrypt(cipherText, secret)',
                '    }\n',
                '    fun decrypt(cipherText: String, secretKey: String): String {',
                '        return decrypt(cipherText, secretKey.toByteArray())',
                '    }\n',
                '    private fun decrypt(cipherText: String, secretKey: ByteArray): String {',
                '        return String(aead.decrypt(Base64.decode(cipherText), secretKey))',
                '    }\n',
                '}'
            ], suffix='\n')

        with open(f'{self.di_route}/MagicianModule.kt', 'w+') as magician_module:
            write_from_iterable(magician_module, [
                f'package {self.pkg_name}.di\n',
                f'import {self.pkg_name}.provider.ElectroLibAccessProvider',
                f'import {self.pkg_name}.utils.magician.Magician',
                f'import com.google.crypto.tink.Aead',
                f'import com.google.crypto.tink.CleartextKeysetHandle',
                f'import com.google.crypto.tink.JsonKeysetReader',
                f'import com.google.crypto.tink.aead.AeadConfig',
                f'import com.google.crypto.tink.subtle.Hex',
                f'import java.nio.charset.Charset',
                f'import dagger.Module',
                f'import dagger.Provides',
                f'import dagger.hilt.InstallIn',
                f'import dagger.hilt.components.SingletonComponent',
                f'import javax.inject.Singleton\n',
                f'@Module',
                f'@InstallIn(SingletonComponent::class)',
                f'class MagicianModule {{',
                f'    @Provides',
                f'    @Singleton',
                f'    fun provideMagician(',
                f'        electroLibAccessProvider: ElectroLibAccessProvider',
                f'    ): Magician {{',
                f'        val bytes = Hex.decode(electroLibAccessProvider.getMasterKey())',
                f'        val masterKey = String(bytes, Charset.forName("UTF-8"))',
                f'        AeadConfig.register() // Registering only Aead Primitive',
                f'        val aead = CleartextKeysetHandle.read(JsonKeysetReader.withString(masterKey))',
                f'            .getPrimitive(Aead::class.java)',
                f'        return Magician(aead, electroLibAccessProvider.getSecretKey().toByteArray())',
                f'    }}',
                f'}}'
            ], suffix='\n')

        with open(f'{self.network_core_route}/BadRequest.kt', 'w+') as core_bad_request:
            write_from_iterable(core_bad_request, [
                f'package {self.pkg_name}.model.network.core\n',
                f'class BadRequest {{',
                f'    var missingParam: String? = null',
                f'    var invalidValueOfParam: String? = null\n',
                f'    fun getMoreInfo(callbacks: BadRequestCallbacks) {{',
                f'        when {{',
                f'            missingParam != null -> callbacks.onMissingParam(missingParam!!)',
                f'            invalidValueOfParam != null -> callbacks.onInvalidValueOfParam(invalidValueOfParam!!)',
                f'            else -> callbacks.onDebugModeDisabled()',
                f'        }}',
                f'    }}',
                f'}}\n',
                f'interface BadRequestCallbacks {{',
                f'    fun onMissingParam(param: String)',
                f'    fun onInvalidValueOfParam(param: String)',
                f'    fun onDebugModeDisabled()',
                f'}}'
            ], suffix='\n')

    def create_service_response_validator(self, agent_name):
        with open(f'{self.network_service_route}/{agent_name}Service.kt', 'w+') as agent_service:
            agent_service.write(f'package {self.pkg_name}.model.network.service\n\n')
            agent_service.write(f'import {self.pkg_name}.model.network.constant.ApiRequestConstant\n')
            agent_service.write(f'import {self.pkg_name}.model.network.response.{agent_name}Data\n')
            agent_service.write(f'import {self.pkg_name}.model.network.core.ElectroResponse\n')
            agent_service.write(f'import retrofit2.Call\n')
            agent_service.write(f'import retrofit2.http.Field\n')
            agent_service.write(f'import retrofit2.http.FormUrlEncoded\n')
            agent_service.write(f'import retrofit2.http.POST\n\n')
            agent_service.write(f'interface {agent_name}Service {{\n')
            agent_service.write(f'    @FormUrlEncoded\n')
            agent_route_name = RouteCreator(f'{agent_name}.php').get_route_name()
            agent_service.write(f'    @POST("{agent_route_name}")\n')
            agent_service.write(f'    fun {agent_name[0].lower() + agent_name[1:]}(\n')
            agent_service.write(f'            @Field(ApiRequestConstant.API_KEY) api_key: String,\n')
            agent_service.write(f'    ): Call<ElectroResponse<{agent_name}Data>>\n')
            agent_service.write(f'}}\n')

        with open(f'{self.network_response_route}/{agent_name}Response.kt', 'w+') as agent_response_file:
            agent_response_file.write(f'package {self.pkg_name}.model.network.response\n\n')
            agent_response_file.write(f'import {self.pkg_name}.model.network.constant.ApiResponseConstant\n')
            agent_response_file.write(f'import com.google.gson.annotations.SerializedName\n\n')

            agent_response_file.write(f'data class {agent_name}Data (\n')
            agent_response_file.write(f'        @SerializedName(ApiResponseConstant.EXCEPTIONS) val exceptions: {agent_name}ResponseClasses.Exceptions?,\n')
            agent_response_file.write(f'        @SerializedName("attribute_name") val attributeName: Boolean?\n')
            agent_response_file.write(f')\n\n')

            agent_response_file.write(f'object {agent_name}ResponseClasses {{\n')
            agent_response_file.write(f'    data class Exceptions( // {self.start_tag}\n')
            agent_response_file.write(f'        @SerializedName(ApiResponseConstant.MISSING_PARAM) val missingParam: String?,\n')
            agent_response_file.write(f'        @SerializedName(ApiResponseConstant.INVALID_VALUE_OF_PARAM) val invalidValueOfParam: String?,\n')
            agent_response_file.write(f'        @SerializedName("some_exception_name") val exceptionName: Boolean?\n')
            agent_response_file.write(f'    ) // {self.end_tag}\n')
            agent_response_file.write('}\n')

        with open(f'{self.network_validator_route}/{agent_name}Validator.kt', 'w+') as agent_validator_file:
            agent_validator_file.write(f'package {self.pkg_name}.model.network.validator\n\n')
            agent_validator_file.write(f'import {self.pkg_name}.model.network.constant.ElectroResponseState\n')
            agent_validator_file.write(f'import {self.pkg_name}.model.network.response.{agent_name}Data\n')
            agent_validator_file.write(f'import {self.pkg_name}.model.network.core.ElectroResponse\n')
            agent_validator_file.write(f'import {self.pkg_name}.model.network.core.BadRequest\n')
            agent_validator_file.write(f'import retrofit2.Response\n\n')

            agent_validator_file.write(f'interface {agent_name}ValidatorCallbacks {{\n')
            agent_validator_file.write(f'    fun onResponseUnsuccessful() // {self.start_tag}\n')
            agent_validator_file.write(f'    fun onUnderMaintenance() // {self.start_tag}\n')
            agent_validator_file.write(f'    fun onBadRequest(badRequest: BadRequest) // {self.start_tag}\n')
            agent_validator_file.write(f'    fun onUnauthorized() // {self.start_tag}\n')
            agent_validator_file.write(f'//    fun on{agent_name}MilestoneCompleted(thing: SomeType, thing2: SomeType)\n')
            agent_validator_file.write(f'}}\n')

            agent_validator_file.write(f'class {agent_name}Validator {{\n')
            agent_validator_file.write(f'    companion object {{\n')
            agent_validator_file.write(f'        fun validate(\n')
            agent_validator_file.write(f'            response: Response<ElectroResponse<{agent_name}Data>>,\n')
            agent_validator_file.write(f'            callbacks: {agent_name}ValidatorCallbacks\n')
            agent_validator_file.write(f'        ) {{\n')
            agent_validator_file.write(f'            when {{\n')
            agent_validator_file.write(f'                response.isSuccessful -> {{\n')
            agent_validator_file.write(f'                    response.body()?.let {{ electroResponse ->\n')
            agent_validator_file.write(f'                        when (electroResponse.responseState) {{\n')
            agent_validator_file.write(f'                            ElectroResponseState.UNDER_MAINTENANCE -> callbacks.onUnderMaintenance()\n')
            agent_validator_file.write(f'                            ElectroResponseState.BAD_REQUEST -> {{\n')
            agent_validator_file.write(f'                                val badRequest = BadRequest()\n')
            agent_validator_file.write(f'                                electroResponse.data?.exceptions?.let {{ exceptions ->\n')
            agent_validator_file.write(f'                                    exceptions.missingParam?.let {{ missingParam ->\n')
            agent_validator_file.write(f'                                        badRequest.missingParam = missingParam\n')
            agent_validator_file.write(f'                                    }}\n')
            agent_validator_file.write('                                     exceptions.invalidValueOfParam?.let { invalidValueOfParam ->\n')
            agent_validator_file.write('                                         badRequest.invalidValueOfParam = invalidValueOfParam\n')
            agent_validator_file.write('                                     }\n')
            agent_validator_file.write(f'                                }}\n')
            agent_validator_file.write(f'                                callbacks.onBadRequest(badRequest)\n')
            agent_validator_file.write(f'                            }}\n')
            agent_validator_file.write(f'                            ElectroResponseState.UNAUTHORIZED -> {{\n')
            agent_validator_file.write(f'                                callbacks.onUnauthorized()\n')
            agent_validator_file.write(f'                            }}\n')
            agent_validator_file.write(f'//                            ElectroResponseState.COMPROMISED -> {{\n')
            agent_validator_file.write(f'//                                callbacks.onDataGotCompromised()\n')
            agent_validator_file.write(f'//                            }}\n')
            agent_validator_file.write(f'                            ElectroResponseState.FAILURE -> {{\n')
            agent_validator_file.write(f'//                                electroResponse.data?.exceptions?.let {{ exceptions ->\n')
            agent_validator_file.write(f'//                                    exceptions.failedToDoSo?.let {{\n')
            agent_validator_file.write(f'//                                        callbacks.onFailedToDoSo()\n')
            agent_validator_file.write(f'//                                    }}\n')
            agent_validator_file.write(f'//                                }}\n')
            agent_validator_file.write(f'                            }}\n')
            agent_validator_file.write(f'                            else -> {{ // OK\n')
            agent_validator_file.write(f'                                electroResponse.data?.let {{ data ->\n')
            agent_validator_file.write(f'//                                    data.areThingsWorked?.let {{\n')
            agent_validator_file.write(f'//                                        callbacks.on{agent_name}MilestoneCompleted(thing1, thing2)\n')
            agent_validator_file.write(f'//                                    }}\n')
            agent_validator_file.write(f'                                }}\n')
            agent_validator_file.write(f'                            }}\n')
            agent_validator_file.write(f'                        }}\n')
            agent_validator_file.write(f'                    }}\n')
            agent_validator_file.write(f'                }}\n')
            agent_validator_file.write(f'                else -> callbacks.onResponseUnsuccessful()\n')
            agent_validator_file.write(f'            }}\n')
            agent_validator_file.write(f'        }}\n')
            agent_validator_file.write(f'    }}\n')
            agent_validator_file.write(f'}}\n')

    def re_assemble_response(self, agent_name, failure_exceptions, compromised_exceptions):
        top_content = []
        bottom_content = []

        with open(f'{self.network_response_route}/{agent_name}Response.kt', 'r') as agent_response_file:
            lines = agent_response_file.readlines()

            for lin in lines:
                top_content.append(lin)
                if self.start_tag in lin:
                    break

            while len(lines) != 0:
                lin = lines[0]
                lines.pop(0)
                if self.end_tag in lin:
                    bottom_content.append(lin)
                    break

            bottom_content.extend(lines)

        with open(f'{self.network_response_route}/{agent_name}Response.kt', 'w+') as agent_response_file:
            write_from_iterable(agent_response_file, top_content)

            agent_response_file.write(f'        @SerializedName(ApiResponseConstant.MISSING_PARAM) val missingParam: String?,\n')
            exceptions_count = len(failure_exceptions) + len(compromised_exceptions)
            needs_comma = exceptions_count > 0
            serialized_val = '@SerializedName(ApiResponseConstant.INVALID_VALUE_OF_PARAM)'
            agent_response_file.write(f'        {serialized_val} val invalidValueOfParam: String?{"," if needs_comma else ""}\n')

            all_exceptions = []
            all_exceptions.extend(failure_exceptions)
            all_exceptions.extend(compromised_exceptions)

            for e in all_exceptions:
                is_last_e = e == all_exceptions[-1]
                agent_response_file.write(f'        @SerializedName("{e}") val {snake_to_camel(e)}: Boolean?{"" if is_last_e else ","}\n')

            write_from_iterable(agent_response_file, bottom_content)

    def re_assemble_validator(self, agent_name, failure_exceptions, compromised_exceptions):
        top_content = []
        interface_methods = []
        ok_content = []
        with open(f'{self.network_validator_route}/{agent_name}Validator.kt', 'r') as agent_validator_file:
            lines = agent_validator_file.readlines()
            while len(lines) != 0:
                lin = lines[0]
                lines.pop(0)
                if f'package {self.pkg_name}' in lin:
                    top_content.append(lin)
                    top_content.append('\n')
                elif f'import {self.pkg_name}' in lin or 'import retrofit2.Response' in lin:
                    top_content.append(lin)
                elif f'interface {agent_name}ValidatorCallbacks' in lin:
                    while '}' not in lin:
                        lin = lines[0]
                        lines.pop(0)
                        if 'fun onResponseUnsuccessful()' in lin:
                            continue
                        elif 'fun onUnderMaintenance()' in lin:
                            continue
                        elif 'fun onBadRequest(badRequest: BadRequest)' in lin:
                            continue
                        elif 'fun onUnauthorized()' in lin:
                            continue
                        elif self.start_tag in lin:
                            continue
                        else:
                            if '}' not in lin:
                                interface_methods.append(lin)
                elif f'                            else -> {{ // OK' in lin:
                    ok_content.append(lin)
                    ok_content.extend(lines)
                    break

        with open(f'{self.network_validator_route}/{agent_name}Validator.kt', 'w+') as agent_validator_file:
            write_from_iterable(agent_validator_file, top_content)  # Writing packages and import statements

            agent_validator_file.write('\n')

            agent_validator_file.write(f'interface {agent_name}ValidatorCallbacks {{\n')
            agent_validator_file.write(f'    fun onResponseUnsuccessful() // {self.start_tag}\n')
            agent_validator_file.write(f'    fun onUnderMaintenance() // {self.start_tag}\n')
            agent_validator_file.write(f'    fun onBadRequest(badRequest: BadRequest) // {self.start_tag}\n')
            agent_validator_file.write(f'    fun onUnauthorized() // {self.start_tag}\n')
            for e in failure_exceptions:
                agent_validator_file.write(f'    fun on{snake_to_pascal(e)}() // {self.start_tag}\n')
            for e in compromised_exceptions:
                agent_validator_file.write(f'    fun on{snake_to_pascal(e)}() // {self.start_tag}\n')
            write_from_iterable(agent_validator_file, interface_methods)
            agent_validator_file.write(f'}}\n')

            agent_validator_file.write('\n')

            write_from_iterable(agent_validator_file, [
                f'class {agent_name}Validator {{',
                f'    companion object {{',
                f'        fun validate(',
                f'            response: Response<ElectroResponse<{agent_name}Data>>,',
                f'            callbacks: {agent_name}ValidatorCallbacks',
                f'        ) {{',
                f'            when {{',
                f'                response.isSuccessful -> {{',
                f'                    response.body()?.let {{ electroResponse ->',
                f'                        when (electroResponse.responseState) {{',
                f'                            ElectroResponseState.UNDER_MAINTENANCE -> callbacks.onUnderMaintenance()',
                f'                            ElectroResponseState.BAD_REQUEST -> {{',
                f'                                val badRequest = BadRequest()',
                f'                                electroResponse.data?.exceptions?.let {{ exceptions ->',
                f'                                    exceptions.missingParam?.let {{ missingParam ->',
                f'                                        badRequest.missingParam = missingParam',
                f'                                    }}',
                '                                     exceptions.invalidValueOfParam?.let { invalidValueOfParam ->',
                '                                         badRequest.invalidValueOfParam = invalidValueOfParam',
                '                                     }',
                f'                                }}',
                f'                                callbacks.onBadRequest(badRequest)',
                f'                            }}',
                f'                            ElectroResponseState.UNAUTHORIZED -> {{',
                f'                                callbacks.onUnauthorized()',
                f'                            }}',
            ], suffix='\n')

            if len(compromised_exceptions) > 0:
                agent_validator_file.write(f'                            ElectroResponseState.COMPROMISED -> {{\n')
                agent_validator_file.write(f'                                electroResponse.data?.exceptions?.let {{ exceptions ->\n')
                for e in compromised_exceptions:
                    agent_validator_file.write(f'                                    exceptions.{snake_to_camel(e)}?.let {{\n')
                    agent_validator_file.write(f'                                        callbacks.on{snake_to_pascal(e)}()\n')
                    agent_validator_file.write(f'                                    }}\n')
                agent_validator_file.write(f'                                }}\n')
                agent_validator_file.write(f'                            }}\n')

            if len(failure_exceptions) > 0:
                agent_validator_file.write(f'                            ElectroResponseState.FAILURE -> {{\n')
                agent_validator_file.write(f'                                electroResponse.data?.exceptions?.let {{ exceptions ->\n')
                for e in failure_exceptions:
                    agent_validator_file.write(f'                                    exceptions.{snake_to_camel(e)}?.let {{\n')
                    agent_validator_file.write(f'                                        callbacks.on{snake_to_pascal(e)}()\n')
                    agent_validator_file.write(f'                                    }}\n')
                agent_validator_file.write(f'                                }}\n')
                agent_validator_file.write(f'                            }}\n')

            write_from_iterable(agent_validator_file, ok_content)

    def make_from_first_pkg_service_response_validator(self, first_pkg_name):
        for service in os.listdir(f'{self.project_root}/app/android/java/{first_pkg_name.replace(".", "/")}/model/network/service'):
            with open(f'{self.network_service_route}/{service}', 'w+') as agent_service_to_write:
                with open(f'{self.project_root}/app/android/java/{first_pkg_name.replace(".", "/")}/model/network/service/{service}', 'r') as agent_service:
                    for lin in agent_service.readlines():
                        if first_pkg_name in lin:
                            lin = lin.replace(first_pkg_name, self.pkg_name)
                        agent_service_to_write.write(lin)

        for response_file in os.listdir(f'{self.project_root}/app/android/java/{first_pkg_name.replace(".", "/")}/model/network/response'):
            with open(f'{self.network_response_route}/{response_file}', 'w+') as agent_response_to_write:
                with open(f'{self.project_root}/app/android/java/{first_pkg_name.replace(".", "/")}/model/network/response/{response_file}', 'r') as agent_response:
                    for lin in agent_response.readlines():
                        if first_pkg_name in lin:
                            lin = lin.replace(first_pkg_name, self.pkg_name)
                        agent_response_to_write.write(lin)

        for validator_file in os.listdir(f'{self.project_root}/app/android/java/{first_pkg_name.replace(".", "/")}/model/network/validator'):
            with open(f'{self.network_validator_route}/{validator_file}', 'w+') as agent_validator_to_write:
                with open(f'{self.project_root}/app/android/java/{first_pkg_name.replace(".", "/")}/model/network/validator/{validator_file}', 'r') as agent_validator:
                    for lin in agent_validator.readlines():
                        if first_pkg_name in lin:
                            lin = lin.replace(first_pkg_name, self.pkg_name)
                        agent_validator_to_write.write(lin)
