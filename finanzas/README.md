# Mis Finanzas — guía de la app

App personal de gastos, gastos fijos, precios y deudas. Tema oscuro, en pesos.
Vive en la carpeta `finanzas/` del repo de Mis Hábitos y no comparte código con esa app.

- Sitio: https://santistark-ctrl.github.io/Mis-Habitos/finanzas/
- Archivos: `index.html` (toda la app, HTML + CSS + JS sin dependencias), `manifest.json`, `icon-192.png`, `icon-512.png`.
- Se edita directo `index.html`; no hay paso de armado. Publicar: commit y push a `main`.

## Pantallas

- **Inicio:** gasto de hoy, de la semana (lunes a domingo) y del mes, presupuesto, saldo de deudas, próximos fijos y últimos gastos. El botón + carga un gasto.
- **Gastos:** lista por día con búsqueda, filtro por categoría y por mes; resumen con total, comparación con el mes anterior, barras por categoría y presupuestos; dividir un gasto; exportar a planilla (CSV).
- **Gasto con productos:** al cargar un gasto se pueden elegir productos de Precios (o crear uno nuevo) con cantidad y precio; el monto pasa a ser la suma y queda bloqueado. Se guarda en `gasto.items` (`{prod, nombre, cant, precio}`) y `gasto.lugar`, y cada precio se agrega al historial del producto si no estaba para esa fecha.
- **Fijos:** suscripciones mensuales o anuales. El día del cobro se anota solo un gasto. Se pueden pausar.
- **Precios:** productos con historial de precios, variación y comparación entre lugares. "También lo compré" anota el gasto.
- **Deudas:** personas con saldo (te debe / le debés), préstamos, pagos parciales e historial.
- **Ajustes (⚙):** presupuesto general, categorías (crear, renombrar, borrar, presupuesto por categoría), sincronización, exportar e importar.

## Datos (localStorage, prefijo `mis-finanzas:`)

- `data`: `{v, cfg:{presu,upd}, gastos, cats, prods, precios, personas, movs, fijos}`. Cada colección es un objeto por `id`; cada registro lleva `upd` (fecha de modificación) y, si se borró, `del:1`.
- No se sincronizan: `token`, `gist`, `ultima-sync`.
- Gasto generado por un fijo: id `fx-<idFijo>-<AAAA-MM>`. Por eso no se duplica entre dispositivos y, si se borra a mano, no vuelve.
- Movimientos de deuda: `presto` y `lepague` suman a lo que te deben; `meprestaron` y `mepago` restan.

## Sincronización

- Usa un Gist privado propio (archivo `mis-finanzas-sync.json`). Toma el token de `mis-finanzas:token` y, si no hay, el de Mis Hábitos (`rastreador-habitos:sync-token`), que está en el mismo origen.
- Combina sola, registro por registro: gana el que se modificó más tarde. No hay avisos de conflicto ni recargas.
- Sincroniza al abrir, 2,5 s después de cada cambio, al volver a la ventana, al recuperar la conexión y cada 60 s con la ventana visible.
- Si la copia de la nube no se puede leer, no la pisa. Si hay más de un Gist de finanzas en la cuenta, todos los dispositivos usan el más viejo.
