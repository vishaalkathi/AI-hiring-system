import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    ArrowRight,
    Check,
    Eye,
    EyeOff,
    LockKeyhole,
    Mail,
    ShieldCheck,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [rememberMe, setRememberMe] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            const user = await login(email, password);

            if (user.role === "CANDIDATE") {
                navigate("/candidate/dashboard");
            } else if (user.role === "EMPLOYER") {
                navigate("/employer/dashboard");
            } else {
                navigate("/");
            }
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Login failed. Please check your credentials."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-surface px-4 py-8 sm:px-6">

            {/* Background decoration */}
            <div className="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-primary/10 blur-3xl" />

            <div className="pointer-events-none absolute -bottom-32 -right-32 h-80 w-80 rounded-full bg-tertiary/10 blur-3xl" />

            <div className="relative w-full max-w-md">

                {/* Login Card */}
                <div className="rounded-2xl bg-white p-6 shadow-sm sm:p-8">

                    {/* Logo + Heading */}
                    <div className="flex flex-col items-center text-center">

                        <div className="relative mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-surface-low">
                            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-lg font-bold text-white">
                                H
                            </div>

                            <span className="absolute -right-1 -top-1 h-3.5 w-3.5 rounded-full bg-primary-container ring-2 ring-white">
                                <span className="absolute inset-1 rounded-full bg-white" />
                            </span>
                        </div>

                        <h1 className="text-2xl font-bold tracking-tight text-on-surface">
                            Sign in to your account
                        </h1>

                        <p className="mt-2 max-w-sm text-sm leading-6 text-on-surface-variant">
                            Welcome back. Enter your credentials to access your
                            talent dashboard.
                        </p>
                    </div>

                    {/* Form */}
                    <form
                        onSubmit={handleSubmit}
                        className="mt-7 flex flex-col gap-5"
                    >

                        {/* Email */}
                        <div>
                            <label
                                htmlFor="email"
                                className="mb-1.5 block text-xs font-bold text-on-surface"
                            >
                                Email Address
                            </label>

                            <div className="relative">
                                <Mail
                                    size={17}
                                    className="absolute left-3.5 top-1/2 -translate-y-1/2 text-outline"
                                />

                                <input
                                    id="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => {
                                        setEmail(e.target.value);
                                        setError("");
                                    }}
                                    placeholder="alex.carter@company.com"
                                    required
                                    className="
                                        w-full rounded-lg
                                        bg-surface-low
                                        py-2.5 pl-10 pr-4
                                        text-sm text-on-surface
                                        outline-none
                                        transition-all
                                        placeholder:text-outline
                                        focus:ring-2
                                        focus:ring-primary/25
                                    "
                                />
                            </div>
                        </div>

                        {/* Password */}
                        <div>
                            <label
                                htmlFor="password"
                                className="mb-1.5 block text-xs font-bold text-on-surface"
                            >
                                Password
                            </label>

                            <div className="relative">
                                <LockKeyhole
                                    size={17}
                                    className="absolute left-3.5 top-1/2 -translate-y-1/2 text-outline"
                                />

                                <input
                                    id="password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    value={password}
                                    onChange={(e) => {
                                        setPassword(e.target.value);
                                        setError("");
                                    }}
                                    placeholder="••••••••••••"
                                    required
                                    className="
                                        w-full rounded-lg
                                        bg-surface-low
                                        py-2.5 pl-10 pr-11
                                        text-sm text-on-surface
                                        outline-none
                                        transition-all
                                        placeholder:text-outline
                                        focus:ring-2
                                        focus:ring-primary/25
                                    "
                                />

                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowPassword(
                                            (visible) => !visible
                                        )
                                    }
                                    className="
                                        absolute right-2 top-1/2
                                        -translate-y-1/2
                                        rounded-lg p-1.5
                                        text-outline
                                        transition-colors
                                        hover:bg-surface-high
                                        hover:text-on-surface
                                    "
                                    aria-label={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showPassword ? (
                                        <EyeOff size={17} />
                                    ) : (
                                        <Eye size={17} />
                                    )}
                                </button>
                            </div>
                        </div>

                        {/* Error */}
                        {error && (
                            <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2.5">
                                <p className="text-xs font-medium leading-5 text-red-600">
                                    {error}
                                </p>
                            </div>
                        )}

                        {/* Remember + Forgot */}
                        <div className="flex items-center justify-between gap-3">

                            <label className="group flex cursor-pointer items-center gap-2">
                                <input
                                    type="checkbox"
                                    checked={rememberMe}
                                    onChange={(e) =>
                                        setRememberMe(e.target.checked)
                                    }
                                    className="sr-only"
                                />

                                <span
                                    className={`
                                        flex h-4 w-4 items-center justify-center
                                        rounded
                                        transition-colors
                                        ${
                                            rememberMe
                                                ? "bg-primary text-white"
                                                : "bg-surface-high text-transparent"
                                        }
                                    `}
                                >
                                    <Check
                                        size={12}
                                        strokeWidth={3}
                                    />
                                </span>

                                <span className="select-none text-xs text-on-surface-variant group-hover:text-on-surface">
                                    Remember me
                                </span>
                            </label>

                            <button
                                type="button"
                                onClick={() =>
                                    setError(
                                        "Password recovery will be available soon."
                                    )
                                }
                                className="text-xs font-semibold text-primary transition-colors hover:text-primary-container"
                            >
                                Forgot password?
                            </button>
                        </div>

                        {/* Login Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="
                                group mt-1 flex w-full
                                items-center justify-center gap-2
                                rounded-xl
                                bg-primary
                                px-4 py-3
                                text-sm font-bold
                                text-white
                                shadow-sm
                                transition-all
                                hover:bg-primary-container
                                hover:shadow-md
                                disabled:cursor-not-allowed
                                disabled:opacity-70
                            "
                        >
                            {loading ? (
                                <>
                                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                                    <span>Logging in...</span>
                                </>
                            ) : (
                                <>
                                    <span>Sign In</span>

                                    <ArrowRight
                                        size={16}
                                        className="transition-transform group-hover:translate-x-0.5"
                                    />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Divider */}
                    <div className="relative my-7 flex items-center justify-center">
                        <div className="h-px w-full bg-surface-high" />

                        <span className="absolute bg-white px-3 text-[10px] font-bold uppercase tracking-wider text-outline">
                            Or continue with
                        </span>
                    </div>

                    {/* Social Login */}
                    <div className="w-full">

                        <button
                            type="button"
                            onClick={() =>
                                setError(
                                    "Google sign-in will be connected soon."
                                )
                            }
                            className="
                                flex w-full items-center justify-center 
                                gap-2
                                rounded-lg bg-surface-low
                                px-3 py-2.5
                                transition-colors
                                hover:bg-surface-high
                            "
                            aria-label="Continue with Google"
                        >
                            <span className="text-sm font-bold text-[#4285F4]">
                                G
                            </span>
                        </button>
                    </div>

                    {/* Register */}
                    <div className="mt-7 border-t border-surface-high pt-5 text-center">
                        <p className="text-sm text-on-surface-variant">
                            Don't have an account?

                            <Link
                                to="/register"
                                className="ml-1 font-bold text-primary transition-colors hover:text-primary-container"
                            >
                                Create an account
                            </Link>
                        </p>
                    </div>
                </div>

                {/* Security Badge */}
                <div className="mt-4 flex items-center justify-center gap-1.5 text-on-surface-variant/70">
                    <ShieldCheck size={14} />

                    <span className="text-[10px] font-bold uppercase tracking-wider">
                        Secure account authentication
                    </span>
                </div>
            </div>
        </main>
    );
}