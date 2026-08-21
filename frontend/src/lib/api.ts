/**
 * Client HTTP centralise pour appeler l API backend FastAPI.
 * 
 * Ajoute automatiquement le token JWT dans les headers de chaque requete.
 * Redirige vers /login si le token est invalide/expire (401).
 */
import axios from "axios";

// URL de base du backend FastAPI (change en production)
const API_BASE_URL = "http://localhost:8000";

// Instance axios configuree
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor : ajoute automatiquement le token JWT dans chaque requete
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor de reponse : si 401 (token invalide), on vire l utilisateur
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expire ou invalide
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      // Rediriger vers login (seulement si on nest pas deja sur /login)
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);