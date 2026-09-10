import { useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import TopNavbar from "../components/TopNavbar";

export default function CandidateLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-surface text-on-surface">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <TopNavbar
          onMenuClick={() => setSidebarOpen(true)}
        />

        <main className="min-w-0 flex-1 px-4 pt-20 sm:px-6 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}