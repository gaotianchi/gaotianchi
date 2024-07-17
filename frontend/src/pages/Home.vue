<script setup lang="ts">
import { getMyProfile } from '@/apis';
import type { MyProfile } from '@/typing';
import { onMounted, ref, type Ref } from 'vue';
const myProfile: Ref<MyProfile | null> = ref(null)

onMounted(() => {
    getMyProfile().then((mp) => {
        myProfile.value = mp;
        if (mp.blogSubTitle) {
            document.title = mp.blogTitle + " -- " + mp.blogSubTitle;
        } else {
            document.title = mp.blogTitle;
        }
    })
})
</script>

<template>
    <main>
        <header class="flex items-center space-x-4 p-4 bg-gray-100">
            <img alt="logo" class="logo rounded-full w-32 h-32 object-cover m-3" src="@/assets/logo.png" />
            <div class="flex flex-col m-0 sjdkfslsdf">
                <p class="text-lg font-semibold">{{ myProfile?.profile }}</p>
                <nav class="mt-2">
                    <RouterLink class="text-base font-normal text-gray-500 list-none hover:text-gray-900 mr-1" to="/">主页
                    </RouterLink>
                    <RouterLink class="text-base font-normal text-gray-500 list-none hover:text-gray-900 ml-1"
                        to="/resume">
                        简历
                    </RouterLink>
                </nav>
            </div>
        </header>
        <RouterView />
    </main>
</template>

<style lang="css">
header {
    display: flex;
    flex-direction: column;
}

nav {
    text-align: center;
}
</style>