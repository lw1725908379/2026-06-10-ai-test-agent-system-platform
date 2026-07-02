import * as React from "react";
import { cn } from "@/lib/utils";
// @ts-expect-error  MC8yOmFIVnBZMlhsaUpqbWxvYzZUa0p6VUE9PToyMmVmM2JiZQ==

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Textarea.displayName = "Textarea";
// eslint-disable  MS8yOmFIVnBZMlhsaUpqbWxvYzZUa0p6VUE9PToyMmVmM2JiZQ==

export { Textarea };

