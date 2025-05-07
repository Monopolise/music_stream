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
    register: async ({ request, cookies }) => {
        const formData = await request.formData()
        const username = formData.get('username')
        const password = formData.get('password')
        const name = formData.get('name')
        const displayName = formData.get('displayName')
        const csrfToken = formData.get('csrfmiddlewaretoken')

        // Retrieve the sessionid cookie
        const sessionCookieValue = cookies.get('csrfSessionid')

        let res = ""
        try {
            // Attempt login
            res = await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/api/register/`,
                { username, password, name, displayName },
                {
                    headers: {
                        'cookie': `sessionid=${sessionCookieValue}`, // Send the session cookie
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,  // Include CSRF token
                    },
                    withCredentials: true
                }
            );

        } catch (error) {
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

        throw redirect(303, `/success?message=${encodeURIComponent(res.data.message)}&qrCode=${encodeURIComponent(res.data.qr_code)}`);

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

        console.log(sessionId)

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