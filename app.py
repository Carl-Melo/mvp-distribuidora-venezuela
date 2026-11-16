import os
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Usuario, Cliente, Venda

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-desenvolvimento-segura')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///distribuidora.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def inicializar_banco():
    db.create_all()
    if not Usuario.query.first():
        admin = Usuario(nome='Operador Balcao', email='admin@distribuidora.com', ativo=True)
        admin.definir_senha('123456')
        db.session.add(admin)
    if not Cliente.query.first():
        c1 = Cliente(nome_razao='Carlos Silva (Mercearia Central)', tipo_cliente='juridica', telefone_whatsapp='5595991112222', status='ativo')
        c2 = Cliente(nome_razao='Maria Oliveira', tipo_cliente='fisica', telefone_whatsapp='5595993334444', status='ativo')
        db.session.add_all([c1, c2])
    db.session.commit()

with app.app_context():
    inicializar_banco()

def calcular_lucro(valor_venda, custo_estimado):
    return Decimal(str(valor_venda)) - Decimal(str(custo_estimado))

@app.route('/')
def index():
    vendas = Venda.query.all()
    faturamento = sum((v.valor_venda for v in vendas), Decimal('0.00'))
    lucro = sum((v.lucro_liquido for v in vendas), Decimal('0.00'))
    pendencias = Venda.query.filter_by(status_pagamento='pendente').count()
    return render_template('index.html', faturamento=faturamento, lucro=lucro, pendencias=pendencias)

@app.route('/nova-venda', methods=['GET', 'POST'])
def nova_venda():
    clientes = Cliente.query.filter_by(status='ativo').all()
    if request.method == 'POST':
        valor = Decimal(request.form['valor_venda'])
        custo = Decimal(request.form['custo_estimado'])
        modalidade = request.form['modalidade']
        pagamento = request.form['forma_pagamento']
        cliente_id = request.form.get('cliente_id')

        if pagamento == 'credito' and not cliente_id:
            flash('Selecione um cliente cadastrado para registrar venda no Crédito Cliente.', 'erro')
            return render_template('nova_venda.html', clientes=clientes)

        status = 'pendente' if pagamento == 'credito' else 'pago'
        venda = Venda(
            valor_venda=valor,
            custo_estimado=custo,
            lucro_liquido=calcular_lucro(valor, custo),
            modalidade=modalidade,
            forma_pagamento=pagamento,
            status_pagamento=status,
            usuario_id=1,
            cliente_id=int(cliente_id) if cliente_id else None
        )
        db.session.add(venda)
        db.session.commit()
        return redirect(url_for('credito_cliente'))

    return render_template('nova_venda.html', clientes=clientes)

@app.route('/credito-cliente')
def credito_cliente():
    pendentes = Venda.query.filter_by(status_pagamento='pendente').all()
    return render_template('credito.html', pendentes=pendentes)

@app.route('/dar-baixa/<int:venda_id>', methods=['POST'])
def dar_baixa(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    venda.status_pagamento = 'pago'
    db.session.commit()
    return redirect(url_for('credito_cliente'))

if __name__ == '__main__':
    app.run(debug=True)
