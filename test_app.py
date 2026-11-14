import pytest
from decimal import Decimal
from app import app, db, calcular_lucro
from models import Usuario, Cliente, Venda

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            usuario = Usuario(nome='Lucia Color', email='lucia@venezuela.com')
            usuario.definir_senha('SenhaSegura123')
            cliente = Cliente(nome_razao='Mercearia Boa Vida', tipo_cliente='atacado', telefone_whatsapp='54999990101')
            db.session.add_all([usuario, cliente])
            db.session.commit()
        yield client

def test_unitario_calculo_lucro_liquido():
    assert calcular_lucro(Decimal('280.00'), Decimal('200.00')) == Decimal('80.00')

def test_unitario_hash_senha():
    u = Usuario(nome='Teste', email='t@t.com')
    u.definir_senha('12345678')
    assert u.senha_hash != '12345678'
    assert u.verificar_senha('12345678') is True

def test_integracao_bloqueio_credito_sem_cliente(client):
    resposta = client.post('/nova-venda', data={
        'valor_venda': '150.00',
        'custo_estimado': '100.00',
        'modalidade': 'atacado',
        'forma_pagamento': 'credito',
        'cliente_id': ''
    })
    assert resposta.status_code == 200
    assert b'Selecione um cliente cadastrado' in resposta.data

def test_integracao_registro_venda_e_baixa(client):
    resposta = client.post('/nova-venda', data={
        'valor_venda': '280.00',
        'custo_estimado': '200.00',
        'modalidade': 'atacado',
        'forma_pagamento': 'credito',
        'cliente_id': '1'
    }, follow_redirects=True)
    assert resposta.status_code == 200
    assert b'Mercearia Boa Vida' in resposta.data
