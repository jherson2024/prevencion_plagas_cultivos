import React, { useState, useRef } from 'react';
import {
  subirImagen,
  crearUbicacion,
  crearCaptura,
} from '../../services/CapturaDatosCampo';

const SubirImagen = ({ UsuCod, MapParCod, mapaUrl }) => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [nota, setNota] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [subiendo, setSubiendo] = useState(false);
  const [coordenada, setCoordenada] = useState(null);
  const imgRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setMensaje('');
  };

  const handleClickEnMapa = (e) => {
    const rect = imgRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    setCoordenada({ x: parseFloat(x.toFixed(2)), y: parseFloat(y.toFixed(2)) });
  };

  const handleSubir = async () => {
    if (!file || !coordenada) {
      setMensaje('Selecciona una imagen y un punto en el mapa');
      return;
    }

    try {
      setSubiendo(true);
      // 1. Subir imagen
      const imagen = await subirImagen(file);
      const CapImaCod = imagen.ImaCod;

      // 2. Crear ubicación
      const ubicacion = await crearUbicacion({
        UbiMapParCod: MapParCod,
        UbiCoo: coordenada.x,
        UbiCooB: coordenada.y,
        UbiCom: nota,
      });
      const CapUbiCod = ubicacion.UbiCod;

      // 3. Crear captura
      await crearCaptura({
        CapUsuCod: UsuCod,
        CapImaCod,
        CapUbiCod,
        CapNot: nota,
      });

      setMensaje('✅ Captura registrada correctamente');
      setFile(null);
      setPreview(null);
      setNota('');
      setCoordenada(null);
    } catch (err) {
      console.error(err);
      setMensaje('❌ Error al registrar la captura');
    } finally {
      setSubiendo(false);
    }
  };

  return (
    <div>
      <h3>📍 Captura en Mapa de Parcela</h3>
      <input type="file" accept="image/*" onChange={handleFileChange} />

      {file && (
        <>
          <p>Haz clic en el mapa para marcar la ubicación de la imagen</p>
          <div style={{ position: 'relative', display: 'inline-block' }}>
            <img
              ref={imgRef}
              src={mapaUrl}
              alt="Mapa parcela"
              onClick={handleClickEnMapa}
              style={{ width: '100%', maxWidth: '600px', marginTop: '10px', border: '1px solid #ccc' }}
            />
            {coordenada && (
              <div
                style={{
                  position: 'absolute',
                  top: `${coordenada.y}%`,
                  left: `${coordenada.x}%`,
                  transform: 'translate(-50%, -50%)',
                  width: '10px',
                  height: '10px',
                  backgroundColor: 'red',
                  borderRadius: '50%',
                }}
              />
            )}
          </div>
        </>
      )}

      <textarea
        placeholder="Notas (opcional)"
        value={nota}
        onChange={(e) => setNota(e.target.value)}
        style={{ display: 'block', width: '100%', marginTop: '10px' }}
      />

      <button onClick={handleSubir} disabled={subiendo} style={{ marginTop: '10px' }}>
        {subiendo ? 'Registrando...' : 'Registrar Captura'}
      </button>

      {mensaje && <p style={{ marginTop: '10px' }}>{mensaje}</p>}
    </div>
  );
};

export default SubirImagen;
