<script setup lang="ts">
import type { TweetDetail } from "@/typings";
import { ref, type Ref } from "vue";
import { patchATweet, deleteATweet } from "@/apis";
import { loginStatus } from "@/store";
const props = defineProps<{
    tweet: TweetDetail;
}>()
const emits = defineEmits(["delete"])
const isModalOpen = ref(false);
const currentIndex = ref(0);
const cardStatus: Ref<"normal" | "edit"> = ref("normal");
const currentText = ref(props.tweet.text);

function openModal(index: number) {
    currentIndex.value = index;
    isModalOpen.value = true;
};

function closeModal() {
    isModalOpen.value = false;
};

function prevImage() {
    if (currentIndex.value > 0) {
        currentIndex.value--;
    } else {
        currentIndex.value = props.tweet.photoProfiles.length - 1;
    }
};

function nextImage() {
    if (currentIndex.value < props.tweet.photoProfiles.length - 1) {
        currentIndex.value++;
    } else {
        currentIndex.value = 0;
    }
};

function updateTweet(): void {
    patchATweet(currentText.value, props.tweet.id).then((td) => {
        cardStatus.value = "normal";
    })
}

function deleteTweet(): void {
    deleteATweet(props.tweet.id).then(() => {
        emits("delete", props.tweet)
    })
}
</script>
<template>
    <div class="bg-white rounded-lg shadow-lg overflow-hidden max-w-lg w-full mx-auto mt-10">
        <img v-if="tweet.photoProfiles?.length > 0" :src="tweet.photoProfiles[0].url" alt="Mountain"
            class="w-full h-64 object-cover">
        <div ref="imageScroll" class="flex overflow-x-auto gap-2 p-2 image-scroll">
            <div v-for="(image, index) in tweet.photoProfiles" :key="index"
                class="flex-shrink-0 flex justify-center items-center border h-20 w-24 bg-blue-100">
                <img :src="image.url" @click="openModal(index)" class="cursor-pointer" />
            </div>
        </div>
        <div class="p-6">
            <p v-if="cardStatus == 'normal'" class="text-gray-700 leading-tight mb-4">
                {{ currentText }}
            </p>
            <div v-else class="max-w-xl mx-auto">
                <div class="w-full px-3">
                    <textarea rows="10" v-model="currentText"
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"></textarea>
                </div>
                <div class="flex justify-between w-full px-3">
                    <div class="md:flex md:items-center">
                    </div>
                    <button @click="updateTweet"
                        class="focus:outline-black text-white text-sm py-2.5 px-4 border-b-4 border-yellow-600 bg-yellow-500 hover:bg-yellow-400"
                        type="button">
                        提交
                    </button>
                </div>
            </div>
            <div class="flex justify-between items-center">
                <div class="flex items-center" v-if="loginStatus">
                    <!-- <span class="text-gray-800 font-semibold">{{ tweet.user.username }}</span> -->
                    <button @click="() => cardStatus = 'edit'"
                        class="focus:outline-black text-white text-sm py-2.5 px-4 border-b-4 border-blue-600 bg-blue-500 hover:bg-blue-400">编辑</button>
                    <button @click="deleteTweet"
                        class="focus:outline-black text-white text-sm py-2.5 px-4 border-b-4 border-red-600 bg-red-500 hover:bg-red-400">删除</button>
                </div>
                <span class="text-gray-600">{{ tweet.createdAt }}</span>
            </div>
        </div>

        <!-- Fullscreen Modal -->
        <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
            <div class="relative">
                <img :src="tweet.photoProfiles[currentIndex].url" class="max-h-screen max-w-full" />
                <button @click="closeModal" class="absolute top-2 right-2 text-white text-3xl">&times;</button>
                <button @click="prevImage"
                    class="absolute left-2 top-1/2 transform -translate-y-1/2 text-white text-3xl">&#8249;</button>
                <button @click="nextImage"
                    class="absolute right-2 top-1/2 transform -translate-y-1/2 text-white text-3xl">&#8250;</button>
            </div>
        </div>
    </div>
</template>
<style>
.image-scroll {
    scroll-behavior: smooth;
}
</style>