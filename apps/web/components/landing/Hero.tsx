import Link from "next/link";
import { ShaderBackdrop } from "./ShaderBackdrop";

export function Hero() {
  return (
    <section className="relative z-10 isolate min-h-screen overflow-hidden">
      <ShaderBackdrop />
      <div className="relative z-10 mx-auto flex min-h-screen max-w-[1240px] flex-col items-center justify-center px-6 pb-28 pt-24 text-center md:px-10 md:pb-32 md:pt-28">
        <h1 className="font-display text-ink">
          <span
            className="reveal block text-[clamp(3.6rem,11vw,11rem)] font-[440] leading-[0.92] tracking-[-0.035em]"
            style={{ ["--d" as string]: "160ms" }}
          >
            Code review
          </span>

          <span
            className="reveal mt-1 block text-[clamp(3.6rem,11vw,11rem)] leading-[0.92] tracking-[-0.04em]"
            style={{ ["--d" as string]: "300ms" }}
          >
            <span className="italic font-[420] text-accent">
              that&nbsp;remembers.
            </span>
          </span>
        </h1>

        <p
          className="reveal mt-10 max-w-[44ch] text-[1.05rem] leading-[1.6] text-ink-soft md:text-[1.15rem]"
          style={{ ["--d" as string]: "480ms" }}
        >
          Lineage learns how your team reviews and brings it back on every pull
          request.
        </p>

        <div className="reveal mt-10" style={{ ["--d" as string]: "620ms" }}>
          <Link href="#cta" className="btn btn-primary text-[0.95rem]">
            Request access
            <span aria-hidden className="arrow">
              →
            </span>
          </Link>
        </div>
      </div>
    </section>
  );
}
