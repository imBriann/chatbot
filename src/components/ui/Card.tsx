import type { HTMLAttributes, ReactNode } from 'react';
import './Card.css';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outline' | 'glass';
  padding?: 'sm' | 'md' | 'lg';
  children?: ReactNode;
}

export function Card({
  variant = 'default',
  padding = 'md',
  className = '',
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={`card card--${variant} card--${padding} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
