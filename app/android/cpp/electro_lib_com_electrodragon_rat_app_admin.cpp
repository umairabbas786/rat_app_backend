#include <jni.h>
#include <string>

extern "C" JNIEXPORT jstring JNICALL
Java_com_electrodragon_rat_1app_1admin_provider_ElectroLibAccessProvider_getMasterKey(JNIEnv* env, jobject _j) {
    std::string s = "7b227072696d6172794b65794964223a313837383230353535382c226b6579223a5b7b226b657944617461223a7b227479706555726c223a22747970652e676f6f676c65617069732e636f6d2f676f6f676c652e63727970746f2e74696e6b2e41657347636d4b6579222c2276616c7565223a22476944724d685963634531347749714f4a50375946656b4370585550344b6a71556150513557534c6f72504e42413d3d222c226b65794d6174657269616c54797065223a2253594d4d4554524943227d2c22737461747573223a22454e41424c4544222c226b65794964223a313837383230353535382c226f757470757450726566697854797065223a2254494e4b227d5d7d";
    return env->NewStringUTF(s.c_str());
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_electrodragon_rat_1app_1admin_provider_ElectroLibAccessProvider_getSecretKey(JNIEnv* env, jobject _j) {
    std::string s = "TJUA4THX8L7UXNSI9QYAMY6DCM55O7LWW1PHXJGX3BIICNPK42US4S2UIUKKG0Z905FG66";
    return env->NewStringUTF(s.c_str());
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_electrodragon_rat_1app_1admin_provider_ElectroLibAccessProvider_getServerBaseUrl(JNIEnv* env, jobject _j) {
    std::string s = "https://api.rat_app.com/";
    return env->NewStringUTF(s.c_str());
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_electrodragon_rat_1app_1admin_provider_ElectroLibAccessProvider_getServerApiKey(JNIEnv* env, jobject _j) {
    std::string s = "no key";
    return env->NewStringUTF(s.c_str());
}
