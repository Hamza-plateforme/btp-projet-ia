
'use client';

import React, { useState } from "react";

export default function FeedbackForm() {
  const [feedback, setFeedback] = useState('');
  const [result, setResult] = useState<any>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setResult(null);
    const response = await fetch('http://localhost:5000/analyse-feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback }),
    });
    const data = await response.json();
    setResult(data);
  }

  return (
    <div style={{
      padding: 32,
      maxWidth: 600,
      margin: "40px auto",
      background: "#18192b",
      borderRadius: 18,
      boxShadow: "0 8px 34px 0 #212a4670",
      color: "#f7fafc",
      fontFamily: "Inter, Arial, sans-serif"
    }}>
      <img src="/logo.png" alt="Logo RetroMind"
        style={{
          width: 120, margin: "0 auto 20px auto", display: "block", borderRadius: 16
        }} />
      <h1 style={{ textAlign: "center", marginBottom: 20, fontSize: 32, color: "#69a8ea" }}>
        RetroMind – Assistant d'équipe IA
      </h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={feedback}
          onChange={e => setFeedback(e.target.value)}
          rows={4}
          cols={60}
          placeholder="Exprime ton feedback ici..."
          style={{
            width: "100%",
            borderRadius: 8,
            padding: 12,
            border: "1px solid #333",
            marginBottom: 16,
            fontSize: 17
          }}
        />
        <br />
        <button type="submit" style={{
          background: "#69a8ea",
          color: "#fff",
          fontWeight: "bold",
          padding: "10px 24px",
          border: "none",
          borderRadius: 8,
          fontSize: 18,
          cursor: "pointer"
        }}>Analyser</button>
      </form>
      {result && (
        <div style={{ marginTop: 28 }}>
          <h3 style={{ color: "#80ffd0" }}>Analyse IA :</h3>
          <p><b>Synthèse</b> : {result.synthese}</p>
          <p><b>Émotion</b> : {result.emotion}</p>
          <p><b>Thème</b> : {result.theme}</p>
          <p><b>Suggestion</b> : {result.suggestion}</p>
        </div>
      )}
    </div>
  );
}
