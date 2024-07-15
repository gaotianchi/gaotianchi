import { reactive, ref, type Ref } from "vue";
import type { TweetDetail  } from "./typings";
import { getPageTweets } from "./apis";

export const loginStatus = ref(false);
export const homePageTweets = reactive({
    page: 1,
    isFetching: false,
    tweets: [] as TweetDetail[],
    addNewTweet(newTweet: TweetDetail) {
        this.tweets.unshift(newTweet)
    },
    addHistoryTweets(historyTweets: TweetDetail[]) {
        this.tweets = [...this.tweets, ...historyTweets]
    },
    removeDeleteTweet(toRemove: TweetDetail) {
        this.tweets = this.tweets.filter(t => t.id !== toRemove.id)
    },
    async loadTweets() {
        if (this.isFetching) return;
        this.isFetching = true;
        const historyTweets = await getPageTweets(this.page);
        homePageTweets.addHistoryTweets(historyTweets);
        this.page++;
        this.isFetching = false;
    }
})