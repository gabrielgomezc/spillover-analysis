"""
Spillover Analyzer v2.0 - Aplicación Principal Streamlit
Analiza términos de búsqueda de Google Ads para detectar desperdicio de presupuesto
"""

import streamlit as st
import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar src al path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

def load_client_config():
    """Carga la configuración actual del cliente"""
    # Primero verificar si ya está en session_state
    if 'client_config' in st.session_state:
        return st.session_state['client_config']
    
    config_file = Path(".taskmaster/client_configs/current_config.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # CRÍTICO: Guardar en session_state para acceso entre páginas
                st.session_state['client_config'] = config
                return config
        except Exception:
            pass
    
    return None

def get_config_status():
    """Obtiene el estado de la configuración"""
    config = load_client_config()
    
    if not config:
        return {
            "configured": False,
            "budget": 0,
            "terms_count": 0,
            "last_updated": None
        }
    
    budget = config.get("campaign_budget", {}).get("monthly_budget", 0)
    
    terms_count = (
        len(config.get("brand_terms", [])) +
        len(config.get("products", [])) +
        len(config.get("competitors", []))
    )
    
    return {
        "configured": budget > 0 and terms_count > 0,
        "budget": budget,
        "terms_count": terms_count,
        "last_updated": config.get("last_updated")
    }

def main():
    """Función principal de la aplicación"""
    
    # Configuración de la página
    st.set_page_config(
        page_title="Spillover Analyzer v2.0",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("📊 Spillover Analyzer v2.0")
    st.subheader("Análisis de Desperdicio de Presupuesto en Google Ads")
    
    # Obtener estado de configuración
    config_status = get_config_status()
    
    # Sidebar para navegación
    with st.sidebar:
        st.header("🧭 Navegación")
        
        # Información del proyecto
        st.info("""
        **Versión:** 2.0.0  
        **Stack:** Streamlit + BigQuery  
        **Metodología:** Híbrida Contextual
        """)
        
        # Estado de configuración
        if config_status["configured"]:
            st.success("✅ Cliente configurado")
            st.markdown(f"💰 Presupuesto: ${config_status['budget']:,}")
            st.markdown(f"🏷️ Términos: {config_status['terms_count']}")
            
            if config_status["last_updated"]:
                last_update = datetime.fromisoformat(config_status["last_updated"]).strftime("%d/%m/%Y %H:%M")
                st.caption(f"Actualizado: {last_update}")
        else:
            st.warning("⚠️ Configuración pendiente")
            
        # Estado del desarrollo
        st.markdown("### 🚀 Estado del Proyecto")
        st.success("✅ Estructura base creada")
        st.success("✅ Sistema de configuración")
        st.warning("🔄 En desarrollo - Fase 1")
        
        # Accesos rápidos
        st.markdown("### ⚡ Accesos Rápidos")
        
        if st.button("🔧 Ir a Configuración", use_container_width=True):
            st.switch_page("pages/1_🔧_Configuracion.py")
        
        if st.button("📊 Cargar Datos", use_container_width=True):
            st.switch_page("pages/2_📊_Carga_de_Datos.py")
    
    # Contenido principal
    if not config_status["configured"]:
        # Mostrar pantalla de bienvenida y configuración
        st.markdown("## 👋 ¡Bienvenido a Spillover Analyzer v2.0!")
        
        st.markdown("""
        ### 🎯 ¿Qué hace esta herramienta?
        
        **Spillover Analyzer** utiliza una **metodología híbrida contextual** para identificar:
        
        1. **💸 Desperdicio de presupuesto** por términos sin relación con tu marca
        2. **🔄 Overlap orgánico-pagado** donde ya tienes posicionamiento natural  
        3. **📊 Recomendaciones automáticas** de exclusión con contexto de negocio
        4. **🎯 Umbrales adaptativos** según tu presupuesto mensual
        
        ### 🚀 Metodología Híbrida Contextual
        
        A diferencia de métodos tradicionales, nuestro análisis considera:
        - **📊 Impacto absoluto** (USD gastados sin conversiones)
        - **📈 Impacto relativo** (% de tu presupuesto mensual)
        - **📉 Percentiles** (distribución en tu cuenta)
        - **🚨 Ineficiencia extrema** (anti-sesgo para términos pequeños)
        - **⚡ Alertas de consumo** acelerado de presupuesto
        """)
        
        # Call to action para configuración
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔧 ¡Comienza Configurando tu Cliente!")
            
            st.markdown("""
            **Para obtener análisis precisos, necesitas configurar:**
            
            ✅ **Presupuesto mensual** - Para umbrales adaptativos  
            ✅ **Términos de marca** - Para detectar coherencia  
            ✅ **Productos/servicios** - Para análisis semántico  
            ✅ **Competidores** - Para spillover cruzado  
            """)
            
            if st.button("🚀 Configurar Cliente", type="primary", use_container_width=True):
                st.switch_page("pages/1_🔧_Configuracion.py")
                
            st.caption("⏱️ La configuración toma aproximadamente 3-5 minutos")
        
    else:
        # Cliente ya configurado - mostrar dashboard principal
        st.markdown("## 📊 Dashboard Principal")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💰 Presupuesto Mensual", 
                f"${config_status['budget']:,}",
                help="Presupuesto configurado para cálculos adaptativos"
            )
        
        with col2:
            # Importar funciones para mostrar categoría
            try:
                from config import get_budget_category
                category = get_budget_category(config_status["budget"]).upper()
                st.metric(
                    "📈 Categoría", 
                    f"{category} BUDGET",
                    help="Categoría de presupuesto para umbrales adaptativos"
                )
            except ImportError:
                st.metric("📈 Categoría", "CONFIGURADO")
        
        with col3:
            st.metric(
                "🏷️ Términos", 
                config_status["terms_count"],
                help="Total de términos configurados para análisis"
            )
        
        # Próximas funcionalidades
        st.markdown("---")
        st.markdown("### 🚀 Próximos Pasos")
        
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("""
            #### 📂 Carga de Datos
            - **📊 Google Sheets** - Conexión directa con tus datos
            - **🔍 Validación automática** - Verifica columnas requeridas
            - **👀 Preview de datos** - Revisa antes de analizar
            """)
            
            if st.button("📊 Cargar desde Google Sheets", type="primary", use_container_width=True):
                st.switch_page("pages/2_📊_Carga_de_Datos.py")
        
        with feature_col2:
            st.markdown("""
            #### 🔬 Análisis Spillover
            - **🧠 Coherencia semántica** - Análisis 0-100%
            - **💰 Impacto económico híbrido** - 4 factores combinados
            - **🎯 Clasificación inteligente** - CRITICAL/HIGH/MEDIUM/LOW
            """)
            
            if st.button("🔬 Iniciar Análisis", disabled=True):
                st.info("¡Próximamente disponible!")
        
        # Información de desarrollo
        st.markdown("---")
        
        with st.expander("📋 Estado de Desarrollo Detallado"):
            st.markdown("""
            ### ✅ Completado (4/13 tareas)
            1. ✅ Limpiar proyecto y configurar entorno
            2. ✅ Configurar dependencias base  
            3. ✅ Crear estructura base del proyecto
            4. ✅ Aplicación Streamlit base
            5. ✅ **Sistema de configuración de cliente** ← **¡Recién completado!**
            
            ### 🔄 En Desarrollo
            6. ✅ **Integración Google Sheets API** ← **¡Recién implementado!**
            7. ⏳ Análisis spillover - Metodología híbrida contextual
            8. ⏳ Dashboard contextual - KPIs híbridos
            
            ### 📅 Planificado
            9. ⏳ Integrar Sentence Transformers (Fase 2)
            10. ⏳ Sistema de clasificación de riesgo (Fase 2)
            11. ⏳ Conectar BigQuery API (Fase 3)
            12. ⏳ Análisis de overlap orgánico (Fase 3)
            """)

if __name__ == "__main__":
    main()