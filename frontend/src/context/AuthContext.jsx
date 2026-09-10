import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import api from "../api/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // --------------------------------------------------------
    // Check whether user is already logged in
    // --------------------------------------------------------

    useEffect(() => {

        const token = localStorage.getItem("access_token");

        if (!token) {
            setLoading(false);
            return;
        }

        api.get("/auth/me")
            .then((response) => {
                setUser(response.data);
            })
            .catch(() => {
                localStorage.removeItem("access_token");
                setUser(null);
            })
            .finally(() => {
                setLoading(false);
            });

    }, []);


    // --------------------------------------------------------
    // Login
    // --------------------------------------------------------

    const login = async (email, password) => {

        const response = await api.post(
            "/auth/login",
            {
                email,
                password,
            }
        );

        const token = response.data.access_token;

        localStorage.setItem(
            "access_token",
            token
        );

        // Get current user after login
        const userResponse = await api.get(
            "/auth/me"
        );

        setUser(userResponse.data);

        return userResponse.data;
    };


    // --------------------------------------------------------
    // Logout
    // --------------------------------------------------------

    const logout = () => {

        localStorage.removeItem(
            "access_token"
        );

        setUser(null);
    };


    // --------------------------------------------------------
    // Context
    // --------------------------------------------------------

    const value = {
        user,
        loading,
        isAuthenticated: !!user,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}


// ------------------------------------------------------------
// Hook
// ------------------------------------------------------------

export function useAuth() {

    const context = useContext(
        AuthContext
    );

    if (!context) {
        throw new Error(
            "useAuth must be used inside AuthProvider"
        );
    }

    return context;
}