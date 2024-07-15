<script setup lang="ts">
import { getAdminProfile, patchAUserProfile } from "@/apis";
import type { UserProfile } from "@/typings";
import { onMounted, ref, type Ref } from "vue";
import { loginStatus } from "@/store";

const currentUserProfile: Ref<UserProfile> = ref({ id: 0, profile: "", registerAt: "", username: "" });
const profileStatus: Ref<"normal" | "edit"> = ref("normal");
const currentProfile = ref("")

onMounted(() => {
  getAdminProfile().then((up) => {
    currentUserProfile.value = up;
    currentProfile.value = up.profile;
  })
})

function updateProfile(): void {
  patchAUserProfile(currentUserProfile.value?.username, currentProfile.value).then((up) => {
    profileStatus.value = "normal";
  })
}

</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ currentUserProfile?.username }}</h1>
    <div>
      <h3 v-if="profileStatus == 'normal'">
        {{ currentProfile }}
      </h3>
      <textarea v-if="profileStatus == 'edit'" rows="10" v-model="currentProfile"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"></textarea>

      <button @click="() => profileStatus = 'edit'"
        class="focus:outline-black text-white text-sm py-2.5 px-4 border-b-4 border-blue-600 bg-blue-500 hover:bg-blue-400">编辑</button>
    </div>
    <div v-if="profileStatus == 'edit' && loginStatus" class="flex justify-between w-full px-3">
      <div class="md:flex md:items-center">
      </div>
      <button @click="updateProfile"
        class="focus:outline-black text-white text-sm py-2.5 px-4 border-b-4 border-yellow-600 bg-yellow-500 hover:bg-yellow-400"
        type="button">
        提交
      </button>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {

  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
