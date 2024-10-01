import { json } from '@sveltejs/kit';
import { handleLogin } from '$lib/server/auth';

export async function POST(event) {
    const result = await handleLogin(event);

    if (!result.success) {
        return json({success: false});
    }

    return json({success: true});
}