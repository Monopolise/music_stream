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
    login: async ({ request, cookies }) => {
        const formData = await request.formData()
        const username = formData.get('username')
        const password = formData.get('password')
        const csrfToken = formData.get('csrfmiddlewaretoken')
        const mfa_code = formData.get('mfa_code')

        // Retrieve the sessionid cookie
        const sessionCookieValue = cookies.get('csrfSessionid')

        try {
            // Attempt login
            const res = await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/api/login/`,
                { username, password, mfa_code },
                {
                    headers: {
                        'cookie': `sessionid=${sessionCookieValue}`, // Send the session cookie
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,  // Include CSRF token
                    },
                    withCredentials: true
                }
            );

            console.log(res.data.session_token)
            cookies.set('authSessionid', res.data.session_token, {"path": "/", "httpOnly": true, "samesite": "lax"})

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

        // If login is successful
        // Redirect to the homepage or another page
        throw redirect(302, '/')

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