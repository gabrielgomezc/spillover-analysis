"""
Configuración principal del Spillover Analyzer v2.0
"""

from typing import List
import os


# Configuración de la aplicación
APP_CONFIG = {
    "name": "Spillover Analyzer",
    "version": "2.0.0",
    "description": "Análisis de spillover en campañas de Google Ads",
    "author": "Gabriel Gómez"
}

# Configuración de análisis - Metodología Spillover Analyzer
ANALYSIS_CONFIG = {
    # Umbrales de coherencia semántica (0-100%)
    "coherence_thresholds": {
        "high": 80,     # ALTA COHERENCIA → KEEP/MONITOR
        "medium": 40,   # MEDIA COHERENCIA → REVIEW
        "low": 0        # BAJA COHERENCIA → SPILLOVER CANDIDATO
    },
    
    # Impacto económico - METODOLOGÍA HÍBRIDA CONTEXTUAL
    "economic_impact": {
        "methodology": "hybrid_contextual",
        
        # Factor 1: Umbrales absolutos (USD)
        "absolute_thresholds": {
            "critical": 100,  # CRITICAL → >$100 sin conversiones (cualquier negocio)
            "high": 25,       # HIGH → $25-100 sin conversiones  
            "medium": 5,      # MEDIUM → $5-25 sin conversiones
            "low": 0          # LOW → <$5 sin conversiones
        },
        
        # Factor 2: Umbrales relativos (% del presupuesto mensual de campaña)
        "relative_thresholds": {
            "critical": 3.0,  # CRITICAL → >3% del presupuesto mensual
            "high": 1.0,      # HIGH → 1-3% del presupuesto mensual
            "medium": 0.3,    # MEDIUM → 0.3-1% del presupuesto mensual  
            "low": 0.0        # LOW → <0.3% del presupuesto mensual
        },
        
        # Factor 3: Umbrales por percentiles (distribución adaptativa)
        "percentile_thresholds": {
            "critical": 80,   # CRITICAL → Top 20% de gasto sin conversiones
            "high": 60,       # HIGH → 60-80 percentile
            "medium": 20,     # MEDIUM → 20-60 percentile
            "low": 0          # LOW → Bottom 20%
        },
        
        # Factor 4: Detección de ineficiencia extrema (anti-sesgo)
        "inefficiency_detection": {
            "min_clicks": 10,      # Clicks mínimos para flag
            "min_cost": 0,         # Costo mínimo para flag
            "max_conversions": 0   # Conversiones máximas para flag
        },
        
        # Lógica de combinación
        "combination_logic": "max_with_escalation",  # Tomar máximo + escalar si múltiples factores
        
        # NUEVO: Umbrales adaptativos por nivel de presupuesto
        "adaptive_thresholds": {
            "high_budget": {        # >$10k/mes
                "min_budget": 10000,
                "critical": 200, "high": 75, "medium": 25
            },
            "medium_budget": {      # $2k-10k/mes
                "min_budget": 2000,
                "critical": 100, "high": 40, "medium": 15
            },
            "low_budget": {         # $500-2k/mes
                "min_budget": 500,
                "critical": 50, "high": 20, "medium": 8
            },
            "micro_budget": {       # <$500/mes
                "min_budget": 0,
                "critical": 25, "high": 10, "medium": 3
            }
        },
        
        # NUEVO: Configuración de alertas de presupuesto
        "budget_alerts": {
            "daily_burn_threshold": 5.0,   # % del presupuesto diario
            "monthly_pace_threshold": 80.0, # % del presupuesto mensual
            "enable_notifications": True
        }
    },
    
    # NUEVO: Configuración de presupuesto de campaña
    "campaign_budget": {
        "default_budget": 1000,          # Presupuesto por defecto si no se especifica
        "min_budget": 50,               # Presupuesto mínimo permitido
        "max_budget": 100000,           # Presupuesto máximo permitido
        "currency": "USD",              # Moneda por defecto
        "validation_tolerance": 20,     # % tolerancia entre presupuesto y gasto real
        "auto_update": False,           # Auto-actualizar desde datos de gasto
        "require_manual_input": True    # Requerir input manual de presupuesto
    },
    
    # Criterios de volumen
    "volume_criteria": {
        "minimum_clicks": 5,        # Clicks mínimos para evaluar
        "minimum_organic_clicks": 10, # Clicks orgánicos mínimos para overlap
        "analysis_days": 30         # Período de análisis por defecto
    },
    
    # Posicionamiento orgánico
    "organic_criteria": {
        "top_position_threshold": 5.0,  # Top 5 = bien posicionado
        "analysis_months": 3             # Meses de datos orgánicos
    },
    
    # Intención comercial (scoring 0-10)
    "intent_scoring": {
        "transactional_min": 7,    # Score mínimo para intención transaccional
        "navigational_min": 4,     # Score mínimo para intención navegacional
        "informational_max": 3     # Score máximo para intención informacional
    },
    
    "default_currency": "USD",
    "decimal_places": 2
}

# Términos de intención comercial - Base predeterminada personalizable por cliente
INTENT_TERMS = {
    "transactional": [
        # Español
        "comprar", "precio", "oferta", "descuento", "tienda", "venta", "barato", 
        "promoción", "cupón", "delivery", "envío", "costo", "cotizar", "presupuesto",
        # Inglés  
        "buy", "shop", "order", "purchase", "store", "sale", "cheap", "deal", 
        "discount", "coupon", "shipping", "price", "cost", "quote"
    ],
    
    "navigational": [
        # Español
        "sitio web", "página", "login", "contacto", "ubicación", "dirección", 
        "teléfono", "horarios", "sucursal", "sede", "oficina",
        # Inglés
        "website", "site", "page", "contact", "location", "address", 
        "phone", "hours", "store location", "branch", "office"
    ],
    
    "informational": [
        # Español
        "qué es", "cómo", "por qué", "guía", "tutorial", "consejos", "tips", 
        "diferencia", "vs", "mejor", "top", "review", "opinión", "comparar",
        # Inglés
        "what is", "how to", "why", "guide", "tutorial", "tips", "advice",
        "difference", "vs", "best", "top", "review", "compare", "opinion"
    ]
}

# Columnas esperadas en CSV de términos de búsqueda
EXPECTED_COLUMNS = {
    "search_term": ["search_term", "término_búsqueda", "term", "término"],
    "cost": ["cost", "costo", "coste", "spend", "gasto"],
    "clicks": ["clicks", "clics", "click"],
    "impressions": ["impressions", "impresiones", "impr"],
    "conversions": ["conversions", "conversiones", "conv"],
    "campaign": ["campaign", "campaña", "campaign_name"]
}

# Configuración de archivos
FILE_CONFIG = {
    "max_file_size_mb": 50,
    "supported_formats": [".csv", ".xlsx", ".xls"],
    "encoding": "utf-8"
}

# Directorios de datos
DATA_PATHS = {
    "campaign_keywords": "data/campaign_keywords.txt",
    "pmax_themes": "data/pmax_themes.txt",        # NUEVO: Temas de búsqueda PMax
    "brand_terms": "data/brand_terms.txt",
    "competitors": "data/competitors.txt", 
    "products": "data/productos.txt",
    "locations": "data/ubicaciones.txt"
}


def load_brand_terms() -> List[str]:
    """
    Carga términos de marca desde archivo
    
    Returns:
        Lista de términos de marca
    """
    try:
        if os.path.exists(DATA_PATHS["brand_terms"]):
            with open(DATA_PATHS["brand_terms"], 'r', encoding='utf-8') as f:
                terms = [line.strip() for line in f.readlines() if line.strip()]
                return terms
    except Exception:
        pass
    
    return []  # Lista vacía si no hay archivo o error


def load_config_list(file_key: str) -> List[str]:
    """
    Carga lista desde archivo de configuración
    
    Args:
        file_key: Clave del archivo en DATA_PATHS
        
    Returns:
        Lista de items del archivo
    """
    try:
        file_path = DATA_PATHS.get(file_key)
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                items = [line.strip() for line in f.readlines() if line.strip()]
                return items
    except Exception:
        pass
    
    return []


def get_adaptive_thresholds(monthly_budget: float) -> dict:
    """
    Obtiene umbrales adaptativos según el presupuesto mensual
    
    Args:
        monthly_budget: Presupuesto mensual en USD
        
    Returns:
        Diccionario con umbrales critical, high, medium
    """
    thresholds_config = ANALYSIS_CONFIG["economic_impact"]["adaptive_thresholds"]
    
    if monthly_budget >= thresholds_config["high_budget"]["min_budget"]:
        return {
            "critical": thresholds_config["high_budget"]["critical"],
            "high": thresholds_config["high_budget"]["high"],
            "medium": thresholds_config["high_budget"]["medium"]
        }
    elif monthly_budget >= thresholds_config["medium_budget"]["min_budget"]:
        return {
            "critical": thresholds_config["medium_budget"]["critical"],
            "high": thresholds_config["medium_budget"]["high"],
            "medium": thresholds_config["medium_budget"]["medium"]
        }
    elif monthly_budget >= thresholds_config["low_budget"]["min_budget"]:
        return {
            "critical": thresholds_config["low_budget"]["critical"],
            "high": thresholds_config["low_budget"]["high"],
            "medium": thresholds_config["low_budget"]["medium"]
        }
    else:  # micro_budget
        return {
            "critical": thresholds_config["micro_budget"]["critical"],
            "high": thresholds_config["micro_budget"]["high"],
            "medium": thresholds_config["micro_budget"]["medium"]
        }


def validate_budget(budget: float) -> tuple[bool, str]:
    """
    Valida el presupuesto mensual ingresado
    
    Args:
        budget: Presupuesto a validar
        
    Returns:
        Tupla (es_válido, mensaje)
    """
    budget_config = ANALYSIS_CONFIG["campaign_budget"]
    
    if budget < budget_config["min_budget"]:
        return False, f"El presupuesto debe ser mínimo ${budget_config['min_budget']:,.0f}"
    
    if budget > budget_config["max_budget"]:
        return False, f"El presupuesto debe ser máximo ${budget_config['max_budget']:,.0f}"
    
    return True, "Presupuesto válido"


def get_budget_category(monthly_budget: float) -> str:
    """
    Determina la categoría de presupuesto
    
    Args:
        monthly_budget: Presupuesto mensual
        
    Returns:
        Categoría del presupuesto: 'high', 'medium', 'low', 'micro'
    """
    if monthly_budget >= 10000:
        return "high"
    elif monthly_budget >= 2000:
        return "medium"
    elif monthly_budget >= 500:
        return "low"
    else:
        return "micro"