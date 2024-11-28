import type { Writable } from "svelte/store";
import { writable } from "svelte/store";
import { browser } from "$app/environment";

function getToken(tokenType: string): string | null {
    const token = browser && localStorage.getItem(tokenType);
    if (token) {
        console.log(`${tokenType} retrieved from storage.`);
        return token;
    } else {
        console.log(`${tokenType} not found.`);
        return null;
    }
}

function saveToken(token: Record<string, string>): void {
    try {
        browser && localStorage.setItem(token[0], token[1]);
    } catch {
        console.log(`Error saving token.`);
    } finally {
        console.log(`token saved.`);
    }
}

const savedAccessToken: string | null = getToken("accessToken");
export const accessToken: Writable<string> = writable(savedAccessToken || "");
accessToken.subscribe(token => saveToken({ accessToken: token }));

const savedRefreshToken: string | null = getToken("refreshToken");
export const refreshToken: Writable<string> = writable(savedRefreshToken || "");
refreshToken.subscribe(token => saveToken({ refreshToken: token }));
