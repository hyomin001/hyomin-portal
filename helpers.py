# ============================================================
# utils/helpers.py — 공통 유틸 (포맷, 쿨다운 등)
# ============================================================
import time
import re
import numpy as np
import streamlit as st


def format_korean_money(num) -> str:
    """숫자를 한국식 단위(조/억/만)로 포맷"""
    if num is None or num != num or num == 0:   # nan check
        return "0원"
    is_neg = num < 0
    num = abs(int(num))
    jo   = num // 10**12
    eok  = (num % 10**12) // 10**8
    man  = (num % 10**8) // 10**4
    won  = num % 10**4
    parts = []
    if jo:   parts.append(f"{jo:,}조")
    if eok:  parts.append(f"{eok:,}억")
    if man:  parts.append(f"{man:,}만")
    if won or not parts: parts.append(f"{won:,}")
    res = " ".join(parts) + "원"
    return f"-{res}" if is_neg else res


def parse_korean_money(text: str):
    """'1000억', '1.5조', '5000만' 등을 정수로 파싱. 실패 시 None 반환."""
    if not text:
        return None
    text = text.replace(",", "").replace(" ", "").strip()
    if text.isdigit():
        return int(text)
    units = {"조": 10**12, "억": 10**8, "만": 10**4}
    total = 0
    matches = re.findall(r"([0-9.]+)([조억만]?)", text)
    if not matches:
        try:
            clean = re.sub(r"[^0-9.]", "", text)
            return int(float(clean)) if clean else None
        except Exception:
            return None
    for val, unit in matches:
        total += float(val) * units.get(unit, 1)
    return int(total)


def fmt_crypto_price(price: float) -> str:
    if price >= 1_000_000:  return f"₩{price:,.0f}"
    elif price >= 1:        return f"₩{price:,.2f}"
    elif price >= 0.01:     return f"₩{price:,.4f}"
    else:                   return f"₩{price:.8f}"


def fmt_crypto_qty(qty: float, cid: str) -> str:
    if cid in ("BTC", "ETH"):    return f"{qty:.6f}"
    elif cid in ("SOL", "HYO"):  return f"{qty:.4f}"
    else:                        return f"{qty:,.2f}"


# ── 쿨다운 ───────────────────────────────────────────────────
def set_cooldown(key: str):
    st.session_state[f"_cd_{key}"] = time.time()


def cooldown_remaining(key: str, seconds: float = 2.0) -> float:
    last = st.session_state.get(f"_cd_{key}", 0)
    return max(0.0, seconds - (time.time() - last))
