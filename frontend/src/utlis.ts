import type { TokenData } from "./typing";
export function setAccessToken(data: TokenData): void {
	localStorage.setItem("accessToken", JSON.stringify(data));
}
export function deleteAccessToken(): void {
	localStorage.setItem("accessToken", "")
}
export function getAccessToken(): TokenData | null {
	const data = localStorage.getItem("accessToken");
	if (data) {
		return JSON.parse(data);
	} else {
		return null;
	}
}
export function getAuthorization(): string {
	const tokenData = getAccessToken();
	return tokenData?.tokenType + " " + tokenData?.accessToken;
}