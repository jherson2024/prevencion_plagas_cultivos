import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import {
  crearParcela,
  listarParcelasPorUsuario,
  modificarParcela,
  eliminarParcela,
  listarZonas,
  crearCultivo,
  listarCultivosPorParcela,
  modificarCultivo,
  eliminarCultivo
} from '../../services/ZonaTrabajoMapeo';
import '../../css/styles.css';

const GestionParcelas = () => {
  const { user } = useAuth();
  const [parcelas, setParcelas] = useState([]);
  const [zonas, setZonas] = useState([]);
  const [form, setForm] = useState({
    MapZonGeoCod: '',
    MapNom: '',
    MapAnc: '',
    MapAlt: '',
    MapCom: '',
    archivo: null
  });
  const [editando, setEditando] = useState(null);
  const [mensaje, setMensaje] = useState('');
  const [cultivos, setCultivos] = useState({});
  const [cultivosRegistrados, setCultivosRegistrados] = useState({});
  const [editandoCultivo, setEditandoCultivo] = useState(null);
  const urlBase = api.defaults.baseURL;

  useEffect(() => {
    if (user?.UsuCod) {
      cargarParcelas();
      cargarZonas();
    }
  }, [user]);

  const cargarParcelas = async () => {
    const data = await listarParcelasPorUsuario(user.UsuCod);
    setParcelas(data);

    // Cargar cultivos de todas las parcelas
    data.forEach((p) => {
      cargarCultivos(p.MapCod);
    });
  };

  const cargarZonas = async () => {
    const data = await listarZonas();
    setZonas(data);
  };

  const cargarCultivos = async (parcelaId) => {
    const data = await listarCultivosPorParcela(parcelaId);
    setCultivosRegistrados((prev) => ({ ...prev, [parcelaId]: data }));
  };

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'archivo') {
      setForm({ ...form, archivo: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('MapUsuCod', user.UsuCod);
      formData.append('MapZonGeoCod', form.MapZonGeoCod);
      formData.append('MapNom', form.MapNom);
      formData.append('MapAnc', form.MapAnc);
      formData.append('MapAlt', form.MapAlt);
      formData.append('MapCom', form.MapCom);
      if (form.archivo) formData.append('archivo', form.archivo);

      if (editando) {
        await modificarParcela(editando, {
          MapNom: form.MapNom,
          MapAnc: form.MapAnc,
          MapAlt: form.MapAlt,
          MapCom: form.MapCom
        });
        setMensaje('Parcela modificada correctamente');
      } else {
        await crearParcela(formData);
        setMensaje('Parcela registrada con éxito');
      }

      setForm({
        MapZonGeoCod: '',
        MapNom: '',
        MapAnc: '',
        MapAlt: '',
        MapCom: '',
        archivo: null
      });
      setEditando(null);
      cargarParcelas();
    } catch (error) {
      console.error(error);
      setMensaje('Error al procesar la parcela');
    }
  };

  const handleEditar = (parcela) => {
    setForm({
      MapZonGeoCod: parcela.MapZonGeoCod,
      MapNom: parcela.MapNom,
      MapAnc: parcela.MapAnc,
      MapAlt: parcela.MapAlt,
      MapCom: parcela.MapCom,
      archivo: null
    });
    setEditando(parcela.MapCod);
  };

  const handleEliminar = async (MapCod) => {
    if (window.confirm('¿Eliminar esta parcela?')) {
      await eliminarParcela(MapCod);
      setMensaje('Parcela eliminada');
      cargarParcelas();
    }
  };

  const handleCultivoChange = (e, parcelaId) => {
    const { name, value } = e.target;
    setCultivos((prev) => ({
      ...prev,
      [parcelaId]: {
        ...prev[parcelaId],
        [name]: value,
      }
    }));
  };

  const handleCultivoSubmit = async (parcelaId) => {
    const cultivo = cultivos[parcelaId];
    if (!cultivo?.CulNomCul || !cultivo?.CulFecIni || !cultivo?.CulFecFin) {
      alert('Completa todos los campos del cultivo');
      return;
    }

    try {
      await crearCultivo({
        CulMapParCod: parcelaId,
        CulNomCul: cultivo.CulNomCul,
        CulFecIni: cultivo.CulFecIni,
        CulFecFin: cultivo.CulFecFin,
        CulObs: cultivo.CulObs || ''
      });
      setCultivos((prev) => ({ ...prev, [parcelaId]: {} }));
      await cargarCultivos(parcelaId);
    } catch (err) {
      console.error(err);
      alert('Error al registrar cultivo');
    }
  };

  const handleEditarCultivo = (cultivo) => {
    setEditandoCultivo(cultivo.CulCod);
    setCultivos((prev) => ({
      ...prev,
      [cultivo.CulMapParCod]: {
        CulNomCul: cultivo.CulNomCul,
        CulFecIni: cultivo.CulFecIni.split('T')[0],
        CulFecFin: cultivo.CulFecFin.split('T')[0],
        CulObs: cultivo.CulObs
      }
    }));
  };

  const handleGuardarModificacionCultivo = async (parcelaId, cultivoId) => {
    const cultivo = cultivos[parcelaId];
    await modificarCultivo(cultivoId, cultivo);
    setEditandoCultivo(null);
    await cargarCultivos(parcelaId);
  };

  const handleEliminarCultivo = async (parcelaId, cultivoId) => {
    await eliminarCultivo(cultivoId);
    await cargarCultivos(parcelaId);
  };

  return (
    <div className="contenedor-principal">
      <h2 className="titulo">Gestión de Parcelas</h2>
      {mensaje && <div className="mensaje">{mensaje}</div>}

      <form onSubmit={handleSubmit} className="formulario">
        <select name="MapZonGeoCod" value={form.MapZonGeoCod} onChange={handleChange} required>
          <option value="">Seleccionar zona geográfica</option>
          {zonas.map((zona) => (
            <option key={zona.ZonCod} value={zona.ZonCod}>{zona.ZonNom}</option>
          ))}
        </select>
        <input type="text" name="MapNom" placeholder="Nombre de la parcela" value={form.MapNom} onChange={handleChange} required />
        <input type="number" name="MapAnc" placeholder="Ancho (m)" value={form.MapAnc} onChange={handleChange} required />
        <input type="number" name="MapAlt" placeholder="Alto (m)" value={form.MapAlt} onChange={handleChange} required />
        <input type="text" name="MapCom" placeholder="Observaciones" value={form.MapCom} onChange={handleChange} />
        {!editando && (
          <input type="file" name="archivo" accept="image/*" onChange={handleChange} required />
        )}
        <button type="submit">{editando ? 'Modificar Parcela' : 'Registrar Parcela'}</button>
      </form>

      <div className="tabla-parcelas">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Dimensiones</th>
              <th>Observaciones</th>
              <th>Mapa</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {parcelas.map((p) => (
              <React.Fragment key={p.MapCod}>
                <tr>
                  <td>{p.MapNom}</td>
                  <td>{p.MapAnc} x {p.MapAlt} m</td>
                  <td>{p.MapCom}</td>
                  <td>
                    {p.MapImaMap && (
                      <img src={`${urlBase}/${p.MapImaMap}`} alt="mapa" width="100" />
                    )}
                  </td>
                  <td>
                    <button onClick={() => handleEditar(p)}>Editar</button>
                    <button onClick={() => handleEliminar(p.MapCod)}>Eliminar</button>
                  </td>
                </tr>
                <tr>
                  <td colSpan="5">
                    <div className="formulario-cultivo">
                      <input
                        type="text"
                        name="CulNomCul"
                        placeholder="Cultivo"
                        value={cultivos[p.MapCod]?.CulNomCul || ''}
                        onChange={(e) => handleCultivoChange(e, p.MapCod)}
                      />
                      <input
                        type="date"
                        name="CulFecIni"
                        value={cultivos[p.MapCod]?.CulFecIni || ''}
                        onChange={(e) => handleCultivoChange(e, p.MapCod)}
                      />
                      <input
                        type="date"
                        name="CulFecFin"
                        value={cultivos[p.MapCod]?.CulFecFin || ''}
                        onChange={(e) => handleCultivoChange(e, p.MapCod)}
                      />
                      <input
                        type="text"
                        name="CulObs"
                        placeholder="Observaciones"
                        value={cultivos[p.MapCod]?.CulObs || ''}
                        onChange={(e) => handleCultivoChange(e, p.MapCod)}
                      />
                      <button onClick={() => handleCultivoSubmit(p.MapCod)}>Registrar cultivo</button>
                    </div>

                    {cultivosRegistrados[p.MapCod]?.length > 0 && (
                      <table>
                        <thead>
                          <tr>
                            <th>Nombre</th>
                            <th>Inicio</th>
                            <th>Fin</th>
                            <th>Obs</th>
                            <th>Acciones</th>
                          </tr>
                        </thead>
                        <tbody>
                          {cultivosRegistrados[p.MapCod].map((c) => (
                            <tr key={c.CulCod}>
                              <td>
                                {editandoCultivo === c.CulCod ? (
                                  <input
                                    name="CulNomCul"
                                    value={cultivos[p.MapCod]?.CulNomCul || ''}
                                    onChange={(e) => handleCultivoChange(e, p.MapCod)}
                                  />
                                ) : c.CulNomCul}
                              </td>
                              <td>
                                {editandoCultivo === c.CulCod ? (
                                  <input
                                    type="date"
                                    name="CulFecIni"
                                    value={cultivos[p.MapCod]?.CulFecIni || ''}
                                    onChange={(e) => handleCultivoChange(e, p.MapCod)}
                                  />
                                ) : c.CulFecIni.split('T')[0]}
                              </td>
                              <td>
                                {editandoCultivo === c.CulCod ? (
                                  <input
                                    type="date"
                                    name="CulFecFin"
                                    value={cultivos[p.MapCod]?.CulFecFin || ''}
                                    onChange={(e) => handleCultivoChange(e, p.MapCod)}
                                  />
                                ) : c.CulFecFin.split('T')[0]}
                              </td>
                              <td>
                                {editandoCultivo === c.CulCod ? (
                                  <input
                                    name="CulObs"
                                    value={cultivos[p.MapCod]?.CulObs || ''}
                                    onChange={(e) => handleCultivoChange(e, p.MapCod)}
                                  />
                                ) : c.CulObs}
                              </td>
                              <td>
                                {editandoCultivo === c.CulCod ? (
                                  <button onClick={() => handleGuardarModificacionCultivo(p.MapCod, c.CulCod)}>Guardar</button>
                                ) : (
                                  <button onClick={() => handleEditarCultivo(c)}>Editar</button>
                                )}
                                <button onClick={() => handleEliminarCultivo(p.MapCod, c.CulCod)}>Eliminar</button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </td>
                </tr>
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default GestionParcelas;
