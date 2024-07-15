export type PhotoProfile = {
    id: number;
    url: string;
    tweetId: number;
    userId: number;
}

export type PhotoDetail = {
    id: number;
    url: string;
    tweetProfile: TweetProfile;
    userProfile: UserProfile;
    filename: string;
}

export type TweetProfile = {
    id: number;
    text: string;
    createdAt: string;
    userId: number;
}

export type TweetDetail = {
    id: number;
    text: string;
    createdAt: string;
    userProfile: UserProfile;
    photoProfiles: PhotoProfile[];
}

export type UserProfile = {
    id: number;
    username: string;
    profile: string;
    registerAt: string;
}

export type UserDetail = {
    id: number;
    username: string;
    profile: string;
    registerAt: string;
    tweetProfiles: TweetProfile[];
    photoProfiles: PhotoProfile[];
}

export type TokenData = {
    accessToken: string;
    tokenType: string;
}

export interface FilePreview {
    file: File;
    previewUrl: string;
}