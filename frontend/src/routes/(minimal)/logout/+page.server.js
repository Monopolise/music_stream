import { redirect } from '@sveltejs/kit';
import axios from 'axios';

export async function load({ cookies }) {
    try {
        // Fetch CSRF token and session cookie from Django backend using Axios
        await axios.get(`${import.meta.env.VITE_BACKEND_URL}/api/logout/`, {
            withCredentials: true
        });
        
        // Delete session-related cookies
        cookies.delete('authSessionid', { path: '/' });
        cookies.delete('csrfSessionid', { path: '/' });

        // Redirect to the login page after successful logout
        throw redirect(302, '/login');
    } catch (error) {
        // Handle errors and return a failure if something goes wrong
        return {
            status: 500,
            error: new Error('Failed to log out')
        };
    }
}
