import { useMemo, useState } from "react";
import {
  Search,
  FolderOpen,
  Hourglass,
  Star,
  CalendarDays,
  Terminal,
  PenTool,
  Triangle,
  Cloud,
  Database,
  Layers,
  Globe,
  ChevronLeft,
  ChevronRight,
  SlidersHorizontal,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const APPLICATIONS = [
  {
    id: 1,
    company: "TechNova",
    role: "Lead React Engineer",
    location: "Remote (US)",
    date: "Oct 22, 2024",
    daysAgo: "4 days ago",
    status: "Under Review",
    statusType: "review",
    icon: Terminal,
  },
  {
    id: 2,
    company: "Figma",
    role: "Staff UI Engineer",
    location: "San Francisco / Hybrid",
    date: "Oct 18, 2024",
    daysAgo: "8 days ago",
    status: "Interview Scheduled",
    statusType: "interview",
    icon: PenTool,
  },
  {
    id: 3,
    company: "Vercel",
    role: "Principal Design Technologist",
    location: "Remote (Global)",
    date: "Oct 14, 2024",
    daysAgo: "12 days ago",
    status: "Technical Assessment",
    statusType: "assessment",
    icon: Triangle,
  },
  {
    id: 4,
    company: "CloudScale Inc.",
    role: "Frontend Architect",
    location: "Austin, TX",
    date: "Oct 10, 2024",
    daysAgo: "16 days ago",
    status: "Interview Scheduled",
    statusType: "interview",
    icon: Cloud,
  },
  {
    id: 5,
    company: "Supabase",
    role: "Full Stack Engineer",
    location: "Remote",
    date: "Oct 02, 2024",
    daysAgo: "24 days ago",
    status: "Offer Extended",
    statusType: "offer",
    icon: Database,
  },
  {
    id: 6,
    company: "Linear",
    role: "Senior UI Engineer",
    location: "Remote (EU/US)",
    date: "Sep 28, 2024",
    daysAgo: "28 days ago",
    status: "Application Received",
    statusType: "received",
    icon: Layers,
  },
  {
    id: 7,
    company: "Datadog",
    role: "Staff Frontend Engineer",
    location: "Remote (US / Canada)",
    date: "Sep 24, 2024",
    daysAgo: "32 days ago",
    status: "Under Review",
    statusType: "review",
    icon: Terminal,
  },
  {
    id: 8,
    company: "Stripe",
    role: "Senior Frontend Engineer",
    location: "Remote",
    date: "Sep 21, 2024",
    daysAgo: "35 days ago",
    status: "Under Review",
    statusType: "review",
    icon: Globe,
  },
  {
    id: 9,
    company: "Notion",
    role: "Design Technologist",
    location: "New York / Hybrid",
    date: "Sep 18, 2024",
    daysAgo: "38 days ago",
    status: "Shortlisted",
    statusType: "shortlisted",
    icon: PenTool,
  },
  {
    id: 10,
    company: "GitLab",
    role: "Senior Full Stack Engineer",
    location: "Remote",
    date: "Sep 15, 2024",
    daysAgo: "41 days ago",
    status: "Application Received",
    statusType: "received",
    icon: Terminal,
  },
  {
    id: 11,
    company: "Vite",
    role: "Frontend Platform Engineer",
    location: "Remote",
    date: "Sep 11, 2024",
    daysAgo: "45 days ago",
    status: "Shortlisted",
    statusType: "shortlisted",
    icon: Triangle,
  },
  {
    id: 12,
    company: "Atlassian",
    role: "Senior React Engineer",
    location: "Remote / Hybrid",
    date: "Sep 08, 2024",
    daysAgo: "48 days ago",
    status: "Rejected",
    statusType: "rejected",
    icon: Layers,
  },
];

const STATUS_STYLES = {
  review: {
    className: "bg-surface-high text-primary",
    icon: Hourglass,
  },
  interview: {
    className: "bg-primary/10 text-primary",
    icon: CalendarDays,
  },
  assessment: {
    className: "bg-tertiary-fixed text-tertiary",
    icon: Terminal,
  },
  offer: {
    className: "bg-secondary-container text-primary",
    icon: Star,
  },
  received: {
    className: "bg-surface-container text-on-surface-variant",
    icon: FolderOpen,
  },
  shortlisted: {
    className: "bg-secondary-container text-primary",
    icon: Star,
  },
  rejected: {
    className: "bg-error/10 text-error",
    icon: FolderOpen,
  },
};

function ApplicationStatus({ application }) {
  const config = STATUS_STYLES[application.statusType] || STATUS_STYLES.received;
  const Icon = config.icon;

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold whitespace-nowrap ${config.className}`}
    >
      <Icon size={13} />
      {application.status}
    </span>
  );
}

function CompanyIcon({ application }) {
  const Icon = application.icon;

  return (
    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-surface-low text-primary">
      <Icon size={22} />
    </div>
  );
}

export default function AppliedJobs() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("review");
  const [sort, setSort] = useState("newest");
  const [page, setPage] = useState(1);

  const pageSize = 6;

  const statusCounts = useMemo(() => {
    return {
      review: APPLICATIONS.filter((item) => item.statusType === "review").length,
      shortlisted: APPLICATIONS.filter(
        (item) => item.statusType === "shortlisted"
      ).length,
    };
  }, []);

  const filteredApplications = useMemo(() => {
    let result = [...APPLICATIONS];

    if (statusFilter !== "all") {
      result = result.filter(
        (application) => application.statusType === statusFilter
      );
    }

    const query = search.trim().toLowerCase();

    if (query) {
      result = result.filter((application) =>
        [
          application.company,
          application.role,
          application.location,
          application.status,
        ]
          .join(" ")
          .toLowerCase()
          .includes(query)
      );
    }

    if (sort === "oldest") {
      result.reverse();
    }

    if (sort === "company") {
      result.sort((a, b) => a.company.localeCompare(b.company));
    }

    if (sort === "status") {
      result.sort((a, b) => a.status.localeCompare(b.status));
    }

    return result;
  }, [search, statusFilter, sort]);

  const totalPages = Math.max(
    1,
    Math.ceil(filteredApplications.length / pageSize)
  );

  const currentPage = Math.min(page, totalPages);

  const visibleApplications = filteredApplications.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const handleSearchChange = (event) => {
    setSearch(event.target.value);
    setPage(1);
  };

  const handleStatusChange = (status) => {
    setStatusFilter(status);
    setPage(1);
  };

  return (
    <main className="min-w-0 w-full bg-surface">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 pb-10">
        {/* Page Header */}
        <section className="flex flex-col gap-5 pt-6 sm:pt-8">
          <div>

            <h1 className="text-2xl font-black tracking-tight text-on-surface sm:text-3xl">
              My Applications
            </h1>

            <p className="mt-1 text-sm text-on-surface-variant">
              Track, manage, and prepare for all 12 submitted job applications.
            </p>
          </div>

          {/* KPI Ribbon */}
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="flex flex-col justify-between rounded-xl bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
                  Total Applications
                </span>

                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-surface-container text-on-surface-variant">
                  <FolderOpen size={16} />
                </div>
              </div>

              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-black tracking-tight text-on-surface">
                  12
                </span>
                <span className="text-[11px] font-bold text-secondary">
                  100% active
                </span>
              </div>
            </div>

            <div className="flex flex-col justify-between rounded-xl bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
                  In Review
                </span>

                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-surface-high text-primary">
                  <Hourglass size={16} />
                </div>
              </div>

              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-black tracking-tight text-on-surface">
                  4
                </span>
                <span className="text-[11px] text-on-surface-variant">
                  Avg 3d
                </span>
              </div>
            </div>

            <div className="flex flex-col justify-between rounded-xl bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-outline">
                  Shortlisted
                </span>

                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Star size={16} />
                </div>
              </div>

              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-3xl font-black tracking-tight text-on-surface">
                  3
                </span>
                <span className="text-[11px] font-bold text-secondary">
                  Active rounds
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Filters */}
        <section className="flex flex-col gap-3 rounded-2xl bg-white p-4 shadow-sm lg:flex-row lg:items-center lg:justify-between">
          <div className="flex min-w-0 flex-1 flex-col gap-3 sm:flex-row sm:items-center">
            <div className="relative min-w-0 flex-1 sm:max-w-md">
              <Search
                size={19}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-outline"
              />

              <input
                type="text"
                value={search}
                onChange={handleSearchChange}
                placeholder="Filter by role, company name, or tech stack..."
                className="w-full rounded-xl bg-surface-low py-2.5 pl-10 pr-4 text-sm text-on-surface outline-none placeholder:text-outline focus:bg-white focus:ring-2 focus:ring-primary/20"
              />
            </div>

            <div className="flex gap-1.5 overflow-x-auto pb-1">
            <button
                type="button"
                onClick={() => handleStatusChange("review")}
                className={`whitespace-nowrap rounded-full px-3 py-2 text-xs font-semibold transition-colors ${
                statusFilter === "review"
                    ? "bg-primary text-white"
                    : "bg-surface-low text-on-surface/65 hover:text-on-surface"
                }`}
            >
                Under Review ({statusCounts.review})
            </button>

            <button
                type="button"
                onClick={() => handleStatusChange("shortlisted")}
                className={`whitespace-nowrap rounded-full px-3 py-2 text-xs font-semibold transition-colors ${
                statusFilter === "shortlisted"
                    ? "bg-primary text-white"
                    : "bg-surface-low text-on-surface/65 hover:text-on-surface"
                }`}
            >
                Shortlisted ({statusCounts.shortlisted})
            </button>

            <button
                type="button"
                onClick={() => handleStatusChange("all")}
                className={`whitespace-nowrap rounded-full px-3 py-2 text-xs font-semibold transition-colors ${
                statusFilter === "all"
                    ? "bg-primary text-white"
                    : "bg-surface-low text-on-surface/65 hover:text-on-surface"
                }`}
            >
                All Applications
            </button>
            </div>
          </div>

          <div className="flex items-center gap-2 self-end lg:self-auto">
            <div className="flex items-center rounded-xl bg-surface-low  px-3 py-2">
              <span className="mr-2 text-[11px] font-bold text-outline">
                Sort:
              </span>

              <select
                value={sort}
                onChange={(event) => {
                  setSort(event.target.value);
                  setPage(1);
                }}
                className="max-w-[180px] cursor-pointer bg-transparent text-xs font-bold text-on-surface outline-none"
              >
                <option value="newest">Application Date (Newest)</option>
                <option value="oldest">Application Date (Oldest)</option>
                <option value="company">Company (A-Z)</option>
                <option value="status">Status</option>
              </select>
            </div>

            <button
              type="button"
              className="flex h-9 w-9 items-center justify-center rounded-xl bg-surface-container-low text-on-surface-variant transition-colors hover:bg-surface-container"
              title="Table Preferences"
            >
              <SlidersHorizontal size={17} />
            </button>
          </div>
        </section>

        {/* Applications Table */}
        <section className="overflow-hidden rounded-2xl bg-white shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[850px] border-collapse text-left">
              <thead>
                <tr className="bg-surface-low text-[11px] font-bold uppercase tracking-wider text-outline">
                  <th className="w-1/2 px-5 py-4 font-bold">
                    Company &amp; Role
                  </th>
                  <th className="w-1/4 px-5 py-4 font-bold">Date Applied</th>
                  <th className="w-1/4 px-5 py-4 font-bold">
                    Current Status
                  </th>
                </tr>
              </thead>

              <tbody>
                {visibleApplications.length > 0 ? (
                  visibleApplications.map((application, index) => (
                    <tr
                      key={application.id}
                      className={`group transition-colors hover:bg-surface-container-low/60 ${
                        index % 2 === 1 ?  "bg-surface-low/40" : "bg-surface-bright" 
                      }`}
                    >
                      <td className="px-5 py-4">
                        <button
                          type="button"
                          onClick={() =>
                            navigate(`/candidate/jobs/${application.id}`)
                          }
                          className="flex min-w-0 items-center gap-3 text-left"
                        >
                          <CompanyIcon application={application} />

                          <div className="flex min-w-0 flex-col">
                            <span className="truncate text-sm font-bold text-on-surface transition-colors group-hover:text-primary">
                              {application.role}
                            </span>

                            <div className="flex min-w-0 flex-wrap items-center gap-1.5 text-xs text-on-surface-variant">
                              <span className="font-semibold text-on-surface">
                                {application.company}
                              </span>

                              <span>•</span>

                              <span className="flex items-center gap-1">
                                <Globe size={12} />
                                {application.location}
                              </span>
                            </div>
                          </div>
                        </button>
                      </td>

                      <td className="whitespace-nowrap px-5 py-4">
                        <span className="text-sm font-semibold text-on-surface">
                          {application.date}
                        </span>
                        <p className="mt-0.5 text-xs text-outline">
                          {application.daysAgo}
                        </p>
                      </td>

                      <td className="whitespace-nowrap px-5 py-4">
                        <ApplicationStatus application={application} />
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan="3"
                      className="px-5 py-16 text-center text-sm text-on-surface-variant"
                    >
                      No applications match your current filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex flex-col items-center justify-between gap-3 border-t border-surface-container-low bg-white p-4 sm:flex-row">
            <p className="text-xs text-on-surface-variant">
              Showing{" "}
              <span className="font-bold text-on-surface">
                {filteredApplications.length === 0
                  ? 0
                  : (currentPage - 1) * pageSize + 1}
                -
                {Math.min(currentPage * pageSize, filteredApplications.length)}
              </span>{" "}
              of{" "}
              <span className="font-bold text-on-surface">
                {filteredApplications.length}
              </span>{" "}
              applications
            </p>

            <div className="flex items-center gap-1">
              <button
                type="button"
                disabled={currentPage === 1}
                onClick={() => setPage((value) => Math.max(1, value - 1))}
                className="flex h-8 w-8 items-center justify-center rounded-lg bg-surface-container-low text-outline transition-colors hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-50"
              >
                <ChevronLeft size={17} />
              </button>

              {Array.from({ length: totalPages }, (_, index) => index + 1).map(
                (pageNumber) => (
                  <button
                    key={pageNumber}
                    type="button"
                    onClick={() => setPage(pageNumber)}
                    className={`flex h-8 w-8 items-center justify-center rounded-lg text-xs font-bold transition-colors ${
                      currentPage === pageNumber
                        ? "bg-primary text-white"
                        : "text-on-surface hover:bg-surface-container"
                    }`}
                  >
                    {pageNumber}
                  </button>
                )
              )}

              <button
                type="button"
                disabled={currentPage === totalPages}
                onClick={() =>
                  setPage((value) => Math.min(totalPages, value + 1))
                }
                className="flex h-8 w-8 items-center justify-center rounded-lg text-on-surface transition-colors hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-50"
              >
                <ChevronRight size={17} />
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}