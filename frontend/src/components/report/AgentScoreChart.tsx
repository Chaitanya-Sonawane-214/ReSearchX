import {
  Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, LabelList,
} from "recharts";
import { scoreTone, TONE_HEX } from "../../lib/status";

export function AgentScoreChart({ agentScores }: { agentScores: Record<string, number> }) {
  const data = Object.entries(agentScores).map(([name, score]) => ({
    name: name.replace(" Agent", "").replace("Matching", ""),
    score,
  }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 16, right: 12, left: -20, bottom: 0 }}>
          <XAxis
            dataKey="name"
            tick={{ fontSize: 11, fill: "var(--color-ink-500)" }}
            axisLine={{ stroke: "var(--color-ink-200)" }}
            tickLine={false}
            interval={0}
            angle={-20}
            textAnchor="end"
            height={50}
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fontSize: 11, fill: "var(--color-ink-400)" }}
            axisLine={false}
            tickLine={false}
            width={30}
          />
          <Tooltip
            cursor={{ fill: "var(--color-ink-50)" }}
            formatter={(value) => [`${value}/100`, "Score"]}
            contentStyle={{ fontSize: 12, borderRadius: 8, borderColor: "var(--color-ink-200)" }}
          />
          <Bar dataKey="score" radius={[6, 6, 0, 0]} maxBarSize={42}>
            <LabelList dataKey="score" position="top" style={{ fontSize: 11, fill: "var(--color-ink-600)", fontWeight: 600 }} />
            {data.map((d) => (
              <Cell key={d.name} fill={TONE_HEX[scoreTone(d.score)]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
