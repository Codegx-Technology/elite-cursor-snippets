// [TASK]: Create a reusable Progress component.
// [GOAL]: Provide a consistent, enterprise-grade progress indicator.
// [CONSTRAINTS]: Use Tailwind CSS, support different values and max values.
// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + atomicstrategy
// [CONTEXT]: Building core UI components for the Shujaa Studio enterprise frontend.

"use client";

import * as React from "react";
import * as ProgressPrimitive from "@radix-ui/react-progress";

import { cn } from "@/lib/utils"; // Assuming a utility for class merging

const Progress = React.forwardRef<
  React.ElementRef<typeof ProgressPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>
>(({ className, value, ...props }, ref) => (
  <ProgressPrimitive.Root
    ref={ref}
    className={cn(
      "relative h-4 w-full overflow-hidden rounded-full bg-secondary",
      className
    )}
    {...props}
  >
    <ProgressPrimitive.Indicator
      className="h-full w-full flex-1 bg-primary transition-all"
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </ProgressPrimitive.Root>
));
Progress.displayName = ProgressPrimitive.Root.displayName;

export { Progress };
