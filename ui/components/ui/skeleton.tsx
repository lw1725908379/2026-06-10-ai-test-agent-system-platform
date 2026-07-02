import { cn } from "@/lib/utils";
// FIXME  MC8yOmFIVnBZMlhsaUpqbWxvYzZSMkpXY1E9PTozN2Q1NmE4NQ==

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  );
}

export { Skeleton };
// @ts-expect-error  MS8yOmFIVnBZMlhsaUpqbWxvYzZSMkpXY1E9PTozN2Q1NmE4NQ==
