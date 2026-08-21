/**
 * Service pour toutes les operations liees aux colis.
 * Encapsule les appels HTTP vers /colis, /colis/{id}, etc.
 */
import { api } from "../lib/api";

// Types partages avec le backend (miroir des schemas Pydantic)
export interface Colis {
  id: number;
  code_barres: string;
  telephone: string;
  statut: string;
  sent_at: string | null;
  reminder_sent_at: string | null;
  created_at: string;
}

export interface Adresse {
  id: number;
  colis_id: number;
  ligne1: string | null;
  ville: string | null;
  code_postal: string | null;
  latitude: number | null;
  longitude: number | null;
  source: string;
  extracted_at: string;
}

export interface ColisWithAdresse extends Colis {
  adresse: Adresse | null;
}

// Liste tous les colis (les plus recents en premier)
export async function listColis(): Promise<Colis[]> {
  const response = await api.get<Colis[]>("/colis");
  return response.data;
}

// Recupere un colis par son id avec son adresse
export async function getColis(id: number): Promise<ColisWithAdresse> {
  const response = await api.get<ColisWithAdresse>(`/colis/${id}`);
  return response.data;
}

// Cree un nouveau colis (declenche l envoi WhatsApp cote backend)
export async function createColis(code_barres: string, telephone: string): Promise<Colis> {
  const response = await api.post<Colis>("/colis", { code_barres, telephone });
  return response.data;
}