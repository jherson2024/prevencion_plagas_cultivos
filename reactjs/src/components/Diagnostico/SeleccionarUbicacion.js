import React, { useRef, useState } from 'react';
import { crearUbicacion } from '../../services/CapturaDatosCampo';

const SeleccionarUbicacion = ({ MapParCod, mapaUrl }) => {
  const [coordenadas, setCoordenadas] = useState([]);
  const [comentario, setComentario] = useState('');
  const [mensaje, setMensaje] = useState('');
  const imgRef = useRef(null);

  const manejarClick = async (e) => {
    const rect = imgRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    const nuevaUbicacion = {
      UbiMapParCod: MapParCod,
      UbiCoo: parseFloat(x.toFixed(2)),
      UbiCooB: parseFloat(y.toFixed(2)),
      UbiCom: comentario,
    };

    try {
      const res = await crearUbicacion(nuevaUbicacion);
      setCoordenadas([...coordenadas, { ...nuevaUbicacion, UbiCod: res.UbiCod }]);
      setComentario('');
      setMensaje('📍 Punto registrado correctamente');
    } catch (err) {
      console.error(err);
      setMensaje('❌ Error al registrar punto');
    }
  };

  return (
    <div>
      <h3>🗺️ Seleccionar puntos en mapa de parcela</h3>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <img
          ref={imgRef}
          src={mapaUrl}
          alt="Mapa parcela"
          onClick={manejarClick}
          style={{ width: '100%', maxWidth: '600px', border: '1px solid #ccc' }}
        />
        {coordenadas.map((coord, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              top: `${coord.UbiCooB}%`,
              left: `${coord.UbiCoo}%`,
              transform: 'translate(-50%, -50%)',
              width: '10px',
              height: '10px',
              backgroundColor: 'red',
              borderRadius: '50%',
            }}
            title={coord.UbiCom}
          />
        ))}
      </div>

      <textarea
        value={comentario}
        onChange={(e) => setComentario(e.target.value)}
        placeholder="Comentario (opcional)"
        style={{ display: 'block', marginTop: '10px', width: '100%' }}
      />

      {mensaje && <p>{mensaje}</p>}
    </div>
  );
};

export default SeleccionarUbicacion;
