import type { Writable } from "svelte/store";
import { writable } from "svelte/store";

export async function getUser(accessToken: string): Promise<string | null> {
    const response = await fetch(`http://127.0.0.1:8000/users`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (response.status == 200) {
        const user: string = await response.json();
        return user.split("@")[0];
    } else if (response.status == 401) {
        console.log("Username or password incorrect.");
    } else {
        console.log("Error logging in.");
    }

    return null;
}

export const user: Writable<string | null> = writable(null);
