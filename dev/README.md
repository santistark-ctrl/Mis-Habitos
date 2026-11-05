# Mis Hábitos — guía para editar y publicar

App personal de hábitos, Foco (pomodoro), Estado (notas por materia) y Plan (planificador de estudio).
Se usa desde el navegador en notebook y PC, y como app instalada en el celular.
Los datos se sincronizan entre dispositivos con un Gist privado de GitHub.

- Sitio: https://santistark-ctrl.github.io/Mis-Habitos/ (GitHub Pages, rama `main`, raíz del repo)
- Repo: https://github.com/santistark-ctrl/Mis-Habitos

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La app completa (bundle). Es lo que se publica. **Es la fuente de verdad.** |
| `sw.js` | Service worker *network-first*: si hay internet siempre baja la versión nueva; sin internet usa la última guardada. |
| `.nojekyll` | Para que Pages sirva los archivos tal cual. |
| `dev/tool.py` | Desarma y vuelve a armar `index.html` para poder editarlo. |

## Cómo editar (paso a paso)

1. Cloná el repo y entrá a la carpeta.
2. `python3 dev/tool.py check`: confirma que el desarmado y armado de `index.html` deja el archivo idéntico.
3. `python3 dev/tool.py unpack`: crea `dev/work/` (no se sube a git) con:
   - `template.html`: la app (HTML + React por runtime x-dc con `<sc-if>` / `<sc-for>` y `{{ }}`). La instancia del componente queda en `window.__fusInst`.
   - `widget.js`: el planificador (pestaña 🗓️ Plan y la tarjeta "Hoy toca" en Foco › Estudio).
   - `sync.js`: la sincronización con GitHub (el chip ☁ arriba a la izquierda).
4. Editá esos archivos. Conviene hacer reemplazos de texto exactos y verificar que cada uno aparezca una sola vez.
5. `python3 dev/tool.py pack`: rearma `index.html` (verifica la sintaxis JS con `node --check` si está instalado).
6. Probalo localmente: `python3 -m http.server` y abrí `http://localhost:8000/`. Con Playwright se puede automatizar; el fondo WebGL hace lenta la carga, conviene usar `page.evaluate(...click())`.
7. Commit y push a `main`. Pages publica en 1 o 2 minutos.
8. En cada dispositivo, recargar con **Ctrl + F5** (en el celu, cerrar y abrir la app).

No cambiar nada que no se pidió: el dueño quiere que la app no se rompa ni cambie de más.

## Datos (localStorage, prefijo `rastreador-habitos:`)

- `v1` hábitos · `fusion` rituales/foco por día/materias/notas · `pomodoro` materias, duración, segundos por materia, historial
- `juego` · `pausa` · `name` · `wallpaper` · `plan-estudio` (evaluaciones, ajustes, feriados/paros, log)
- No se sincronizan: `sync-*` (token, gist, meta, backup, dispositivo, usuario), `plan-estudio-ui`, `foco-vivo` (foco en curso, sobrevive a recargas).

## Planificador (widget.js)

- 1 h de plan = 1 pomodoro (foco + descanso, p. ej. 50 + 10 min). Las horas hechas se calculan con los minutos de Foco.
- Modos Auto (reparte según importancia y fecha) y Manual (horas por día de la semana, más cambios por día).
- Días libres, feriados y paros, con horas disponibles por día.
- Vistas: Evaluaciones (Editar cambia la fecha y todo lo demás), Horario, Calendario, Ajustes.
- Viaja en Exportar/Importar de la app (`planEstudio`).

## Sincronización (sync.js)

- Cada dispositivo pega una vez un token de GitHub con permiso **gist**. El token queda solo en ese navegador: nunca va al código, ni al repo, ni al chat.
- Archivo `mis-habitos-sync.json` en un Gist privado: `{app, v, rev, pushId, hist, updatedAt, device, data:{clave:valor}}`.
- Detecta cambios envolviendo `localStorage.setItem` y `removeItem`. Sube 3 s después del cambio (como máximo 15 s). Antes de subir, siempre lee la nube.
- Si la nube cambió y este dispositivo no tiene cambios propios, baja los datos y recarga la página. Si los dos cambiaron, muestra un aviso con tres opciones: **Combinar las dos** (recomendada: suma pomodoros, hábitos y notas), Solo la del otro, o Solo la de este. Lo que se descarta queda como copia restaurable.
- `hist` (últimos pushIds) detecta cuando otro dispositivo guardó sin ver lo último que subió este.
- Si hay más de un Gist de sincronización en la cuenta, todos los dispositivos pasan al **más viejo** y el que cambia de copia combina sus datos.
- Robustez:
  - Timeout de 20 s por pedido.
  - Si una sincronización queda trabada, se libera a los 60 s.
  - Revisa la nube cada 45 s con la ventana visible, al volver a la ventana, al recuperar la conexión y si pasaron más de 2 min sin comprobar.
  - Si hay otra pestaña de la app abierta en el mismo navegador y cambia los datos, esta se recarga.
- El panel ☁ muestra la versión (#rev), quién la subió, la copia de la nube (primeros 6 caracteres del Gist) y los minutos de foco de hoy. Si dos dispositivos muestran la misma versión y la misma copia, tienen los mismos datos.

## Problemas ya resueltos (por si reaparecen)

- **Un dispositivo no recibe datos aunque esté en verde:**
  - Comparar en ☁ la "Copia en la nube". Si es distinta, había dos Gists; ahora se unifican solos.
  - Comparar la versión. Si está atrasada, recargar con Ctrl + F5.
- **Una pestaña abierta durante días no sincronizaba:** un pedido colgado dejaba la sincronización trabada. Se resolvió con el timeout y la liberación automática.
- **Un modal oculto bloqueaba los clics:** `.me-modal` usa `display:flex`, así que hace falta `[hidden]{display:none!important}`.
- **En el celular la página se desbordaba:** la grilla de 14 días necesita `minmax(0,1fr)`.
- **Pausa de hábitos:** el cargador tiene que conservar `pausaDesde` y `pausas`.
