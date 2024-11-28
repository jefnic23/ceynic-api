import type { Handle } from '@sveltejs/kit';
import { handleRefresh } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
	if (event.url.pathname.startsWith('/admin')) {
		const accessToken = event.cookies.get("access");
		const refreshToken = event.cookies.get("refresh");

		if (!accessToken && !refreshToken) {
			return await resolve(event);
		}

		// If access token is missing, attempt a refresh if refresh token is available
		if (!accessToken && refreshToken) {
			const attemptRefresh = await handleRefresh(event.cookies);
			if (attemptRefresh) {
				event.locals.user = "me";
			} else {
				return await resolve(event);
			}
		}

		// Either access token exists or refresh was successful
		// return await resolve(event);
	}

	// todo: get user
	// const user = await db.user.findUnique({
	// 	where: { userAuthToken: session },
	// 	select: { username: true, role: true },
	// })

	event.locals.user = "me";

	// if (user) {
	// 	event.locals.user = {
	// 		name: user.username,
	// 		role: user.role.name,
	// 	}
	// }

	return await resolve(event);
};