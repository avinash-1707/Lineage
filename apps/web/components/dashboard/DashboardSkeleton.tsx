export function DashboardSkeleton() {
  return (
    <main className="relative z-10 flex min-h-dvh">
      <aside className="hidden h-dvh w-[280px] shrink-0 flex-col gap-3 border-r border-line-soft bg-paper/40 p-4 lg:flex">
        <div className="h-9 w-32 animate-pulse rounded-md bg-line" />
        <div className="mt-4 h-16 w-full animate-pulse rounded-md bg-line-soft" />
        {[0, 1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="h-11 w-full animate-pulse rounded-md bg-line-soft"
          />
        ))}
        <div className="mt-auto h-14 w-full animate-pulse rounded-md bg-line" />
      </aside>
      <section className="mx-auto w-full max-w-[1100px] px-5 pb-24 pt-10 sm:px-8 md:pt-14 lg:px-12">
        <div className="h-3 w-32 animate-pulse rounded-full bg-line" />
        <div className="mt-4 h-14 w-2/3 animate-pulse rounded-md bg-line" />
        <div className="mt-3 h-4 w-1/2 animate-pulse rounded-md bg-line-soft" />
        <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="h-32 animate-pulse rounded-lg border border-line bg-paper"
            />
          ))}
        </div>
        <div className="mt-8 h-64 animate-pulse rounded-lg border border-line bg-paper" />
      </section>
    </main>
  );
}
