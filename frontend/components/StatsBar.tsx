import { Mention } from "@/lib/api";

interface Props {
  mentions: Mention[];
}

export default function StatsBar({ mentions }: Props) {
  const total = mentions.length;
  const negative = mentions.filter((m) => m.sentiment === "negative").length;
  const positive = mentions.filter((m) => m.sentiment === "positive").length;
  const crisis = mentions.filter((m) => m.mention_type === "crisis").length;
  const avgScore =
    total > 0
      ? Math.round(
          mentions
            .filter((m) => m.reputation_score !== null)
            .reduce((acc, m) => acc + (m.reputation_score ?? 0), 0) /
            mentions.filter((m) => m.reputation_score !== null).length
        )
      : 0;

  const stats = [
    { label: "Total de menções", value: total, color: "text-white" },
    { label: "Negativas", value: negative, color: "text-red-400" },
    { label: "Positivas", value: positive, color: "text-green-400" },
    { label: "Score médio", value: `${avgScore}/100`, color: "text-blue-400" },
    { label: "Crises", value: crisis, color: "text-orange-400" },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
      {stats.map((s) => (
        <div key={s.label} className="bg-gray-900 rounded-xl p-4">
          <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
          <p className="text-gray-400 text-xs mt-1">{s.label}</p>
        </div>
      ))}
    </div>
  );
}
