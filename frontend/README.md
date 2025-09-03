# ShujaaStudio Frontend

A Kenya-first enterprise SaaS platform for AI-powered content creation built with [Next.js](https://nextjs.org).

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Development Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Storybook: `npm run storybook`

## Features

### 🛠️ Development Experience
- **Independent Frontend Development**: Works with or without backend
- **API Mock Data System**: Comprehensive fallback for all endpoints
- **Clean Console Output**: No repetitive logging or 404 errors
- **TypeScript Strict Mode**: Full type safety and compliance

### 🔌 API Mock Data System
The frontend includes comprehensive mock data for seamless development:

- **Plan Service**: Automatic fallback when `API_BASE` not configured
- **Admin Dashboard**: Mock users, tenants, and audit logs
- **Error Handling**: Consistent pattern across all services

### 🎨 Kenya-First Design
- **Cultural Authenticity**: Subtle Kenyan elements without overwhelming UI
- **Mobile-First**: Responsive design optimized for Kenyan market
- **Enterprise Quality**: Production-ready components and workflows

## Development Guidelines

### Console Error Prevention
- Avoid debug logging in production components
- Validate manifest.json references to existing files
- Clean `.next` directory if experiencing build errors

### API Service Pattern
```typescript
export async function fetchData(): Promise<DataType[]> {
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

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
