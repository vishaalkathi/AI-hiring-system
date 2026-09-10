import {
  LayoutDashboard,
  BriefcaseBusiness,
  ClipboardList,
  Settings,
  LogOut,
  X,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const navItems = [
  {
    label: "Dashboard",
    path: "/employer/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Jobs Created",
    path: "/employer/jobs",
    icon: BriefcaseBusiness,
  },
  {
    label: "View Applications",
    path: "/employer/applications",
    icon: ClipboardList,
  },
];

function SidebarContent({ onNavigate }) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  return (
    <>
      {/* Logo */}
      <div className="flex h-20 items-center px-6">
        <button
          type="button"
          onClick={() => {
            navigate("/employer/dashboard");
            onNavigate?.();
          }}
          className="flex items-center gap-3"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-lg font-bold text-white">
            H
          </div>

          <span className="text-xl font-bold tracking-tight text-on-surface">
            HireSense
          </span>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">
        <div className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onNavigate}
                className={({ isActive }) =>
                  [
                    "flex min-w-0 items-center gap-3 rounded-xl px-4 py-3",
                    "text-sm font-semibold transition-all",
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-on-surface/70 hover:bg-surface-low hover:text-on-surface",
                  ].join(" ")
                }
              >
                <Icon
                  size={20}
                  strokeWidth={2}
                  className="shrink-0"
                />

                <span className="min-w-0 flex-1 truncate">
                  {item.label}
                </span>
              </NavLink>
            );
          })}
        </div>
      </nav>

      {/* Workspace section */}
      <div className="border-t border-outline/10 p-4">
        {/* Workspace */}
        <button
          onClick={() => {
            navigate("/employer/profile");
            onNavigate?.();
          }}
          className="
            mb-3 flex w-full min-w-0 items-center gap-3
            rounded-xl p-2 text-left
            transition-colors hover:bg-surface-low
          "
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 font-bold text-primary">
            TN
          </div>

          <div className="min-w-0">
            <p className="truncate text-sm font-bold text-on-surface">
              TechNova Workspace
            </p>

            <p className="text-xs text-on-surface/60">
              Sarah · HR
            </p>
          </div>
        </button>
        

        {/* Log out */}
        <button
          type="button"
          onClick={() => {
            logout();
            navigate("/login");
          }}
          className="
            flex w-full items-center gap-3
            rounded-xl px-3 py-2.5
            text-sm font-semibold text-on-surface/70
            transition-colors
            hover:bg-surface-low hover:text-on-surface
          "
        >
          <LogOut size={18} />
          <span>Log out</span>
        </button>

        {/* Settings */}
        <button
          type="button"
          onClick={() => {
            navigate("/employer/settings");
            onNavigate?.();
          }}
          className="
            flex w-full items-center gap-3
            rounded-xl px-3 py-2.5
            text-sm font-semibold text-on-surface/70
            transition-colors
            hover:bg-surface-low hover:text-on-surface
          "
        >
          <Settings size={18} className="shrink-0" />
          <span>Settings</span>
        </button>
      </div>
    </>
  );
}

function RecruiterSidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <button
          type="button"
          onClick={onClose}
          className="
            fixed inset-0 z-40
            bg-black/30
            backdrop-blur-[2px]
            lg:hidden
          "
          aria-label="Close navigation"
        />
      )}

      {/* Desktop sidebar */}
      <aside
        className="
          fixed left-0 top-0 z-40
          hidden h-screen w-[260px] shrink-0
          flex-col
          border-r border-outline/10
          bg-surface
          lg:flex
        "
      >
        <SidebarContent />
      </aside>

      {/* Mobile sidebar */}
      <aside
        className={`
          fixed left-0 top-0 z-50
          flex h-screen w-[280px]
          flex-col
          border-r border-outline/10
          bg-surface
          shadow-2xl
          transition-transform duration-300
          lg:hidden
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        {/* Close */}
        <button
          type="button"
          onClick={onClose}
          className="
            absolute right-4 top-5
            flex h-9 w-9 items-center justify-center
            rounded-lg
            text-on-surface/60
            hover:bg-surface-low
            hover:text-on-surface
          "
          aria-label="Close navigation"
        >
          <X size={20} />
        </button>

        <SidebarContent onNavigate={onClose} />
      </aside>
    </>
  );
}

export default RecruiterSidebar;