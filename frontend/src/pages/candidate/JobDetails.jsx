import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  Bookmark,
  Building2,
  Check,
  ChevronRight,
  Clock3,
  Code2,
  DollarSign,
  ExternalLink,
  Heart,
  MapPin,
  Share2,
  Sparkles,
} from "lucide-react";

// ---------------------------------------------------------
// Mock job data
// Keep this aligned with the Datadog card in Jobs.jsx
// ---------------------------------------------------------

const MOCK_JOB = {
  id: 1,
  company: "Datadog",
  title: "Staff Frontend Engineer – Core Platform",
  match: 96,
  location: "Remote (US / Canada)",
  employmentType: "Full-time",
  salary: "$210,000 – $255,000 + Equity",
  posted: "2 hours ago",

  description:
    "Own the architecture of Datadog's next-generation Observability Canvas, building web experiences that handle millions of concurrent real-time nodes.",

  skills: [
    "React 19",
    "TypeScript",
    "WebGL",
    "Performance Optimization",
    "Design Systems",
  ],

  overview: [
    "The Observability Canvas is at the heart of how our customers understand complex systems. As a Staff Frontend Engineer, you'll serve as an architectural anchor for the web platform, designing the foundations that power a distributed, real-time, reactive canvas experience.",
    "You'll work across the product suite to push the boundaries of what's possible in the browser, including Chromium runtime introspection, Canvas/WebGL rendering, and developer experience improvements used by more than 400 frontend engineers.",
  ],

  responsibilities: [
    {
      title: "Canvas Architecture & Client Rendering",
      description:
        "Design and evolve rendering architecture using React, WebGL, Web Workers, and SharedArrayBuffers for highly interactive experiences.",
    },
    {
      title: "Runtime Profiling & Garbage Collection Elimination",
      description:
        "Use DevTools Performance, heap snapshots, and browser profiling techniques to eliminate layout thrashing and optimize compositing.",
    },
    {
      title: "High-Scale Data Visualization Strategy",
      description:
        "Build scalable visualization systems for time-series graphs, service topologies, flame graphs, and other complex datasets.",
    },
    {
      title: "RFC Culture & Technical Mentorship",
      description:
        "Lead RFC reviews, mentor engineers across teams, and establish benchmarking practices that keep performance regressions out of CI.",
    },
  ],

  requiredQualifications: [
    "7+ Years High-Scale Web",
    "Modern JavaScript & TypeScript Mastery",
    "Chromium Internals & Profiling",
  ],

  preferredQualifications: [
    "Open Source Ecosystem: Vite, Rollup, SWC",
    "Wasm & WebGL / WebGPU: Rust/C++ → WebAssembly",
    "Design Systems At Scale",
  ],

  benefits: [
    {
      title: "100% Medical, Dental, Vision",
      description: "Family coverage from day one",
    },
    {
      title: "$2,500 Home Office & Wellness",
      description: "Annual allowance",
    },
    {
      title: "401(k) with 5% Match",
      description: "Immediate vesting",
    },
    {
      title: "Unlimited PTO & Recharge Weeks",
      description: "Flexible time off to recharge",
    },
  ],
};

export default function JobDetails() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [bookmarked, setBookmarked] = useState(false);

  // For now, every details page resolves to our mock job.
  // Later this will become GET /jobs/:id.
  const job = MOCK_JOB;

  const handleApply = () => {
    navigate(`/candidate/jobs/${job.id}/apply`);
  };

  const handleBack = () => {
    navigate("/candidate/jobs");
  };

  const handleShare = async () => {
    const shareData = {
      title: `${job.title} at ${job.company}`,
      text: `Check out this job opportunity at ${job.company}.`,
      url: window.location.href,
    };

    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else if (navigator.clipboard) {
        await navigator.clipboard.writeText(window.location.href);
        alert("Job link copied to clipboard.");
      }
    } catch (error) {
      // User cancelled the native share dialog.
      console.log("Share cancelled:", error);
    }
  };

  return (
    <div className="w-full pb-28">
      {/* ---------------------------------------------------
          Breadcrumb
      --------------------------------------------------- */}
      <div className="mx-auto w-full max-w-7xl py-5">
        <button
          type="button"
          onClick={handleBack}
          className="group inline-flex items-center gap-2 text-sm font-bold text-on-surface/55 transition hover:text-primary"
        >
          <ArrowLeft
            size={17}
            className="transition-transform group-hover:-translate-x-0.5"
          />
          Back to Job Openings
        </button>
      </div>
    {/* ---------------------------------------------------
        Compact Job Header
    --------------------------------------------------- */}
    <section className="mx-auto w-full max-w-7xl">
        <div className="rounded-2xl border border-on-surface/5 bg-white shadow-sm">
            <div className="flex flex-col gap-5 p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">
                {/* Job identity */}
                <div className="flex min-w-0 items-center gap-4">
                    {/* Datadog logo */}
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#632ca6] text-xl font-black text-white shadow-sm sm:h-14 sm:w-14">
                        D
                    </div>

                    <div className="min-w-0">
                        <div className="flex flex-wrap items-center gap-2">
                            <h1 className="break-words text-xl font-black tracking-tight text-on-surface sm:text-2xl">
                                {job.title}
                            </h1>

                            <span className="inline-flex shrink-0 items-center gap-1 rounded-full bg-primary/10 px-2.5 py-1 text-xs font-extrabold text-primary">
                                <Sparkles size={11} />
                                {job.match}% Match
                            </span>
                        </div>

                        <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1.5 text-xs font-semibold text-on-surface/50 sm:text-sm">
                            <span className="inline-flex items-center gap-1.5">
                                <Building2 size={14} />
                                {job.company}
                            </span>

                            <span className="hidden text-on-surface/20 sm:inline">
                                •
                            </span>

                            <span className="inline-flex items-center gap-1.5">
                                <MapPin size={14} />
                                {job.location}
                            </span>

                            <span className="hidden text-on-surface/20 sm:inline">
                                •
                            </span>

                            <span>{job.employmentType}</span>
                        </div>

                        <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs font-bold text-on-surface/55">
                            <span className="inline-flex items-center gap-1">
                                <DollarSign size={13} />
                                {job.salary}
                            </span>

                            <span className="inline-flex items-center gap-1">
                                <Clock3 size={13} />
                                {job.posted}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Actions */}
                <div className="flex shrink-0 flex-wrap gap-2">
                    <button
                        type="button"
                        onClick={() => setBookmarked((value) => !value)}
                        className={`inline-flex items-center gap-2 rounded-xl border px-3.5 py-2.5 text-xs font-bold transition ${
                            bookmarked
                                ? "border-primary/20 bg-primary/10 text-primary"
                                : "border-on-surface/10 bg-white text-on-surface/65 hover:bg-surface-low"
                        }`}
                    >
                        {bookmarked ? (
                            <Heart size={15} fill="currentColor" />
                        ) : (
                            <Bookmark size={15} />
                        )}

                        <span className="hidden sm:inline">
                            {bookmarked ? "Saved" : "Bookmark"}
                        </span>
                    </button>

                    <button
                        type="button"
                        onClick={handleShare}
                        className="inline-flex items-center gap-2 rounded-xl border border-on-surface/10 bg-white px-3.5 py-2.5 text-xs font-bold text-on-surface/65 transition hover:bg-surface-low"
                    >
                        <Share2 size={15} />

                        <span className="hidden sm:inline">
                            Share Requisition
                        </span>

                        <span className="sm:hidden">Share</span>
                    </button>

                    <button
                        type="button"
                        onClick={handleApply}
                        className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-xs font-extrabold text-white shadow-sm transition hover:bg-primary-container"
                    >
                        Apply Now
                        <ChevronRight size={15} />
                    </button>
                </div>
            </div>
        </div>
    </section>

      {/* ---------------------------------------------------
          Main content
      --------------------------------------------------- */}
      <section className="mx-auto mt-6 grid w-full max-w-7xl grid-cols-1 gap-6 xl:grid-cols-3">
        {/* =================================================
            LEFT COLUMN
        ================================================= */}
        <div className="min-w-0 space-y-6 xl:col-span-2">
          {/* Role Overview */}
          <ContentCard title="Role Overview & Mission">
            <div className="space-y-4 text-sm leading-7 text-on-surface/70">
              {job.overview.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
          </ContentCard>

          {/* Responsibilities */}
          <ContentCard title="Key Responsibilities">
            <div className="space-y-5">
              {job.responsibilities.map((item, index) => (
                <div
                  key={item.title}
                  className="flex gap-4 rounded-2xl border border-on-surface/5 bg-surface-low/45 p-4"
                >
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-sm font-black text-primary">
                    {index + 1}
                  </div>

                  <div className="min-w-0">
                    <h3 className="text-sm font-extrabold text-on-surface">
                      {item.title}
                    </h3>

                    <p className="mt-1.5 text-sm leading-6 text-on-surface/60">
                      {item.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </ContentCard>

          {/* Qualifications */}
          <ContentCard title="Qualifications">
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <QualificationColumn
                title="Required"
                items={job.requiredQualifications}
                required
              />

              <QualificationColumn
                title="Preferred"
                items={job.preferredQualifications}
              />
            </div>
          </ContentCard>
        </div>

        {/* =================================================
            RIGHT COLUMN
        ================================================= */}
        <aside className="min-w-0 space-y-6">
          {/* Compensation */}
          <ContentCard title="Compensation & Benefits">
            <div className="space-y-4">
              {job.benefits.map((benefit) => (
                <div key={benefit.title} className="flex gap-3">
                  <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <Check size={14} strokeWidth={3} />
                  </div>

                  <div className="min-w-0">
                    <p className="text-sm font-extrabold text-on-surface">
                      {benefit.title}
                    </p>
                    <p className="mt-0.5 text-xs leading-5 text-on-surface/50">
                      {benefit.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </ContentCard>

          {/* Tech Stack */}
          <ContentCard
            title="Tech Stack & Skills"
            action={
              <span className="rounded-full bg-primary/10 px-2.5 py-1 text-xs font-extrabold text-primary">
                {job.skills.length} of {job.skills.length}
              </span>
            }
          >
            <div className="flex flex-wrap gap-2">
              {job.skills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-on-surface/8 bg-surface-low px-3 py-2 text-xs font-bold text-on-surface/70"
                >
                  <Code2 size={13} className="text-primary" />
                  {skill}
                </span>
              ))}
            </div>
          </ContentCard>

          {/* Match preview */}
          <div className="rounded-2xl border border-primary/15 bg-primary/5 p-5">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-white">
                <Sparkles size={18} />
              </div>

              <div className="min-w-0">
                <p className="text-sm font-extrabold text-on-surface">
                  Strong candidate match
                </p>

                <p className="mt-1 text-xs leading-5 text-on-surface/55">
                  Your verified skills align strongly with the requirements
                  for this role.
                </p>

                <button
                  type="button"
                  onClick={handleApply}
                  className="mt-3 inline-flex items-center gap-1 text-xs font-extrabold text-primary hover:underline"
                >
                  Continue to application
                  <ChevronRight size={13} />
                </button>
              </div>
            </div>
          </div>
        </aside>
      </section>

      {/* ---------------------------------------------------
          Floating application CTA
      --------------------------------------------------- */}
      <button
        type="button"
        onClick={handleApply}
        className="fixed bottom-5 right-5 z-30 inline-flex items-center gap-2 rounded-2xl bg-primary px-5 py-3.5 text-sm font-extrabold text-white shadow-xl transition hover:bg-primary-container sm:bottom-7 sm:right-7"
      >
        Apply Now
        <ChevronRight size={17} />
      </button>
    </div>
  );
}

// ---------------------------------------------------------
// Reusable components
// ---------------------------------------------------------

function ContentCard({ title, action, children }) {
  return (
    <section className="rounded-2xl border border-on-surface/5 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex items-center justify-between gap-4">
        <h2 className="text-lg font-black tracking-tight text-on-surface">
          {title}
        </h2>

        {action}
      </div>

      {children}
    </section>
  );
}

function QualificationColumn({ title, items, required = false }) {
  return (
    <div>
      <div className="mb-3 flex items-center gap-2">
        <span
          className={`h-2 w-2 rounded-full ${
            required ? "bg-primary" : "bg-tertiary"
          }`}
        />

        <h3 className="text-sm font-extrabold text-on-surface">{title}</h3>
      </div>

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item} className="flex gap-2.5">
            <Check
              size={16}
              className="mt-0.5 shrink-0 text-primary"
              strokeWidth={2.5}
            />

            <p className="text-sm leading-6 text-on-surface/65">{item}</p>
          </div>
        ))}
      </div>
    </div>
  );
}