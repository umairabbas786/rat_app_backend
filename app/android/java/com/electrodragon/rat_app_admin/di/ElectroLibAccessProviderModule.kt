package com.electrodragon.rat_app_admin.di

import com.electrodragon.rat_app_admin.provider.ElectroLibAccessProvider
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
class ElectroLibAccessProviderModule {
    @Provides
    @Singleton
    fun provideElectroLibAccessProviderModule(): ElectroLibAccessProvider {
        return ElectroLibAccessProvider()
    }
}
