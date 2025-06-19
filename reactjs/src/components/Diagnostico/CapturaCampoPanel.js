import React, { useState, useEffect } from 'react';
import SubirImagen from './SubirImagen';
import SeleccionarUbicacion from './SeleccionarUbicacion';
import { listarCapturas } from '../../services/CapturaDatosCampo';

const CapturaCampoPanel = ({ UsuCod, MapParCod, mapaUrl }) => {
  const [historial, setHistorial] = useState([]);

  const cargarHistorial = async () => {
    try {
      const data = await listarCapturas({ usuarioId: UsuCod, parcelaId: MapParCod });
      setHistorial(data);
    } catch (error) {
      console.error('Error al cargar historial de capturas', error);
    }
  };

  useEffect(() => {
    cargarHistorial();
  }, [UsuCod, MapParCod]);

  return (
    <div>
      <h2>📋 Panel de Captura de Datos de Campo</h2>

      <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
        <div style={{ flex: 1 }}>
          <SubirImagen UsuCod={UsuCod} MapParCod={MapParCod} />
        </div>

        <div style={{ flex: 1 }}>
          <SeleccionarUbicacion MapParCod={MapParCod} mapaUrl={mapaUrl} />
        </div>
      </div>

      <hr style={{ margin: '2rem 0' }} />

      <h3>🖼️ Historial de Capturas</h3>
      {historial.length === 0 ? (
        <p>No hay capturas registradas todavía.</p>
      ) : (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {historial.map((cap) => (
            <div key={cap.CapCod} style={{ border: '1px solid #ddd', padding: '1rem' }}>
              <img src={cap.ImaUrl} alt="captura" width="200" />
              <p><strong>Notas:</strong> {cap.CapNot}</p>
              <p><strong>Fecha:</strong> {cap.CapFec}</p>
              <p><strong>Ubicación:</strong> ({cap.UbiCoo.toFixed(2)}%, {cap.UbiCooB.toFixed(2)}%)</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CapturaCampoPanel;
