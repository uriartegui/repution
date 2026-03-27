"use client";

import { useState } from "react";
import { Company, createMention } from "@/lib/api";

interface Props {
  companies: Company[];
  onClose: () => void;
  onCreated: () => void;
}

export default function AddMentionModal({
  companies,
  onClose,
  onCreated,
}: Props) {
  const [form, setForm] = useState({
    company_id: companies[0]?.id ?? 0,
    source: "google",
    author: "",
    content: "",
  });
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    await createMention({
      ...form,
      author: form.author || undefined,
    });
    setLoading(false);
    onCreated();
  }

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-2xl p-6 w-full max-w-lg space-y-4">
        <h2 className="text-lg font-semibold">Nova menção</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm text-gray-400 block mb-1">Empresa</label>
            <select
              className="w-full bg-gray-800 text-white rounded-lg px-3 py-2 text-sm"
              value={form.company_id}
              onChange={(e) =>
                setForm({ ...form, company_id: Number(e.target.value) })
              }
            >
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-400 block mb-1">Fonte</label>
            <select
              className="w-full bg-gray-800 text-white rounded-lg px-3 py-2 text-sm"
              value={form.source}
              onChange={(e) => setForm({ ...form, source: e.target.value })}
            >
              <option value="google">Google</option>
              <option value="instagram">Instagram</option>
              <option value="twitter">Twitter/X</option>
              <option value="reclame_aqui">Reclame Aqui</option>
              <option value="facebook">Facebook</option>
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-400 block mb-1">
              Autor (opcional)
            </label>
            <input
              className="w-full bg-gray-800 text-white rounded-lg px-3 py-2 text-sm"
              placeholder="Nome do autor"
              value={form.author}
              onChange={(e) => setForm({ ...form, author: e.target.value })}
            />
          </div>

          <div>
            <label className="text-sm text-gray-400 block mb-1">
              Conteúdo da menção
            </label>
            <textarea
              className="w-full bg-gray-800 text-white rounded-lg px-3 py-2 text-sm min-h-[100px]"
              placeholder="Cole aqui o texto da menção..."
              required
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
            />
          </div>

          <div className="flex gap-3 justify-end">
            <button
              type="button"
              onClick={onClose}
              className="text-sm text-gray-400 hover:text-white transition px-4 py-2"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-sm font-medium px-5 py-2 rounded-lg transition"
            >
              {loading ? "Analisando..." : "Analisar com IA"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
