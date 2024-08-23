import React from "react";
import { GoogleLogin, GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';

const googleClientId = '137347691807-2ehifvqvrlfqvqagvargud88sg13uuvm.apps.googleusercontent.com';
const baseURL = "http://localhost:8000";

const handleGoogleLoginSuccess = async (response) => {
    console.log("res", response);
    try {
        const { data } = await axios.post(`${baseURL}/api/auth/google/`, {
            access_token: response.credential,
        });

        console.log('Login Success:', data);
        localStorage.setItem('access_token', data.access_token);

        window.location.href = '/';
    } catch (error) {
        console.error('Login failed:', error.response?.data || error.message);
    }
};


const handleGoogleLoginFailure = (error) => {
    console.error('Google Login Failed:', error);
};

const GoogleLoginComponent = () => (
    <GoogleOAuthProvider clientId={googleClientId}>
        <GoogleLogin
            onSuccess={handleGoogleLoginSuccess}
            onError={handleGoogleLoginFailure}
        />
    </GoogleOAuthProvider>
);

export default GoogleLoginComponent;
