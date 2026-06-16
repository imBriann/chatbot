import type { InputHTMLAttributes, ReactNode } from 'react';
import './Input.css';

interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  helper?: string;
  error?: string;
  size?: 'sm' | 'md' | 'lg';
  icon?: ReactNode;
  containerClassName?: string;
}

export function Input({
  label,
  helper,
  error,
  size = 'md',
  icon,
  containerClassName = '',
  className = '',
  id,
  ...props
}: InputProps) {
  const inputId = id || props.name;

  return (
    <div className={`input ${containerClassName}`}>
      {label && (
        <label className="input__label" htmlFor={inputId}>
          {label}
        </label>
      )}
      <div className={`input__wrapper input__wrapper--${size} ${error ? 'input__wrapper--error' : ''}`}>
        {icon && <span className="input__icon">{icon}</span>}
        <input
          id={inputId}
          className={`input__field ${className}`}
          {...props}
        />
      </div>
      {error ? (
        <span className="input__error">{error}</span>
      ) : (
        helper && <span className="input__helper">{helper}</span>
      )}
    </div>
  );
}
