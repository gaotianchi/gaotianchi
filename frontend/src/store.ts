import { reactive, ref, type Ref } from "vue";
import type { TweetDetail, UserProfile  } from "./typings";
import { getPageTweets, getUserProfile, verifyUser } from "./apis";

export const loginStatus = ref(false);
export const currentUser = reactive({
    loginStatus: false,
    signIn(up: UserProfile) {
        this.loginStatus = true;
        localStorage.setItem("userProfile", JSON.stringify(up))
    },
    signOut() {
        localStorage.removeItem("userProfile")
    },
    loadUser() :UserProfile | null {
        const up = localStorage.getItem("userProfile")
        if (!up) return null;
        const userProfile = JSON.parse(up);
        return userProfile; 
    }
})
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

