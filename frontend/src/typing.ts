export type MyProfile = {
    id: number;
    username: string;
    authorName: string;
    profile: string;
    registerAt: string;
    blogTitle: string;
    blogSubTitle: string;
    resume: string;
}

export type TweetProfile = {
    id: number;
    text: string;
    createdAt: string;
    meId: number;
}

export type PhotoProfile = {
    id: number;
    url: string;
    tweetId: number;
    meId: number;
}

export type MyDetail = {
    id: number;
    username: string;
    authorName: string;
    profile: string;
    registerAt: string;
    blogTitle: string;
    blogSubTitle: string;
    resume: string;
    tweetProfiles: TweetProfile[];
    photoProfiles: PhotoProfile[];
}

export type TweetDetail = {
    id: number;
    text: string;
    createdAt: string;
    myProfile: MyProfile;
    photoProfiles: PhotoProfile[];
}

export type PhotoDetail = {
    id: number;
    url: string;
    myProfile: MyProfile;
    tweetProfile: TweetProfile;
}

export type TokenData = {
    accessToken: string;
    tokenType: string;
}

export interface FilePreview {
    file: File;
    previewUrl: string;
}