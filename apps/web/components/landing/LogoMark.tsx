type Props = {
  size?: number;
  className?: string;
  title?: string;
};

export function LogoMark({ size = 22, className = "", title }: Props) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role={title ? "img" : "presentation"}
      aria-label={title}
      className={className}
    >
      {/* current review node */}
      <circle cx="12" cy="3.6" r="1.9" fill="currentColor" />

      {/* branches to ancestor row */}
      <path
        d="M12 5.6 L5.5 11.2 M12 5.6 L18.5 11.2"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />

      {/* ancestor nodes · one filled accent (the recalled precedent) */}
      <circle
        cx="5.5"
        cy="11.4"
        r="1.5"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <circle cx="18.5" cy="11.4" r="1.5" fill="var(--accent, currentColor)" />

      {/* memory loop · dashed arc connecting the ancestors */}
      <path
        d="M5.5 13 Q 12 18.4 18.5 13"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeDasharray="0.1 3"
      />

      {/* descent line to root */}
      <path
        d="M12 15.2 L12 20.4"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />

      {/* root */}
      <circle cx="12" cy="20.6" r="1.3" fill="currentColor" />
    </svg>
  );
}
