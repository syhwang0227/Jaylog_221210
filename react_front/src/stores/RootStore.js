// RootStore.js 파일: stores 관리
import { createContext, useContext } from "react";
import AuthStore from "stores/AuthStore";


const StoreContext = createContext();

export const StoreProvider = ({ children }) => {
    return (<StoreContext.Provider
        value={{
        authStore : AuthStore(),
        }}
    >
        {children}
    </StoreContext.Provider>
    );
};

/** @type {AuthStore()} useAuthStore */  // 타입 지정 / JS보다 타입스크립트 사용하는 이유
export const useAuthStore = () => useContext(StoreContext).authStore;