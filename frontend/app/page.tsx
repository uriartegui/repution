"use client";

import { useEffect, useState } from "react";
import { getMentions, getCompanies, triggerCollect, Company, Mention } from "@/lib/api";
import MentionCard from "@/components/MentionCard";
import StatsBar from "@/components/StatsBar";
import AddMentionModal from "@/components/AddMentionModal";

export default function Home() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [mentions, setMentions] = useState<Mention[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [collecting, setCollecting] = useState(false);

  async function load(companyId?: number) {
    setLoading(true);
    const [c, m] = await Promise.all([
      getCompanies(),
      getMentions(companyId),
    ]);
    setCompanies(c);
    setMentions(m);
    setLoading(false);
  }

  useEffect(() => {
    load(selectedCompany ?? undefined);
  }, [selectedCompany]);

  async function handleCollect() {
    setCollecting(true);
    await triggerCollect(selectedCompany ?? undefined);
    setTimeout(() => {
      load(selectedCompany ?? undefined);
      setCollecting(false);
    }, 30000);
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-5xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Repution</h1>
            <p className="text-gray-400 text-sm">Monitoramento de reputação</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleCollect}
              disabled={collecting}
              className="bg-gray-800 hover:bg-gray-700 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
            >
              {collecting ? "Coletando..." : "⟳ Coletar agora"}
            </button>
            <button
              onClick={() => setShowModal(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
            >
              + Nova menção
            </button>
          </div>
        </div>

        {/* Filtro por empresa */}
        {companies.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setSelectedCompany(null)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition ${
                selectedCompany === null
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-400 hover:bg-gray-700"
              }`}
            >
              Todas
            </button>
            {companies.map((c) => (
              <button
                key={c.id}
                onClick={() => setSelectedCompany(c.id)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition ${
                  selectedCompany === c.id
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                }`}
              >
                {c.name}
              </button>
            ))}
          </div>
        )}

        {/* Stats */}
        <StatsBar mentions={mentions} />

        {/* Lista de menções */}
        {loading ? (
          <p className="text-gray-500 text-center py-12">Carregando...</p>
        ) : mentions.length === 0 ? (
          <p className="text-gray-500 text-center py-12">Nenhuma menção encontrada.</p>
        ) : (
          <div className="space-y-3">
            {mentions.map((m) => (
              <MentionCard key={m.id} mention={m} />
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <AddMentionModal
          companies={companies}
          onClose={() => setShowModal(false)}
          onCreated={() => {
            setShowModal(false);
            load(selectedCompany ?? undefined);
          }}
        />
      )}
    </main>
  );
}
