<script setup lang="ts">
import { postToken, getUserProfile } from "@/apis";
import { setAccessToken } from "@/utlis";
import { ref } from "vue";
import { useRouter } from 'vue-router';
import { currentUser } from "@/store";
const username = ref<string>("");
const password = ref<string>("");
const router = useRouter();

async function submit(): Promise<void> {
    if (username.value && password.value) {
        try {
            const responseData = await postToken(username.value, password.value);
            setAccessToken(responseData)
            console.log("登录成功！")
            getUserProfile(username.value).then((up) => {
                currentUser.signIn(up);
                console.log(currentUser);
                router.push("/")
            })
        } catch (error) {
            console.log(error);
            console.log("登录失败！")
        }
    } else {
        console.log("不能为空！")
    }
}

</script>
<template>
    <div class=" bg-white rounded-lg overflow-hidden shadow-lg mx-auto" style="min-width: 400px">
        <div class="p-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-2">Welcome Back!</h2>
            <p class="text-gray-700 mb-6">Please sign in to your account</p>
            <form @submit.prevent="submit()">
                <div class="mb-4">
                    <label class="block text-gray-700 font-bold mb-2" for="username">
                        Username
                    </label>
                    <input
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="username" type="text" placeholder="Username" v-model="username">
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 font-bold mb-2" for="password">
                        Password
                    </label>
                    <input
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="password" type="password" placeholder="Password" v-model="password">
                </div>
                <div class="flex items-center justify-between">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit">
                        Sign In
                    </button>
                    <RouterLink to="/signup"
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
                        Sign up
                    </RouterLink>
                </div>
            </form>
        </div>
    </div>
</template>
