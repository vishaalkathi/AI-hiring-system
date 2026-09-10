import {
    ArrowRight,
    BriefcaseBusiness,
    CheckCircle2,
    ChevronRight,
    Edit3,
    Filter,
    Plus,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const jobs = [
    {
        id: 1,
        title: "Lead React Engineer",
        type: "Full-time",
        location: "Remote (US)",
        salary: "$140k - $165k",
        posted: "4d ago",
        applicants: 38,
        newApplicants: 12,
        shortlisted: 6,
    },
    {
        id: 2,
        title: "Senior Fullstack AI Engineer",
        type: "Full-time",
        location: "SF (Hybrid)",
        salary: "$195k - $235k",
        posted: "1w ago",
        applicants: 54,
        newApplicants: 18,
        shortlisted: 10,
    },
    {
        id: 3,
        title: "Staff Frontend Architect",
        type: "Full-time",
        location: "Remote (US/CA)",
        salary: "$210k - $255k",
        posted: "2w ago",
        applicants: 26,
        newApplicants: 4,
        shortlisted: 8,
    },
];

const applications = [
    {
        id: 1,
        name: "Alex Carter",
        email: "alex.carter@example.com",
        initials: "AC",
        role: "Lead React Engineer",
        match: 98,
        date: "Oct 24, 2024",
    },
    {
        id: 2,
        name: "Maya Lin",
        email: "maya.lin@domain.io",
        initials: "ML",
        role: "Senior Fullstack AI Engineer",
        match: 94,
        date: "Oct 23, 2024",
    },
    {
        id: 3,
        name: "David Kim",
        email: "david.kim@network.com",
        initials: "DK",
        role: "Staff Frontend Architect",
        match: 91,
        date: "Oct 22, 2024",
    },
    {
        id: 4,
        name: "Elena Rostova",
        email: "elena.rostova@devmail.org",
        initials: "ER",
        role: "Lead React Engineer",
        match: 89,
        date: "Oct 21, 2024",
    },
    {
        id: 5,
        name: "Jordan Hayes",
        email: "jordan.hayes@vector.co",
        initials: "JH",
        role: "Senior Fullstack AI Engineer",
        match: 96,
        date: "Oct 20, 2024",
    },
];

function JobCard({ job, onViewApplications, onEdit }) {
    return (
        <div
            className="
                group flex min-w-0 flex-col
                rounded-xl bg-white p-4
                shadow-sm
                transition-all duration-300
                hover:-translate-y-0.5 hover:shadow-md
                sm:p-5
            "
        >
            {/* Main content */}
            <div className="min-w-0 flex-1">
                {/* Header */}
                <div className="flex min-w-0 items-start justify-between gap-3">
                    {/* Job identity */}
                    <div className="flex min-w-0 items-start gap-3 sm:gap-4">
                        <div
                            className="
                                flex h-11 w-11 shrink-0
                                items-center justify-center
                                rounded-xl
                                bg-surface-low
                                text-primary
                                sm:h-12 sm:w-12
                            "
                        >
                            <BriefcaseBusiness size={22} />
                        </div>

                        <div className="min-w-0 flex-1">
                            <h3
                                className="
                                    break-words
                                    text-[18px] leading-6
                                    font-semibold
                                    text-on-surface
                                    transition-colors
                                    group-hover:text-primary
                                    sm:text-[20px] sm:leading-7
                                "
                            >
                                {job.title}
                            </h3>

                            <p
                                className="
                                    mt-0.5
                                    break-words
                                    text-sm
                                    text-outline
                                "
                            >
                                {job.type} • {job.location}
                            </p>
                        </div>
                    </div>

                    {/* Active status */}
                    <span
                        className="
                            flex w-fit shrink-0
                            items-center gap-1
                            rounded-full
                            border border-[#ccfbf1]
                            bg-[#e6f7f5]
                            px-2 py-1
                            text-[10px]
                            font-bold
                            text-[#0f766e]
                        "
                    >
                        <CheckCircle2 size={13} />
                        Active
                    </span>
                </div>

                {/* Salary */}
                <div className="mt-4">
                    <span
                        className="
                            inline-flex
                            rounded-lg
                            bg-surface-low
                            px-3 py-1.5
                            text-[11px]
                            font-semibold
                            text-on-surface
                        "
                    >
                        {job.salary}
                    </span>
                </div>

                {/* Application stats */}
                <div className="mt-4 flex min-w-0 flex-wrap gap-2">
                    {/* Applicants */}
                    <div
                        className="
                            flex items-center gap-1.5
                            rounded-lg
                            bg-surface-low
                            px-2.5 py-1.5
                            text-xs
                        "
                    >
                        <span className="font-bold text-on-surface">
                            {job.applicants}
                        </span>

                        <span className="text-outline">
                            Applicants
                        </span>

                        <span
                            className="
                                ml-1 rounded-full
                                bg-[#e6f7f5]
                                px-1.5 py-0.5
                                text-[10px] font-bold
                                text-[#0f766e]
                            "
                        >
                            +{job.newApplicants} new
                        </span>
                    </div>

                    {/* Shortlisted */}
                    <div
                        className="
                            flex items-center gap-1.5
                            rounded-lg
                            bg-surface-low
                            px-2.5 py-1.5
                            text-xs
                        "
                    >
                        <span className="font-bold text-primary">
                            {job.shortlisted}
                        </span>

                        <span className="text-outline">
                            Shortlisted
                        </span>
                    </div>
                </div>
            </div>

            {/* Buttons */}
            <div
                className="
                    mt-5 flex
                    items-center justify-between
                    border-t border-outline/10
                    pt-4
                "
            >
                <button
                    type="button"
                    onClick={() => onViewApplications(job.id)}
                    className="flex w-full
                        items-center
                        justify-center
                        gap-2
                        rounded-xl
                        bg-[#00685f]
                        px-5 py-2
                        text-[13px]
                        font-semibold
                        text-white
                        shadow-sm
                        transition-colors
                        hover:bg-[#008378]
                        sm:w-auto"
                >
                    View Applications
                    <ChevronRight size={16} />
                </button>

                <button
                    type="button"
                    onClick={() => onEdit(job.id)}
                    className="
                        rounded-lg p-1.5
                        text-outline
                        transition-colors
                        hover:bg-surface-low
                        hover:text-on-surface
                    "
                    title="Edit Post"
                >
                    <Edit3 size={17} />
                </button>
            </div>
        </div>
    );
}

function ApplicationRow({ application, onReview }) {
    return (
        <tr
            className="
                transition-colors
                odd:bg-white
                even:bg-surface-low/40
                hover:bg-surface-low/70
            "
        >
            <td className="px-5 py-4 sm:px-6">
                <div className="flex min-w-0 items-center gap-3">
                    <div
                        className="
                            flex h-10 w-10 shrink-0
                            items-center justify-center
                            rounded-full
                            bg-surface-low
                            text-sm font-bold
                            text-primary
                        "
                    >
                        {application.initials}
                    </div>

                    <div className="flex min-w-0 flex-col">
                        <span
                            className="
                                truncate
                                text-sm font-semibold
                                text-on-surface
                            "
                        >
                            {application.name}
                        </span>

                        <span
                            className="
                                truncate
                                text-xs
                                text-outline
                            "
                        >
                            {application.email}
                        </span>
                    </div>
                </div>
            </td>

            <td
                className="
                    px-5 py-4
                    text-sm font-semibold
                    text-on-surface
                    sm:px-6
                "
            >
                {application.role}
            </td>

            <td className="px-5 py-4 sm:px-6">
                <span
                    className="
                        inline-flex items-center gap-1
                        rounded-full
                        border border-[#ccfbf1]
                        bg-[#e6f7f5]
                        px-2.5 py-1
                        text-xs font-semibold
                        text-[#0f766e]
                    "
                >
                    <CheckCircle2 size={14} />
                    {application.match}% Match
                </span>
            </td>

            <td
                className="
                    whitespace-nowrap
                    px-5 py-4
                    text-xs
                    text-outline
                    sm:px-6
                "
            >
                {application.date}
            </td>

            <td className="px-5 py-4 text-right sm:px-6">
                <button
                    type="button"
                    onClick={() => onReview(application.id)}
                    className="
                        rounded-full
                        bg-surface-low
                        px-4 py-2
                        text-xs font-semibold
                        text-on-surface
                        transition-colors
                        hover:bg-surface-high
                    "
                >
                    Review
                </button>
            </td>
        </tr>
    );
}

export default function RecruiterDashboard() {
    const navigate = useNavigate();

    const handlePostJob = () => {
        navigate("/recruiter/jobs/new");
    };

    const handleViewApplications = (jobId) => {
        navigate(`/recruiter/jobs/${jobId}/applications`);
    };

    const handleEditJob = (jobId) => {
        navigate(`/recruiter/jobs/${jobId}/edit`);
    };

    const handleReviewApplication = (applicationId) => {
        navigate(`/recruiter/applications/${applicationId}`);
    };

    return (
        <main
            className="
                relative min-h-screen
                w-full min-w-0
                bg-surface
            "
        >
            <div
                className="
                    flex w-full min-w-0
                    flex-col
                    pb-10
                "
            >
                {/* Header */}
                <div
                    className="
                        flex flex-col lg:flex-row lg:items-center justify-between gap-4 pt-6 mb-8
                    "
                >
                    <div>
                        <h1
                            className="
                                text-2xl font-bold
                                tracking-tight
                                text-on-surface
                                sm:text-[28px]
                            "
                        >
                            Welcome back, Sarah 👋
                        </h1>

                        <p
                            className="
                                mt-1 text-sm
                                text-outline
                            "
                        >
                            Here is what your hiring pipeline and job
                            postings look like today.
                        </p>
                    </div>
                </div>

                {/* Jobs Created */}
                <section className="flex flex-col gap-4">
                    <div
                        className="
                            flex items-center
                            justify-between gap-3
                        "
                    >
                        <div className="flex items-center gap-2">
                            <h2
                                className="
                                    text-xl font-bold
                                    text-on-surface
                                "
                            >
                                Jobs Created
                            </h2>

                            <span
                                className="
                                    rounded-full
                                    bg-surface-high
                                    px-2 py-0.5
                                    text-[11px] font-bold
                                    text-on-surface
                                "
                            >
                                8 Live
                            </span>
                        </div>

                        <button
                            type="button"
                            onClick={() => navigate("/recruiter/jobs")}
                            className="
                                group inline-flex
                                items-center gap-1
                                text-sm font-semibold
                                text-primary
                                transition-colors
                                hover:text-primary-container
                            "
                        >
                            View All (8)

                            <ArrowRight
                                size={17}
                                className="
                                    transition-transform
                                    group-hover:translate-x-1
                                "
                            />
                        </button>
                    </div>

                    <div
                        className="
                            grid grid-cols-1 gap-5
                            md:grid-cols-2
                            xl:grid-cols-3
                        "
                    >
                        {jobs.map((job) => (
                            <JobCard
                                key={job.id}
                                job={job}
                                onViewApplications={
                                    handleViewApplications
                                }
                                onEdit={handleEditJob}
                            />
                        ))}
                    </div>
                </section>

                {/* New Applications */}
                <section className="flex flex-col mt-10">
                    <div
                        className="
                            flex items-center justify-between mb-5
                        "
                    >
                        <div className="flex items-center gap-2">
                            <h2
                                className="
                                    text-xl font-bold
                                    text-on-surface
                                "
                            >
                                New Applications
                            </h2>

                            <span
                                className="
                                    rounded-full
                                    bg-surface-low
                                    px-2 py-0.5
                                    text-[11px] font-bold
                                    text-primary
                                "
                            >
                                5 Recent
                            </span>
                        </div>

                        <button
                            type="button"
                            onClick={() =>
                                navigate("/recruiter/applications")
                            }
                            className="
                                group inline-flex
                                items-center gap-1
                                text-sm font-semibold
                                text-primary
                                transition-colors
                                hover:text-primary-container
                            "
                        >
                            Manage Applications

                            <ArrowRight
                                size={17}
                                className="
                                    transition-transform
                                    group-hover:translate-x-1
                                "
                            />
                        </button>
                    </div>

                    <div
                        className="
                            overflow-hidden
                            rounded-xl
                            bg-white
                            shadow-sm
                        "
                    >
                        <div className="overflow-x-auto">
                            <table
                                className="
                                    w-full min-w-[760px]
                                    border-collapse
                                    text-left
                                "
                            >
                                <thead>
                                    <tr
                                        className="
                                            bg-surface-low
                                            text-[11px]
                                            font-bold
                                            uppercase
                                            tracking-wider
                                            text-outline
                                        "
                                    >
                                        <th className="px-5 py-3.5 sm:px-6">
                                            Candidate
                                        </th>

                                        <th className="px-5 py-3.5 sm:px-6">
                                            Target Role
                                        </th>

                                        <th className="px-5 py-3.5 sm:px-6">
                                            AI Match
                                        </th>

                                        <th className="px-5 py-3.5 sm:px-6">
                                            Applied Date
                                        </th>

                                        <th className="px-5 py-3.5 text-right sm:px-6">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {applications.map((application) => (
                                        <ApplicationRow
                                            key={application.id}
                                            application={application}
                                            onReview={
                                                handleReviewApplication
                                            }
                                        />
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>
            </div>
        </main>
    );
}