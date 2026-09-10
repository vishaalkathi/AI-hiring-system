import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  Building2,
  CheckCircle2,
  ShieldCheck,
  Badge,
  FileText,
  Upload,
  Eye,
  Link as LinkIcon,
  Code2,
  Send,
  Lock,
  Check,
  X,
  Save,
  Sparkles,
  MapPin,
  DollarSign,
  Clock3,
} from "lucide-react";

const MOCK_JOB = {
  id: 1,
  company: "TechNova",
  title: "Lead React Engineer",
  match: 98,
  salary: "$140k – $165k / yr",
  type: "Full-time",
  location: "Remote (US / CA)",
  recruiter: "Sarah Lin",
  skills: [
    "React 18+",
    "TypeScript",
    "Next.js App Router",
    "Tailwind CSS",
    "State Management",
    "Web Performance",
    "Node.js Microservices",
  ],
};

const INITIAL_FORM = {
  name: "Alex Carter",
  email: "alex.carter@example.com",
  phone: "+1 (555) 382-9012",
  titleLocation: "Senior Frontend Engineer • San Francisco, CA",
  linkedin: "linkedin.com/in/alexcarter-dev",
  github: "github.com/alexcarter",
  coverLetter: "",
  additionalInfo: "",
};


export default function JobApplication() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [form, setForm] = useState(INITIAL_FORM);
  const [showConfirm, setShowConfirm] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const [resumeFile, setResumeFile] = useState(null);

  const job = MOCK_JOB;

  const updateField = (field, value) => {
    setForm((current) => ({
      ...current,
      [field]: value,
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
    };

  const handleSaveDraft = () => {
    setDraftSaved(true);

    setTimeout(() => {
      setDraftSaved(false);
    }, 1800);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!resumeFile) {
        alert("Please upload your resume before submitting.");
        return;
    }
    setShowConfirm(true);
  };

  const confirmSubmission = () => {
    setSubmitted(true);
  };

  const closeModal = () => {
    setShowConfirm(false);
  };

  return (
    <>
      <div className="mx-auto w-full max-w-6xl pb-32">
        {/* Breadcrumb */}
        <div className="pt-5 sm:pt-7">
          <button
            onClick={() => navigate("/candidate/jobs")}
            className="
              inline-flex items-center gap-2
              text-xs font-semibold
              text-on-surface/55
              transition-colors
              hover:text-primary
              sm:text-sm
            "
          >
            <ArrowLeft size={16} />
            Job Openings
          </button>

          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-on-surface/45">
            <span>/</span>
            <span>{job.company}</span>
            <span>/</span>
            <span className="font-semibold text-primary">
              Application Portal
            </span>
          </div>
        </div>

        {/* Job Header */}
        <section
          className="
            mt-5 rounded-2xl
            border border-outline/10
            bg-white
            p-5 shadow-sm
            sm:p-6
          "
        >
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex min-w-0 items-start gap-4">
              <div
                className="
                  flex h-14 w-14 shrink-0
                  items-center justify-center
                  rounded-xl bg-secondary/10
                  text-secondary
                "
              >
                <Building2 size={28} />
              </div>

              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h1
                    className="
                      break-words
                      text-xl font-bold
                      tracking-tight text-on-surface
                      sm:text-2xl
                    "
                  >
                    {job.title}
                  </h1>

                  <span
                    className="
                      inline-flex shrink-0
                      items-center gap-1
                      rounded-full
                      border border-primary/15
                      bg-primary/5
                      px-2.5 py-1
                      text-[11px] font-bold
                      text-primary
                    "
                  >
                    <CheckCircle2 size={13} />
                    {job.match}% Profile Match
                  </span>
                </div>

                <div
                  className="
                    mt-2 flex flex-wrap
                    items-center gap-x-3 gap-y-1.5
                    text-xs text-on-surface/55
                    sm:text-sm
                  "
                >
                  <span className="font-bold text-on-surface">
                    {job.company}
                  </span>

                  <span className="hidden h-1 w-1 rounded-full bg-outline/40 sm:block" />

                  <span className="flex items-center gap-1">
                    <DollarSign size={14} />
                    {job.salary}
                  </span>

                  <span className="hidden h-1 w-1 rounded-full bg-outline/40 sm:block" />

                  <span className="flex items-center gap-1">
                    <Clock3 size={14} />
                    {job.type}
                  </span>

                  <span className="hidden h-1 w-1 rounded-full bg-outline/40 sm:block" />

                  <span className="flex items-center gap-1">
                    <MapPin size={14} />
                    {job.location}
                  </span>
                </div>
              </div>
            </div>

            <div className="hidden shrink-0 flex-col items-end sm:flex">
              <span className="text-[10px] font-bold uppercase tracking-wider text-on-surface/40">
                Application Status
              </span>

              <span className="mt-1 flex items-center gap-1.5 text-xs font-bold text-secondary">
                <span className="h-2 w-2 rounded-full bg-secondary" />
                Ready to Apply
              </span>
            </div>
          </div>
        </section>

        {/* Profile Sync Banner */}
        <section
          className="
            mt-4 flex items-start
            gap-3 rounded-2xl
            bg-primary/5
            p-4
            sm:items-center
            sm:justify-between
          "
        >
          <div className="flex min-w-0 items-start gap-3">
            <div
              className="
                flex h-9 w-9 shrink-0
                items-center justify-center
                rounded-full bg-primary
                text-white
              "
            >
              <ShieldCheck size={18} />
            </div>

            <div className="min-w-0">
              <p className="text-sm font-bold text-on-surface">
                Candidate Profile Synced
              </p>

              <p className="mt-1 text-xs leading-5 text-on-surface/60 sm:text-sm">
                Your verified profile information, resume, skills, and
                portfolio links have been pre-filled. Review everything before
                submitting your application.
              </p>
            </div>
          </div>

          <span
            className="
              hidden shrink-0 items-center gap-1
              rounded-full bg-white
              px-2.5 py-1.5
              text-[10px] font-bold
              text-primary shadow-sm
              md:inline-flex
            "
          >
            <Check size={13} />
            Profile Synced
          </span>
        </section>

        <form
          onSubmit={handleSubmit}
          className="mt-5 flex flex-col gap-5"
        >
          {/* Personal Information */}
          <section
            className="
              rounded-2xl
              border border-outline/10
              bg-white
              p-5 shadow-sm
              sm:p-6
            "
          >
            <SectionHeader
              icon={<Badge size={21} />}
              title="Personal Information"
              badge="From Profile"
            />

            <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
              <InputField
                label="Full Name"
                required
                value={form.name}
                onChange={(value) => updateField("name", value)}
                verified
              />

              <InputField
                label="Email Address"
                required
                type="email"
                value={form.email}
                onChange={(value) => updateField("email", value)}
                verified
              />

              <InputField
                label="Phone Number"
                required
                type="tel"
                value={form.phone}
                onChange={(value) => updateField("phone", value)}
                verified
              />

              <InputField
                label="Current Title & Location"
                value={form.titleLocation}
                onChange={(value) =>
                  updateField("titleLocation", value)
                }
              />

              <InputField
                label="LinkedIn Profile"
                icon={<LinkIcon size={17} />}
                value={form.linkedin}
                onChange={(value) => updateField("linkedin", value)}
              />

              <InputField
                label="GitHub / Portfolio URL"
                icon={<Code2 size={17} />}
                value={form.github}
                onChange={(value) => updateField("github", value)}
              />
            </div>
          </section>

          {/* Resume */}
          <section
            className="
              rounded-2xl
              border border-outline/10
              bg-white
              p-5 shadow-sm
              sm:p-6
            "
          >
            <SectionHeader
              icon={<FileText size={21} />}
              title="Resume & Match Qualifications"
              rightText="PDF or DOCX"
            />

            <div
              className="
                mt-5 flex flex-col gap-4
                rounded-xl bg-surface-low
                p-4
                sm:flex-row sm:items-center sm:justify-between
              "
            >
              <div className="flex min-w-0 items-center gap-3">
            <div
                className="
                flex h-11 w-11 shrink-0
                items-center justify-center
                rounded-xl
                bg-surface-high
                text-primary
                "
            >
                <FileText size={23} />
            </div>

            <div className="min-w-0">
                {resumeFile ? (
                <>
                    <div className="flex flex-wrap items-center gap-2">
                    <p className="break-all text-sm font-bold text-on-surface">
                        {resumeFile.name}
                    </p>

                    <span
                        className="
                        rounded-full
                        bg-primary/10
                        px-2 py-1
                        text-[10px] font-bold
                        text-primary
                        "
                    >
                        Selected
                    </span>
                    </div>

                    
                    <p className="mt-1 text-xs text-on-surface/45">
                    {(resumeFile.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                </>
                ) : (
                <>
                    <p className="text-sm font-bold text-on-surface">
                    No resume selected
                    </p>

                    <p className="mt-1 text-xs text-on-surface/45">
                    Upload a PDF or DOCX resume
                    </p>
                </>
                )}
            </div>
            </div>
              <div className="flex shrink-0 gap-2">
                <button
                    type="button"
                    disabled={!resumeFile || resumeFile.type !== "application/pdf"}
                    onClick={() => {
                        if (!resumeFile) return;

                        const url = URL.createObjectURL(resumeFile);

                        window.open(url, "_blank");
                    }}
                    className="
                        flex items-center gap-1.5
                        rounded-xl bg-white
                        px-3 py-2
                        text-xs font-semibold
                        text-on-surface
                        shadow-sm
                        hover:bg-surface-high
                        disabled:cursor-not-allowed
                        disabled:opacity-40
                    "
                    >
                    <Eye size={15} />
                    Preview
                </button>

                <input
                    id="resume-upload"
                    type="file"
                    accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    onChange={handleResumeChange}
                    className="hidden"
                />

                <label
                    htmlFor="resume-upload"
                    className="
                        flex cursor-pointer items-center gap-1.5
                        rounded-xl bg-white
                        px-3 py-2
                        text-xs font-bold
                        text-primary
                        shadow-sm
                        hover:bg-surface-high
                    "
                >
                <Upload size={15} />
                {resumeFile ? "Replace" : "Upload Resume"}
                </label>
              </div>
            </div>

            {/* Skills */}
            <div className="mt-5">
              <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs font-bold text-on-surface">
                  Verified Skills for this Opening
                </p>

                <span className="text-xs font-bold text-primary">
                  {job.skills.length} / {job.skills.length} Matching Stack
                </span>
              </div>

              <div className="mt-3 flex flex-wrap gap-2">
                {job.skills.map((skill) => (
                  <span
                    key={skill}
                    className="
                      inline-flex items-center gap-1.5
                      rounded-full
                      border border-primary/15
                      bg-primary/5
                      px-3 py-1.5
                      text-[11px] font-semibold
                      text-primary
                    "
                  >
                    <Check size={13} />
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </section>

          {/* Submission Bar */}
          <div
            className="
              sticky bottom-4 z-30
              flex flex-col gap-4
              rounded-2xl
              border border-outline/10
              bg-white/95
              p-4
              shadow-xl
              backdrop-blur-xl
              sm:flex-row
              sm:items-center
              sm:justify-between
              sm:p-5
            "
          >
            <div className="flex min-w-0 items-center gap-3">
              <div
                className="
                  flex h-10 w-10 shrink-0
                  items-center justify-center
                  rounded-full
                  bg-surface-high
                  text-primary
                "
              >
                <Lock size={20} />
              </div>

              <div className="min-w-0">
                <p className="text-sm font-bold text-on-surface">
                  Ready to submit
                </p>

                <p className="mt-0.5 text-xs text-on-surface/45">
                  Your application will be securely submitted to {job.company}.
                </p>
              </div>
            </div>

            <div className="flex w-full gap-2 sm:w-auto">

              <button
                type="submit"
                className="
                  flex flex-[1.4]
                  items-center justify-center gap-2
                  rounded-xl
                  bg-primary
                  px-5 py-2.5
                  text-xs font-bold
                  text-white
                  shadow-md
                  transition-all
                  hover:bg-primary-container
                  active:scale-[0.98]
                  sm:flex-none sm:text-sm
                "
              >
                <Send size={16} />
                Submit Application
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Confirmation Modal */}
      {showConfirm && (
        <div
          className="
            fixed inset-0 z-[100]
            flex items-center justify-center
            bg-black/35
            p-4
            backdrop-blur-sm
          "
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeModal();
            }
          }}
        >
          <div
            className="
              w-full max-w-md
              rounded-2xl
              bg-white
              p-6
              shadow-2xl
              sm:p-8
            "
          >
            {!submitted ? (
              <>
                <div className="text-center">
                  <div
                    className="
                      mx-auto flex h-14 w-14
                      items-center justify-center
                      rounded-full
                      bg-secondary/10
                      text-secondary
                    "
                  >
                    <Send size={24} />
                  </div>

                  <h2 className="mt-4 text-xl font-bold text-on-surface">
                    Submit Application?
                  </h2>

                  <p className="mt-2 text-sm leading-6 text-on-surface/55">
                    Your profile, resume, and application responses will be
                    submitted for the <strong>{job.title}</strong> position at{" "}
                    <strong>{job.company}</strong>.
                  </p>
                </div>

                <div className="mt-5 rounded-xl bg-surface-low p-4">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-on-surface/45">
                      Profile Match
                    </span>

                    <span className="font-bold text-secondary">
                      {job.match}%
                    </span>
                  </div>

                  <div className="mt-3 flex items-center justify-between text-xs">
                    <span className="text-on-surface/45">
                      Resume
                    </span>

                    <span className="font-semibold text-on-surface">
                      AI Parsed
                    </span>
                  </div>

                  <div className="mt-3 flex items-center justify-between text-xs">
                    <span className="text-on-surface/45">
                      Required Skills
                    </span>

                    <span className="font-semibold text-secondary">
                      {job.skills.length}/{job.skills.length}
                    </span>
                  </div>
                </div>

                <div className="mt-5 flex gap-2">
                  <button
                    type="button"
                    onClick={closeModal}
                    className="
                      flex-1
                      rounded-xl
                      border border-outline/15
                      px-4 py-2.5
                      text-sm font-semibold
                      text-on-surface
                      hover:bg-surface-low
                    "
                  >
                    Review
                  </button>

                  <button
                    type="button"
                    onClick={confirmSubmission}
                    className="
                      flex-1
                      rounded-xl
                      bg-primary
                      px-4 py-2.5
                      text-sm font-bold
                      text-white
                      hover:bg-primary-container
                    "
                  >
                    Confirm Submit
                  </button>
                </div>
              </>
            ) : (
              <div className="text-center">
                <div
                  className="
                    mx-auto flex h-16 w-16
                    items-center justify-center
                    rounded-full
                    bg-secondary/10
                    text-secondary
                  "
                >
                  <CheckCircle2 size={34} />
                </div>

                <h2 className="mt-5 text-xl font-bold text-on-surface">
                  Application Submitted!
                </h2>

                <p className="mt-2 text-sm leading-6 text-on-surface/55">
                  Your application for{" "}
                  <strong>{job.title}</strong> at{" "}
                  <strong>{job.company}</strong> has been submitted
                  successfully.
                </p>

                <div className="mt-5 rounded-xl bg-surface-low p-4 text-left">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-on-surface/45">
                      Application ID
                    </span>

                    <span className="font-mono text-xs font-bold text-on-surface">
                      HN-{String(id || "849204").padStart(6, "0")}
                    </span>
                  </div>

                  <div className="mt-3 flex items-center justify-between">
                    <span className="text-xs text-on-surface/45">
                      Status
                    </span>

                    <span className="flex items-center gap-1.5 text-xs font-bold text-secondary">
                      <Check size={13} />
                      Submitted
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => navigate("/candidate/applied")}
                  className="
                    mt-5 w-full
                    rounded-xl
                    bg-primary
                    px-4 py-2.5
                    text-sm font-bold
                    text-white
                    hover:bg-primary-container
                  "
                >
                  View Applied Jobs
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function SectionHeader({ icon, title, badge, rightText }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div className="flex min-w-0 items-center gap-2.5">
        <span className="shrink-0 text-primary">{icon}</span>

        <h2 className="text-base font-bold text-on-surface sm:text-lg">
          {title}
        </h2>
      </div>

      {badge && (
        <span
          className="
            hidden shrink-0
            items-center gap-1
            rounded-full
            bg-primary/5
            px-2.5 py-1.5
            text-[10px] font-bold
            text-primary
            sm:inline-flex
          "
        >
          <CheckCircle2 size={13} />
          {badge}
        </span>
      )}

      {rightText && (
        <span className="shrink-0 text-[10px] font-semibold text-on-surface/40 sm:text-xs">
          {rightText}
        </span>
      )}
    </div>
  );
}

function InputField({
  label,
  required = false,
  type = "text",
  value,
  onChange,
  verified = false,
  icon,
}) {
  return (
    <div className="min-w-0">
      <label className="text-xs font-bold text-on-surface sm:text-sm">
        {label}

        {required && (
          <span className="ml-1 text-red-500">*</span>
        )}
      </label>

      <div className="relative mt-2">
        {icon && (
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface/35">
            {icon}
          </span>
        )}

        <input
          required={required}
          type={type}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          className={`
            h-11 w-full
            rounded-xl
            bg-surface-low
            px-3
            text-sm text-on-surface
            outline-none
            transition-colors
            focus:bg-white
            focus:ring-2 focus:ring-primary/10
            ${icon ? "pl-10" : ""}
            ${verified ? "pr-10" : ""}
          `}
        />

        {verified && (
          <CheckCircle2
            size={17}
            className="
              absolute right-3 top-1/2
              -translate-y-1/2
              text-primary
            "
          />
        )}
      </div>
    </div>
  );
}
