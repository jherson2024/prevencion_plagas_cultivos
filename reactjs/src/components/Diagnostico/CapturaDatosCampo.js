import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import {
  listarParcelasPorUsuario
} from '../../services/ZonaTrabajoMapeo';
import SubirImagen from './SubirImagen';
import SeleccionarUbicacion from './SeleccionarUbicacion';
import { listarCapturas } from '../../services/CapturaDatosCampo';

const CapturaDatosCampo = ({ UsuCod }) => {
  const [parcelas, setParcelas] = useState([]);
  const [parcelaSeleccionada, setParcelaSeleccionada] = useState(null);
  const [historial, setHistorial] = useState([]);
  const API_BASE = api.defaults.baseURL;

  useEffect(() => {
    const cargarParcelas = async () => {
      try {
        const data = await listarParcelasPorUsuario(UsuCod);
        setParcelas(data); // ya no transformamos MapImaMap
      } catch (err) {
        console.error('Error al cargar parcelas', err);
      }
    };

    cargarParcelas();
  }, [UsuCod]);

  const handleSeleccionarParcela = async (mapa) => {
    setParcelaSeleccionada(mapa);
    try {
      const capturas = await listarCapturas({
        usuarioId: UsuCod,
        parcelaId: mapa.MapCod,
      });
      setHistorial(capturas);
    } catch (err) {
      console.error('Error al cargar capturas', err);
    }
  };

  return (
    <div>
      <h2>🧭 Seleccionar Parcela</h2>
      <select onChange={(e) => {
        const index = e.target.value;
        if (index !== '') handleSeleccionarParcela(parcelas[index]);
      }}>
        <option value="">-- Elegir parcela --</option>
        {parcelas.map((p, idx) => (
          <option key={p.MapCod} value={idx}>
            {p.MapNom}
          </option>
        ))}
      </select>

      {parcelaSeleccionada && (
        <>
          <h3>🌿 Parcela: {parcelaSeleccionada.MapNom}</h3>
          <p><strong>Dimensiones:</strong> {parcelaSeleccionada.MapAnc} x {parcelaSeleccionada.MapAlt}</p>

          <SubirImagen
            UsuCod={UsuCod}
            MapParCod={parcelaSeleccionada.MapCod}
            mapaUrl={`${API_BASE}/${parcelaSeleccionada.MapImaMap}`}
          />
          <SeleccionarUbicacion
            MapParCod={parcelaSeleccionada.MapCod}
            mapaUrl={`${API_BASE}/${parcelaSeleccionada.MapImaMap}`}
          />

          <hr />
          <h3>📋 Historial de Capturas</h3>
          {historial.length === 0 ? (
            <p>No hay capturas aún.</p>
          ) : (
            <div style={{ display: 'grid', gap: '1rem' }}>
              {historial.map((cap) => (
                <div key={cap.CapCod} style={{ border: '1px solid #ccc', padding: '1rem' }}>
                  <img src={`${API_BASE}${cap.ImaUrl}`} alt="captura" width="200" />
                  <p><strong>Notas:</strong> {cap.CapNot}</p>
                  <p><strong>Ubicación:</strong> ({cap.UbiCoo}%, {cap.UbiCooB}%)</p>
                  <p><strong>Fecha:</strong> {cap.CapFec}</p>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CapturaDatosCampo;
