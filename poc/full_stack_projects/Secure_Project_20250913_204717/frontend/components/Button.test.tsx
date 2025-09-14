
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// ダミーのボタンコンポーネント
const Button = ({ children }) => <button>{children}</button>;

describe('Button Component', () => {
  test('renders children correctly', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });
});
