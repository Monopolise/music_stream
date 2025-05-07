import { redirect, fail } from '@sveltejs/kit'
import axios from 'axios'

export async function load({ cookies }) {
    try {
        // Fetch CSRF token and session cookie from Django backend using Axios
        const csrfRes = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/api/get_csrf_token/`, {
            withCredentials: true
        });

        setCookie(csrfRes, cookies)

        // Return the CSRF token to be used in the client-side form
        return {
            csrfToken: csrfRes.data.csrf_token,
        };
    } catch (error) {
        console.error('Error fetching CSRF token:', error)
        return {
            csrfToken: null
        };
    }
}

export const actions = {
    addAlbum: async ({ request, cookies }) => {
        const formData = await request.formData()

        const title = formData.get('title');
        const totalTracks = formData.get('totalTracks');
        const file = formData.get('file'); // Get the file (image) from the form data
        const releaseDate = formData.get('releaseDate');
        const description = formData.get('description');
        const label = formData.get('label');
        const csrfToken = formData.get('csrfmiddlewaretoken');

        // Retrieve the sessionid cookie
        const sessionCookieValue = cookies.get('csrfSessionid')
        const authSessionCookieValue = cookies.get('authSessionid');

        // Create FormData object to send metadata and the image file
        const formDataToSend = new FormData();
        formDataToSend.append('title', title);
        formDataToSend.append('totalTracks', totalTracks);
        formDataToSend.append('file', file); // Send the image file
        formDataToSend.append('releaseDate', releaseDate);
        formDataToSend.append('label', label);
        formDataToSend.append('description', description);

        try {
            // Attempt login
            const res = await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/api/add_album/`,
                formDataToSend,
                {
                    headers: {
                        'cookie': `sessionid=${sessionCookieValue}; authSessionid=${authSessionCookieValue}`, // Send the session cookie
                        'X-CSRFToken': csrfToken,  // Include CSRF token
                    },
                    withCredentials: true
                }
            );

        } catch (error) {
            console.log(error)
            // handle all errors
            const newCsrfRes = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/api/get_csrf_token/`, {
                withCredentials: true
            });

            setCookie(newCsrfRes, cookies)

            return fail(500, {
                csrfToken: newCsrfRes.data.csrf_token, // Return new CSRF token
                error: error.response.data.error
            });
        }
    }
};


function setCookie(csrfRes, cookies) {
    // Extract the sessionid cookie from the 'set-cookie' header
    const setCookieHeader = csrfRes.headers['set-cookie']
    const sessionCookie = setCookieHeader?.find(cookie => cookie.startsWith('sessionid='))

    if (sessionCookie) {
        // Parse the Set-Cookie header to extract all attributes
        const cookieParts = sessionCookie.split(';').map(part => part.trim())

        // Extract the session ID value
        const sessionId = cookieParts[0].split('=')[1]

        // Prepare options object for the SvelteKit cookies API
        const cookieOptions = {}
        cookieParts.slice(1).forEach(part => {
            const [key, value] = part.split('=')

            switch (key.toLowerCase()) {
                case 'path':
                    cookieOptions.path = value || '/'
                    break
                case 'max-age':
                    cookieOptions.maxAge = parseInt(value, 10)
                    break
                case 'httponly':
                    cookieOptions.httpOnly = true
                    break
                case 'samesite':
                    cookieOptions.sameSite = value || 'lax'
                    break
                case 'secure':
                    cookieOptions.secure = true
                    break
            }
        })

        // Set the session cookie using the options provided by the server
        cookies.set('csrfSessionid', sessionId, cookieOptions)
    }
}