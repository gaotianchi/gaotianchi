import type { UserProfile, TokenData, TweetProfile, PhotoDetail, TweetDetail } from "./typings"
import { getAuthorization } from "./utlis";

const rootUrl = "http://127.0.0.1:5000"

export async function postAuser(
    username: string,
    password: string
): Promise<UserProfile> {
    const response = await fetch(rootUrl + "/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({username: username, password: password})
    })

    const responseData = await response.json()
    if (response.status == 201) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function postToken(
	username: string,
	password: string
): Promise<TokenData> {
	const response = await fetch(rootUrl + "/token", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			username: username,
			password: password,
			grantType: "password",
		}),
	});
	const responseData = await response.json();
	if (response.status === 200) {
		return responseData;
	} else {
		throw responseData.error;
	}
}
export async function verifyUser(): Promise<boolean> {
	const response = await fetch(rootUrl + "/verify", {
		headers: { Authorization: getAuthorization() },
	});
	if (response.status === 200) {
		return true;
	} else {
		return false;
	}
}

export async function postATweet(text: string): Promise<TweetProfile> {
    const response = await fetch(rootUrl + "/tweets", {
        headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({text: text})
    });
    const responseData = await response.json();
    if (response.status == 201) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function postAPhoto(file: File, tweetId: number): Promise<PhotoDetail> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append("tweetId", tweetId.toString())
    const response = await fetch(rootUrl +'/photos', {
        method: 'POST',
        body: formData,
        headers:  { Authorization: getAuthorization() }
    });
    const responseData = await response.json();
    if (response.status == 201) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function getPageTweets(page: number): Promise<TweetDetail[]> {
    const response = await fetch(rootUrl + "/page-tweets/" + page);
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function getLatestTweet(): Promise<TweetDetail> {
    const response = await fetch(rootUrl + "/tweets");
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function patchATweet(text: string, tweetId: number): Promise<TweetDetail> {
    const response = await fetch(rootUrl + "/tweets/" + tweetId, {
        method: "PATCH",
        headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
        body: JSON.stringify({text: text})
    });
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function deleteATweet(tweetId: number): Promise<void> {
    const response = await fetch(rootUrl + "/tweets/" + tweetId, {
        method: "DELETE",
        headers: { Authorization: getAuthorization()},
    });
    if (response.status == 204) {
        return
    } else {
        throw Error("删除失败");
    }
}

export async function getUserProfile(username: string): Promise<UserProfile> {
    const response = await fetch(rootUrl + "/users/" + username);
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function getAdminProfile(): Promise<UserProfile> {
    const response = await fetch(rootUrl + "/users");
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}

export async function patchAUserProfile(username: string, profile: string): Promise<UserProfile> {
    const response = await fetch(rootUrl + "/user-profile/" + username, {
        method: "PATCH",
        headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
        body: JSON.stringify({"profile": profile})
    });
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}


export async function updateResume(pdfFile: File): Promise<{url: string}>{
    const formData = new FormData()
    formData.append("file", pdfFile)
    const response = await fetch(rootUrl + "/resume", {
        method: "POST",
        headers: { Authorization: getAuthorization()},
        body: formData
    });
    const responseData = await response.json();
    if (response.status == 200) {
        return responseData;
    } else {
        throw responseData.error;
    }
}