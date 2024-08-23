import axios from "axios";


const googleLogin=(accesstoken)=>{
    axios.post('http://localhost:8000/auth/convert-token/',{
        token:accesstoken,
        backend:'google-oauth2',
        grant_type:'convert_token',
        client_id:'DDLoHmtZ6fmbQxV1fE271J1fJRUhmxv7a1Z6cOjN',
        client_secret:'jWi3rZJ71d5H6BwMuSdShM1yhtp25zl4D0TlRloPeVF0IYhXaYzyjrbE0L743gfJWdrtf2EFeADtmW1Ias7H7cZAIRjnknM1rWdLUWnpsmdIJfCisxe8WfxejlAUJksS'
    })
    .then((res)=>{
        localStorage.setItem('access_token',res.data.access_token);
        localStorage.setItem('refresh_token',res.data.refresh_token);
        console.log('Login successful');
    })
    .catch((err) => {
        console.error('Error logging in:', err.response?.data || err.message);
        // Handle error (show message to user, etc.)
    });
}
export default googleLogin;