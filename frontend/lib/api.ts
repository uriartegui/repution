const API_URL = "http://localhost:8000/api/v1";

export interface Company {
  id: number;
  name: string;
  slug: string;
  keywords: string | null;
  brand_tone: string;
  created_at: string;
}

export interface Mention {
  id: number;
  company_id: number;
  source: string;
  source_url: string | null;
  author: string | null;
  content: string;
  sentiment: string | null;
  mention_type: string | null;
  reputation_score: number | null;
  ai_summary: string | null;
  suggested_response: string | null;
  status: string;
  collected_at: string;
}

export async function getCompanies(): Promise<Company[]> {
  const res = await fetch(`${API_URL}/companies/`, { cache: "no-store" });
  return res.json();
}

export async function getMentions(company_id?: number): Promise<Mention[]> {
  const url = company_id
    ? `${API_URL}/mentions/?company_id=${company_id}`
    : `${API_URL}/mentions/`;
  const res = await fetch(url, { cache: "no-store" });
  return res.json();
}

export async function createCompany(data: Omit<Company, "id" | "created_at">) {
  const res = await fetch(`${API_URL}/companies/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function createMention(data: {
  company_id: number;
  source: string;
  author?: string;
  content: string;
}) {
  const res = await fetch(`${API_URL}/mentions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function triggerCollect(company_id?: number) {
  const url = company_id
    ? `${API_URL}/collect/${company_id}`
    : `${API_URL}/collect/`;
  const res = await fetch(url, { method: "POST" });
  return res.json();
}
