<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue';
import type { TweetDetail } from '@/typings';
import { getPageTweets, getLatestTweet, verifyUser } from "@/apis";
import TweetCard from '@/components/TweetCard.vue';
import CreateTweetEditor from '@/components/CreateTweetEditor.vue';
import { homePageTweets, currentUser } from "@/store";

const mainContainer = ref<HTMLElement | null>(null);

function handleScroll() {
  if (mainContainer.value) {
    const bottomOfWindow = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 1;
    if (bottomOfWindow) {
      homePageTweets.loadTweets();
    }
  }
};

function insertLatestTweet(): void {
  setTimeout(() => {
    getLatestTweet().then((tweetDetail) => {
      homePageTweets.addNewTweet(tweetDetail)
    })
  }, 2000)
}

onMounted(() => {
  homePageTweets.loadTweets();
  window.addEventListener('scroll', handleScroll);
});

function remoteDeletedTweet(tweet: TweetDetail): void {
  homePageTweets.removeDeleteTweet(tweet)
}
console.log(currentUser)
</script>
<template>
  <main ref="mainContainer">
    <CreateTweetEditor v-if="currentUser.loginStatus" @submit-form="insertLatestTweet" />
    <TweetCard v-for="t in homePageTweets.tweets" :tweet="t" :key="t.id" @delete="remoteDeletedTweet"></TweetCard>
  </main>
</template>
<style scoped>
main {
  padding: 16px;
}
</style>
