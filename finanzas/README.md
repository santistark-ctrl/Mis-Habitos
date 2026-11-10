# Mis Finanzas — guía de la app

App personal de gastos, gastos fijos, precios y deudas. Tema oscuro, en pesos.
Vive en la carpeta `finanzas/` del repo de Mis Hábitos y no comparte código con esa app.

- Sitio: https://santistark-ctrl.github.io/Mis-Habitos/finanzas/
- Archivos: `index.html` (toda la app, HTML + CSS + JS sin dependencias), `manifest.json`, `icon-192.png`, `icon-512.png`.
- Se edita directo `index.html`; no hay paso de armado. Publicar: commit y push a `main`.

## Pantallas

- **Inicio:** dos cuadros de presupuesto (mes y semana), saldo de deudas, próximos fijos, últimas compras e historial por semanas o meses. El botón + carga un gasto.
  - Cuadro del mes: cuánto queda, si vas bajo o sobre el ritmo (presupuesto × día del mes ÷ días del mes − gastado), barra con la marca de hoy y cuánto podés gastar por día.
  - Cuadro de la semana (lunes a domingo): cuánto queda, una barra por día (roja si ese día superó la séptima parte del semanal) y promedio por día.
  - Historial: usa el presupuesto actual para comparar los períodos pasados; no guarda presupuestos viejos.
- **Gastos:** lista por día con búsqueda, filtro por categoría y por mes; resumen con total, comparación con el mes anterior, barras por categoría y presupuestos; dividir un gasto; exportar a planilla (CSV).
- **Gasto con productos:** al cargar un gasto se pueden elegir productos de Precios (o crear uno nuevo) con cantidad y precio; el monto pasa a ser la suma y queda bloqueado. Se guarda en `gasto.items` (`{prod, nombre, cant, precio}`) y `gasto.lugar`, y cada precio se agrega al historial del producto si no estaba para esa fecha.
- **Fijos:** suscripciones mensuales o anuales. El día del cobro se anota solo un gasto. Se pueden pausar.
- **Precios:** productos con historial de precios, variación y comparación entre lugares. "También lo compré" anota el gasto.
- **Deudas:** personas con saldo (te debe / le debés), préstamos, pagos parciales e historial.
- **Ajustes (⚙):** presupuesto general, categorías (crear, renombrar, borrar, presupuesto por categoría), sincronización, exportar e importar.

## Datos (localStorage, prefijo `mis-finanzas:`)

- `data`: `{v, cfg:{presu,upd}, gastos, cats, prods, precios, personas, movs, fijos}`. Cada colección es un objeto por `id`; cada registro lleva `upd` (fecha de modificación) y, si se borró, `del:1`.
- `cfg.presu` es el presupuesto mensual y `cfg.presuSem` el semanal; si el semanal es 0 se usa la parte proporcional del mensual.
- No se sincronizan: `token`, `gist`, `ultima-sync`, `fondo` (fondo animado activado o no en ese dispositivo).
- Gasto generado por un fijo: id `fx-<idFijo>-<AAAA-MM>`. Por eso no se duplica entre dispositivos y, si se borra a mano, no vuelve.
- Movimientos de deuda: `presto` y `lepague` suman a lo que te deben; `meprestaron` y `mepago` restan.

## Sincronización

- Usa un Gist privado propio (archivo `mis-finanzas-sync.json`). Toma el token de `mis-finanzas:token` y, si no hay, el de Mis Hábitos (`rastreador-habitos:sync-token`), que está en el mismo origen.
- Combina sola, registro por registro: gana el que se modificó más tarde. No hay avisos de conflicto ni recargas.
- Sincroniza al abrir, 2,5 s después de cada cambio, al volver a la ventana, al recuperar la conexión y cada 60 s con la ventana visible.
- Si la copia de la nube no se puede leer, no la pisa. Si hay más de un Gist de finanzas en la cuenta, todos los dispositivos usan el más viejo.

## Fondo animado

- Viene del diseño "Fondo calmo finanzas" (Claude Design). Está en `<div id="fondo">` al principio del body: manchas de color, aro, la imagen `fondo-cara.png`, puntos que suben y tres capas de olas.
- Las olas son tres SVG que llegan todos hasta el borde inferior y se superponen (por eso no quedan huecos). Cada trazo se repite cada 390 unidades, así el desplazamiento de −50% hace un ciclo sin corte.
- Es solo CSS. Se apaga en Ajustes › Apariencia y respeta "reducir movimiento" del sistema.
