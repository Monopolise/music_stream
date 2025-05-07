import { redirect } from '@sveltejs/kit';
import axios from 'axios';

export async function handle({ event, resolve }) {
    // Get the session ID from cookies
    const sessionId = event.cookies.get('authSessionid');
    console.log('Session ID:', sessionId);
    
    const csrfToken = event.cookies.get('csrfSessionid');  // If needed

    try {
        // Make the request to Django backend with the forwarded sessionid cookie
        const response = await axios.get(
            `${import.meta.env.VITE_BACKEND_URL}/api/session/`,
            {
                headers: {
                    // Forward the sessionid and csrftoken cookies (if CSRF is needed)
                    'cookie': `authSessionid=${sessionId}; csrftoken=${csrfToken}`,
                    'Content-Type': 'application/json',
                },
                withCredentials: true,  // To include cookies from SvelteKit server-side requests
            }
        );

        if (response.data.user) {
            // Set the user in locals to use later in the request
            event.locals.user = response.data.user;
            event.locals.role = response.data.role;

        } else {
            event.locals.user = null;
        }

    } catch (error) {
        console.error("Error checking session status:", error.response?.data || error.message);
        event.locals.user = null;
    }
    
    const publicRoutes = ['/login', '/register', '/success'];

    const adminOnlyRoutes = ['/admin']

    // If the user is logged in and tries to access /login or /register, redirect to /
    if (event.locals.user && publicRoutes.includes(event.url.pathname)) {
        throw redirect(303, '/');
    }

    console.log(event.locals.role)
    if (event.locals.role !== 0 && adminOnlyRoutes.includes(event.url.pathname)) {
        throw redirect(303, '/');
    }

    // If the user is not logged in and is trying to access a protected route, redirect to /login
    if (!event.locals.user && !publicRoutes.includes(event.url.pathname)) {
        throw redirect(303, '/login');
    }

    // Continue with the request if the conditions are met
    const response = await resolve(event);
    return response;
}
