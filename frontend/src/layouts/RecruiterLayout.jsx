import { useState } from "react";
import { Outlet } from "react-router-dom";
import RecruiterSidebar from "../components/RecruiterSidebar";
import RecruiterTopNavbar from "../components/RecruiterTopNavbar";

export default function RecruiterLayout() {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="min-h-screen bg-surface text-on-surface">
            <RecruiterSidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
            />

            <div className="min-h-screen lg:ml-[260px]">
                <RecruiterTopNavbar
                    onMenuClick={() => setSidebarOpen(true)}
                />

                <main className="min-w-0 px-4 pt-20 sm:px-6 lg:px-8">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}