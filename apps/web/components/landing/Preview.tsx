import { Reveal } from "./Reveal";

export function Preview() {
  return (
    <section
      id="preview"
      className="relative z-10 mx-auto max-w-[1240px] px-6 py-24 md:px-10 md:py-32"
    >
      <Reveal className="grid grid-cols-12 items-end gap-y-6">
        <div className="col-span-12 md:col-span-7">
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-muted-2">
            Chapter three
          </span>
          <h2 className="mt-4 font-display text-[clamp(2.2rem,5vw,4rem)] leading-none tracking-[-0.03em]">
            A review,
            <br />
            <span className="italic text-accent">arriving as it thinks.</span>
          </h2>
        </div>
        <p className="col-span-12 max-w-[44ch] text-[1rem] leading-[1.55] text-ink-soft md:col-span-5">
          Lineage streams its review the moment a pull request opens. The first
          observations land in seconds, threaded against the lines they belong
          to.
        </p>
      </Reveal>

      <Reveal delay={120} className="mt-14">
        <PRMock />
      </Reveal>
    </section>
  );
}

function PRMock() {
  return (
    <div className="relative overflow-hidden rounded-[22px] border border-line bg-paper/70 shadow-[0_30px_80px_-50px_rgba(26,26,23,0.4)]">
      {/* Title bar */}
      <div className="flex items-center justify-between border-b border-line-soft px-5 py-3.5">
        <div className="flex items-center gap-3 font-mono text-[12px] text-muted">
          <span className="flex items-center gap-1.5">
            <span className="live-dot" aria-hidden />
            <span>open</span>
          </span>
          <span className="text-muted-2">·</span>
          <span>acme/api</span>
          <span className="text-muted-2">·</span>
          <span>pull/214</span>
        </div>
        <span className="hidden font-mono text-[11px] uppercase tracking-[0.2em] text-muted-2 sm:inline">
          reviewing
        </span>
      </div>

      <div className="grid grid-cols-12">
        {/* File tree column */}
        <aside className="col-span-12 border-b border-line-soft p-5 font-mono text-[12px] text-muted md:col-span-4 md:border-b-0 md:border-r">
          <div className="mb-3 text-[10px] uppercase tracking-[0.2em] text-muted-2">
            Changed
          </div>
          <ul className="flex flex-col gap-1.5">
            <FileRow path="app/services/billing.py" stat="+42 .. 11" active />
            <FileRow path="app/services/auth_service.py" stat="+12 .. 4" />
            <FileRow path="app/models/invoice.py" stat="+6 .. 0" />
            <FileRow path="tests/billing_test.py" stat="+88 .. 2" />
          </ul>

          <div className="mt-6 flex items-center justify-between border-t border-line-soft pt-4 text-[10px] uppercase tracking-[0.2em] text-muted-2">
            <span>signal</span>
            <span className="text-ink-soft">3 high · 2 low</span>
          </div>
        </aside>

        {/* Diff + comments */}
        <div className="col-span-12 p-5 md:col-span-8 md:p-6">
          <div className="rounded-xl border border-line-soft bg-bg-elevated/60">
            <div className="border-b border-line-soft px-4 py-2.5 font-mono text-[12px] text-muted">
              app/services/billing.py
            </div>
            <div className="grid grid-cols-[44px_1fr] gap-x-2 px-4 py-3 font-mono text-[12.5px] leading-[1.7]">
              <DiffLine n="38" v="def charge(user, amount):" tone="neutral" />
              <DiffLine n="39" v={"    if not user.active:"} tone="neutral" />
              <DiffLine
                n=""
                v="        raise ValueError('inactive user')"
                tone="remove"
              />
              <DiffLine
                n="40"
                v="        raise InactiveUserError('inactive user')"
                tone="add"
              />
              <DiffLine
                n="41"
                v={"    return gateway.charge(user.id, amount)"}
                tone="neutral"
              />
            </div>
          </div>

          {/* Comment thread */}
          <div className="mt-5 flex flex-col gap-3">
            <Comment
              severity="high"
              file="billing.py"
              line={40}
              body={
                <>
                  <span className="font-mono text-[12px] text-muted-2">
                    [similar to pull/198, accepted]
                  </span>{" "}
                  This call now raises a typed exception, which is good. The
                  surrounding handlers in{" "}
                  <code className="font-mono text-ink">app/api/billing.py</code>{" "}
                  still catch the old{" "}
                  <code className="font-mono text-ink">ValueError</code>. Likely
                  worth updating the catch sites in the same change.
                </>
              }
              streaming
            />
            <Comment
              severity="low"
              file="billing.py"
              line={41}
              body={
                <>
                  Naming nit, recorded as team preference. Internal call sites
                  on <code className="font-mono text-ink">gateway</code> use
                  keyword arguments elsewhere. Consider{" "}
                  <code className="font-mono text-ink">
                    gateway.charge(user_id=user.id, amount=amount)
                  </code>{" "}
                  for consistency with{" "}
                  <code className="font-mono text-ink">PaymentService</code>.
                </>
              }
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function FileRow({
  path,
  stat,
  active,
}: {
  path: string;
  stat: string;
  active?: boolean;
}) {
  return (
    <li
      className={[
        "flex items-center justify-between gap-2 rounded-md px-2 py-1.5 text-[12px]",
        active ? "bg-bg-elevated text-ink" : "text-muted hover:text-ink-soft",
      ].join(" ")}
    >
      <span className="truncate">{path}</span>
      <span className="shrink-0 text-[10.5px] text-muted-2">{stat}</span>
    </li>
  );
}

function DiffLine({
  n,
  v,
  tone,
}: {
  n: string;
  v: string;
  tone: "neutral" | "add" | "remove";
}) {
  const cls =
    tone === "add"
      ? "text-sage"
      : tone === "remove"
        ? "text-accent"
        : "text-ink-soft";
  const bg =
    tone === "add"
      ? "bg-sage/[0.08]"
      : tone === "remove"
        ? "bg-accent/[0.07]"
        : "";
  const sym = tone === "add" ? "+" : tone === "remove" ? "−" : " ";
  return (
    <>
      <span className="select-none text-right text-[11px] text-muted-2">
        {n}
      </span>
      <span className={`flex items-center gap-2 rounded px-1 ${bg} ${cls}`}>
        <span className="w-3 text-muted-2">{sym}</span>
        <span className="truncate">{v}</span>
      </span>
    </>
  );
}

function Comment({
  severity,
  file,
  line,
  body,
  streaming,
}: {
  severity: "high" | "low";
  file: string;
  line: number;
  body: React.ReactNode;
  streaming?: boolean;
}) {
  return (
    <article className="rounded-xl border border-line-soft bg-paper p-4">
      <header className="mb-2 flex items-center gap-2 font-mono text-[11px]">
        <span
          className={[
            "rounded-full px-2 py-0.5 uppercase tracking-[0.18em]",
            severity === "high"
              ? "bg-accent/15 text-accent-deep"
              : "bg-sage/15 text-sage",
          ].join(" ")}
        >
          {severity}
        </span>
        <span className="text-muted-2">
          {file}:{line}
        </span>
      </header>
      <p className="text-[0.94rem] leading-[1.6] text-ink-soft">
        {body}
        {streaming && <span className="caret" aria-hidden />}
      </p>
    </article>
  );
}
