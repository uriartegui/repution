"use client";

import { useState } from "react";
import { Mention } from "@/lib/api";

interface Props {
  mention: Mention;
}

const sentimentConfig = {
  negative: { label: "Negativo", className: "bg-red-500/20 text-red-400" },
  positive: { label: "Positivo", className: "bg-green-500/20 text-green-400" },
  neutral: { label: "Neutro", className: "bg-gray-500/20 text-gray-400" },
};

const typeConfig = {
  complaint: { label: "Reclamação", className: "bg-red-500/10 text-red-300" },
  praise: { label: "Elogio", className: "bg-green-500/10 text-green-300" },
  question: { label: "Dúvida", className: "bg-yellow-500/10 text-yellow-300" },
  crisis: {
    label: "CRISE",
    className: "bg-orange-500/20 text-orange-400 font-bold",
  },
};

const sourceLabels: Record<string, string> = {
  google: "Google",
  google_news: "Google News",
  google_maps: "Google Maps",
  instagram: "Instagram",
  twitter: "Twitter/X",
  reclame_aqui: "Reclame Aqui",
  facebook: "Facebook",
};

export default function MentionCard({ mention }: Props) {
  const [showModal, setShowModal] = useState(false);

  const sentiment =
    sentimentConfig[mention.sentiment as keyof typeof sentimentConfig];
  const type = typeConfig[mention.mention_type as keyof typeof typeConfig];

  const badges = (
    <div className="flex items-center gap-2 flex-wrap">
      <span className="text-xs bg-gray-800 text-gray-300 px-2 py-0.5 rounded-full">
        {sourceLabels[mention.source] ?? mention.source}
      </span>
      {sentiment && (
        <span
          className={`text-xs px-2 py-0.5 rounded-full ${sentiment.className}`}
        >
          {sentiment.label}
        </span>
      )}
      {type && (
        <span className={`text-xs px-2 py-0.5 rounded-full ${type.className}`}>
          {type.label}
        </span>
      )}
    </div>
  );

  return (
    <>
      {/* Card */}
      <div
        className="bg-gray-900 rounded-xl p-4 space-y-2 border border-gray-800 cursor-pointer hover:border-gray-600 transition"
        onClick={() => setShowModal(true)}
      >
        <div className="flex items-start justify-between gap-3">
          {badges}
          {mention.reputation_score !== null && (
            <span className="text-xs text-gray-400 whitespace-nowrap">
              Score:{" "}
              <span className="text-white font-semibold">
                {mention.reputation_score}/100
              </span>
            </span>
          )}
        </div>
        {mention.author && (
          <p className="text-xs text-gray-500">{mention.author}</p>
        )}
        <p className="text-sm text-gray-200 line-clamp-2">{mention.content}</p>
        {mention.ai_summary && (
          <p className="text-xs text-gray-400 italic border-l-2 border-gray-700 pl-3">
            {mention.ai_summary}
          </p>
        )}
        <p className="text-xs text-gray-600">
          {new Date(mention.collected_at).toLocaleString("pt-BR")}
        </p>
      </div>

      {/* Modal */}
      {showModal && (
        <div
          className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
          onClick={() => setShowModal(false)}
        >
          <div
            className="bg-gray-900 rounded-2xl p-6 w-full max-w-2xl space-y-4 max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-3">
              {badges}
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-500 hover:text-white text-xl leading-none"
              >
                ×
              </button>
            </div>

            {mention.reputation_score !== null && (
              <p className="text-sm text-gray-400">
                Score de reputação:{" "}
                <span className="text-white font-semibold">
                  {mention.reputation_score}/100
                </span>
              </p>
            )}

            {mention.author && (
              <p className="text-sm text-gray-500">{mention.author}</p>
            )}

            <p className="text-sm text-gray-200 whitespace-pre-wrap">
              {mention.content}
            </p>

            {mention.ai_summary && (
              <div className="border-l-2 border-gray-700 pl-3">
                <p className="text-xs text-gray-500 mb-1">Resumo da IA</p>
                <p className="text-sm text-gray-400 italic">
                  {mention.ai_summary}
                </p>
              </div>
            )}

            {mention.suggested_response && (
              <div className="bg-blue-950/40 border border-blue-800/40 rounded-lg p-4 space-y-2">
                <p className="text-xs text-blue-400 font-medium">
                  Resposta sugerida
                </p>
                <p className="text-sm text-blue-100">
                  {mention.suggested_response}
                </p>
              </div>
            )}

            {mention.source_url && (
              <a
                href={mention.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-400 hover:underline block"
              >
                Ver original →
              </a>
            )}

            <p className="text-xs text-gray-600">
              {new Date(mention.collected_at).toLocaleString("pt-BR")}
            </p>
          </div>
        </div>
      )}
    </>
  );
}
