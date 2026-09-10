import { useEffect, useState } from "react";
import {
  Badge,
  Camera,
  CheckCircle2,
  Code2,
  ExternalLink,
  Globe,
  Info,
  Link2,
  Mail,
  MapPin,
  Phone,
  Save,
  Trash2,
  Upload,
  User,
  FileText,
  Eye,
  X,
} from "lucide-react";

const INITIAL_PROFILE = {
  fullName: "Alex Carter",
  email: "alex.carter@example.com",
  phone: "+1 (555) 382-9012",
  location: "San Francisco, CA",
  linkedin: "linkedin.com/in/alexcarter-dev",
  github: "github.com/alexcarter",
  leetcode: "leetcode.com/u/alexcarter_code",
  portfolio: "https://alexcarter.dev",
};

const INITIAL_RESUME = {
  name: "Alex_Carter_Resume_2025.pdf",
  size: "1.4 MB",
  updated: "Updated 3 days ago",
};

function SectionHeader({ icon: Icon, title, description, tone = "primary" }) {
  const toneClasses =
    tone === "tertiary"
      ? "bg-surface-low text-tertiary"
      : "bg-surface-low text-primary";

  return (
    <div className="flex items-start gap-3">
      <div
        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${toneClasses}`}
      >
        <Icon size={20} />
      </div>

      <div className="min-w-0 min-h-[64px]">
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

function InputField({
  label,
  icon: Icon,
  value,
  onChange,
  type = "text",
  placeholder,
}) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-bold text-on-surface">
        {label}
      </label>

      <div className="relative">
        <Icon
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-outline"
        />

        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="w-full rounded-lg bg-surface-low py-2.5 pl-9 pr-3 text-sm text-on-surface outline-none transition-all placeholder:text-outline focus:bg-surface-low focus:ring-2 focus:ring-primary/30"
        />
      </div>
    </div>
  );
}

function DeveloperLink({
  label,
  icon: Icon,
  value,
  onChange,
  placeholder,
}) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-bold text-on-surface">
        {label}
      </label>

      <div className="flex min-w-0 items-center gap-2 rounded-lg bg-surface-low p-2 focus-within:ring-2 focus-within:ring-primary/30">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white text-primary">
          <Icon size={16} />
        </div>

        <input
          type="text"
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="min-w-0 flex-1 bg-transparent px-1 text-sm text-on-surface outline-none placeholder:text-outline"
        />

        <ExternalLink
          size={15}
          className="shrink-0 text-outline"
        />
      </div>
    </div>
  );
}

export default function Profile() {
  const [profile, setProfile] = useState(INITIAL_PROFILE);
  const [savedProfile, setSavedProfile] = useState(INITIAL_PROFILE);

  const [resume, setResume] = useState(INITIAL_RESUME);
  const [resumeFile, setResumeFile] = useState(null);

  const [toast, setToast] = useState(null);

  useEffect(() => {
    if (!toast) return;

    const timer = setTimeout(() => {
      setToast(null);
    }, 3000);

    return () => clearTimeout(timer);
  }, [toast]);

  const updateField = (field) => (event) => {
    setProfile((current) => ({
      ...current,
      [field]: event.target.value,
    }));
  };

  const handleResumeChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(file.type)) {
      alert("Please upload a PDF or DOCX file.");
      return;
    }

    const maxSize = 5 * 1024 * 1024;

    if (file.size > maxSize) {
      alert("Resume must be smaller than 5 MB.");
      return;
    }

    setResumeFile(file);

    setResume({
      name: file.name,
      size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
      updated: "Ready to upload",
    });
  };

  const previewResume = () => {
    if (!resume && !resumeFile) {
      alert("No resume available to preview.");
      return;
    }

    if (resumeFile) {
      if (resumeFile.type === "application/pdf") {
        const url = URL.createObjectURL(resumeFile);
        window.open(url, "_blank", "noopener,noreferrer");
      } else {
        alert("DOCX preview is not available in the browser.");
      }

      return;
    }

    alert("Your current resume is stored securely and can be previewed after backend integration.");
  };

  const removeResume = () => {
    setResume(null);
    setResumeFile(null);
  };

  const handleSave = () => {
    setSavedProfile(profile);

    setToast({
      type: "success",
      message: "Profile changes saved successfully.",
    });
  };

  const handleDiscard = () => {
    setProfile(savedProfile);

    setToast({
      type: "info",
      message: "Changes discarded.",
    });
  };

  return (
    <main className="min-w-0 w-full bg-surface">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 pb-24">
        {/* Page Header / Hero */}
        <section className="pt-6 sm:pt-8">
          <div className="rounded-2xl bg-white p-5 shadow-sm sm:p-6">
            <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-center gap-4">
                <div className="relative">
                  <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-primary text-xl font-black text-white">
                    AC
                  </div>

                  <button
                    type="button"
                    className="absolute -bottom-1 -right-1 flex h-7 w-7 items-center justify-center rounded-full bg-white text-primary shadow-sm ring-1 ring-surface-low transition-colors hover:bg-surface-low"
                    title="Change profile photo"
                  >
                    <Camera size={14} />
                  </button>
                </div>

                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <h1 className="truncate text-2xl font-black tracking-tight text-on-surface">
                      My Profile
                    </h1>

                    <span className="inline-flex items-center gap-1 rounded-full bg-secondary-container px-2.5 py-1 text-[10px] font-bold text-primary">
                      <CheckCircle2 size={12} />
                      Profile Complete
                    </span>
                  </div>

                  <p className="mt-1 text-sm text-on-surface-variant">
                    Manage your personal information, developer profiles, and resume.
                  </p>
                </div>
              </div>

              <div className="flex shrink-0 items-center gap-2">
                <span className="hidden text-xs text-outline sm:block">
                  Last saved just now
                </span>
              </div>
            </div>
          </div>
        </section>

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">

        {/* Personal Information */}
        <section className="rounded-2xl bg-white p-5 shadow-sm sm:p-6">
          <SectionHeader
            icon={User}
            title="Personal Information"
            description="Keep your contact details up to date so recruiters can reach you."
          />

          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2">
            <InputField
              label="Full Name"
              icon={User}
              value={profile.fullName}
              onChange={updateField("fullName")}
              placeholder="Your full name"
            />

            <InputField
              label="Email Address"
              icon={Mail}
              type="email"
              value={profile.email}
              onChange={updateField("email")}
              placeholder="you@example.com"
            />

            <InputField
              label="Phone Number"
              icon={Phone}
              type="tel"
              value={profile.phone}
              onChange={updateField("phone")}
              placeholder="+1 (555) 123-4567"
            />

            <InputField
              label="Location"
              icon={MapPin}
              value={profile.location}
              onChange={updateField("location")}
              placeholder="City, Country"
            />
            <div className="md:col-span-2 flex items-start gap-2 rounded-xl bg-surface-low p-3">
            <Info
              size={16}
              className="mt-0.5 shrink-0 text-primary"
            />

            <p className="text-xs leading-5 text-on-surface-variant">
              Connecting your GitHub and LeetCode profiles allows HireSense
              to analyze your public activity and include relevant signals
              in job matching.
            </p>
          </div>
          </div>
        </section>

        {/* Developer Profiles */}
        <section className="rounded-2xl bg-white p-5 shadow-sm sm:p-6">
          <SectionHeader
            icon={Code2}
            title="Developer Profiles"
            description="Connect your public developer profiles so HireSense can better understand your experience."
            tone="tertiary"
          />

          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2">
            <DeveloperLink
              label="LinkedIn"
              icon={Link2}
              value={profile.linkedin}
              onChange={updateField("linkedin")}
              placeholder="linkedin.com/in/your-profile"
            />

            <DeveloperLink
              label="GitHub"
              icon={Code2}
              value={profile.github}
              onChange={updateField("github")}
              placeholder="github.com/your-username"
            />

            <DeveloperLink
              label="LeetCode"
              icon={TerminalIcon}
              value={profile.leetcode}
              onChange={updateField("leetcode")}
              placeholder="leetcode.com/u/your-username"
            />

            <DeveloperLink
              label="Portfolio"
              icon={Globe}
              value={profile.portfolio}
              onChange={updateField("portfolio")}
              placeholder="https://yourportfolio.com"
            />
          </div>

          <div className="mt-5 flex items-start gap-2 rounded-xl bg-surface-low p-3">
            <Info
              size={16}
              className="mt-0.5 shrink-0 text-primary"
            />

            <p className="text-xs leading-5 text-on-surface-variant">
              Connecting your GitHub and LeetCode profiles allows HireSense
              to analyze your public activity and include relevant signals
              in job matching.
            </p>
          </div>
        </section>

        </div>

        {/* Resume */}
        <section className="rounded-2xl bg-white p-5 shadow-sm sm:p-6">
          <SectionHeader
            icon={FileText}
            title="Resume"
            description="Your resume is used by HireSense to extract skills, experience, and role information for job matching."
          />

          <div className="mt-6">
            {resume ? (
              <div className="flex flex-col gap-4 rounded-xl bg-surface-container-low p-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex min-w-0 items-center gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-surface-low text-primary">
                    <FileText size={20} />
                  </div>

                  <div className="min-w-0">
                    <p className="truncate text-sm font-bold text-on-surface">
                      {resume.name}
                    </p>

                    <p className="mt-0.5 text-xs text-outline">
                      {resume.size} • {resume.updated}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={previewResume}
                    className="flex items-center gap-1.5 rounded-lg bg-white px-3 py-2 text-xs font-bold text-on-surface transition-colors hover:bg-surface-low"
                  >
                    <Eye size={14} />
                    Preview
                  </button>

                  <label className="flex cursor-pointer items-center gap-1.5 rounded-lg bg-primary px-3 py-2 text-xs font-bold text-white transition-colors hover:bg-primary-container">
                    <Upload size={14} />
                    Replace
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      onChange={handleResumeChange}
                      className="hidden"
                    />
                  </label>

                  <button
                    type="button"
                    onClick={removeResume}
                    className="flex h-9 w-9 items-center justify-center rounded-lg bg-white text-outline transition-colors hover:bg-error/10 hover:text-error"
                    title="Remove resume"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            ) : (
              <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-outline/30 bg-surface-container-low px-5 py-10 text-center transition-colors hover:bg-surface-low">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-surface-low text-primary">
                  <Upload size={22} />
                </div>

                <p className="mt-3 text-sm font-bold text-on-surface">
                  Upload your resume
                </p>

                <p className="mt-1 text-xs text-outline">
                  PDF or DOCX, up to 5MB
                </p>

                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleResumeChange}
                  className="hidden"
                />
              </label>
            )}
          </div>

          <div className="mt-4 flex items-start gap-2 text-xs text-outline">
            <Badge size={15} className="mt-0.5 shrink-0" />

            <p>
              Your resume is securely stored and analyzed only for hiring
              and job-matching purposes.
            </p>
          </div>
        </section>
      </div>

    {/* Sticky Save Bar */}
    <div className="fixed bottom-4 left-4 right-4 z-30 rounded-2xl border border-surface-high bg-white/90 px-4 py-3 shadow-lg backdrop-blur-md sm:left-6 sm:right-6 lg:left-[284px]">
    <div className="mx-auto flex w-full max-w-7xl items-center justify-end gap-2">
        <div className="hidden items-center gap-2 text-xs text-outline sm:flex mr-auto">
        <CheckCircle2 size={15} className="text-secondary" />
        <span>Your profile is up to date.</span>
        </div>

        <button
        type="button"
        onClick={handleDiscard}
        className="flex items-center gap-1.5 rounded-lg bg-surface-low px-4 py-2.5 text-xs font-bold text-on-surface transition-colors hover:bg-surface-high"
        >
        <X size={14} />
        Discard
        </button>

        <button
        type="button"
        onClick={handleSave}
        className="flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2.5 text-xs font-bold text-white transition-colors hover:bg-primary-container"
        >
        <Save size={14} />
        Save Changes
        </button>
    </div>
    </div>


      {/* Toast */}
      {toast && (
        <div className="fixed bottom-20 right-4 z-40 flex max-w-sm items-center gap-3 rounded-xl bg-white px-4 py-3 shadow-lg ring-1 ring-black/5">
          {toast.type === "success" ? (
            <CheckCircle2 size={18} className="shrink-0 text-secondary" />
          ) : (
            <Info size={18} className="shrink-0 text-primary" />
          )}

          <span className="text-sm font-semibold text-on-surface">
            {toast.message}
          </span>

          <button
            type="button"
            onClick={() => setToast(null)}
            className="ml-auto text-outline hover:text-on-surface"
          >
            <X size={15} />
          </button>
        </div>
      )}
    </main>
  );
}

function TerminalIcon(props) {
  return <Code2 {...props} />;
}