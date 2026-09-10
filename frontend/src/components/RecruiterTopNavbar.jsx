import { useEffect, useRef, useState } from "react";
import {
  Search,
  Bell,
  Menu,
  CheckCircle2,
  BriefcaseBusiness,
  MessageSquare,
  Sparkles,
} from "lucide-react";

function RecruiterTopNavbar({ onMenuClick }) {
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const notificationRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        notificationRef.current &&
        !notificationRef.current.contains(event.target)
      ) {
        setNotificationsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const notifications = [
    {
      id: 1,
      icon: BriefcaseBusiness,
      title: "New Application",
      text: "Alex Carter applied for Lead React Engineer.",
      time: "2h ago",
      unread: true,
    },
    {
      id: 2,
      icon: CheckCircle2,
      title: "Strong Candidate Match",
      text: "A new candidate matches 96% of your job requirements.",
      time: "5h ago",
      unread: true,
    },
    {
      id: 3,
      icon: MessageSquare,
      title: "New Message",
      text: "Maya Lin sent you a message.",
      time: "1d ago",
      unread: false,
    },
  ];

  return (
    <header
      className="
        fixed left-0 right-0 top-0 z-30
        h-20
        border-b border-outline/10
        bg-surface/95
        backdrop-blur
        lg:left-[260px]
      "
    >
      <div className="flex h-full w-full items-center gap-2 px-4 sm:gap-4 sm:px-6 lg:px-8">

        {/* Mobile menu */}
        <button
          type="button"
          onClick={onMenuClick}
          className="
            flex h-11 w-11 shrink-0
            items-center justify-center
            rounded-xl
            text-on-surface/70
            transition-colors
            hover:bg-surface-low
            hover:text-on-surface
            lg:hidden
          "
          aria-label="Open navigation"
        >
          <Menu size={22} />
        </button>

        {/* Search input */}
        <div className="relative min-w-0 flex-1">
          <Search
            size={18}
            className="
              absolute left-3.5 top-1/2
              -translate-y-1/2
              text-on-surface/40
              sm:left-4
            "
          />

          <input
            type="text"
            placeholder="Search applicants, jobs, or skills..."
            className="
              h-11 w-full min-w-0
              rounded-xl
              bg-surface-low
              pl-10 pr-3
              text-sm text-on-surface
              outline-none
              placeholder:text-on-surface/40
              focus:ring-2 focus:ring-primary/20
              sm:pl-11 sm:pr-4
            "
          />
        </div>

        {/* Search button */}
        <button
          className="
            flex h-11 shrink-0
            items-center justify-center gap-2
            rounded-xl
            bg-primary
            px-3
            text-sm font-semibold
            text-white
            transition-colors
            hover:bg-primary-container
            sm:px-5
          "
          aria-label="Search"
        >
          <Search size={18} />

          <span className="hidden sm:inline">
            Search
          </span>
        </button>
        
        {/* Notifications */}
        <div ref={notificationRef} className="relative shrink-0">
          <button
            type="button"
            onClick={() => setNotificationsOpen((open) => !open)}
            className="
              relative flex h-11 w-11
              items-center justify-center
              rounded-xl
              text-on-surface/70
              transition-colors
              hover:bg-surface-low
              hover:text-on-surface
            "
            aria-label="Notifications"
            aria-expanded={notificationsOpen}
          >
            <Bell size={20} />

            {/* Unread indicator */}
            <span
              className="
                absolute right-2.5 top-2
                h-2.5 w-2.5
                rounded-full
                bg-red-500
                ring-2 ring-surface
              "
            />
          </button>

          {/* Notification popup */}
          {notificationsOpen && (
            <div
              className="
                absolute right-0 top-13 z-50
                w-[calc(100vw-2rem)] max-w-sm
                overflow-hidden
                rounded-2xl
                border border-surface-high
                bg-white
                shadow-xl
              "
            >
              {/* Header */}
              <div className="flex items-center justify-between border-b border-outline/10 px-4 py-3">
                <div>
                  <h3 className="text-sm font-bold text-on-surface">
                    Notifications
                  </h3>

                  <p className="mt-0.5 text-[11px] text-on-surface/50">
                    You have 2 unread notifications
                  </p>
                </div>

                <button
                  type="button"
                  className="
                    text-[11px]
                    font-bold
                    text-primary
                    hover:text-primary-container
                  "
                >
                  Mark all read
                </button>
              </div>

              {/* Notifications */}
              <div className="max-h-80 overflow-y-auto">
                {notifications.map((notification) => {
                  const Icon = notification.icon;

                  return (
                    <button
                      key={notification.id}
                      type="button"
                      className={`
                        flex w-full gap-3
                        border-b border-outline/5
                        px-4 py-3
                        text-left
                        transition-colors
                        hover:bg-surface-low
                        ${
                          notification.unread
                            ? "bg-surface-low/50"
                            : "bg-white"
                        }
                      `}
                    >
                      {/* Icon */}
                      <div
                        className="
                          flex h-9 w-9 shrink-0
                          items-center justify-center
                          rounded-lg
                          bg-surface-low
                          text-primary
                        "
                      >
                        <Icon size={17} />
                      </div>

                      {/* Content */}
                      <div className="min-w-0 flex-1">
                        <div className="flex items-start justify-between gap-2">
                          <p className="text-xs font-bold text-on-surface">
                            {notification.title}
                          </p>

                          <span className="shrink-0 text-[10px] text-outline">
                            {notification.time}
                          </span>
                        </div>

                        <p className="mt-0.5 text-[11px] leading-5 text-on-surface/60">
                          {notification.text}
                        </p>
                      </div>

                      {/* Unread dot */}
                      {notification.unread && (
                        <span
                          className="
                            mt-1.5 h-1.5 w-1.5 shrink-0
                            rounded-full
                            bg-primary
                          "
                        />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default RecruiterTopNavbar;