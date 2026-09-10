import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";

import ProtectedRoute from "./components/ProtectedRoute";

import CandidateLayout from "./layouts/CandidateLayout";
import RecruiterLayout from "./layouts/RecruiterLayout";
import ScrollToTop from "./components/ScrollToTop";

import Settings from "./pages/Settings";

import CandidateDashboard from "./pages/candidate/CandidateDashboard";
import RecruiterDashboard from "./pages/recruiter/RecruiterDashboard";

import Jobs from "./pages/candidate/Jobs";
import JobApplication from "./pages/candidate/JobApplication";
import JobDetails from "./pages/candidate/JobDetails";
import AppliedJobs from "./pages/candidate/AppliedJobs";
import Profile from "./pages/candidate/Profile";

import JobsCreated from "./pages/recruiter/JobsCreated";


export default function App() {
    return (
        <>
        <ScrollToTop />
        <Routes>
            {/* Default route */}
            <Route
                path="/"
                element={<Navigate to="/login" replace />}
            />

            {/* Public routes */}

            <Route
                path="/login"
                element={<Login />}
            />

            <Route
                path="/register"
                element={<Register />}
            />


            {/* Candidate routes */}

            <Route
                element={
                    <ProtectedRoute allowedRole="CANDIDATE" />
                }
            >
                <Route
                    element={<CandidateLayout />}
                >
                    <Route
                        path="/candidate/dashboard"
                        element={<CandidateDashboard />}
                    />
                    
                    <Route
                        path="/candidate/jobs"
                        element={<Jobs />}
                    />

                    <Route
                        path="/candidate/jobs/:id"
                        element={<JobDetails />}
                    />

                    <Route
                        path="/candidate/applied"
                        element={<AppliedJobs />}
                    />

                    <Route
                        path="/candidate/profile"
                        element={<Profile />}
                    />

                    <Route 
                        path="/candidate/jobs/:id/apply" 
                        element={<JobApplication />} 
                    />
                    <Route 
                        path="/candidate/settings" 
                        element={<Settings />} 
                    />
                </Route>
            </Route>


            {/* Recruiter routes */}

            <Route
                element={
                    <ProtectedRoute allowedRole="EMPLOYER" />
                }
            >
                <Route element={<RecruiterLayout />}>
                    <Route
                        path="/employer/dashboard"
                        element={<RecruiterDashboard />}
                    />
                    <Route
                        path="/employer/jobs"
                        element={<JobsCreated />}
                    />
                    <Route 
                        path="/employer/settings" 
                        element={<Settings />} 
                    />
                </Route>
            </Route>

        </Routes>
        </>
    );
}