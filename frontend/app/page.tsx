import { Activity, Database, FileText, GitBranch, ShieldCheck } from "lucide-react";

const panels = [
  { title: "Execution Graph", icon: GitBranch, value: "Planning -> Search -> Read -> Verify" },
  { title: "Agent Activity", icon: Activity, value: "8 governed workers online" },
  { title: "Memory", icon: Database, value: "Session, semantic, episodic" },
  { title: "Report", icon: FileText, value: "Evidence-grounded draft stream" },
  { title: "Governance", icon: ShieldCheck, value: "Budget, policy, trace, safety" }
];

export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto grid max-w-7xl gap-6 px-6 py-6">
        <header className="flex items-center justify-between border-b border-zinc-800 pb-4">
          <div>
            <h1 className="text-2xl font-semibold tracking-normal">Omega Research Grid</h1>
            <p className="mt-1 text-sm text-zinc-400">Autonomous research operations console</p>
          </div>
          <button className="rounded-md bg-emerald-500 px-4 py-2 text-sm font-medium text-zinc-950">
            New Run
          </button>
        </header>

        <section className="grid gap-4 md:grid-cols-5">
          {panels.map((panel) => {
            const Icon = panel.icon;
            return (
              <article key={panel.title} className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
                <div className="flex items-center gap-2 text-sm text-zinc-400">
                  <Icon size={16} />
                  <span>{panel.title}</span>
                </div>
                <p className="mt-3 text-sm font-medium text-zinc-100">{panel.value}</p>
              </article>
            );
          })}
        </section>

        <section className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
          <div className="min-h-96 rounded-lg border border-zinc-800 bg-zinc-900 p-4">
            <h2 className="text-sm font-semibold">Live DAG</h2>
            <div className="mt-4 grid gap-3 text-sm">
              {["Planner", "Search", "Reader", "Memory", "Writer", "Critic", "Verification", "Finalizer"].map(
                (agent, index) => (
                  <div key={agent} className="flex items-center gap-3">
                    <span className="grid h-7 w-7 place-items-center rounded-full bg-zinc-800 text-xs">
                      {index + 1}
                    </span>
                    <div className="h-px flex-1 bg-zinc-800" />
                    <span className="w-28 text-zinc-300">{agent}</span>
                  </div>
                )
              )}
            </div>
          </div>

          <div className="min-h-96 rounded-lg border border-zinc-800 bg-zinc-900 p-4">
            <h2 className="text-sm font-semibold">Confidence Heatmap</h2>
            <div className="mt-4 grid gap-2">
              {["Factuality", "Citation Accuracy", "Source Quality", "Reasoning", "Coherence"].map((label, i) => (
                <div key={label} className="grid grid-cols-[8rem_1fr] items-center gap-3 text-sm">
                  <span className="text-zinc-400">{label}</span>
                  <div className="h-2 rounded-full bg-zinc-800">
                    <div
                      className="h-2 rounded-full bg-emerald-400"
                      style={{ width: `${88 - i * 5}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
