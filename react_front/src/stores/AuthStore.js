import jwtDecode from "jwt-decode";
import { useState, useCallback, useEffect } from "react";

const AuthStore = () => {
    const [loginUser, setLoginUser] = useState(undefined);
    const setLoginUserByToken = useCallback((accessToken) => {  // accessToken: 매개변수
        try {
            const decodedAccessToken = jwtDecode(accessToken);
            setLoginUser(decodedAccessToken);
        } catch(e){
            setLoginUser(null);
            
        }
    }, []);

    // 이 위치에서 useEffect들을 사용하는 이유: 화면이 다 나온 뒤(?) 부르기 위해
    useEffect(() => {
        const accessToken = localStorage.getItem("accessToken");
        setLoginUserByToken(accessToken);
    }, []);
    useEffect(() => {
        if(loginUser === null){ // loginUser가 null 이면 아래 코드 실행
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
        }

    }, [loginUser]);

    return {
        loginUser,
        setLoginUser,
        setLoginUserByToken,
    };
};

export default AuthStore;