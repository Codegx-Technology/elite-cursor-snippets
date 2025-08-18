import { render, screen } from '@testing-library/react';
import LoginPage from './page';

// Mock next/navigation useRouter
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('LoginPage', () => {
  it('renders the login form correctly', () => {
    render(<LoginPage />);

    // Check if the main heading is present
    expect(screen.getByRole('heading', { name: /Login to Shujaa Studio/i })).toBeInTheDocument();

    // Check if username and password input fields are present
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();

    // Check if the Login button is present
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
  });
});
