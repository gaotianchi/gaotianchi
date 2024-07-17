<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { getMyProfile } from '@/apis';
const resumeUrl = ref("")
onMounted(() => {
    getMyProfile().then(mp => {
        resumeUrl.value = mp.resume;
        document.title = mp.authorName + "的简历"
    })
})
</script>
<template>
    <div class="w-full">
        <iframe class="w-full min-h-lvh" :src="resumeUrl + '#view=FitH,top'" frameborder="0"></iframe>
    </div>
</template>