import type { HTMLAttributes, ReactNode } from 'react';
import './Badge.css';

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'success' | 'neutral' | 'outline';
  size?: 'sm' | 'md';
  children?: ReactNode;
}

export function Badge({
  variant = 'neutral',
  size = 'md',
  className = '',
  children,
  ...props
}: BadgeProps) {
  return (
    <span className={`badge badge--${variant} badge--${size} ${className}`} {...props}>
      {children}
    </span>
  );
}
