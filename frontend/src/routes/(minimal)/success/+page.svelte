<script>
    export let data
</script>

<div>

    <h1>Registration Success</h1>
    <p>Please add the MFA code to your Authenticator app.</p>
    <p>You will not be able to view this QR code after you exit this page.</p>
    <!-- Display the QR code -->
    <img src={data.qrCode} alt="Your QR code" />
    <a href="/login">Login</a>
</div>
