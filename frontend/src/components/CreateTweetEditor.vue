<script setup lang="ts">
import IconClear from "./icons/IconClear.vue";
import { type Ref, ref } from "vue";
import type { FilePreview } from "@/typings";
import { postATweet, postAPhoto, getLatestTweet } from "@/apis"

const emits = defineEmits(["submitForm"]);

const tweetText: Ref<string> = ref("");
const filePreviews: Ref<FilePreview[]> = ref([]);
const fileInput = ref<HTMLInputElement | null>(null);

function resetFormValue(): void {
    tweetText.value = "";
    filePreviews.value = [];
    fileInput.value = null;
}

function handleFiles(event: Event) {
    const inputFiles = (event.target as HTMLInputElement).files;
    if (inputFiles) {
        Array.from(inputFiles).forEach(file => {
            const reader = new FileReader();
            reader.onload = e => {
                if (e.target?.result) {
                    filePreviews.value.push({ file, previewUrl: e.target.result as string });
                }
            };
            reader.readAsDataURL(file);
        });
    }
};
function removeImage(index: number) {
    filePreviews.value.splice(index, 1);
    const dataTransfer = new DataTransfer();
    filePreviews.value.forEach(fp => {
        dataTransfer.items.add(fp.file);
    });
    if (fileInput.value) {
        fileInput.value.files = dataTransfer.files;
    }
};

function submitForm(): void {
    postATweet(tweetText.value).then((tweetProfile) => {
        if (filePreviews.value.length > 0) {
            filePreviews.value.forEach(fp => {
                postAPhoto(fp.file, tweetProfile.id).then((photoDetail) => {
                })
            })
        }
        resetFormValue()
        emits("submitForm")
    })
}

</script>
<template>
    <form @submit.prevent="submitForm()">
        <div class="parent-EyNP7gqLgx">
            <!-- 文本输入框以及提交按钮 -->
            <div class="parent-EkxKrx9Uel max-w-xlmx-auto">
                <div class="w-full px-3">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                        for="grid-password">
                        Your Message
                    </label>
                    <textarea rows="10" v-model="tweetText"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"></textarea>
                </div>

                <div class="flex justify-between w-full px-3">
                    <!-- 图片拖拽输入框 -->
                    <div class="grow relative  border-2 border-gray-300 border-dashed rounded-lg p-6 mr-1"
                        id="dropzone">
                        <input type="file" accept="image/*" multiple
                            class="absolute inset-0 w-full h-full opacity-0 z-50" @change="handleFiles"
                            ref="fileInput" />
                        <div class="text-center">
                            <img class="mx-auto h-12 w-12" src="https://www.svgrepo.com/show/357902/image-upload.svg"
                                alt="">
                            <h3 class="mt-2 text-sm font-medium text-gray-900">
                                <label for="file-upload" class="relative cursor-pointer">
                                    <span>Drag and drop</span>
                                    <span class="text-indigo-600"> or browse </span>
                                    <span>to upload</span>
                                    <input id="file-upload" name="file-upload" type="file" class="sr-only"
                                        @change="handleFiles">
                                </label>
                            </h3>
                            <p class="mt-1 text-xs text-gray-500">
                                PNG, JPG, GIF up to 10MB
                            </p>
                        </div>
                    </div>
                    <button
                        class="shadow bg-indigo-600 hover:bg-indigo-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-6 rounded"
                        type="submit">
                        Send Message
                    </button>
                </div>
            </div>

            <!-- 图片预览窗格 -->
            <div id="image-preview">
                <div
                    class="grid grid-cols-2 md:grid-cols-3 gap-3 p-4 max-w-[400px] md:max-w-[600px] place-items-center">
                    <div class="child-41UxdJcIgx relative" v-for="(filePreview, index) in filePreviews" :key="index">
                        <IconClear class="absolute right-0 top-2" @click="removeImage(index)" />
                        <img class="preview mt-2 mx-auto max-h-25" :src="filePreview.previewUrl" alt="preview">
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>
