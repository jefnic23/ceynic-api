import { handleLogout } from '$lib/server/auth'
import { redirect } from '@sveltejs/kit'
import type { Actions } from './$types'

export const load = async () => {
    // we only use this endpoint for the api
    // and don't need to see the page
    redirect(302, '/admin')
}

export const actions: Actions = {
    default({ cookies }) {
        handleLogout(cookies);

        // redirect the user
        redirect(302, '/admin')
    },
}
