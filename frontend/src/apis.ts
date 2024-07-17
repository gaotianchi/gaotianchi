import type { MyDetail, MyProfile, PhotoDetail, TokenData, TweetDetail, TweetProfile } from "./typing";
import { getAuthorization } from "./utlis";

const rootUrl = "http://127.0.0.1:5000"

export async function postMe(username: string, password: string): Promise<MyProfile> {
    const response = await fetch(rootUrl + "/me", {
        method: "POST",
        headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
        body: JSON.stringify({username: username, password: password})
    });
    const respData = await response.json();
    if (response.status == 201) {
        return respData;
    } else {
        throw respData.error;
    }
}

export async function patchMe(authorName: string, blogTitle: string, blogSubTitle: string, profile: string, resume: string): Promise<MyDetail> {
	const resp = await fetch(rootUrl + "/me", {
		method: "PATCH",
		headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
		body: JSON.stringify({
			authorName: authorName,
			blogTitle: blogTitle,
			blogSubTitle: blogSubTitle,
			profile: profile,
			resume: resume
		})
	})
	const respData = await resp.json();
    if (resp.status == 200) {
        return respData;
    } else {
        throw respData.error;
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

export async function getMyProfile(): Promise<MyProfile> {
    const response = await fetch(rootUrl + "/my-profile")
    const respData = await response.json()
    if (response.status == 200) {
        return respData;
    } else {
        throw respData.error;
    }
}

export async function patchATweet(text: string, id: number): Promise<TweetDetail> {
	const resp = await fetch(rootUrl + "/tweets/" + id, {
		method: "PATCH",
		headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
		body: JSON.stringify({text: text})
	});
	const data = await resp.json();
	if (resp.status == 200) {
		return data;
	} else {
		throw data.error;
	}
}


export async function deleteATweet(id: number): Promise<void> {
	const resp = await fetch(rootUrl + "/tweets/" + id, {
		method: "DELETE",
		headers: { Authorization: getAuthorization() },
	});
	if (resp.status == 200) {
		return;
	} else {
		throw Error("删除失败！");
	}
}

export async function postATweet(text: string): Promise<TweetProfile> {
	const resp = await fetch(rootUrl+ "/tweets", {
		method: "POST",
		headers: { Authorization: getAuthorization(), "Content-Type": "application/json" },
		body: JSON.stringify({text: text})
	});
	const data = await resp.json();
	if (resp.status == 201) {
		return data;
	} else {
		throw data.error;
	}
}


export async function postAPhoto(f: File, id: number): Promise<PhotoDetail> {
	const formData = new FormData()
	formData.append("photo", f)
	formData.append("tweetId", id.toString())
	const resp = await fetch(rootUrl + "/photos", {
		method: "POST",
		headers: { Authorization: getAuthorization()},
		body: formData
	});
	const data = await resp.json();
	if (resp.status == 201) {
		return data;
	} else {
		throw data.error;
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

export async function putAResume(r: File): Promise<{resumeUrl: string}> {
	const formData = new FormData()
	formData.append("resume", r)
	const resp = await fetch(rootUrl + "/resume", {
		method: "PUT",
		headers: { Authorization: getAuthorization() },
		body: formData
	})
	const data = await resp.json();
	if (resp.status == 201) {
		return data;
	} else {
		throw data.error;
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