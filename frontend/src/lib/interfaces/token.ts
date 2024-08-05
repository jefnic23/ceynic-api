import { jwtDecode } from "jwt-decode";

export interface Token {
    accessToken: string;
    tokenType: string;
    refreshToken: string;
}

export function isExpired(token: string): boolean {
    const decodedToken = jwtDecode(token);

    return (decodedToken.exp as number) >
        Math.floor(Date.now() / 1000)
}
