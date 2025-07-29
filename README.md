# 📊 Spillover Analyzer v2.0

Análisis de desperdicio de presupuesto en campañas de Google Ads mediante detección de spillover y overlap orgánico-pagado.

## ⚠️ **IMPORTANTE: ENTORNO VIRTUAL**

**ANTES DE CUALQUIER TRABAJO EN EL PROYECTO:**
1. ✅ Verificar que el entorno virtual esté ACTIVO: `(venv)` debe aparecer en el prompt
2. ✅ Si no está activo, ejecutar: `.\venv\Scripts\Activate.ps1`
3. ✅ O usar el método rápido: doble clic en `iniciar_app.bat`

**📋 Ver documentación completa en: `ENTORNO_VIRTUAL.md`**

## 🎯 Objetivo

Identificar y cuantificar:
1. **💸 Desperdicio de presupuesto** por términos sin relación con tu marca
2. **🔄 Overlap orgánico-pagado** donde ya tienes posicionamiento natural  
3. **📊 Recomendaciones automáticas** de exclusión

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py --server.port 8080
```

La aplicación estará disponible en: `http://localhost:8080`

## 📁 Estructura del Proyecto

```
├── app.py                    # Aplicación principal Streamlit
├── config.py                 # Configuración principal
├── requirements.txt          # Dependencias Python
├── src/                      # Código fuente
│   ├── analyzers/           # Módulos de análisis
│   │   └── spillover.py     # Analizador de spillover
│   ├── data_connectors/     # Conectores de datos
│   │   └── csv_reader.py    # Lector de CSV
│   └── utils/               # Utilidades
│       └── helpers.py       # Funciones auxiliares
├── data/                    # Archivos de configuración
│   ├── brand_terms.txt      # Términos de marca
│   ├── competitors.txt      # Competidores
│   └── productos.txt        # Lista de productos
└── .taskmaster/             # Sistema TaskMaster
```

## 🛠️ Stack Tecnológico

- **Frontend**: Streamlit
- **Análisis**: pandas + sentence-transformers (futuro)
- **Base de datos**: BigQuery (futuro)
- **Fuente de datos**: Google Sheets (futuro)

## 📋 Estado del Desarrollo

### ✅ Fase 1 - Estructura Base (COMPLETADA)
- [x] Proyecto limpiado
- [x] Dependencias configuradas
- [x] Estructura de archivos creada
- [x] Aplicación Streamlit básica funcionando

### 🔄 Fase 2 - MVP Básico (EN DESARROLLO)
- [ ] Sistema de configuración de cliente
- [ ] Carga de archivos CSV
- [ ] Análisis básico de spillover
- [ ] Dashboard de resultados

### ⏳ Fase 3 - Análisis Semántico
- [ ] Integración de sentence-transformers
- [ ] Análisis de coherencia semántica
- [ ] Scoring avanzado

### ⏳ Fase 4 - Conectores
- [ ] Conector Google Sheets
- [ ] Conector BigQuery
- [ ] Automatización de datos

## 🔧 Configuración

Edita los archivos en `/data/` para personalizar:
- `brand_terms.txt`: Términos de tu marca
- `competitors.txt`: Competidores
- `productos.txt`: Lista de productos

## 📈 Desarrollo Incremental

Este proyecto sigue un enfoque de desarrollo incremental usando TaskMaster para control de tareas. Cada fase se construye sobre la anterior, validando funcionalidad antes de agregar complejidad.

---

**Versión**: 2.0.0  
**Autor**: Gabriel Gómez  
**Stack**: Streamlit + BigQuery + sentence-transformers