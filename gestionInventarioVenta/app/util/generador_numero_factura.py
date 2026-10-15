class GeneradorNumeroFactura:
    PREFIJO = "FAC-"

    @staticmethod
    def generar(secuencia: int) -> str:
        return f"{GeneradorNumeroFactura.PREFIJO}{str(secuencia).zfill(6)}"
