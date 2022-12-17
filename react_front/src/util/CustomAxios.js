import axios from "axios";
import jwtDecode from "jwt-decode";
import { BASE_URL } from "config/Constants";

class CustomAxios {
    static _instance = new CustomAxios();
    static instance = () => {
        return CustomAxios._instance;
    };

    // constructor: 파이썬의 init 역할
    constructor(){
        this.publicAxios = axios.create({ baseURL: BASE_URL})  // this: 파이썬의 self
        this.privateAxios = axios.create({  // 인증이 필요하면 privateAxios
            baseURL: BASE_URL,
            withCredentials: true,
        });
    }
}

export const customAxios =  CustomAxios.instance();