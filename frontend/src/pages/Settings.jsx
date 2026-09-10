import { useState } from "react";
import {
  CheckCircle2,
  KeyRound,
  LockKeyhole,
  Eye,
  EyeOff,
  ShieldCheck,
  Smartphone,
  Bell,
  BriefcaseBusiness,
  MessageSquare,
  UserRound,
  AlertTriangle,
  Trash2,
  PauseCircle,
  ArrowRight,
} from "lucide-react";

function SectionHeader({
  icon: Icon,
  title,
  description,
  tone = "primary",
}) {
  const toneClasses =
    tone === "tertiary"
      ? "bg-surface-low text-tertiary"
      : tone === "error"
        ? "bg-error-container text-error"
        : "bg-surface-low text-primary";

  return (
    <div className="flex items-start gap-3">
      <div
        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${toneClasses}`}
      >
        <Icon size={20} />
      </div>

      <div className="min-w-0">
        <h2 className="text-base font-bold text-on-surface">{title}</h2>

        {description && (
          <p className="mt-0.5 text-xs leading-5 text-on-surface-variant">
            {description}
          </p>
        )}
      </div>
    </div>
  );
}

function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`relative inline-flex h-7 w-12 shrink-0 cursor-pointer items-center rounded-full transition-colors ${
        checked ? "bg-primary" : "bg-outline/30"
      }`}
    >
      <span
        className={`absolute h-5 w-5 rounded-full bg-white shadow-sm transition-transform duration-200 ${
          checked ? "left-6" : "left-1"
        }`}
      />
    </button>
  );
}


function PasswordField({
  label,
  value,
  onChange,
  placeholder,
}) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-bold text-on-surface">
        {label}
      </label>

      <div className="relative">
        <LockKeyhole
          size={17}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-outline"
        />

        <input
          type={visible ? "text" : "password"}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full rounded-lg bg-surface-low py-2.5 pl-10 pr-10 text-sm text-on-surface outline-none transition-all placeholder:text-outline focus:bg-surface-low focus:ring-2 focus:ring-primary/30"
        />

        <button
          type="button"
          onClick={() => setVisible((current) => !current)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-outline transition-colors hover:text-on-surface"
          aria-label={visible ? "Hide password" : "Show password"}
        >
          {visible ? <EyeOff size={17} /> : <Eye size={17} />}
        </button>
      </div>
    </div>
  );
}

function SettingRow({
  icon: Icon,
  title,
  description,
  checked,
  onChange,
}) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-xl bg-surface-low/60 p-3 transition-colors hover:bg-surface-low">
      <div className="flex min-w-0 items-center gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-primary">
          <Icon size={18} />
        </div>

        <div className="min-w-0">
          <p className="text-xs font-bold text-on-surface">
            {title}
          </p>
          <p className="mt-0.5 text-xs leading-5 text-on-surface-variant">
            {description}
          </p>
        </div>
      </div>

      <Toggle checked={checked} onChange={onChange} />
    </div>
  );
}

export default function Settings() {
  const [passwords, setPasswords] = useState({
    current: "",
    next: "",
    confirm: "",
  });

  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);

  const [notifications, setNotifications] = useState({
    jobMatches: true,
    applicationUpdates: true,
    messages: true,
    platformUpdates: false,
  });

  const [showToast, setShowToast] = useState(false);

  const updatePassword = (field, value) => {
    setPasswords((current) => ({
      ...current,
      [field]: value,
    }));
  };

  const updateNotification = (field, value) => {
    setNotifications((current) => ({
      ...current,
      [field]: value,
    }));
  };

  const handlePasswordUpdate = (e) => {
    e.preventDefault();

    if (!passwords.current || !passwords.next || !passwords.confirm) {
      return;
    }

    if (passwords.next !== passwords.confirm) {
      return;
    }

    // Backend password update will be connected later.
    setPasswords({
      current: "",
      next: "",
      confirm: "",
    });

    setShowToast(true);

    setTimeout(() => {
      setShowToast(false);
    }, 2500);
  };

  const handleDeleteAccount = () => {
    const confirmed = window.confirm(
      "Are you sure you want to permanently delete your HireSense account? This action cannot be undone."
    );

    if (!confirmed) return;

    // Backend account deletion will be connected later.
  };

  return (
    <div className="relative w-full min-w-0 pb-10">
      {/* Ambient background */}
      <div className="pointer-events-none absolute -right-20 -top-20 h-72 w-72 rounded-full bg-gradient-to-br from-secondary-container/30 via-surface-high/20 to-transparent blur-3xl" />

      <div className="relative z-10 flex flex-col gap-5">
        {/* Page Header */}
        <div className="flex flex-col gap-1 pb-1">
          <div className="flex items-center gap-2 text-primary">
            <ShieldCheck size={16} />
            <span className="text-[11px] font-bold uppercase tracking-wider">
              Security & Control
            </span>
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-on-surface">
            Account Settings
          </h1>

          <p className="max-w-2xl text-sm leading-6 text-on-surface-variant">
            Manage your account security, notifications, and platform
            preferences.
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
          {/* Left Column */}
          <div className="flex flex-col gap-5 lg:col-span-7">
            {/* Password */}
            <section className="rounded-2xl bg-white p-5 shadow-sm">
              <div className="mb-5 flex items-start justify-between gap-4">
                <SectionHeader
                  icon={KeyRound}
                  title="Password & Credentials"
                  description="Keep your account credentials secure by updating your password regularly."
                />
              </div>

              <form
                onSubmit={handlePasswordUpdate}
                className="flex flex-col gap-4"
              >
                <PasswordField
                  label="Current Password"
                  value={passwords.current}
                  onChange={(value) =>
                    updatePassword("current", value)
                  }
                  placeholder="Enter current password"
                />

                <PasswordField
                  label="New Password"
                  value={passwords.next}
                  onChange={(value) =>
                    updatePassword("next", value)
                  }
                  placeholder="Enter a new password"
                />

                <PasswordField
                  label="Confirm New Password"
                  value={passwords.confirm}
                  onChange={(value) =>
                    updatePassword("confirm", value)
                  }
                  placeholder="Re-enter your new password"
                />

                {passwords.next &&
                  passwords.confirm &&
                  passwords.next !== passwords.confirm && (
                    <p className="text-xs font-semibold text-error">
                      Passwords do not match.
                    </p>
                  )}

                <div className="flex flex-col gap-3 border-t border-surface-high pt-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex items-center gap-2 text-xs text-outline">
                    <LockKeyhole size={14} className="text-primary" />
                    <span>
                      You may be signed out after changing your password.
                    </span>
                  </div>

                  <button
                    type="submit"
                    className="flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-xs font-bold text-white transition-colors hover:bg-primary-container"
                  >
                    Update Password
                    <ArrowRight size={14} />
                  </button>
                </div>
              </form>
            </section>

            {/* Two Factor */}
            <section className="rounded-2xl bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between gap-4">
                <SectionHeader
                  icon={ShieldCheck}
                  title="Two-Factor Authentication"
                  description="Add an extra layer of protection to your account."
                />

                <Toggle
                  checked={twoFactorEnabled}
                  onChange={setTwoFactorEnabled}
                />
              </div>

              {twoFactorEnabled && (
                <div className="mt-5 flex items-center justify-between gap-4 rounded-xl bg-surface-low p-3">
                  <div className="flex min-w-0 items-center gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-primary">
                      <Smartphone size={18} />
                    </div>

                    <div className="min-w-0">
                      <p className="text-xs font-bold text-on-surface">
                        Authenticator App
                      </p>
                      <p className="mt-0.5 text-xs text-on-surface-variant">
                        Configure an authenticator app for secure sign-in.
                      </p>
                    </div>
                  </div>

                  <button
                    type="button"
                    className="shrink-0 rounded-lg bg-white px-3 py-2 text-xs font-bold text-primary shadow-sm transition-colors hover:bg-surface-high"
                  >
                    Configure
                  </button>
                </div>
              )}
            </section>
          </div>

          {/* Right Column */}
          <div className="flex flex-col gap-5 lg:col-span-5">
            {/* Notifications */}
            <section className="rounded-2xl bg-white p-5 shadow-sm">
              <SectionHeader
                icon={Bell}
                title="Notification Preferences"
                description="Choose which updates you want to receive."
                tone="tertiary"
              />

              <div className="mt-5 flex flex-col gap-3">
                <SettingRow
                  icon={BriefcaseBusiness}
                  title="Job Match Recommendations"
                  description="Receive relevant opportunities based on your profile."
                  checked={notifications.jobMatches}
                  onChange={(value) =>
                    updateNotification("jobMatches", value)
                  }
                />

                <SettingRow
                  icon={CheckCircle2}
                  title="Application Updates"
                  description="Get notified when an application changes status."
                  checked={notifications.applicationUpdates}
                  onChange={(value) =>
                    updateNotification("applicationUpdates", value)
                  }
                />

                <SettingRow
                  icon={MessageSquare}
                  title="Messages"
                  description="Receive notifications for new platform messages."
                  checked={notifications.messages}
                  onChange={(value) =>
                    updateNotification("messages", value)
                  }
                />

                <SettingRow
                  icon={Bell}
                  title="Platform Updates"
                  description="Occasional product and feature announcements."
                  checked={notifications.platformUpdates}
                  onChange={(value) =>
                    updateNotification("platformUpdates", value)
                  }
                />
              </div>
            </section>
            {/* Danger Zone */}
            <section className="rounded-2xl bg-red-50/70 p-5 shadow-sm sm:p-6">
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-100 text-red-600">
                  <Trash2 size={20} />
                </div>

                <div className="min-w-0">
                  <h2 className="text-base font-bold text-red-700">
                    Danger Zone
                  </h2>

                  <p className="mt-1 text-xs leading-5 text-red-700/70">
                    Irreversible account actions. Please proceed with caution.
                  </p>
                </div>
              </div>

              <div className="mt-5 space-y-3">
                {/* Deactivate */}
                <div className="flex flex-col gap-4 rounded-xl border border-red-200 bg-white p-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <h3 className="text-sm font-bold text-on-surface">
                      Deactivate Account
                    </h3>

                    <p className="mt-1 text-xs leading-5 text-on-surface/60">
                      Temporarily disable your account and hide your profile.
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      window.alert("Account deactivation will be connected to the backend later.")
                    }
                    className="shrink-0 rounded-lg border border-red-200 bg-red-50 px-4 py-2.5 text-xs font-bold text-red-600 transition-colors hover:bg-red-100"
                  >
                    Deactivate
                  </button>
                </div>

                {/* Delete */}
                <div className="flex flex-col gap-4 rounded-xl border border-red-200 bg-white p-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <h3 className="text-sm font-bold text-on-surface">
                      Delete Account
                    </h3>

                    <p className="mt-1 text-xs leading-5 text-on-surface/60">
                      Permanently delete your account and all associated data.
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() => {
                      const confirmed = window.confirm(
                        "Are you sure you want to permanently delete your account?"
                      );

                      if (confirmed) {
                        window.alert(
                          "Account deletion will be connected to the backend later."
                        );
                      }
                    }}
                    className="shrink-0 rounded-lg bg-red-600 px-4 py-2.5 text-xs font-bold text-white transition-colors hover:bg-red-700"
                  >
                    Delete Account
                  </button>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>

      {/* Success Toast */}
      {showToast && (
        <div className="fixed bottom-5 right-5 z-50 flex items-center gap-2 rounded-xl bg-white px-4 py-3 text-xs font-semibold text-on-surface shadow-lg ring-1 ring-surface-high">
          <CheckCircle2 size={17} className="text-secondary" />
          Password updated successfully.
        </div>
      )}
    </div>
  );
}