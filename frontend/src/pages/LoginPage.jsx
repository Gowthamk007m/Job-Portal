import React from 'react';
import axios from 'axios';
import FacebookLogin from '@greatsumini/react-facebook-login';
import { GoogleLogin } from '@react-oauth/google';
import facebookLogin from './FaceAuth';
// import LinkedInLogin from "./LinkedinAuth";
// import { LinkedIn } from 'react-linkedin-login-oauth2';


const responseFacebook = (res) => {
    console.log(res);
    facebookLogin(res.accessToken);
};

const handleGoogleLoginSuccess = async (response) => {
    try {
        const { credential } = response;
        console.log('Google ID Token:', credential);

        // Send the ID token to your backend for verification
        const res = await axios.post('http://localhost:8000/accounts/api/login/google/', {
            token: credential,
        });

        console.log('Backend response:', res.data);
        localStorage.setItem('access_token',res.data.access_token);
        localStorage.setItem('refresh_token',res.data.refresh_token);
        console.log('Login successful');
        // Handle successful login (store tokens, redirect, etc.)
    } catch (error) {
        console.error('Error logging in with Google:', error);
    }
};

const handleGoogleLoginFailure = (error) => {
    console.error('Google Login failed:', error);
};

function LoginPage(props) { return (
        <div className='flex gap-4'>
              <GoogleLogin
                    onSuccess={handleGoogleLoginSuccess}
                    onError={handleGoogleLoginFailure}
            />
            <FacebookLogin appId='1221914495661734' fields='name,email,picture' onSuccess={responseFacebook} />
          {/* <LinkedIn clientId='86vwq0slixoekm'/> */}
          
        </div>
    );
}
export default LoginPage;