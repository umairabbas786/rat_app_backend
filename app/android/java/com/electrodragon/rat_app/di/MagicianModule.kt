package com.electrodragon.rat_app.di

import com.electrodragon.rat_app.provider.ElectroLibAccessProvider
import com.electrodragon.rat_app.utils.magician.Magician
import com.google.crypto.tink.Aead
import com.google.crypto.tink.CleartextKeysetHandle
import com.google.crypto.tink.JsonKeysetReader
import com.google.crypto.tink.aead.AeadConfig
import com.google.crypto.tink.subtle.Hex
import java.nio.charset.Charset
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
class MagicianModule {
    @Provides
    @Singleton
    fun provideMagician(
        electroLibAccessProvider: ElectroLibAccessProvider
    ): Magician {
        val bytes = Hex.decode(electroLibAccessProvider.getMasterKey())
        val masterKey = String(bytes, Charset.forName("UTF-8"))
        AeadConfig.register() // Registering only Aead Primitive
        val aead = CleartextKeysetHandle.read(JsonKeysetReader.withString(masterKey))
            .getPrimitive(Aead::class.java)
        return Magician(aead, electroLibAccessProvider.getSecretKey().toByteArray())
    }
}
