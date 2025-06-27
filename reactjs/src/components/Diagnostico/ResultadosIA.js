import React, { useEffect, useState } from 'react';
import { listarParcelasPorUsuario } from '../../services/ZonaTrabajoMapeo';
import { listarCapturas, detectarPlaga } from '../../services/CapturaDatosCampo';
import api from '../../services/api';

const ResultadosIA = ({ UsuCod }) => {
  const [parcelas, setParcelas] = useState([]);
  const [parcelaSeleccionada, setParcelaSeleccionada] = useState(null);
  const [capturas, setCapturas] = useState([]);
  const [resultadosIA, setResultadosIA] = useState({}); // clave: cap.CapCod
  const [procesando, setProcesando] = useState({}); // para mostrar loading por captura

  const API_BASE = api.defaults.baseURL;

  useEffect(() => {
    const cargarParcelas = async () => {
      try {
        const data = await listarParcelasPorUsuario(UsuCod);
        setParcelas(data);
      } catch (error) {
        console.error('Error al cargar parcelas:', error);
      }
    };

    cargarParcelas();
  }, [UsuCod]);

  const handleSeleccionarParcela = async (mapa) => {
    setParcelaSeleccionada(mapa);
    try {
      const data = await listarCapturas({ usuarioId: UsuCod, parcelaId: mapa.MapCod });
      setCapturas(data);
    } catch (error) {
      console.error('Error al cargar capturas:', error);
    }
  };

  const analizarCaptura = async (capCod, iaNombre) => {
    try {
      setProcesando((prev) => ({ ...prev, [capCod]: true }));
      const resultado = await detectarPlaga({ cap_cod: capCod, ia_nombre: iaNombre });
      console.log("resultado recibido")
      console.log(resultado) 
      setResultadosIA((prev) => ({ ...prev, [capCod]: resultado }));
    } catch (error) {
      console.error('Error al analizar imagen:', error);
      alert('Error al procesar con IA');
    } finally {
      setProcesando((prev) => ({ ...prev, [capCod]: false }));
    }
  };

  return (
    <div>
      <h2> Resultados de análisis con IA</h2>

      <label>Seleccionar parcela:</label>
      <select onChange={(e) => {
        const idx = e.target.value;
        if (idx !== '') handleSeleccionarParcela(parcelas[idx]);
      }}>
        <option value="">-- Elige una parcela --</option>
        {parcelas.map((p, idx) => (
          <option key={p.MapCod} value={idx}>{p.MapNom}</option>
        ))}
      </select>

      {capturas.length > 0 && (
        <div style={{ marginTop: '1rem' }}>
          <h3> Capturas en esta parcela</h3>
          <div style={{ display: 'grid', gap: '1rem' }}>
            {capturas.map((cap) => (
              <div key={cap.CapCod} style={{ border: '1px solid #ccc', padding: '1rem' }}>
                <img src={`${API_BASE}${cap.ImaUrl}`} alt="Captura" width="200" />
                <p><strong>Notas:</strong> {cap.CapNot}</p>

                <div>
                  <button disabled={procesando[cap.CapCod]} onClick={() => analizarCaptura(cap.CapCod, 'chatgpt')}> ChatGPT</button>
                  <button disabled={procesando[cap.CapCod]} onClick={() => analizarCaptura(cap.CapCod, 'gemini')}> Gemini</button>
                  <button disabled={procesando[cap.CapCod]} onClick={() => analizarCaptura(cap.CapCod, 'deepseck')}> DeepSeck</button>
                </div>

                {procesando[cap.CapCod] && <p>  Analizando con IA...</p>}

                {resultadosIA[cap.CapCod] && (
                  <div style={{ marginTop: '0.5rem', background: '#eef', padding: '0.5rem' }}>
                    <h4> ^=   Resultado ({resultadosIA[cap.CapCod].ia_nombre}):</h4>
                    <p><strong>Plaga detectada?</strong> {resultadosIA[cap.CapCod].PlaDet ? 'Si' : 'No'}</p>
                    <p><strong>Nombre:</strong> {resultadosIA[cap.CapCod].NomPla || 'Ninguna'}</p>
                    <p><strong>Severidad:</strong> {resultadosIA[cap.CapCod].SevPla || 'N/A'}</p>
                    <p><strong>Acciones:</strong> {resultadosIA[cap.CapCod].AccRec || 'Ninguna'}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultadosIA;
