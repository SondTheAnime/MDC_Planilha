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
from views import create_salary_df

def show_export_options(df, data):
    st.subheader("Exportar Dados")
    
    tab1, tab2 = st.tabs(["📊 Dados Gerais", "💰 Salários"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            export_csv(df, "orcamento")
        with col2:
            export_excel(df, "orcamento")
        with col3:
            export_pdf(df, "orcamento", is_salary=False)
    
    with tab2:
        df_salarios = create_salary_df(data)
        col1, col2, col3 = st.columns(3)
        with col1:
            export_csv(df_salarios, "salarios")
        with col2:
            export_excel(df_salarios, "salarios")
        with col3:
            export_pdf(df_salarios, "salarios", is_salary=True)

def export_csv(df, prefix):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f'{prefix}_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        help="Clique para baixar os dados em formato CSV"
    )

def export_excel(df, prefix):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    
    excel_data = output.getvalue()
    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name=f'{prefix}_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="Clique para baixar os dados em formato Excel"
    )

def export_pdf(df, prefix, is_salary=False):
    pdf_file = create_pdf(df, is_salary)
    with open(pdf_file, "rb") as pdf:
        st.download_button(
            label="📥 Download PDF",
            data=pdf,
            file_name=f'{prefix}_{datetime.now().strftime("%Y%m%d")}.pdf',
            mime='application/pdf',
            help="Clique para baixar os dados em formato PDF"
        ) 

def create_pdf(df, is_salary=False):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        doc = SimpleDocTemplate(
            tmp_file.name,
            pagesize=landscape((23.4*72, 16.5*72)),  # A2 em pontos
            rightMargin=30,
            leftMargin=30,
            topMargin=40,
            bottomMargin=30
        )
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.textColor = HexColor('#2c3e50')
        title_style.fontSize = 28
        
        title = 'Relatório de Salários' if is_salary else 'Orçamento Escolar MDC'
        elements.append(Paragraph(title, title_style))
        
        date_style = styles['Normal']
        date_style.alignment = 1  # Centralizado
        date_style.textColor = HexColor('#7f8c8d')
        date_style.fontSize = 14
        
        tz_br = pytz.timezone('America/Sao_Paulo')
        current_time = datetime.now(tz_br)
        date_str = f"Gerado em {current_time.strftime('%d/%m/%Y às %H:%M:%S')}"
        elements.append(Paragraph(date_str, date_style))
        
        elements.append(Spacer(1, 20))
        
        # Formatar números e ajustar cabeçalhos
        df_formatted = df.copy()
        if is_salary:
            # Renomear colunas com quebras de linha
            df_formatted.columns = [
                'Cargo',
                'Salário\nBase (R$)',
                'Qtd.',
                'INSS\n(R$)',
                'FGTS\n(R$)',
                'Acid.\n(R$)',
                'Educ.\n(R$)',
                'DSR\n(R$)',
                '13º\n(R$)',
                'Sist.S\n(R$)',
                'Férias\n(R$)',
                'Total\nEncargos (R$)',
                'Custo por\nFuncionário (R$)',
                'Custo Total\nMensal (R$)'
            ]
            for col in df_formatted.columns:
                if "R$" in col:
                    df_formatted[col] = df_formatted[col].apply(lambda x: f'R$ {x:,.2f}')
        else:
            df_formatted['Custo Unitário (R$)'] = df_formatted['Custo Unitário (R$)'].apply(lambda x: f'R$ {x:,.2f}')
            df_formatted['Valor Unitário Final (R$)'] = df_formatted['Valor Unitário Final (R$)'].apply(lambda x: f'R$ {x:,.2f}')
            df_formatted['Custo Mensal Total (R$)'] = df_formatted['Custo Mensal Total (R$)'].apply(lambda x: f'R$ {x:,.2f}')
            df_formatted['Margem de Lucro (%)'] = df_formatted['Margem de Lucro (%)'].apply(lambda x: f'{x}%')
        
        data = [df_formatted.columns.tolist()] + df_formatted.values.tolist()
        
        if is_salary:
            col_widths = [
                150,  # Cargo
                120,  # Salário Base
                60,   # Quantidade
                110,   # INSS
                110,   # FGTS
                110,   # Acidente
                110,   # Educação
                110,   # DSR
                110,   # 13º
                110,   # Sistema S
                110,   # Férias
                150,  # Total Encargos
                150,  # Custo por Funcionário
                150   # Custo Total Mensal
            ]
            font_size = 14  # Fonte maior
            header_height = 50
        else:
            col_widths = [
                290,  # Descrição do Item
                170,  # Custo Unitário
                190,  # Quantidade Mensal
                190,  # Margem de Lucro
                210,  # Valor Unitário Final
                210   # Custo Mensal Total
            ]
            font_size = 14
            header_height = 40
        
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        elements.append(Spacer(1, 50))
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), font_size + 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 25),
            ('TOPPADDING', (0, 0), (-1, 0), 25),
            ('LINEHEIGHT', (0, 0), (-1, 0), 1.5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('TOPPADDING', (0, 1), (-1, -1), 12),  # Mais espaço entre linhas
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),  # Mais espaço entre linhas
            *[('BACKGROUND', (0, i), (-1, i), HexColor('#f5f6fa')) for i in range(2, len(data), 2)],
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),  # Linha da grade mais grossa
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))
        
        elements.append(table)
        doc.build(elements)
        return tmp_file.name 