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
    addArtist: async ({ request, cookies }) => {
        const formData = await request.formData();

        const name = formData.get('name');
        const debutDate = formData.get('debutDate');
        const bio = formData.get('bio');
        const csrfToken = formData.get('csrfmiddlewaretoken');

        // Retrieve the sessionid cookie
        const sessionCookieValue = cookies.get('csrfSessionid');
        const authSessionCookieValue = cookies.get('authSessionid');

        // Create JSON payload to send
        const jsonData = {
            name: name,
            debutDate: debutDate,
            bio: bio
        };

        try {
            // Send the request with JSON payload
            const res = await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/api/add_artist/`,
                JSON.stringify(jsonData), // Convert the data to JSON string
                {
                    headers: {
                        'cookie': `sessionid=${sessionCookieValue}; authSessionid=${authSessionCookieValue}`, // Send the session cookie
                        'X-CSRFToken': csrfToken,  // Include CSRF token
                        'Content-Type': 'application/json',  // Set the content type to JSON
                    },
                    withCredentials: true
                }
            );

            // Handle successful response here (optional)

        } catch (error) {
            console.log(error);
            
            // Fetch a new CSRF token if an error occurs
            const newCsrfRes = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/api/get_csrf_token/`, {
                withCredentials: true
            });

            setCookie(newCsrfRes, cookies);

            // Return the new CSRF token and the error response
            return fail(500, {
                csrfToken: newCsrfRes.data.csrf_token, // Return new CSRF token
                error: error.response?.data?.error || 'Unknown error occurred'
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