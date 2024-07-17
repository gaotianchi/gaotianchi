<script setup lang="ts">
import { patchMe, putAResume, getMyProfile } from '@/apis';
import { onMounted, reactive, ref, type Ref } from 'vue';
import { useRouter } from "vue-router";
document.title = "配置用户基本信息"
const mySettings = reactive({
    authorName: "",
    blogTitle: "",
    blogSubTitle: "",
    profile: "",
    resume: "",
})
const router = useRouter();
onMounted(() => {
    getMyProfile().then(mp => {
        mySettings.authorName = mp.authorName;
        mySettings.blogTitle = mp.blogTitle;
        mySettings.blogSubTitle = mp.blogSubTitle;
        mySettings.profile = mp.profile;
        mySettings.resume = mp.resume;
    })
})
function handleFile(e: Event): void {
    const inputFiles = (e.target as HTMLInputElement).files;
    if (inputFiles) {
        const pdf = inputFiles[0];
        putAResume(pdf).then(resp => {
            mySettings.resume = resp.resumeUrl;
        })
    }
}
function submitForm(): void {
    if (mySettings.authorName && mySettings.blogTitle && mySettings.profile && mySettings.resume) {
        patchMe(mySettings.authorName, mySettings.blogTitle, mySettings.blogSubTitle, mySettings.profile, mySettings.resume).then(resp => {
            router.push("/")
        })
    }
}

</script>
<template>
    <div class="flex justify-center mt-20 px-8">
        <form class="max-w-2xl" @submit.prevent="submitForm">
            <div class="flex flex-wrap border shadow rounded-lg p-3 dark:bg-gray-600">
                <h2 class="text-xl text-gray-600 dark:text-gray-300 pb-2">Account settings:</h2>

                <div class="flex flex-col gap-2 w-full border-gray-400">

                    <div>
                        <label class="text-gray-600 dark:text-gray-400">Author
                            name
                        </label>
                        <input v-model="mySettings.authorName"
                            class="w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
                            type="text">
                    </div>

                    <div>
                        <label class="text-gray-600 dark:text-gray-400">Blog title</label>
                        <input v-model="mySettings.blogTitle"
                            class="w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
                            type="text">
                    </div>
                    <div>
                        <label class="text-gray-600 dark:text-gray-400">Blog sub title</label>
                        <input v-model="mySettings.blogSubTitle"
                            class="w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
                            type="text">
                    </div>
                    <div>
                        <label class="text-gray-600 dark:text-gray-400">profile</label>
                        <textarea v-model="mySettings.profile"
                            class="w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
                            name="bio"></textarea>
                    </div>

                    <div>
                        <label class="text-gray-600 dark:text-gray-400">resume</label>
                        <input type="file" name="file" id="file" class="sr-only" accept="application/pdf"
                            @change="handleFile" />
                        <label for="file"
                            class="relative flex min-h-[100px] items-center justify-center rounded-md border border-dashed border-[#e0e0e0] p-12 text-center">
                            <div>
                                <span class="mb-2 text-xl font-semibold text-[#07074D]">
                                    Drop files here
                                </span>
                                <span class="mb-2 text-base font-medium text-[#6B7280]">
                                    Or
                                </span>
                                <span
                                    class="inline-flex rounded border border-[#e0e0e0] py-2 px-7 text-base font-medium text-[#07074D]">
                                    Browse
                                </span>
                            </div>
                        </label>
                        <div
                            class="relative flex  items-center justify-center rounded-md border border-dashed border-[#e0e0e0] ">
                            <iframe class="min-h-[400px]" v-if="mySettings.resume"
                                :src="mySettings.resume + '#view=FitH,top'" frameborder="0"></iframe>
                        </div>
                    </div>
                    <div class="flex justify-end">
                        <button @click="() => router.push('/')"
                            class="py-1.5 px-3 m-1 text-center border rounded-md text-black  hover:bg-violet-500 hover:text-gray-100 dark:text-gray-200 dark:bg-violet-700"
                            type="submit">Skip</button>
                        <button
                            class="py-1.5 px-3 m-1 text-center bg-violet-700 border rounded-md text-white  hover:bg-violet-500 hover:text-gray-100 dark:text-gray-200 dark:bg-violet-700"
                            type="submit">Save changes</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>