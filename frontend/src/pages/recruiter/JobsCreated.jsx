import { useMemo, useState } from "react";
import {
  Search,
  Sparkles,
  Bell,
  Layers3,
  Users,
  Globe2,
  MapPin,
  Clock3,
  CreditCard,
  Plus,
  ArrowRight,
  ArrowUpDown,
  ChevronDown,
  Info,
} from "lucide-react";

const jobs = [
  {
    id: 1,
    category: "Frontend Core",
    title: "Lead React Engineer",
    status: "Active",
    location: "Remote (US)",
    locationType: "remote",
    type: "Full-time",
    salary: "$140k - $165k",
    description:
      "Architect mission-critical web experiences, lead micro-frontend initiatives, and mentor junior developers.",
    applications: 38,
    shortlist: 6,
    posted: "Posted 4 days ago",
    department: "Engineering",
    skills: ["React 18+", "TypeScript", "Next.js", "Tailwind CSS"],
  },
  {
    id: 2,
    category: "AI Platform",
    title: "Senior Fullstack AI Engineer",
    status: "Active",
    location: "San Francisco (Hybrid)",
    locationType: "hybrid",
    type: "Full-time",
    salary: "$195k - $235k",
    description:
      "Develop generative AI evaluation pipelines and real-time agent workflows using LLMs and Python.",
    applications: 54,
    shortlist: 10,
    posted: "Posted 1 week ago",
    department: "AI Platform",
    skills: ["Next.js", "Python", "LangChain", "PostgreSQL"],
  },
  {
    id: 3,
    category: "Platform Engineering",
    title: "Staff Frontend Architect",
    status: "Active",
    location: "Remote (US/CA)",
    locationType: "remote",
    type: "Full-time",
    salary: "$210k - $255k",
    description:
      "Architect high-throughput observability canvas rendering real-time streaming time-series metrics at 60 FPS.",
    applications: 26,
    shortlist: 8,
    posted: "Posted 2 weeks ago",
    department: "Engineering",
    skills: ["React 19", "WebGL", "TypeScript", "Perf Opt"],
  },
  {
    id: 4,
    category: "Product Design",
    title: "Senior UI/UX Product Designer",
    status: "Active",
    location: "New York (Hybrid)",
    locationType: "hybrid",
    type: "Full-time",
    salary: "$160k - $190k",
    description:
      "Design end-to-end design systems, candidate portals, and interactive talent assessment tools.",
    applications: 24,
    shortlist: 4,
    posted: "Posted 3 weeks ago",
    department: "Design",
    skills: ["Figma", "Design Systems", "Prototyping", "User Research"],
  },
];

function IconBadge({ children, className = "" }) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-lg bg-surface-low px-2.5 py-1 text-xs text-on-surface ${className}`}
    >
      {children}
    </span>
  );
}

function JobCard({ job }) {
  return (
    <div className="group flex flex-col justify-between rounded-3xl bg-white p-6 shadow-sm transition-all duration-300 hover:shadow-md">
      <div>
        <div className="mb-4 flex items-start justify-between gap-2">
          <div className="flex min-w-0 flex-col">
            <span className="mb-1 text-[11px] font-bold uppercase tracking-wider text-secondary">
              {job.category}
            </span>

            <h3 className="text-xl font-semibold tracking-tight text-on-surface transition-colors group-hover:text-primary">
              {job.title}
            </h3>
          </div>

          <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-[#bdece2] px-2.5 py-1 text-[11px] font-semibold text-[#224e47]">
            <span className="h-2 w-2 animate-pulse rounded-full bg-primary" />
            {job.status}
          </span>
        </div>

        <div className="mb-4 flex flex-wrap items-center gap-2 text-sm text-outline">
          <IconBadge>
            {job.locationType === "remote" ? (
              <Globe2 size={15} className="text-outline" />
            ) : (
              <MapPin size={15} className="text-outline" />
            )}
            {job.location}
          </IconBadge>

          <IconBadge>
            <Clock3 size={15} className="text-outline" />
            {job.type}
          </IconBadge>

          <IconBadge className="bg-[#bdece2]/40 font-semibold text-[#224e47]">
            <CreditCard size={15} />
            {job.salary}
          </IconBadge>
        </div>

        <p className="mb-6 line-clamp-2 text-[13px] leading-[18px] text-[#3d4947]">
          {job.description}
        </p>

        <div className="mb-4 flex items-center justify-around rounded-2xl bg-surface-low p-3">
          <div className="flex flex-1 flex-col text-center">
            <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
              Apps
            </span>
            <span className="text-base font-semibold text-on-surface">
              {job.applications}
            </span>
          </div>

          <div className="h-6 w-px bg-outline/20" />

          <div className="flex flex-1 flex-col text-center">
            <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
              Shortlist
            </span>
            <span className="text-base font-semibold text-primary">
              {job.shortlist}
            </span>
          </div>
        </div>

        <div className="mb-6 flex flex-wrap gap-1.5">
          {job.skills.map((skill) => (
            <span
              key={skill}
              className="rounded-md bg-surface-high px-2 py-0.5 text-[11px] font-semibold text-[#3d4947]"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      <div className="-mx-6 -mb-6 rounded-b-3xl bg-surface-low/40 p-6 pt-4">
        <div className="flex items-center justify-between text-[11px] font-bold text-outline">
          <span>{job.posted}</span>
        </div>
      </div>
    </div>
  );
}

function CreateJobCard({ onCreate }) {
  return (
    <button
      type="button"
      onClick={onCreate}
      className="group relative flex min-h-[360px] cursor-pointer flex-col items-center justify-between overflow-hidden rounded-3xl bg-[#bdece2]/20 p-8 text-center shadow-sm transition-all duration-300 hover:bg-[#bdece2]/40 hover:shadow-md"
    >
      <div className="pointer-events-none absolute inset-0 rounded-3xl bg-gradient-to-b from-[#89f5e7]/20 via-transparent to-transparent" />

      <div className="relative flex w-full justify-end">
        <span className="rounded-full bg-[#89f5e7] px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-[#00201d]">
          Instant Onboard
        </span>
      </div>

      <div className="relative my-auto flex flex-col items-center px-4">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary text-white shadow-lg transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-container">
          <Plus size={32} />
        </div>

        <h2 className="mb-2 text-xl font-semibold tracking-tight text-on-surface">
          Create New Job
        </h2>

        <p className="max-w-xs text-[13px] leading-[18px] text-[#3d4947]">
          Set up a new role requisition, define responsibilities,
          compensation, and AI evaluation criteria.
        </p>
      </div>

      <div className="relative w-full pt-4">
        <div className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-6 py-3 text-base font-semibold text-white shadow-sm transition-all group-hover:bg-primary-container">
          <span>Start Draft</span>
          <ArrowRight
            size={18}
            className="transition-transform group-hover:translate-x-1"
          />
        </div>
      </div>
    </button>
  );
}

export default function ExploreJobs() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("All Departments");
  const [status, setStatus] = useState("All Statuses");
  const [sortNewest, setSortNewest] = useState(true);

  const filteredJobs = useMemo(() => {
    let result = jobs.filter((job) => {
      const query = search.toLowerCase().trim();

      const matchesSearch =
        !query ||
        job.title.toLowerCase().includes(query) ||
        job.category.toLowerCase().includes(query) ||
        job.location.toLowerCase().includes(query) ||
        job.skills.some((skill) => skill.toLowerCase().includes(query));

      const matchesDepartment =
        department === "All Departments" ||
        job.department === department;

      const matchesStatus =
        status === "All Statuses" || job.status === status;

      return matchesSearch && matchesDepartment && matchesStatus;
    });

    result = [...result].sort((a, b) =>
      sortNewest ? a.id - b.id : b.id - a.id
    );

    return result;
  }, [search, department, status, sortNewest]);

  const handleCreateJob = () => {
    // Wire this to your create-job route later.
    console.log("Create new job");
  };

  return (
    <div className="relative w-full overflow-hidden pb-8">
      {/* Ambient background glow */}
      <div className="pointer-events-none absolute -right-24 -top-24 -z-10 h-96 w-96 rounded-full bg-[#89f5e7]/30 blur-3xl" />
      <div className="pointer-events-none absolute left-1/3 top-48 -z-10 h-80 w-80 rounded-full bg-[#bdece2]/20 blur-3xl" />

      <div className="flex w-full flex-col">
        {/* Header */}
        <div className="mb-8 flex flex-col gap-5">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-on-surface sm:text-[28px]">
                Jobs Created
              </h1>
            </div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="flex items-center justify-between rounded-2xl bg-white p-4 shadow-sm">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#bdece2] text-primary">
                  <Layers3 size={24} />
                </div>

                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
                    Jobs Open
                  </span>

                  <div className="text-[28px] font-bold leading-8 tracking-tight text-on-surface">
                    4{" "}
                    <span className="ml-1 text-[11px] font-bold text-primary">
                      Active
                    </span>
                  </div>
                </div>
              </div>

              <span className="rounded-md bg-surface-high px-2 py-1 text-[11px] font-bold text-[#3d4947]">
                100% capacity
              </span>
            </div>

            <div className="flex items-center justify-between rounded-2xl bg-white p-4 shadow-sm">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#d8e2ff] text-tertiary">
                  <Users size={24} />
                </div>

                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
                    Total Applications
                  </span>

                  <div className="text-[28px] font-bold leading-8 tracking-tight text-on-surface">
                    142{" "}
                    <span className="ml-1 text-[11px] font-bold text-primary">
                      ↑ 18%
                    </span>
                  </div>
                </div>
              </div>

              <span className="rounded-md bg-[#bdece2] px-2 py-1 text-[11px] font-bold text-[#224e47]">
                High Demand
              </span>
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-col items-stretch justify-between gap-4 rounded-2xl bg-white p-4 shadow-sm lg:flex-row lg:items-center">
            <div className="relative max-w-xl flex-1">
              <Search
                size={20}
                className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-outline"
              />

              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Filter by role, department, or location..."
                className="w-full rounded-xl bg-surface-low py-3 pl-11 pr-4 text-sm text-on-surface outline-none transition-all placeholder:text-outline focus:bg-surface"
              />
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <div className="relative">
                <select
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  className="appearance-none rounded-xl bg-surface-low py-3 pl-4 pr-10 text-[13px] font-semibold text-[#3d4947] outline-none transition-colors hover:bg-surface-high"
                >
                  <option>All Departments</option>
                  <option>Engineering</option>
                  <option>Design</option>
                  <option>Product</option>
                  <option>AI Platform</option>
                </select>

                <ChevronDown
                  size={18}
                  className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-outline"
                />
              </div>

              <div className="relative">
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="appearance-none rounded-xl bg-surface-low py-3 pl-4 pr-10 text-[13px] font-semibold text-[#3d4947] outline-none transition-colors hover:bg-surface-high"
                >
                  <option>All Statuses</option>
                  <option>Active</option>
                  <option>Draft</option>
                  <option>Paused</option>
                </select>

                <ChevronDown
                  size={18}
                  className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-outline"
                />
              </div>

              <button
                type="button"
                onClick={() => setSortNewest((value) => !value)}
                className="inline-flex items-center gap-1.5 rounded-xl bg-surface-low px-4 py-3 text-[13px] font-semibold text-[#3d4947] transition-colors hover:bg-surface-high"
                title="Toggle sorting order"
              >
                <ArrowUpDown size={18} />
                {sortNewest ? "Newest First" : "Oldest First"}
              </button>
            </div>
          </div>
        </div>

        {/* Jobs Grid */}
        <div className="mb-10 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
          <CreateJobCard onCreate={handleCreateJob} />

          {filteredJobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>

        {/* Empty state */}
        {filteredJobs.length === 0 && (
          <div className="mb-10 rounded-2xl bg-white p-10 text-center shadow-sm">
            <Search className="mx-auto mb-3 text-outline" size={28} />
            <h2 className="text-base font-semibold text-on-surface">
              No jobs found
            </h2>
            <p className="mt-1 text-sm text-outline">
              Try changing your search or filters.
            </p>
          </div>
        )}

        {/* Pagination */}
        <div className="flex flex-col items-center justify-between gap-4 rounded-2xl bg-white p-4 shadow-sm sm:flex-row">
          <div className="flex items-center gap-2 text-[13px] text-[#3d4947]">
            <Info size={18} className="text-primary" />

            <span>
              Showing{" "}
              <strong className="font-semibold text-on-surface">
                {filteredJobs.length} active jobs
              </strong>{" "}
              of 4 open requisitions
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              disabled
              className="rounded-lg bg-surface-low px-4 py-2 text-[13px] font-semibold text-[#3d4947] opacity-50"
            >
              Previous
            </button>

            <span className="rounded-lg bg-primary px-3 py-1.5 text-[11px] font-bold text-white">
              1
            </span>

            <button
              type="button"
              disabled
              className="rounded-lg bg-surface-low px-4 py-2 text-[13px] font-semibold text-[#3d4947] opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}