<script setup lang="ts">
import { ref, type Ref } from 'vue';
import { updateResume } from "@/apis";

const resumeFile: Ref<File | null> = ref(null);
const pdfUrl = ref("")

function submitForm(): void {
    if (resumeFile.value) {
        updateResume(resumeFile.value).then((responseData) => {

        })
    }
}

function handleFile(e: Event): void {
    const inputFiles = (e.target as HTMLInputElement).files;
    if (inputFiles) {
        const pdf = inputFiles[0];
        resumeFile.value = pdf;
    }
}

</script>
<template>
    <div class="iframe-container">
        <form @submit.prevent="submitForm">
            <input type="file" @change="handleFile" accept="application/pdf" id="pdfInput">
            <button @click=""
                class="focus:outline-black text-white text-sm py-2.5 px-4 border-b-4 border-blue-600 bg-blue-500 hover:bg-blue-400">更新</button>
            <iframe src="http://127.0.0.1:5000/user-resume#view=FitH,top" frameborder="0"></iframe>
        </form>
    </div>
</template>
<style lang="css">
.iframe-container {
    min-height: 100vh;
}

iframe {
    width: 100%;
    height: 100%;
    min-height: 800px;
}
</style>