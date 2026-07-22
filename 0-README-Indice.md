# 0 · Japón 2027 — Índice del proyecto

Carpeta maestra del viaje (pareja · 28 oct – 23 nov 2027). Todo está numerado y
ordenado para que no haya desorden.

```
Japon-2027/
├── CLAUDE.md                           ← briefing para AI (lee esto primero)
├── capture.md                          ← captura rápida desde cualquier dispositivo
├── 0-README-Indice.md                  ← este archivo (empieza aquí)
├── 1-Dashboard-Interactivo/
│   └── 1.1-Documento-Maestro-Japon-2027.html   ← ábrelo con doble clic (8 pestañas)
├── 2-Datos-del-Viaje/
│   └── 2.1-Datos-e-Items-Completos.md           ← todos los datos, tablas e items
├── 3-Publicacion-Web/
│   ├── index.html                               ← copia lista para GitHub Pages
│   └── 3.1-Instrucciones-GitHub-Pages.md        ← cómo publicar el link público
├── 4-Archivo-Historico/
│   └── 4.1-Dashboard-v1-Version-Inicial.html    ← primera versión (referencia)
└── 5-Tools/
    ├── requirements.txt                         ← dependencias Python
    ├── flights/scraper.py                       ← tracker de precios Turkish multi-city
    ├── currency/convert.py                      ← tasas USD/COP y USD/JPY
    ├── reminders/notify.py                      ← alertas de hitos del checklist
    └── docs/export-pdf.py                       ← exportar datos a PDF offline
```

## Qué es cada cosa

- **1.1 · Documento Maestro (HTML).** El dashboard principal. Un solo archivo, sin
  dependencias, funciona offline. 8 pestañas: Ruta & Vuelos, Calendario, Ciudades,
  Trenes, Presupuesto, Ahorro, Vigilar Vuelos (con extractor de precios) y Checklist.
  La bitácora y el checklist se guardan en el navegador donde lo abras.

- **2.1 · Datos e Items Completos (MD).** La fuente de verdad en texto: fechas,
  segmentos de vuelo, ciudades, trenes, presupuesto, plan de ahorro, gatillos de
  precio, checklist y las restricciones/principios del viaje.

- **3 · Publicación Web.** `index.html` es la copia idéntica del dashboard, con el
  nombre exacto que pide GitHub Pages. `3.1` explica cómo subirlo y obtener el link
  público para compartir con terceros.

- **4.1 · Archivo histórico.** La primera versión del dashboard, guardada por si
  quieres compararla. No es la versión activa.

## Notas

- El dashboard también existe como *artifact* dentro de la app de Claude (barra
  lateral). Ese es privado; para compartir con otras personas usa la carpeta
  `3-Publicacion-Web`.
- TRM de trabajo: 3.950 COP/USD · Fondo objetivo al despegue: 39,8M COP.
- Fecha más crítica de todo el plan: **radicar la visa de Japón ~1 ago 2027.**
