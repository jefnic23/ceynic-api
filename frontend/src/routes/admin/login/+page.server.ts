import { redirect} from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { handleLogin } from '$lib/server/auth';

export const load: PageServerLoad = async () => {}

export const actions: Actions = {
    login: async (event) => {
        const result = await handleLogin(event);

        if (result.success) {
            redirect(302, "/admin");
        } else {
            return { credentials: true }
        }
    }
} 