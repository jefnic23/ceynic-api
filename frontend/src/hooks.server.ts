import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	if (event.url.pathname.startsWith('/admin')) {
		const accessToken = event.cookies.get("access");

		if (!accessToken) {
			return await resolve(event);
		}
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