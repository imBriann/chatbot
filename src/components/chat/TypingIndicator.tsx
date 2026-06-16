import './TypingIndicator.css';

export function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <div className="typing-indicator__avatar">🤖</div>
      <div className="typing-indicator__dots">
        <span className="typing-indicator__dot" />
        <span className="typing-indicator__dot" />
        <span className="typing-indicator__dot" />
      </div>
    </div>
  );
}
