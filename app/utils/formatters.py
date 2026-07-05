def format_rupiah(amount: int) -> str:
    """Format angka integer menjadi string format Rupiah (e.g. 17500000 -> Rp 17.500.000)"""
    try:
        if amount is None:
            return "Rp 0"
        return f"Rp {amount:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return f"Rp {amount}"

def format_all_rupiah_in_dict(data):
    """
    Secara rekursif menelusuri kamus/list dan memformat semua value integer 
    yang merupakan kelipatan besar (kemungkinan biaya, misal > 1000) menjadi string Rupiah.
    """
    if isinstance(data, dict):
        return {k: format_all_rupiah_in_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [format_all_rupiah_in_dict(v) for v in data]
    elif isinstance(data, int) and data >= 1000:
        return format_rupiah(data)
    else:
        return data
