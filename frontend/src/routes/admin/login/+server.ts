import { json } from '@sveltejs/kit';
import { handleLogin } from '$lib/server/auth';

export async function POST(event) {
    const result = await handleLogin(event);

    return json({success: result.success});
}