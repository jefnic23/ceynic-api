import type { Token } from '$lib/interfaces/token';
import { type Cookies } from '@sveltejs/kit';

export function setCookie(name: string, token: string, maxAge: number, cookies: Cookies) {
    cookies.set(name, token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        path: '/admin',
        maxAge: maxAge,
        sameSite: 'strict',
    });
}

export async function handleLogin({ request, cookies }: { request: Request, cookies: Cookies }) {
    const formData = await request.formData();

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: request.method,
        body: formData
    });

    if (response.status != 200) {
        return { success: false };
    }

    const responseData: Token = await response.json();

    setCookie('access', responseData.accessToken, 60 * 5, cookies);
    setCookie('refresh', responseData.refreshToken, 60 * 60 * 24 * 30, cookies);

    return { success: true };
}
