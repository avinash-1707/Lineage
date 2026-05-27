"use client";

import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { Dialog } from "radix-ui";
import { useState } from "react";

import { GithubMark } from "@/components/auth/GithubMark";
import { githubLoginUrl } from "@/lib/auth";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

const EASE_PAPER: [number, number, number, number] = [0.32, 0.72, 0, 1];
const EASE_PANEL: [number, number, number, number] = [0.22, 1, 0.36, 1];
const EASE_INK: [number, number, number, number] = [0.65, 0, 0.35, 1];
const EASE_EXIT: [number, number, number, number] = [0.4, 0, 1, 1];

export function LoginModal({ open, onOpenChange }: Props) {
  const reduceMaybe = useReducedMotion();
  const reduce = reduceMaybe === true;
  const [redirecting, setRedirecting] = useState(false);

  const initialPanel = reduce
    ? { opacity: 0 }
    : { opacity: 0, y: 16, rotateX: -2 };
  const animatePanel = reduce
    ? { opacity: 1 }
    : { opacity: 1, y: 0, rotateX: 0 };
  const exitPanel = reduce ? { opacity: 0 } : { opacity: 0, y: 8 };

  const fadeUp = (delay: number) =>
    reduce
      ? {
          initial: { opacity: 0 },
          animate: { opacity: 1 },
          transition: { duration: 0.2 },
        }
      : {
          initial: { opacity: 0, y: 6 },
          animate: { opacity: 1, y: 0 },
          transition: { duration: 0.28, ease: "easeOut" as const, delay },
        };

  const fade = (delay: number) =>
    reduce
      ? {
          initial: { opacity: 0 },
          animate: { opacity: 1 },
          transition: { duration: 0.2 },
        }
      : {
          initial: { opacity: 0 },
          animate: { opacity: 1 },
          transition: { duration: 0.28, ease: "easeOut" as const, delay },
        };

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open ? (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild forceMount>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.32, ease: EASE_PAPER }}
                className="fixed inset-0 z-80 bg-contrast-bg/80 backdrop-blur-[3px]"
              />
            </Dialog.Overlay>

            <Dialog.Content
              asChild
              forceMount
              aria-describedby="login-reassurance"
              onOpenAutoFocus={(e) => {
                e.preventDefault();
                document.getElementById("login-github-button")?.focus();
              }}
            >
              <motion.div
                initial={initialPanel}
                animate={animatePanel}
                exit={exitPanel}
                transition={{
                  duration: reduce ? 0.2 : 0.32,
                  ease: reduce ? "easeOut" : EASE_PANEL,
                  delay: reduce ? 0 : 0.04,
                }}
                style={{ transformOrigin: "top center" }}
                className={[
                  "fixed z-90",
                  "inset-x-3 bottom-3 sm:inset-auto sm:left-1/2 sm:top-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2",
                  "w-auto sm:w-[min(92vw,560px)]",
                  "overflow-hidden",
                  "rounded-[24px] sm:rounded-[28px]",
                  "border border-line bg-paper text-ink",
                  "shadow-[0_40px_80px_-30px_rgba(0,0,0,0.7),0_8px_24px_-12px_rgba(0,0,0,0.5)]",
                  "outline-none",
                ].join(" ")}
              >
                {/* atmospheric warmth — radial breathing behind glyph */}
                <div
                  aria-hidden
                  className="paper-warmth pointer-events-none absolute inset-0"
                />

                {/* illuminated capital L — bleeds off top-left */}
                <motion.span
                  aria-hidden
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.08 }}
                  transition={{
                    duration: reduce ? 0.2 : 0.72,
                    ease: reduce ? "easeOut" : EASE_INK,
                    delay: reduce ? 0 : 0.24,
                  }}
                  className="pointer-events-none absolute -left-4 -top-10 select-none font-display italic leading-none text-highlight sm:-left-3 sm:-top-14"
                  style={{
                    fontSize: "clamp(10rem, 28vw, 17rem)",
                    fontWeight: 420,
                  }}
                >
                  L
                </motion.span>

                {/* close button */}
                <Dialog.Close
                  className="absolute right-4 top-4 z-10 grid h-8 w-8 place-items-center rounded-full border border-line text-muted transition-colors duration-200 hover:border-ink-soft hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
                  aria-label="Close"
                >
                  <svg
                    aria-hidden
                    viewBox="0 0 16 16"
                    width={12}
                    height={12}
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={1.5}
                    strokeLinecap="round"
                  >
                    <path d="M3 3l10 10M13 3L3 13" />
                  </svg>
                </Dialog.Close>

                <div className="relative z-1 flex flex-col gap-7 px-6 pb-7 pt-12 sm:px-10 sm:pb-10 sm:pt-14">
                  {/* header group (A) */}
                  <div className="flex flex-col gap-4">
                    <motion.span
                      {...fadeUp(0)}
                      className="font-mono text-[10.5px] uppercase tracking-[0.24em] text-muted"
                    >
                      Chapter · Sign in
                    </motion.span>

                    <Dialog.Title asChild>
                      <motion.h2
                        {...fadeUp(0.05)}
                        className="max-w-[18ch] font-display text-[clamp(2rem,4.6vw,2.65rem)] italic leading-[1.02] tracking-tight text-ink"
                      >
                        Continue the lineage.
                      </motion.h2>
                    </Dialog.Title>

                    <Dialog.Description asChild>
                      <motion.p
                        {...fadeUp(0.1)}
                        className="max-w-[40ch] text-[0.95rem] leading-[1.55] text-ink-soft"
                      >
                        Sign in to pick up where your team&apos;s reviews left
                        off.
                      </motion.p>
                    </Dialog.Description>
                  </div>

                  {/* hairline divider */}
                  <motion.div {...fade(0.18)} className="h-px w-full bg-line" />

                  {/* body group (B) */}
                  <motion.div {...fade(0.18)} className="flex flex-col gap-5">
                    <a
                      id="login-github-button"
                      href={githubLoginUrl()}
                      onClick={() => setRedirecting(true)}
                      data-redirecting={redirecting ? "true" : "false"}
                      aria-disabled={redirecting}
                      aria-label={
                        redirecting ? "Redirecting to GitHub" : undefined
                      }
                      className="github-cta group flex w-full items-center justify-center gap-3 rounded-full border border-line bg-contrast-bg px-6 py-3.5 text-[0.95rem] font-medium text-contrast-fg hover:bg-[#0f0d0a] hover:tracking-[-0.005em] focus-visible:outline-none active:translate-y-px aria-disabled:cursor-progress aria-disabled:opacity-90"
                    >
                      {redirecting ? (
                        <span className="gh-loader" aria-hidden />
                      ) : (
                        <>
                          <GithubMark size={18} className="text-contrast-fg" />
                          <span className="github-cta-label">
                            Continue with GitHub
                          </span>
                          <span
                            aria-hidden
                            className="github-cta-arrow inline-block transition-transform duration-300 ease-out group-hover:translate-x-1"
                          >
                            →
                          </span>
                        </>
                      )}
                    </a>

                    <div className="flex flex-wrap items-center gap-2">
                      <ScopePill>read:user</ScopePill>
                      <ScopePill>user:email</ScopePill>
                      <span className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted-2">
                        · scopes requested
                      </span>
                    </div>

                    <p
                      id="login-reassurance"
                      className="max-w-[46ch] text-[0.82rem] leading-[1.55] text-muted"
                    >
                      Your code stays yours. We never read repository contents
                      without an explicit install.
                    </p>
                  </motion.div>

                  {/* footer */}
                  <motion.div
                    {...fade(0.18)}
                    className="flex items-center justify-between border-t border-line-soft pt-4 font-mono text-[10px] uppercase tracking-[0.22em] text-muted-2"
                  >
                    <span>Lineage</span>
                    <span className="flex items-center gap-3">
                      <a
                        href="/terms"
                        className="transition-colors hover:text-ink-soft"
                      >
                        Terms
                      </a>
                      <span aria-hidden>·</span>
                      <a
                        href="/privacy"
                        className="transition-colors hover:text-ink-soft"
                      >
                        Privacy
                      </a>
                    </span>
                  </motion.div>
                </div>
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        ) : null}
      </AnimatePresence>
    </Dialog.Root>
  );
}

function ScopePill({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex items-center rounded-full border border-line-soft bg-bg-elevated px-2.5 py-1 font-mono text-[10px] uppercase tracking-[0.18em] text-ink-soft">
      {children}
    </span>
  );
}
