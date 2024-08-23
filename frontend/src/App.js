import LoginPage from "./pages/LoginPage";
import { GoogleOAuthProvider } from '@react-oauth/google';

function App() {
  return (
    <GoogleOAuthProvider clientId="137347691807-2ehifvqvrlfqvqagvargud88sg13uuvm.apps.googleusercontent.com">
    <div className="App">
      <div className="text-center">
        
      <LoginPage/>

      </div>
    </div>
    </GoogleOAuthProvider>
  );
}

export default App;
