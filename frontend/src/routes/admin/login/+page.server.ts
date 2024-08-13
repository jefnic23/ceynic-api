import { redirect} from '@sveltejs/kit';
import type { Action, Actions, PageServerLoad } from './$types';
import { handleLogin } from '$lib/server/auth';

export const load: PageServerLoad = async () => {}

const login: Action = async (event) => {
    const result = await handleLogin(event);

    redirect(302, "/admin");
}

export const actions: Actions = { login }