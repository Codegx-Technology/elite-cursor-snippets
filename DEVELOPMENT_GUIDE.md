# Development Guide

This guide provides instructions for developers working on the Shujaa Studio project. It covers the project setup, development workflow, coding conventions, and UI best practices.

## 1. Project Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd ShujaaStudio
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Download AI models (optional):**

    Create the following directories:

    ```bash
    mkdir -p models/tts models/llm models/img models/music
    ```

    Download the required models and place them in the corresponding directories.

## 2. Frontend Development

### **Development Environment Setup**

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Storybook: `npm run storybook`

### **API Mock Data System**

The frontend includes a comprehensive mock data system for development without backend dependencies:

#### **Plan Service Mock Data**
- Automatically provides mock plan status when `API_BASE` is not configured
- Realistic usage/quota data for testing UI components
- File: `src/widgets/PlanGuardWidget/planService.ts`

#### **Admin Dashboard Mock Data**
- **Users**: 3 sample users (admin, active, inactive) with proper TypeScript compliance
- **Tenants**: 3 sample tenants with different plans (Enterprise, Professional, Free)
- **Audit Logs**: 4 realistic audit entries with proper timestamps
- File: `src/widgets/SuperAdminDashboardWidget/adminService.ts`

#### **Error Handling Pattern**
All API services follow this consistent pattern:
```typescript
export async function fetchData(): Promise<DataType[]> {
  // Use mock data when backend is not available
  if (!API_BASE || API_BASE === "") {
    console.warn("No API_BASE configured, using mock data");
    return Promise.resolve(mockData);
  }

  try {
    const response = await apiClient.getData();
    return handleApiResponse(response);
  } catch (error) {
    console.warn("Backend not available, using mock data:", error);
    return Promise.resolve(mockData);
  }
}
```

### **Console Error Prevention**

- **No Debug Logging**: Avoid console.log statements in production components
- **Manifest Validation**: Ensure all referenced files exist in public directory
- **Build Cache**: Clean `.next` directory if experiencing manifest errors

### **UI Icon Best Practices**

For maximum stability and zero external dependencies, use **inline SVGs** instead of icon libraries:

```tsx
// ✅ RECOMMENDED: Inline SVG (bulletproof)
const HomeIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
  </svg>
);

// ❌ AVOID: External icon libraries (dependency risk)
import { FaHome } from 'react-icons/fa';
```

### **Icon Implementation Guidelines**
- Use `className="w-5 h-5"` for consistent sizing
- Use `fill="currentColor"` to inherit text color
- Maintain Kenya-first design with appropriate colors
- Test icons across all breakpoints for mobile responsiveness

### **Preventive Measures**
Run the fa6 import checker before builds:
```bash
npm run check-fa6  # Detects any react-icons/fa6 imports
```

## 3. Development Workflow

1.  **Run the application:**

    *   **Web Interface:**

        ```bash
        python generate_video.py
        ```

    *   **Command-Line Interface:**

        ```bash
        python offline_video_maker/generate_video.py "Your prompt here"
        ```

2.  **Testing:**

    Run the test script to verify the video generation pipeline:

    ```bash
    python offline_video_maker/test_video_generation.py
    ```

## 3. Enterprise-Grade UI Development Workflow

To ensure we build a truly enterprise-grade UI, we will adhere to a strict Component-Driven Development (CDD) workflow. This methodology is our standard for all UI development, whether adding new features or fixing bugs.

### Core Principles

1.  **Check the Codebase First:** Before writing any new code, thoroughly check the existing codebase for a similar feature or component. The goal is to enhance and reuse, not to reinvent.
2.  **Consult the Design System:** The `UI_DESIGN_SYSTEM.md` file is our single source of truth for all design tokens (colors, fonts, spacing, etc.). All components must adhere to this system.
3.  **Use Elite-Cursor-Snippets:** These are our "workflow tokens" and are mandatory for building and refactoring components. They ensure consistency, quality, and adherence to our Kenya-first principles.

### Workflow Steps

1.  **Understand the Task:** Clearly define the goal of the new feature or bug fix.
2.  **Explore the Existing UI:** Identify any existing components that can be reused or enhanced.
3.  **Consult `UI_DESIGN_SYSTEM.md`:** Refer to the design system for the correct design tokens and CSS classes.
4.  **Select the Right Elite-Cursor-Snippet:** Choose the appropriate snippet (e.g., `autocomp` for a new component, `refactorclean` for an existing one).
5.  **Build or Refactor the Component:** Write clean, well-documented, and reusable code, leveraging our custom UI components (`Card`, `Button`, `Badge`, `Progress`, `FormInput`, `Table`, `ScrollArea`, `useToast`).
6.  **Document as You Go:** Add clear comments to explain the purpose, props, and usage of the component.
7.  **Test Thoroughly:** Ensure the component works as expected and does not introduce any regressions.

### Recent UI Development Highlights:

*   **Dashboard Page**: Enhanced with a PlanGuard overview and dynamic display of recent projects.
*   **Pricing/Usage Page**: Expanded to include current subscription details and usage statistics.
*   **Settings Page**: Implemented a robust tabbed navigation for various settings sections, including initial scaffolding for tenant branding.

## 4. Elite Cursor Snippets Methodology

The Elite Cursor Snippets are not just comments; they are a core part of our development methodology. They are context patterns that guide our AI-assisted development and ensure that we build high-quality, maintainable, and consistent code.

**Snippet Format:**

```
// [KEY]: Value
```

**Common Keys:**

*   `[TASK]`: A description of the task that the code is supposed to accomplish.
*   `[GOAL]`: The objective of the code.
*   `[CONSTRAINTS]`: Any limitations or constraints on the code.
*   `[SNIPPET]`: The name of the snippet being used.
*   `[CONTEXT]`: The context in which the code is being used.
*   `[PROGRESS]`: The current status of the code.
*   `[NEXT]`: The next step in the development process.
*   `[LOCATION]`: The location of the code in the project.

By using these snippets, we provide our AI development partner with the necessary context to understand our intentions and generate code that aligns with our project's goals and standards. It is mandatory to use these snippets for all new features and bug fixes.

## 5. Coding Conventions

*   **Style:** Follow the PEP 8 style guide for Python code.
*   **Docstrings:** Use Google-style docstrings for all modules, classes, and functions.
*   **Comments:** Use comments to explain complex logic and to provide context for your code.
*   **Naming:** Use descriptive names for variables, functions, and classes.