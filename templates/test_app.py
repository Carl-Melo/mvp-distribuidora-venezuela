from decimal import Decimal
from app import calcular_lucro

def test_calculo_lucro_liquido():
    valor_venda = Decimal('280.00')
    custo = Decimal('200.00')
    resultado = calcular_lucro(valor_venda, custo)
    assert resultado == Decimal('80.00')

def test_calculo_lucro_zero():
    resultado = calcular_lucro(Decimal('50.00'), Decimal('50.00'))
    assert resultado == Decimal('0.00')
