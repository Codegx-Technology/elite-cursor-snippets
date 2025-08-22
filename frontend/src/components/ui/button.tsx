// [TASK]: Create a reusable Button component.
// [GOAL]: Provide a consistent, enterprise-grade button with various styles and states.
// [CONSTRAINTS]: Use Tailwind CSS, support different variants (primary, secondary, ghost), sizes, and disabled state.
// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + atomicstrategy
// [CONTEXT]: Building core UI components for the Shujaa Studio enterprise frontend.

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils"; // Assuming a utility for class merging

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

import { LoadingSpinner } from '@/components/LoadingSpinner'; // Import LoadingSpinner

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean; // New prop for loading state
  leadingIcon?: React.ReactNode; // New prop for leading icon
  trailingIcon?: React.ReactNode; // New prop for trailing icon
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, loading, leadingIcon, trailingIcon, children, ...props }, ref) => {
    const Comp = asChild ? "span" : "button";
    return (
      <Comp
        className={cn(
          buttonVariants({ variant, size, className }),
          loading && "relative" // Add relative positioning for spinner overlay
        )}
        ref={ref}
        disabled={props.disabled || loading} // Disable button when loading
        {...props}
      >
        {loading && (
          <span className="absolute inset-0 flex items-center justify-center">
            <LoadingSpinner size="sm" variant="minimal" /> {/* Use minimal spinner for small size */}
          </span>
        )}
        <span className={cn(loading && "opacity-0")}> {/* Hide content when loading */}
          {leadingIcon && <span className="mr-2">{leadingIcon}</span>}
          {children}
          {trailingIcon && <span className="ml-2">{trailingIcon}</span>}
        </span>
      </Comp>
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
