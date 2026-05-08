"""
features.py — Funciones de Feature Engineering reutilizables
Proyecto: Cancelaciones de Reservas Hoteleras
"""

import pandas as pd
import numpy as np


# ─── Tabla de comisiones OTA para el join ──────────────────────────────────────

OTA_COMMISSIONS = pd.DataFrame({
    "market_segment_type": ["Online", "Offline", "Corporate", "Aviation", "Complementary"],
    "ota_commission_pct":  [0.15,      0.10,      0.05,        0.08,        0.00],
    "channel_label":       ["OTA online", "OTA offline", "Corporativo", "Aerolínea", "Gratuito"]
})


def add_ota_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza el join con la tabla de comisiones OTA y calcula
    el costo neto estimado de cada reserva para el hotel.

    Parámetros
    ----------
    df : DataFrame con columna 'market_segment_type' y 'avg_price_per_room'

    Retorna
    -------
    DataFrame con columnas adicionales:
        - ota_commission_pct : porcentaje de comisión del canal
        - channel_label      : nombre legible del canal
        - net_revenue_est    : ingreso neto estimado por noche (precio * (1 - comisión))
    """
    df = df.merge(OTA_COMMISSIONS, on="market_segment_type", how="left")
    df["net_revenue_est"] = df["avg_price_per_room"] * (1 - df["ota_commission_pct"])
    return df


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea variables derivadas orientadas al análisis y a Feature Engineering futuro.

    Variables creadas
    -----------------
    lead_time_bin       : antelación categorizada (misma semana / 1–4 semanas / 1–3 meses / +3 meses)
    total_guests        : total de personas en la reserva (adultos + niños + bebés)
    is_family           : 1 si hay niños o bebés en la reserva
    has_special_request : 1 si el huésped hizo al menos 1 petición especial
    price_tier          : tercil de precio (bajo / medio / alto)
    is_weekend_arrival  : 1 si la llegada es en fin de semana (viernes o sábado)
    """
    df = df.copy()

    # Categorías de antelación
    bins   = [-1, 7, 30, 90, df["lead_time"].max() + 1]
    labels = ["misma_semana", "1_4_semanas", "1_3_meses", "mas_3_meses"]
    df["lead_time_bin"] = pd.cut(df["lead_time"], bins=bins, labels=labels)

    # Composición del grupo
    guest_cols = [c for c in ["no_of_adults", "no_of_children", "no_of_weekend_nights"]
                  if c in df.columns]
    adult_col   = "no_of_adults"   if "no_of_adults"   in df.columns else None
    children_col = "no_of_children" if "no_of_children" in df.columns else None

    if adult_col and children_col:
        df["total_guests"] = df[adult_col] + df[children_col]
        df["is_family"]    = (df[children_col] > 0).astype(int)

    # Señal de compromiso (peticiones especiales)
    if "no_of_special_requests" in df.columns:
        df["has_special_request"] = (df["no_of_special_requests"] > 0).astype(int)

    # Tercil de precio
    if "avg_price_per_room" in df.columns:
        df["price_tier"] = pd.qcut(
            df["avg_price_per_room"],
            q=3,
            labels=["precio_bajo", "precio_medio", "precio_alto"],
            duplicates="drop"
        )

    # Llegada en fin de semana (si hay columna de noches de fin de semana)
    if "no_of_weekend_nights" in df.columns:
        df["is_weekend_arrival"] = (df["no_of_weekend_nights"] > 0).astype(int)

    return df


def encode_target(df: pd.DataFrame, col: str = "booking_status") -> pd.DataFrame:
    """
    Codifica la variable objetivo como binaria.
    'Canceled' → 1, 'Not_Canceled' → 0
    """
    df = df.copy()
    df["is_canceled"] = (df[col] == "Canceled").astype(int)
    return df
