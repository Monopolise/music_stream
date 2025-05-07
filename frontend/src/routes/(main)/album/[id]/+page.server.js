import axios from 'axios'

export async function load({ params }) {
    console.log(params.id)
    try {
        const response = await axios.post(
            `${import.meta.env.VITE_BACKEND_URL}/api/get_album/`,
            {
                album_name: params.id,
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )

        return response.data

    } catch (error) {
    }
}