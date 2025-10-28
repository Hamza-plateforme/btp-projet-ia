'use client';

import React, { useEffect, useState } from "react";

export default function Feedbacks() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://localhost:5000/historique')
      .then(res => res.json())
      .then(setFeedbacks);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Historique des feedbacks analysés</h2>
      <ul>
        {feedbacks.map((fb, idx) => (
          <li key={idx} style={{ marginBottom: 20 }}>
            <b>Feedback :</b> {fb.feedback}<br/>
            <b>Synthèse :</b> {fb.synthese}<br/>
            <b>Émotion :</b> {fb.emotions}<br/>
            <b>Suggestion :</b> {fb.suggestion}
          </li>
        ))}
      </ul>
    </div>
  );
}
