import React from "react";
import clsx from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
}

const variants: Record<NonNullable<ButtonProps["variant"]>, string> = {
  primary: "bg-accent text-white hover:bg-indigo-500",
  secondary: "bg-white/10 text-white hover:bg-white/20",
  ghost: "bg-transparent text-white/70 hover:text-white",
  danger: "bg-danger text-white hover:bg-red-500",
};

export function Button({ variant = "secondary", className, ...props }: ButtonProps) {
  return (
    <button
      className={clsx(
        "rounded-lg px-3 py-2 text-xs font-semibold transition",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
