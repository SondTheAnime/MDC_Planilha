import streamlit as st
import pandas as pd
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
from reportlab.lib.colors import HexColor
import pytz

def show_export_options(df):
    st.subheader("Exportar Dados")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        export_csv(df)
    with col2:
        export_excel(df)
    with col3:
        export_pdf(df)

def export_csv(df):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f'orcamento_escolar_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        help="Clique para baixar os dados em formato CSV"
    )

def export_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Orçamento')
    
    excel_data = output.getvalue()
    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name=f'orcamento_escolar_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="Clique para baixar os dados em formato Excel"
    )

def export_pdf(df):
    pdf_file = create_pdf(df)
    with open(pdf_file, "rb") as pdf:
        st.download_button(
            label="📥 Download PDF",
            data=pdf,
            file_name=f'orcamento_escolar_{datetime.now().strftime("%Y%m%d")}.pdf',
            mime='application/pdf',
            help="Clique para baixar os dados em formato PDF"
        ) 

def create_pdf(df):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        doc = SimpleDocTemplate(
            tmp_file.name,
            pagesize=landscape(A4),
            rightMargin=30,
            leftMargin=30,
            topMargin=40,
            bottomMargin=30
        )
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.textColor = HexColor('#2c3e50')
        title_style.fontSize = 24
        elements.append(Paragraph('Orçamento Escolar MDC', title_style))
        elements.append(Spacer(1, 30))
        
        # Formatar números
        df_formatted = df.copy()
        df_formatted['Custo Unitário (R$)'] = df_formatted['Custo Unitário (R$)'].apply(lambda x: f'R$ {x:,.2f}')
        df_formatted['Valor Unitário Final (R$)'] = df_formatted['Valor Unitário Final (R$)'].apply(lambda x: f'R$ {x:,.2f}')
        df_formatted['Custo Mensal Total (R$)'] = df_formatted['Custo Mensal Total (R$)'].apply(lambda x: f'R$ {x:,.2f}')
        df_formatted['Margem de Lucro (%)'] = df_formatted['Margem de Lucro (%)'].apply(lambda x: f'{x}%')
        
        data = [df_formatted.columns.tolist()] + df_formatted.values.tolist()
        
        # Larguras ajustadas para A4 paisagem
        col_widths = [200, 120, 120, 120, 140, 140]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Estilo da tabela melhorado
        table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Corpo da tabela
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Linhas zebradas
            *[('BACKGROUND', (0, i), (-1, i), HexColor('#f5f6fa')) for i in range(2, len(data), 2)],
            
            # Bordas
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#bdc3c7')),
            
            # Alinhamentos específicos
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Primeira coluna à esquerda
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),  # Valores numéricos à direita
        ]))
        
        elements.append(table)
        
        # Adiciona data de geração no horário de Brasília
        data_style = styles['Normal']
        data_style.textColor = HexColor('#7f8c8d')
        data_style.fontSize = 8
        elements.append(Spacer(1, 20))
        
        # Configurando horário de Brasília
        fuso_brasil = pytz.timezone('America/Sao_Paulo')
        data_hora_brasil = datetime.now(fuso_brasil)
        
        elements.append(Paragraph(
            f'Gerado em: {data_hora_brasil.strftime("%d/%m/%Y %H:%M")}',
            data_style
        ))
        
        doc.build(elements)
        return tmp_file.name 