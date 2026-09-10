import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ allowedRole }) {
    const {
        user,
        loading,
        isAuthenticated,
    } = useAuth();

    // Wait for AuthContext to determine
    // whether the user is logged in.
    if (loading) {
        return <h1>Loading...</h1>;
    }

    // Not logged in
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    // Logged in, but wrong role
    if (
        allowedRole &&
        user?.role !== allowedRole
    ) {
        return <Navigate to="/" replace />;
    }

    return <Outlet />;
}