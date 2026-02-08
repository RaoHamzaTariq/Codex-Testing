import React from "react";
import clsx from "clsx";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={clsx(
        "rounded-xl border border-white/10 bg-card/80 p-4 shadow-sm",
        className
      )}
      {...props}
    />
  );
}

export function CardHeader({ className, ...props }: CardProps) {
  return <div className={clsx("mb-3", className)} {...props} />;
}

export function CardTitle({ className, ...props }: CardProps) {
  return <h3 className={clsx("text-sm font-semibold", className)} {...props} />;
}

export function CardContent({ className, ...props }: CardProps) {
  return <div className={clsx("space-y-2", className)} {...props} />;
}
