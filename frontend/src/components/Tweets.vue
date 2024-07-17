<script setup lang="ts">
import { homePageTweets, currentUser } from '@/store';
import { onMounted, onUnmounted, ref } from 'vue';
import { getLatestTweet } from "@/apis";
import Editor from './Editor.vue';
import TweetCard from './TweetCard.vue';
import type { TweetDetail } from '@/typing';


function handleScroll() {
    const bottomOfWindow = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 1;
    if (bottomOfWindow) {
        homePageTweets.loadTweets();
    }
}

function insertLatestTweet(): void {
    setTimeout(() => {
        getLatestTweet().then((tweetDetail) => {
            homePageTweets.addNewTweet(tweetDetail);
        });
    }, 2000);
}

onMounted(() => {
    homePageTweets.loadTweets();
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});

function remoteDeletedTweet(tweet: TweetDetail): void {
    homePageTweets.removeDeleteTweet(tweet);
}

</script>

<template>
    <Editor v-if="currentUser.loginStatus" @submit-form="insertLatestTweet" />
    <TweetCard v-for="t in homePageTweets.tweets" :tweet="t" :key="t.id" @delete="remoteDeletedTweet"></TweetCard>
</template>
