import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  BriefcaseBusiness,
  Building2,
  Check,
  CheckCircle2,
  Clock3,
  Info,
  MapPin,
  Sparkles,
} from "lucide-react";

const recommendedJobs = [
  {
    id: 1,
    title: "Lead React Engineer",
    company: "TechNova",
    subtitle: "Seed to Series B",
    match: 95,
    location: "Remote",
    salary: "$140k - $165k",
    skills: "React, TypeScript, GraphQL",
    icon: Building2,
  },
  {
    id: 2,
    title: "Frontend Architect",
    company: "CloudScale Inc.",
    subtitle: "Enterprise Cloud",
    match: 88,
    location: "SF (Hybrid)",
    salary: "$170k - $195k",
    skills: "Next.js, WebGL, Design Systems",
    icon: Building2,
  },
  {
    id: 3,
    title: "Senior Full Stack AI Developer",
    company: "SynthLabs AI",
    subtitle: "LLM Infra",
    match: 92,
    location: "Remote / US",
    salary: "$150k - $180k",
    skills: "Python, React, LLMs",
    icon: Building2,
  },
];

const recentApplications = [
  {
    id: 1,
    company: "Stripe",
    companyInitial: "S",
    role: "Senior Frontend Engineer",
    applied: "Applied 2 days ago",
    status: "Under Review",
    message: "Recruiter screening scheduling in progress.",
    reference: "Ref #ST-8841",
    action: "View timeline",
    icon: Info,
  },
  {
    id: 2,
    company: "Vercel",
    companyInitial: "▲",
    role: "Principal Design Technologist",
    applied: "Applied 1 week ago",
    status: "Tech Assessment",
    message: "Take-home due in 3 days.",
    reference: "Github repo shared",
    action: "Open prompt",
    icon: Clock3,
  },
  {
    id: 3,
    company: "Linear",
    companyInitial: "L",
    role: "Product Engineer",
    applied: "Applied 2 weeks ago",
    status: "Submitted",
    message: "Profile viewed by hiring manager.",
    reference: "Status stable",
    action: "Follow up",
    icon: Check,
  },
];

function JobRecommendationCard({ job, onQuickDetails, onApply }) {
  const Icon = job.icon;

  return (
    <div className="rounded-xl bg-white p-4 shadow-sm ring-1 ring-black/5 sm:p-5">
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-start gap-3">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#f2f3ff] text-[#00685f] sm:h-12 sm:w-12">
            <Icon size={22} />
          </div>

          <div className="min-w-0">
            <h3 className="truncate text-[18px] leading-6 font-bold text-[#131b2e] sm:text-[20px] sm:leading-7">
              {job.title}
            </h3>

            <p className="mt-0.5 text-sm font-semibold text-[#3d4947]">
              {job.company}
            </p>

            <p className="mt-0.5 text-xs text-[#6d7a77]">
              {job.subtitle}
            </p>
          </div>
        </div>

        <div className="shrink-0 rounded-full bg-[#e6f7f5] px-2.5 py-1 text-[11px] font-bold text-[#00685f]">
          {job.match}% Match
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        <span className="flex items-center gap-1 rounded-full bg-[#f2f3ff] px-2.5 py-1.5 text-[11px] font-medium text-[#3d4947]">
          <MapPin size={12} />
          {job.location}
        </span>

        <span className="rounded-full bg-[#f2f3ff] px-2.5 py-1.5 text-[11px] font-medium text-[#3d4947]">
          {job.salary}
        </span>

        <span className="rounded-full bg-[#f2f3ff] px-2.5 py-1.5 text-[11px] font-medium text-[#3d4947]">
          {job.skills}
        </span>
      </div>

      <div className="mt-5 flex items-center justify-between gap-3 border-t border-[#e2e7ff] pt-4">
        <button 
          onClick={() => onQuickDetails(job.id)} 
          className=" 
            w-full 
            rounded-xl 
            bg-[#f2f3ff] 
            px-4 py-2 
            text-[13px] 
            font-semibold 
            text-[#131b2e] 
            transition-colors 
            hover:bg-[#eaedff] 
            sm:w-auto 
          " 
        >
          Quick Details
        </button>

        <button 
          onClick={() => onApply(job.id)} 
          className=" 
            w-full 
            rounded-xl 
            bg-[#00685f] 
            px-4 py-2 
            text-[13px] 
            font-semibold 
            text-white 
            shadow-sm 
            transition-colors 
            hover:bg-[#008378] 
            sm:w-auto 
          " 
        >
          Apply
        </button>
      </div>
    </div>
  );
}

function ApplicationCard({ application }) {
  const Icon = application.icon;

  return (
    <div className="rounded-xl bg-white p-4 shadow-sm ring-1 ring-black/5 sm:p-5">
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#f2f3ff] text-lg font-bold text-[#00685f]">
            {application.companyInitial}
          </div>

          <div className="min-w-0">
            <h3 className="truncate text-base leading-6 font-bold text-[#131b2e]">
              {application.role}
            </h3>

            <p className="mt-0.5 text-[13px] font-semibold text-[#3d4947]">
              {application.company}
            </p>

            <p className="mt-0.5 text-[13px] text-[#6d7a77]">
              {application.applied}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-1.5 rounded-full bg-[#f2f3ff] px-2.5 py-1 text-[11px] font-semibold text-[#3d4947]">
          <Icon size={12} />
          {application.status}
        </div>
      </div>

      <div className="mt-4 rounded-lg bg-[#f2f3ff] p-2 text-[13px] leading-5 text-[#3d4947]">
        {application.message}
      </div>

      <div className="mt-4 flex items-center justify-between gap-3 border-t border-[#e2e7ff] pt-4">
        <span className="text-[11px] font-medium text-[#6d7a77]">
          {application.reference}
        </span>

        <button className="text-[11px] font-semibold text-[#00685f] transition-colors hover:text-[#008378]">
          {application.action}
        </button>
      </div>
    </div>
  );
}

export default function CandidateDashboard() {
  const navigate = useNavigate();
  const handleQuickDetails = (jobId) => { 
    navigate(`/candidate/jobs/${jobId}`); 
  }; 
  const handleApply = (jobId) => { 
    navigate(`/candidate/jobs/${jobId}/apply`); 
  };

  return (
    <div className="pb-10">
      {/* Page Header */}
      <div className="flex flex-col justify-between gap-4 pt-6 mb-8 lg:flex-row lg:items-center">
        <div>
          <h1 className="flex items-center gap-2 text-2xl leading-8 font-bold tracking-tight text-[#131b2e] sm:text-[28px]">
            Welcome back, Alex
            <span className="inline-block animate-bounce text-[30px]">
              👋
            </span>
          </h1>

          <p className="mt-1 text-sm leading-[22px] text-[#6d7a77]">
            Here is what your AI agent found for you today.
          </p>
        </div>
      </div>

      {/* Recommendations */}
      <section className="mb-10 flex flex-col">
        <div className="mb-5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles size={22} className="text-[#00685f]" />

            <h2 className="text-xl font-bold text-[#131b2e]">
              Top AI Recommendations
            </h2>
          </div>

          <button
            onClick={() => navigate("/candidate/jobs")}
            className="flex items-center gap-1 text-[13px] font-semibold text-[#00685f] transition-colors hover:text-[#008378]"
          >
            View all matches
            <ArrowRight size={16} />
          </button>
        </div>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {recommendedJobs.map((job) => (
            <JobRecommendationCard 
            key={job.id} 
            job={job} 
            onQuickDetails={handleQuickDetails}
            onApply={handleApply}/>
          ))}
        </div>
      </section>

      {/* Recent Applications */}
      <section className="flex flex-col">
        <div className="mb-5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock3 size={22} className="text-[#6d7a77]" />

            <h2 className="text-xl font-bold text-[#131b2e]">
              Recent Applications & Live Status
            </h2>
          </div>

          <button
            onClick={() => navigate("/candidate/applied")}
            className="flex items-center gap-1 text-[13px] font-semibold text-[#00685f] transition-colors hover:text-[#008378]"
          >
            Manage 12 applications
            <ArrowRight size={16} />
          </button>
        </div>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {recentApplications.map((application) => (
            <ApplicationCard
              key={application.id}
              application={application}
            />
          ))}
        </div>
      </section>
    </div>
  );
}