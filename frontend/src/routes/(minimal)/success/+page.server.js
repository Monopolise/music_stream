export function load({ url }) {
    const message = url.searchParams.get('message');
    const qrCode = url.searchParams.get('qrCode');
    
    return { message, qrCode };
}