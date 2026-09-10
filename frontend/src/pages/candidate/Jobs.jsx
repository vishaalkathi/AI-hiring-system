import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  Clock3,
  MapPin,
  DollarSign,
  Sparkles,
  Bookmark,
  RefreshCw,
  Send,
  ChevronDown,
} from "lucide-react";

const JOBS = [
  {
    id: 1,
    company: "Datadog",
    title: "Staff Frontend Engineer – Core Platform",
    match: 96,
    mode: "Remote",
    posted: "2h ago",
    location: "Remote (US/CA)",
    salary: "$210k – $255k",
    salaryMin: 210,
    experience: "Staff / Principal (8+ yrs)",
    description:
      "Architect high-throughput observability canvas rendering real-time streaming time-series metrics at 60 FPS.",
    skills: ["React 19", "TypeScript", "WebGL", "Perf Opt"],
    icon: "D",
  },
  {
    id: 2,
    company: "Scale AI",
    title: "Senior Fullstack AI Engineer",
    match: 92,
    mode: "Hybrid",
    posted: "5h ago",
    location: "San Francisco (Hybrid)",
    salary: "$195k – $235k",
    salaryMin: 195,
    experience: "Senior (5+ yrs)",
    description:
      "Build generative AI evaluation interfaces and production agent workflows that accelerate foundational model training.",
    skills: ["Next.js", "Python", "LangChain", "PostgreSQL"],
    icon: "S",
  },
  {
    id: 3,
    company: "Monzo",
    title: "Lead React Native Developer – FinTech",
    match: 89,
    mode: "Remote",
    posted: "1d ago",
    location: "Remote (US/UK)",
    salary: "$185k – $220k",
    salaryMin: 185,
    experience: "Lead / Director",
    description:
      "Lead mobile frontend craftsmanship on zero-latency payment flows and biometric banking security used by 9M+ users.",
    skills: ["React Native", "TypeScript", "iOS / Swift", "Micro-frontends"],
    icon: "M",
  },
  {
    id: 4,
    company: "Notion",
    title: "Senior UI/UX Design Technologist",
    match: 94,
    mode: "Hybrid",
    posted: "2d ago",
    location: "New York (Hybrid)",
    salary: "$190k – $230k",
    salaryMin: 190,
    experience: "Senior (5+ yrs)",
    description:
      "Bridge interaction design and design tokens across Notion’s modular collaborative workspace ecosystem.",
    skills: ["Framer Motion", "React", "Design Tokens", "a11y"],
    icon: "N",
  },
];

const EXPERIENCE_OPTIONS = [
  "All Experience",
  "Senior (5+ yrs)",
  "Staff / Principal (8+ yrs)",
  "Lead / Director",
];

const SALARY_OPTIONS = [
  "Any Compensation",
  "$140k – $180k",
  "$180k – $240k+",
  "$240k+",
];

function JobCard({ job, bookmarked, onBookmark, onApply, onReadMore }) {
  return (
    <article
      className="
        min-w-0 overflow-hidden rounded-2xl
        border border-outline/10
        bg-white
        p-4
        shadow-sm
        transition-all duration-200
        hover:-translate-y-0.5 hover:shadow-md
        sm:p-5
      "
    >
      {/* Company + Match */}
      <div className="flex min-w-0 items-start justify-between gap-3">
        <div className="flex min-w-0 items-center gap-3">
          <div
            className="
              flex h-10 w-10 shrink-0 items-center justify-center
              rounded-xl bg-primary/10
              text-base font-bold text-primary
            "
          >
            {job.icon}
          </div>

          <div className="min-w-0">
            <p className="truncate text-sm font-bold text-on-surface">
              {job.company}
            </p>

            <div className="mt-0.5 flex items-center gap-1 text-xs text-on-surface/50">
              <Clock3 size={12} />
              <span>{job.posted}</span>
            </div>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-1.5">
          <span
            className="
              flex items-center gap-1 rounded-full
              bg-secondary/10 px-2 py-1.5
              text-[11px] font-bold text-secondary
            "
          >
            <Sparkles size={11} />
            {job.match}%
          </span>

          <button
            onClick={() => onBookmark(job.id)}
            className={`
              flex h-8 w-8 items-center justify-center rounded-lg
              transition-colors
              ${
                bookmarked
                  ? "bg-primary/10 text-primary"
                  : "text-on-surface/40 hover:bg-surface-low hover:text-on-surface"
              }
            `}
            aria-label={
              bookmarked
                ? `Remove ${job.title} bookmark`
                : `Bookmark ${job.title}`
            }
          >
            <Bookmark
              size={17}
              fill={bookmarked ? "currentColor" : "none"}
            />
          </button>
        </div>
      </div>

      {/* Title */}
      <h2
        className="
          mt-4
          break-words
          text-base font-bold leading-snug
          text-on-surface
          sm:text-lg
        "
      >
        {job.title}
      </h2>

      {/* Location + Salary */}
      <div className="mt-2.5 flex flex-wrap items-center gap-x-3 gap-y-1.5 text-xs text-on-surface/60">
        <span className="flex min-w-0 items-center gap-1.5">
          <MapPin size={14} className="shrink-0" />
          <span className="break-words">{job.location}</span>
        </span>

        <span className="flex items-center gap-1.5">
          <DollarSign size={14} className="shrink-0" />
          {job.salary}
        </span>
      </div>

      {/* Description */}
      <p className="mt-3 line-clamp-2 text-xs leading-5 text-on-surface/65 sm:text-sm sm:leading-6">
        {job.description}
      </p>

      {/* Skills */}
      <div className="mt-4 flex flex-wrap gap-1.5">
        {job.skills.map((skill) => (
          <span
            key={skill}
            className="
              rounded-lg bg-surface-low
              px-2 py-1
              text-[10px] font-semibold text-on-surface/70
              sm:text-xs
            "
          >
            {skill}
          </span>
        ))}
      </div>

      {/* Actions */}
      <div className="mt-5 flex gap-2">
        <button
          onClick={() => onReadMore(job)}
          className="
            flex min-w-0 flex-1 items-center justify-center
            rounded-xl border border-outline/15
            px-3 py-2.5
            text-xs font-semibold text-on-surface
            transition-colors
            hover:bg-surface-low
            sm:text-sm
          "
        >
          Read More
        </button>

        <button
          onClick={() => onApply(job)}
          className="
            flex min-w-0 flex-1 items-center justify-center gap-1.5
            rounded-xl bg-primary
            px-3 py-2.5
            text-xs font-bold text-white
            transition-colors
            hover:bg-primary-container
            sm:text-sm
          "
        >
          Apply
          <Send size={14} />
        </button>
      </div>
    </article>
  );
}

function SelectControl({ value, options, onChange }) {
  return (
    <div className="relative min-w-0 flex-1">
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="
          h-10 w-full appearance-none
          rounded-xl
          border border-outline/10
          bg-surface-low
          px-3 pr-8
          text-xs font-medium text-on-surface
          outline-none
          focus:border-primary/30
          focus:ring-2 focus:ring-primary/10
        "
      >
        {options.map((option) => (
          <option key={option}>{option}</option>
        ))}
      </select>

      <ChevronDown
        size={15}
        className="
          pointer-events-none
          absolute right-3 top-1/2
          -translate-y-1/2
          text-on-surface/50
        "
      />
    </div>
  );
}

export default function Jobs() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [experience, setExperience] = useState("All Experience");
  const [salary, setSalary] = useState("Any Compensation");
  const [minMatch, setMinMatch] = useState(85);
  const [workMode, setWorkMode] = useState("All Modes");
  const [sortBy, setSortBy] = useState("Highest AI Relevance");
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);

  const filteredJobs = useMemo(() => {
    let result = JOBS.filter((job) => {
      const searchText = search.trim().toLowerCase();

      const matchesSearch =
        !searchText ||
        [
          job.company,
          job.title,
          job.location,
          job.description,
          ...job.skills,
        ]
          .join(" ")
          .toLowerCase()
          .includes(searchText);

      const matchesExperience =
        experience === "All Experience" ||
        job.experience === experience;

      const matchesSalary =
        salary === "Any Compensation" ||
        (salary === "$140k – $180k" &&
          job.salaryMin >= 140 &&
          job.salaryMin < 180) ||
        (salary === "$180k – $240k+" &&
          job.salaryMin >= 180 &&
          job.salaryMin < 240) ||
        (salary === "$240k+" && job.salaryMin >= 240);

      const matchesMatch = job.match >= minMatch;

      const matchesMode =
        workMode === "All Modes" ||
        (workMode === "90%+ AI Match Only" && job.match >= 90) ||
        job.mode === workMode.replace("Fully ", "");

      return (
        matchesSearch &&
        matchesExperience &&
        matchesSalary &&
        matchesMatch &&
        matchesMode
      );
    });

    if (sortBy === "Highest AI Relevance") {
      result.sort((a, b) => b.match - a.match);
    }

    if (sortBy === "Newest") {
      result.sort((a, b) => a.id - b.id);
    }

    if (sortBy === "Highest Salary") {
      result.sort((a, b) => b.salaryMin - a.salaryMin);
    }

    return result;
  }, [
    search,
    experience,
    salary,
    minMatch,
    workMode,
    sortBy,
  ]);

  const toggleBookmark = (jobId) => {
    setBookmarkedJobs((current) =>
      current.includes(jobId)
        ? current.filter((id) => id !== jobId)
        : [...current, jobId]
    );
  };

  const handleApply = (job) => {
    navigate(`/candidate/jobs/${job.id}/apply`);
  };

  const handleReadMore = (job) => {
    navigate(`/candidate/jobs/${job.id}`);
  };

  const resetFilters = () => {
    setSearch("");
    setExperience("All Experience");
    setSalary("Any Compensation");
    setMinMatch(85);
    setWorkMode("All Modes");
    setSortBy("Highest AI Relevance");
  };

  return (
    <div className="mx-auto w-full max-w-7xl pb-12">
      {/* Page Header */}
      <section className="pt-6 sm:pt-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div className="min-w-0">
            <h1 className="text-2xl font-bold tracking-tight text-on-surface sm:text-3xl">
              Explore Job Openings
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-on-surface/60 sm:text-base">
              Curated opportunities tailored directly to your verified
              skills, salary preferences, and career trajectory goals.
            </p>
          </div>

          <button
            onClick={resetFilters}
            className="
              flex shrink-0 items-center justify-center gap-2
              rounded-xl border border-outline/15
              bg-white
              px-4 py-2.5
              text-sm font-semibold text-on-surface
              hover:bg-surface-low
            "
          >
            <RefreshCw size={16} />
            Reset Filters
          </button>
        </div>
      </section>

      {/* Compact Filters */}
      <section
        className="
          mt-6 rounded-2xl
          border border-outline/10
          bg-white
          p-4 shadow-sm
        "
      >
        {/* Primary Filters */}
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
          {/* Search */}
          <div className="relative min-w-0 flex-1">
            <Search
              size={17}
              className="
                absolute left-3.5 top-1/2
                -translate-y-1/2
                text-on-surface/35
              "
            />

            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search roles, skills, or companies..."
              className="
                h-10 w-full
                rounded-xl
                bg-surface-low
                pl-10 pr-4
                text-xs text-on-surface
                outline-none
                placeholder:text-on-surface/40
                focus:ring-2 focus:ring-primary/15
                sm:text-sm
              "
            />
          </div>

          {/* Experience */}
          <div className="w-full lg:w-44">
            <SelectControl
              value={experience}
              options={EXPERIENCE_OPTIONS}
              onChange={setExperience}
            />
          </div>

          {/* Salary */}
          <div className="w-full lg:w-44">
            <SelectControl
              value={salary}
              options={SALARY_OPTIONS}
              onChange={setSalary}
            />
          </div>

          {/* Sort */}
          <div className="w-full lg:w-48">
            <SelectControl
              value={sortBy}
              options={[
                "Highest AI Relevance",
                "Newest",
                "Highest Salary",
              ]}
              onChange={setSortBy}
            />
          </div>
        </div>

        {/* Secondary Filters */}
        <div
          className="
            mt-3 flex flex-col gap-4
            border-t border-outline/10
            pt-3
            lg:flex-row lg:items-center
          "
        >
          {/* Match Slider */}
          <div className="min-w-0 lg:flex-1">
            <div className="flex items-center justify-between gap-3">
              <label
                htmlFor="match-threshold"
                className="text-xs font-semibold text-on-surface"
              >
                Match Threshold
              </label>

              <span className="text-xs font-bold text-primary">
                {minMatch}%+
              </span>
            </div>

            <input
              id="match-threshold"
              type="range"
              min="70"
              max="98"
              value={minMatch}
              onChange={(event) =>
                setMinMatch(Number(event.target.value))
              }
              className="mt-1.5 w-full accent-primary"
            />

            <div className="flex justify-between text-[10px] text-on-surface/35">
              <span>70%</span>
              <span>98%</span>
            </div>
          </div>

          {/* Work Modes */}
          <div className="min-w-0 lg:flex-[1.8]">
            <p className="mb-1.5 text-xs font-semibold text-on-surface">
              Work Mode
            </p>

            <div className="flex flex-wrap gap-1.5">
              {[
                "All Modes",
                "Fully Remote",
                "Hybrid",
                "90%+ AI Match Only",
              ].map((mode) => {
                const active = workMode === mode;

                return (
                  <button
                    key={mode}
                    onClick={() => setWorkMode(mode)}
                    className={`
                      rounded-full
                      px-3 py-1.5
                      text-[11px] font-semibold
                      transition-colors
                      ${
                        active
                          ? "bg-primary text-white"
                          : "bg-surface-low text-on-surface/65 hover:text-on-surface"
                      }
                    `}
                  >
                    {mode}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Reset */}
          <button
            onClick={resetFilters}
            className="
              flex shrink-0 items-center justify-center gap-2
              rounded-xl
              border border-outline/10
              px-3.5 py-2
              text-xs font-semibold text-on-surface/65
              hover:bg-surface-low hover:text-on-surface
              lg:self-end
            "
          >
            <RefreshCw size={14} />
            Reset
          </button>
        </div>
      </section>

      {/* Result Summary */}
      <div className="mt-6 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-bold text-on-surface">
            Recommended Roles
          </p>

          <p className="mt-1 text-xs text-on-surface/50">
            {filteredJobs.length} high-confidence match
            {filteredJobs.length !== 1 ? "es" : ""}
          </p>
        </div>

        <span className="hidden text-xs font-medium text-on-surface/45 sm:block">
          Sorting by: {sortBy}
        </span>
      </div>

      {/* Job Feed */}
      {filteredJobs.length > 0 ? (
        <section
          className="
            mt-4 grid min-w-0
            grid-cols-1 gap-4
            sm:grid-cols-2
            xl:grid-cols-3
          "
        >
          {filteredJobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              bookmarked={bookmarkedJobs.includes(job.id)}
              onBookmark={toggleBookmark}
              onApply={handleApply}
              onReadMore={handleReadMore}
            />
          ))}
        </section>
      ) : (
        <div
          className="
            mt-4 rounded-2xl
            border border-dashed border-outline/20
            bg-white
            px-6 py-14
            text-center
          "
        >
          <div
            className="
              mx-auto flex h-12 w-12
              items-center justify-center
              rounded-full bg-surface-low
            "
          >
            <Search size={21} className="text-on-surface/45" />
          </div>

          <h3 className="mt-4 text-base font-bold text-on-surface">
            No matching jobs
          </h3>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-on-surface/55">
            Try lowering your match threshold or changing one of the
            filters.
          </p>
        </div>
      )}

      {/* Bottom Summary */}
      <section
        className="
          mt-6 flex flex-col gap-4
          rounded-2xl
          bg-primary/5
          p-4
          sm:flex-row sm:items-center sm:justify-between
          sm:p-5
        "
      >
        <div className="flex min-w-0 items-start gap-3">
          <span className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full bg-secondary" />

          <p className="text-sm leading-6 text-on-surface/70">
            Showing{" "}
            <span className="font-bold text-on-surface">
              {filteredJobs.length}
            </span>{" "}
            of 42 high-confidence recommendations tailored for Alex Carter
          </p>
        </div>

        <div className="flex flex-col gap-2 sm:flex-row">
          <button
            onClick={resetFilters}
            className="
              flex items-center justify-center gap-2
              rounded-xl
              px-4 py-2.5
              text-sm font-semibold text-primary
              hover:bg-primary/10
            "
          >
            <RefreshCw size={15} />
            Refresh Feed
          </button>

          <button
            className="
              rounded-xl bg-primary
              px-4 py-2.5
              text-sm font-bold text-white
              hover:bg-primary-container
            "
          >
            Load Next 10 Roles
          </button>
        </div>
      </section>
    </div>
  );
}
